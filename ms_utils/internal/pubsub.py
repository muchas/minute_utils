import json
import pika
from contextlib import contextmanager

from ms_utils.logging import get_stdout_logger


logger = get_stdout_logger(__name__)


@contextmanager
def get_channel(settings, type_='topic'):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBIT_HOST)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=settings.RABBIT_EXCHANGE, type=type_)

    yield channel

    connection.close()


def get_producer(settings):
    def produce(message, key):
        logger.info('producing new event [message:{},key:{}]'.format(message, key))

        try:
            with get_channel(settings) as channel:
                channel.basic_publish(exchange=settings.RABBIT_EXCHANGE,
                                      routing_key=key,
                                      body=json.dumps(message))
        except Exception:
            logger.exception('error during pubsub event producing [message:{},key:{}]'
                             .format(message, key))
            return False
        return True

    return produce


def consume(settings, callback, binding_keys):
    with get_channel(settings) as channel:
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        for key in binding_keys:
            channel.queue_bind(
                exchange=settings.RABBIT_EXCHANGE,
                queue=queue_name, routing_key=key)

        channel.basic_consume(callback, queue=queue_name, no_ack=True)
        channel.start_consuming()
