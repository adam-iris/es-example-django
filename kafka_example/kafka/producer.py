import kafka_interface as kafka
import uuid
import datetime
import logging
from es_lib.utils import get_instance_data, safe_json
from kafka_example.models import ExampleValue

LOGGER = logging.getLogger(__name__)


class ProducerSingleton:
    """
    Create just one producer
    """
    instance = None

    @classmethod
    def singleton(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = cls.create(*args, **kwargs)
        return cls.instance

    @classmethod
    def create(cls, topic):
        return kafka.kafka_producer(topic)


def produce_example_message(value):
    """
    Produce one message
    """
    topic = 'example'
    producer = ProducerSingleton.singleton(topic)

    model = ExampleValue(
        value=value,
        timestamp=datetime.datetime.utcnow(),
    )
    model.clean()
    instance_data = get_instance_data(model)
    LOGGER.info(safe_json(instance_data))
    message = {
        'data_id': model.data_id,
        'timestamp': model.timestamp.isoformat(),
        'value': model.value,
    }
    key = {
        'key': str(uuid.uuid1()),
    }
    producer.produce(key, message)
    producer.flush()
    return message
