from django.db import models

from modelcluster.models import ClusterableModel
from wagtail.core.fields import StreamField
from wagtail.core.blocks import URLBlock
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, FieldRowPanel
from base.blocks import MapBlock
from .constants import DEFAULT_MAX_LENGTH


@register_snippet
class Location(ClusterableModel):
    TX = 'TX'
    STATE_CHOICES = (
        (TX, 'Texas'),
    )

    USA = 'United States'
    COUNTRY_CHOICES = (
        (USA, 'United States'),
    )

    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    street = models.TextField()
    city = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='Austin')
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default=TX)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default=USA)
    zip = models.CharField(max_length=50)

    map = StreamField(
        [
            (
                'location', MapBlock(zoom_level=7, marker_description=name, marker_title=street)
            )
        ],
        blank=True
    )

    panels = [
        FieldPanel('name'),
        MultiFieldPanel(children=[
            FieldPanel('street'),
            FieldPanel('city', classname='col5'),
            FieldPanel('state', classname='col4'),
            FieldPanel('zip', classname='col2'),
            FieldPanel('country', classname='col5'),
            StreamFieldPanel('map')
        ], heading='Location'),
    ]

    def __str__(self):
        return self.name
