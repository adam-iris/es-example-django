from django.db import models
import uuid
from datetime import timedelta
import random


def data_identifier():
    """
    Return some random value for a message
    """
    return "example:py/%s" % str(uuid.uuid1())


def random_message():
    """
    Return some random message
    """
    PEOPLE = [
        'Homer', 'Marge', 'Bart', 'Lisa', 'Maggie', 'Moe', 'Barney', 
        'Carl', 'Lenny', 'Mr. Burns', 'Bumblebee Man', 'McBain',
    ]
    PLACES = [
        '642 Evergreen Terrace', "Moe's Bar", 'Springfield Elementary',
        'Springfield Nuclear Power Plant', 'Capital City',
    ]
    return "%s calls %s from %s" % (
        random.choice(PEOPLE),
        random.choice(PEOPLE),
        random.choice(PLACES),
    )


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
        max_length=64,
        blank=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.data_id:
            self.data_id = data_identifier()
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
