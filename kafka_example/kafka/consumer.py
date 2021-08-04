import kafka_interface as kafka
import logging
from kafka_example.models import ExampleValue
from es_common.utils import retry, RetryableError

LOGGER = logging.getLogger(__name__)


class RetryableConsumerError(RetryableError):
    """
    Indicates a condition where the consumer should retry
    """


def rethrow_error(err):
    """
    Convert a low-level kafka error, mainly this is to throw
    a retryable error if we can
    """
    # Topic is unknown
    name = getattr(err, 'name', '')
    if name.startswith('UNKNOWN_TOPIC'):
        raise RetryableConsumerError("Unknown topic")


class ExampleConsumer(object):
    """
    Just consumes from the topic
    """
    topic = 'example'

    def consume(self, message):
        """
        Consume one message
        """
        LOGGER.info("Message: %s", message)
        value = message.get('value', {})
        obj = ExampleValue(**value)
        obj.clean()
        obj.save()

    @retry(count=100, delay=2, backoff=2)
    def run(self):
        """
        Consume messages
        """
        consumer = kafka.kafka_consumer(self.topic)
        LOGGER.info("Starting consumer")

        try:
            while True:
                message = consumer.consume()
                self.consume(message)
        except Exception as e:
            LOGGER.error("Failed with %s", e)
            # Maybe rethrow as an alternate type
            rethrow_error(e)
            # Otherwise, throw the original
            raise

        
