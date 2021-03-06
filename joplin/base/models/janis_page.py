import os
import graphene
import traceback

from django.db import models, ProgrammingError
from django.conf import settings
from wagtail.search import index
from wagtail.utils.decorators import cached_classmethod
from wagtail.admin.edit_handlers import FieldPanel, ObjectList, TabbedInterface
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from flags.state import flag_enabled

from base.models.site_settings import JanisBranchSettings


class JanisBasePage(Page):
    """
    This is base page class made for our pages to inherit from.
    It is abstract, which for Django means that it isn't stored as it's own table
    in the DB.
    We use it to add functionality that we know will be desired by all other pages,
    such as setting the preview fields and urls for janis stuff to make our headless
    setup work smoothly
    """

    parent_page_types = ['base.HomePage']
    subpage_types = []
    search_fields = Page.search_fields + [
        index.RelatedFields('owner', [
            index.SearchField('last_name', partial_match=True),
            index.FilterField('last_name'),
        ])
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author_notes = RichTextField(
        # max_length=DEFAULT_MAX_LENGTH,
        features=['ul', 'ol', 'link'],
        blank=True,
        verbose_name='Notes for authors (Not visible on the resident facing site)'
    )

    notes_content_panel = [
        FieldPanel('author_notes')
    ]

    coa_global = models.BooleanField(default=False, verbose_name='Make this a top level page')

    def janis_url(self):
        """
        This function parses various attributes of related content types to construct the
        expected url structure for janis.

        For attributes with multiple relations, it ONLY takes the FIRST one.
        """
        try:
            """
             These use ternary operators with some appropriate conditionals
             the idea is: return this value in these cases or tell use you got
             nothing (see the privacy policy info page for example).

             'None' responses get filtered out and removed from the URL path.

             TODO:
             make this more abstract(potentially not by content type)
             further check if the order of conditionals affects performance
             Better utilization of querysets may be possible for better performance
            """
            page_slug = self.slug or None
            has_no_theme = [
                'service page',
                'topic page',
                'information page',
                'department page',
                'guide page',
                'official document page',
                'form container',
                'location page'
            ]
            has_no_topic_collection = has_no_theme

            has_no_topic = [
                'topic page',
                'topic collection page',
                'department page',
                'location page'
            ]

            theme_slug = (
                self.theme.slug
                if self.content_type.name not in has_no_theme
                else None
            )
            # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#first
            topic_collection_slug = (
                self.topiccollections.first().topiccollection.slug
                if
                (
                    self.content_type.name not in has_no_topic_collection and
                    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#exists
                    self.topiccollections.exists()
                )
                else None
            )
            topic_slug = (
                self.topics.first().topic.slug
                if
                (
                    self.content_type.name not in has_no_topic and
                    self.topics.exists()
                )
                else None
            )

            # add hardcoded language path to base url
            base_url = f"{self.janis_url_base('publish_janis_branch')}/en"

            # Quick location page exception
            if self.content_type.name == 'location page':
                location_url = base_url + '/location/' + page_slug
                return location_url

            # attributes for the url are needed by not discovered yet lets fetch them
            # looking for missing elements, deducing content type from what works and what dosen't
            # this is pretty ugly and ought to be cleaned up
            if theme_slug is None and self.content_type.name != 'department page':
                try:
                    theme_slug = self.topics.first().topic.topiccollections.first().topiccollection.theme.slug or None
                    topic_collection_slug = self.topics.first().topic.topiccollections.first().topiccollection.slug or None
                except AttributeError as e:
                    try:
                        theme_slug = self.topiccollections.first().topiccollection.theme.slug or None
                        topic_collection_slug = self.topiccollections.first().topiccollection.slug or None
                    except AttributeError as e:
                        # this is for pages just under departments
                        theme_slug = self.related_departments.all()[0].related_department.slug or None
                    finally:
                        paths_list = [
                            base_url,
                            theme_slug,
                            topic_collection_slug,
                            topic_slug,
                            page_slug]
                        janis_url = '/'.join(filter(None, (paths_list)))
                        return janis_url
            # collect all our path elements
            paths_list = [
                base_url,
                theme_slug,
                topic_collection_slug,
                topic_slug,
                page_slug
            ]
            # join them together, filtering out empty ones

            janis_url = '/'.join(filter(None, (paths_list)))
            return janis_url
        except Exception as e:
            # right now this is a catch-all,
            print("!janis url error!:", self.title, e)
            print(traceback.format_exc())
            return "#"
            pass

    def janis_preview_url_end(self, revision=None):
        """
            Optional "revision" parameter to get the janis_preview_url for a specific revision
            Otherwise, it will return the janis_preview_url for the latest revision
        """
        if revision:
            url_page_type = revision.page.janis_url_page_type
        else:
            revision = self.get_latest_revision()
            url_page_type = self.janis_url_page_type
        try:
            global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)
            url_end = f"preview/{url_page_type}/{global_id}"
        except AttributeError:
            # TODO: make previews work for test fixture pages that may not have revisions/global_ids
            url_end = f"preview/{url_page_type}/"

        if settings.ISSTAGING or settings.ISPRODUCTION:
            return url_end
        else:
            # Pass address of CMS_API if we are not running on Staging or Production
            # Janis will query from its default CMS_API if a param is not provided
            return url_end + f"?CMS_API={settings.CMS_API}"

    def janis_url_base(self, janis_branch):
        """
        returns a valid url of the base URL in janis:
            Use hardcoded JANIS_URL for staging and prod
            Otherwise, use configurable branch setting

        TODO: this and url_base in site settings could probably
        be revisited for semantics to be less confusing
        """
        if settings.ISSTAGING or settings.ISPRODUCTION:
            return os.getenv("JANIS_URL")
        else:
            branch_settings = JanisBranchSettings.objects.first()
            return branch_settings.url_base(janis_branch)

    # alias for url base function
    janis_preview_url_start = janis_url_base

    # TODO this function and preview_url_data are pretty similar, we can probably consolidate them
    def janis_preview_url(self, revision=None, lang="en"):
        return f"{self.janis_preview_url_start('preview_janis_branch')}/{lang}/{self.janis_preview_url_end(revision=revision)}"

    # data needed to construct preview URLs for any language
    # [janis_preview_url_start]/[lang]/[janis_preview_url_end]
    # ex: http://localhost:3000/es/preview/information/UGFnZVJldmlzaW9uTm9kZToyMjg=
    def preview_url_data(self, revision=None):
        return {
            "janis_preview_url_start": self.janis_preview_url_start('preview_janis_branch'),
            "janis_preview_url_end": self.janis_preview_url_end(revision=revision),
        }

    @property
    def status_string(self):
        """
        override wagtail default
        see https://github.com/wagtail/wagtail/blob/f44d27642b4a6932de73273d8320bbcb76330c21/wagtail/core/models.py#L1010
        """
        if not self.live:
            if self.expired:
                return ("Expired")
            elif self.approved_schedule:
                return ("Scheduled")
            else:
                return ("Draft")
        else:
            if self.approved_schedule:
                return ("Live + Scheduled")
            elif self.has_unpublished_changes:
                return ("Live + Draft")
            else:
                return ("Live")

    @cached_classmethod
    def get_edit_handler(cls):
        if hasattr(cls, 'edit_handler'):
            return cls.edit_handler.bind_to(model=cls)

        editor_panels = [
            ObjectList(cls.content_panels + [AdminOnlyFieldPanel('coa_global', classname="admin-only-field")], heading='Content'),
            ObjectList(cls.notes_content_panel, heading='Notes')

        ]

        try:
            if flag_enabled('SHOW_EXTRA_PANELS'):
                editor_panels += (PermissionObjectList(cls.promote_panels,
                                             heading='SEO'),
                                  PermissionObjectList(cls.settings_panels,
                                             heading='Settings'))
        except ProgrammingError as e:
            print("some problem, maybe with flags")
            pass

        edit_handler = TabbedInterface(editor_panels)

        return edit_handler.bind_to(model=cls)

    class Meta:
        abstract = True
        # https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#custom-permissions
        permissions = [
            ("view_extra_panels", "Can view extra panels"),
            ("view_snippets", "Can view snippets"),
            ("add_snippets", "Can add snippet"),
            ("delete_snippets", "Can delete snippet"),
        ]


