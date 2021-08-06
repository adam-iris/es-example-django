from django.db import models
from datetime import timedelta
from kafka_example.utils import create_data_identifier, random_message
from appconf import AppConf


class ExampleAppConf(AppConf):
    """
    Defaults for settings that can be overridden in settings.py
    The real setting has the app prefix, eg. TOPIC overrides EXAMPLE_TOPIC
    """
    TOPIC = "example"


class ExampleValue(models.Model):
    """
    Simple model corresponding to the example avro value
    """
    data_id = models.CharField(
        max_length=1024,
        blank=True,
    )
    data_provenance = models.JSONField(default=list)
    timestamp = models.DateTimeField()
    value = models.CharField(
        max_length=250,
        blank=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.data_id:
            self.data_id = create_data_identifier()
        if not self.value:
            self.value = random_message()

    def add_provenance(self, provenance_id):
        """
        Add an element to the provenance list
        """
        if provenance_id not in self.data_provenance:
            self.data_provenance.append(provenance_id)
    
    def delay(self):
        """
        Calculate the delay from when the message was sent to when
        it was saved to the db
        """
        if self.timestamp and self.created_date:
            return self.created_date - self.timestamp

    def delay_ms(self):
        """
        Get the delay in ms
        """
        return self.delay() / timedelta(milliseconds=1)
