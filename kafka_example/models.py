from django.db import models
from datetime import timedelta
from kafka_example.utils import create_data_identifier, random_message


class ExampleValue(models.Model):
    """
    Simple model corresponding to the example avro value
    """
    data_id = models.CharField(
        max_length=64,
        blank=True,
    )
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

    def delay(self):
        """
        Calculate the delay from when the message was sent to when
        it was saved to the db
        """
        if self.timestamp and self.created_date:
            return self.created_date - self.timestamp

    def delay_ms(self):
        """
        Calculate the delay from when the message was sent to when
        it was saved to the db
        """
        return self.delay() / timedelta(milliseconds=1)