class AdminOnlyFieldPanel(FieldPanel):
    def on_form_bound(self):
        model_name = self.model.__name__
        self.bound_field = self.form[self.field_name]
        self.help_text = self.bound_field.help_text
        # If user is superuser and page is Service Page or Information Page
        # show the field panel text "Make This a Top Level Page"
        if self.request.user.is_superuser:
            if model_name is 'ServicePage' or model_name is 'InformationPage':
                self.heading = self.bound_field.label
            else:
                self.heading = ""
        else:
            self.heading = ""

    def render_as_object(self):
        model_name = self.model.__name__
        # Checks to see if user is super user, if so render object
        # if not, return empty string which overrides the object/checkbox
        if not self.request.user.is_superuser:
            return ''
        if model_name is not 'ServicePage' and model_name is not 'InformationPage':
            return ''

        return super().render_as_object()


class PermissionObjectList(ObjectList):
    def __init__(self, children=(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hide_panel = True
        self.children = children

    def on_form_bound(self):
        if self.request.user.has_perm('base.view_extra_panels'):
            # tabbed_interface.html checks to see if the panel should be hid
            # and if so prevents the tab from being added
            self.hide_panel = False
        return super().on_form_bound()

    def render(self):
        # this only hides the content of the tab, not the tab/heading itself
        if not self.request.user.has_perm('base.view_extra_panels'):
            return ""

        return super().render()
