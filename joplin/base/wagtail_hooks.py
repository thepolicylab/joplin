from django.db import models
from django import forms
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.utils.html import escape
from wagtail.core.models import Page
from wagtail.core.rich_text import LinkHandler
from wagtail.core.rich_text.pages import PageLinkHandler
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html_join
from webpack_loader import utils as webpack_loader_utils
from wagtail.admin.auth import permission_required

from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.admin.widgets import Button, ButtonWithDropdownFromHook, PageListingButton
from wagtail.core import hooks

from base.models import HomePage, Location, Contact, JanisUrl
from base.models.janis_url import TopicCollectionPageJanisUrl, TopicPageJanisUrl, DepartmentPageJanisUrl, LocationPageJanisUrl, InformationPageJanisUrl, ServicePageJanisUrl, OfficialDocumentPageJanisUrl, GuidePageJanisUrl, FormContainerJanisUrl

from html.parser import HTMLParser

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler


# Following this: https://docs.python.org/3/library/html.parser.html#examples
class CheckForDataInHTMLParser(HTMLParser):
    has_data = False

    def handle_data(self, data):
        self.has_data = True


@hooks.register('before_edit_page')
def before_edit_page(request, page):
    print(f'BeforeEditHook request: {request}')
    print(f'BeforeEditHook page: "{page}" of type "{type(page)}"')

    assert request.user.is_authenticated
    print(
        f'BeforeEditHook {request.user.email} is in groups {[group.name for group in request.user.groups.all()]}')


@hooks.register('construct_main_menu')
def configure_main_menu(request, menu_items):
    """
    Each item in the nav has icons. Here are the names for the icons within the Material icon font set that we have in Joplin:
    Content: "create"
    Map: "map"
    Locations: "location_on"
    Images: "photo"
    Contacts: "contact_phone"
    Users: "account_circle"
    """
    menu_items[:] = [item for item in menu_items if item.name not in
                     # here were excluding some default generated menu items per UX
                     [
                         'explorer',
                         'settings',
                         'snippets'
                     ]
                     ]

    # replace wagtail icon with material-icons class to use that font
    for item in menu_items:
        item.classnames = item.classnames.replace(
            'icon ', 'material-icons ', 1)


@hooks.register('register_admin_menu_item')
def register_page_list_menu_item():
    # home = HomePage.objects.first()
    return MenuItem('Pages', '/admin/pages/search/', classnames='icon icon-home', order=10)


@hooks.register('register_admin_menu_item')
def register_map_menu_item():
    return PermissionMenuItem('Maps', "/admin/snippets/base/map/", classnames='material-icons icon-maps', order=20)


@hooks.register('register_admin_menu_item')
def register_locations_menu_item():
    return PermissionMenuItem('Locations', "/admin/snippets/base/location/", classnames='material-icons icon-locations', order=30)


@hooks.register('register_admin_menu_item')
def register_contacts_menu_item():
    return PermissionMenuItem('Contacts', "/admin/snippets/base/contact/", classnames='material-icons icon-contacts', order=40)


@hooks.register('register_admin_menu_item')
def register_users_menu_item():
    return MenuItem('Users', "/admin/users/", classnames="material-icons icon-users", order=50)


# Allow users to edit JanisBranchSettings on PR branches and Local only
if settings.ISLOCAL or settings.ISREVIEW:
    # Need to add custom js webpack bundle
    class BranchSettingsMenuItem(MenuItem):
        @property
        def media(self):
            super_media = super(BranchSettingsMenuItem, self).media
            js = super_media._js
            css = super_media._css
            js.append(webpack_loader_utils.get_files('janisBranchSettings')[0]['url'])
            return forms.Media(css=css, js=js)

        def is_shown(self, request):
            return request.user.is_superuser

    @hooks.register('register_admin_menu_item')
    def register_options_menu_item():
        return BranchSettingsMenuItem('Options', "/admin/settings/base/janisbranchsettings/2/", classnames="material-icons icon-settings", order=60)

# example of rendering custom nested menu items
# class LocationModelAdmin(ModelAdmin):
#     model = Location
#     search_fields = ('street',)
#
#
# class ContactModelAdmin(ModelAdmin):
#     model = Contact
#
# class ReallyAwesomeGroup(ModelAdminGroup):
#     menu_label = 'Important Snippets'
#     items = (LocationModelAdmin, ContactModelAdmin)
#
#
# modeladmin_register(ReallyAwesomeGroup)


