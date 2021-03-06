from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from base.forms import OfficialDocumentPageForm

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel

from .janis_page import JanisBasePage

from .constants import DEFAULT_MAX_LENGTH
from .widgets import countMe, countMeTextArea, AUTHOR_LIMITS
from countable_field import widgets

"""
This is a page that displays a list of Official Documents (model: umentPageOfficialDocument).
This page can be assigned to multiple topics or departments.
The Documents will be displayed in date descending order (newest first by the "date" field).
Eventually the OfficialDocumentPageOfficialDocument should be replaced by a model using Wagtail Documents
"""


class OfficialDocumentPage(JanisBasePage):
    janis_url_page_type = "official_document"
    base_form_class = OfficialDocumentPageForm

    description = models.TextField(blank=True)

    content_panels = [
        FieldPanel('title_en', widget=countMe),
        FieldPanel('title_es', widget=countMe),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description', widget=countMeTextArea),
        InlinePanel('topics', label='Topics'),
        InlinePanel('related_departments', label='Related Departments'),
        InlinePanel('official_documents', label="Documents", heading="Entries will be listed by document date (newest first)."),
    ]


"""
An OfficialDocumentPageOfficialDocument is an Official Document belonging to a single OfficialDocumentPage.
One OfficialDocumentPage can have many OfficialDocumentPageOfficialDocuments.
"""


class OfficialDocumentPageOfficialDocument(Orderable):
    page = ParentalKey(OfficialDocumentPage, related_name='official_documents')
    date = models.DateField(verbose_name="Document date", null=True)
    title = models.CharField(verbose_name="Document title", max_length=DEFAULT_MAX_LENGTH)
    authoring_office = models.CharField(verbose_name="Authoring office of document", max_length=DEFAULT_MAX_LENGTH)
    summary = models.TextField(verbose_name="Document summary")
    name = models.CharField(verbose_name="Name of Document", max_length=DEFAULT_MAX_LENGTH)
    document = models.ForeignKey(Document, null=True, blank=False, on_delete=models.SET_NULL, related_name='+')

    panels = [
        FieldPanel('date'),
        FieldPanel('title', widget=countMe),
        FieldPanel('authoring_office', widget=countMe),
        FieldPanel('summary', widget=widgets.CountableWidget(attrs={
            'data-count': 'characters',
            'data-max-count': AUTHOR_LIMITS['document_summary'],
            'data-count-direction': 'down'
        })),
        FieldPanel('name', widget=countMe),
        DocumentChooserPanel('document')
    ]

    class Meta:
        indexes = [models.Index(fields=['-date'])]


class OfficialDocumentPageRelatedDepartments(ClusterableModel):
    page = ParentalKey(OfficialDocumentPage, related_name='related_departments', default=None)
    related_department = models.ForeignKey(
        "base.departmentPage",
        on_delete=models.PROTECT,
    )

    panels = [
        PageChooserPanel("related_department"),
    ]


class OfficialDocumentPageTopic(ClusterableModel):
    page = ParentalKey(OfficialDocumentPage, related_name='topics')
    topic = models.ForeignKey('base.TopicPage', verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topic'),
    ]

    def __str__(self):
        return self.topic.text
