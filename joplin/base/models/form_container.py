from django.db import models

from wagtail.core.fields import RichTextField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel

from base.forms import FormContainerForm

from .janis_page import JanisBasePage

from .constants import WYSIWYG_GENERAL
from .widgets import countMe, countMeTextArea
from countable_field import widgets

class FormContainer(JanisBasePage):
    janis_url_page_type = "form"
    base_form_class = FormContainerForm

    description = models.TextField(verbose_name='Form description', blank=True)
    form_url = models.URLField(
        verbose_name='Enter the URL of your Formstack form',
        help_text='This link can be found under Share > "Link to this form on your website or email:"',
        blank=True,
    )

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        InlinePanel('topics', label='Topics'),
        InlinePanel('related_departments', label='Related Departments'),
        FieldPanel('description', widget=countMeTextArea),
        FieldPanel('form_url'),
    ]

class FormContainerRelatedDepartments(ClusterableModel):
    page = ParentalKey(FormContainer, related_name='related_departments', default=None)
    related_department = models.ForeignKey(
        "base.departmentPage",
        on_delete=models.PROTECT,
    )

    panels = [
        # Use a SnippetChooserPanel because blog.BlogAuthor is registered as a snippet
        PageChooserPanel("related_department"),
    ]

class FormContainerTopic(ClusterableModel):
    page = ParentalKey(FormContainer, related_name='topics')
    topic = models.ForeignKey('base.TopicPage', verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topic'),
    ]

    def __str__(self):
        return self.topic.text