@hooks.register('register_joplin_page_listing_buttons')
def joplin_page_listing_buttons(page, page_perms, is_parent=False):
    if page_perms.can_edit():
        yield PageListingButton(
            _('Edit'),
            reverse('wagtailadmin_pages:edit', args=[page.id]),
            attrs={'title': _("Edit '{title}'").format(
                title=page.get_admin_display_title())},
            priority=10
        )
    if page.has_unpublished_changes:
        try:
            yield PageListingButton(
                _('View draft'),
                page.janis_preview_url(),
                attrs={'title': _("Preview draft version of '{title}'").format(
                    title=page.get_admin_display_title()), 'target': '_blank'},
                priority=20
            )
        except Exception as e:
            raise e
    if page.live and page.url and hasattr(page, 'janis_url'):
        yield PageListingButton(
            _('View live'),
            page.janis_url(),
            attrs={'target': "_blank", 'title': _("View live version of '{title}'").format(
                title=page.get_admin_display_title())},
            priority=30
        )

    # make the author notes icon appear if latest revision has notes
    latest_revision_as_page = page.get_latest_revision_as_page()
    if hasattr(latest_revision_as_page, 'author_notes') and latest_revision_as_page.author_notes:
        yield Button(
            _('📝'),
            'javascript:null;',
            attrs={'title': _("Notes for authors entered"),
                   'class': 'has-author-notes'},
            priority=70
        )

    yield ButtonWithDropdownFromHook(
        _('More'),
        hook_name='register_joplin_page_listing_more_buttons',
        page=page,
        page_perms=page_perms,
        is_parent=is_parent,
        attrs={'target': '_blank', 'title': _("View more options for '{title}'").format(
            title=page.get_admin_display_title())},
        priority=50
    )


@hooks.register('register_joplin_page_listing_more_buttons')
def joplin_page_listing_more_buttons(page, page_perms, is_parent=False):
    if not page.is_root():
        yield Button(
            _('Copy'),
            reverse('wagtailadmin_pages:copy', args=[page.id]),
            attrs={'title': _("Copy page '{title}'").format(
                title=page.get_admin_display_title())},
            priority=20
        )
    # if not page.live:
    #     yield Button(
    #         _('Archive'),
    #         "#TODO-archive",
    #         attrs={'title': _("Archive page '{title}'").format(title=page.get_admin_display_title())},
    #         priority=30
    #     )
    if page_perms.can_unpublish():
        yield Button(
            _('Unpublish'),
            reverse('wagtailadmin_pages:unpublish', args=[page.id]),
            attrs={'title': _("Unpublish page '{title}'").format(
                title=page.get_admin_display_title())},
            priority=40
        )
    if page_perms.can_publish() and page.has_unpublished_changes:
        yield Button(
            _('Publish'),
            reverse('publish', args=[page.id]),
            attrs={'title': _("Publish page '{title}'").format(
                title=page.get_admin_display_title())},
            priority=50
        )
    if not page.is_root():
        yield Button(
            _('Revisions'),
            reverse('wagtailadmin_pages:revisions_index', args=[page.id]),
            attrs={'title': _("View revision history for '{title}'").format(
                title=page.get_admin_display_title())},
            priority=60
        )
    if page_perms.can_delete():
        yield Button(
            _('Delete'),
            reverse('wagtailadmin_pages:delete', args=[page.id]),
            attrs={'title': _("Delete page '{title}'").format(
                title=page.get_admin_display_title())},
        )


@hooks.register('register_rich_text_features')
def register_button_feature(features):
    """
    Registering the `button` feature, which allows you to assign the given
    css classes to a highlighted element, which makes it look like a button
    on the frontend
    """
    feature_name = 'rich-text-button-link'
    type_ = 'rich-text-button-link'
    tag = 'div'

    control = {
        'type': type_,
        'label': 'Button',
        'description': 'Make me look like a button',
        # Optionally, we can tell Draftail what element to use when displaying those blocks in the editor.
        'element': 'div',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {tag: BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'div', 'props': {'class': 'usa-button-primary rich-text-button-link'}}}},
    })


@hooks.register('construct_page_chooser_queryset')
def show_live_pages_only(pages, request):
    pages = pages.filter(live=True)

    return pages


class InternalLinkHandler(LinkHandler):
    identifier = 'page'

    @staticmethod
    def get_model():
        return Page

    @classmethod
    def get_instance(cls, attrs):
        return super().get_instance(attrs).specific

    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            page = cls.get_instance(attrs)
            return '<a href="%s">' % escape(page.janis_url())
        except Page.DoesNotExist:
            return "<a>"
        except Exception as e:
            print("!janis url hook error!:", self.title, e)
            print(traceback.format_exc())
            pass


@hooks.register('register_rich_text_features', order=1)
def register_link_handler(features):
    features.register_link_type(InternalLinkHandler)


# In here we're going to remake all the urls for this page
@hooks.register('after_edit_page')
def after_edit_page(request, page):
    # Make sure we're publishing so our Janis urls reflect the live site
    # taking this from https://github.com/wagtail/wagtail/blob/349fca66f32ecf3df6316b0cffb4e5fd0d24d6c7/wagtail/admin/views/pages.py#L228
    publishing = bool(request.POST.get('action-publish'))
    if not publishing:
        return

    # Clear out all old urls
    for janis_url in page.janis_urls.all():
        janis_url.janis_url.delete()

    # Create the new urls
    new_urls = []

    # Page type matters here
    page_type = page._meta.object_name

    # todo: not have magic language arrays hiding around the codebase
    languages = ['en', 'es']
    for language in languages:
        # If we're a topic collection page we only have one url
        # /theme_slug/topic_collection_slug/
        if page_type == 'TopicCollectionPage':
            new_url = JanisUrl.create(
                        topic_collection_page=page,
                        theme=page.theme,
                        page_type=page_type,
                        language=language)
            new_url.save()
            new_urls.append(new_url)

        # If we're a topic page, we have a url for ever topic collection we belong to
        # /theme_slug/topic_collection_slug/topic_slug/
        elif page_type == 'TopicPage':
            for topic_page_topic_collection in page.topiccollections.all():
                new_url = JanisUrl.create(
                            topic_page=page,
                            topic_collection_page=topic_page_topic_collection.topiccollection,
                            theme=topic_page_topic_collection.topiccollection.theme,
                            page_type=page_type,
                            language=language)
                new_url.save()
                new_urls.append(new_url)

        # If we're a department page we only have one url
        # /department_slug/
        elif page_type == 'DepartmentPage':
            new_url = JanisUrl.create(
                        department_page=page,
                        page_type=page_type,
                        language=language)
            new_url.save()
            new_urls.append(new_url)

        # If we're a location page we only have one url
        # /location/location_slug/
        elif page_type == 'LocationPage':
            new_url = JanisUrl.create(
                        location_page=page,
                        page_type=page_type,
                        language=language)
            new_url.save()
            new_urls.append(new_url)

        # If we're any other page type, we need to make all our urls
        # /theme_slug/topic_collection_slug/topic_slug/page_slug/
        # /department_slug/page_slug/
        # /page_slug/
        else:
            for page_topic in page.topics.all():
                for topic_page_topic_collection in page_topic.topiccollections.all():
                    new_url = JanisUrl.create(
                                information_page=page if page_type == 'InformationPage' else None,
                                service_page=page if page_type == 'ServicePage' else None,
                                guide_page=page if page_type == 'GuidePage' else None,
                                official_documents_page=page if page_type == 'OfficialDocumentPage' else None,
                                form_container=page if page_type == 'FormContainer' else None,
                                topic_page=page_topic.topic,
                                topic_collection_page=topic_page_topic_collection.topiccollection,
                                theme=topic_page_topic_collection.topiccollection.theme,
                                page_type=page_type,
                                language=language)
                    new_url.save()
                    new_urls.append(new_url)

            for page_department in page.related_departments.all():
                new_url = JanisUrl.create(
                    information_page=page if page_type == 'InformationPage' else None,
                    service_page=page if page_type == 'ServicePage' else None,
                    guide_page=page if page_type == 'GuidePage' else None,
                    official_documents_page=page if page_type == 'OfficialDocumentPage' else None,
                    form_container=page if page_type == 'FormContainer' else None,
                    department_page=page_department.department,
                    page_type=page_type,
                    language=language)
                new_url.save()
                new_urls.append(new_url)

            # Todo: top level



    # todo: This can definitely be less copypasta'd and more pythonic
    if page_type == 'TopicCollectionPage':
        page.janis_urls = [TopicCollectionPageJanisUrl(janis_url=url, page=page) for url in new_urls]
        page.save()

    if page_type == 'TopicPage':
        page.janis_urls = [TopicPageJanisUrl(janis_url=url, page=page) for url in new_urls]
        page.save()

    if page_type == 'DepartmentPage':
        page.janis_urls = [DepartmentPageJanisUrl(janis_url=url, page=page) for url in new_urls]
        page.save()

    if page_type == 'LocationPage':
        page.janis_urls = [LocationPageJanisUrl(janis_url=url, page=page) for url in new_urls]
        page.save()

    if page_type == 'InformationPage':
        page.janis_urls = [InformationPageJanisUrl(janis_url=url, page=page) for url in new_urls]
        page.save()

    if page_type == 'ServicePage':
        page.janis_urls = [ServicePageJanisUrl(janis_url=url, page=page) for url in new_urls]
        page.save()

    if page_type == 'GuidePage':
        page.janis_urls = [GuidePageJanisUrl(janis_url=url, page=page) for url in new_urls]
        page.save()

    if page_type == 'OfficialDocumentPage':
        page.janis_urls = [OfficialDocumentPageJanisUrl(janis_url=url, page=page) for url in new_urls]
        page.save()

    if page_type == 'FormContainer':
        page.janis_urls = [FormContainerJanisUrl(janis_url=url, page=page) for url in new_urls]
        page.save()


# By default all menu items are shown all the time.
# This checks for permission and returns True if the item should be shown
class PermissionMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.has_perm('base.view_snippets')
