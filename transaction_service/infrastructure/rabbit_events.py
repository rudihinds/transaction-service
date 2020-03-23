from pika import ConnectionParameters, BlockingConnection

from transaction_service.utils import transpose_event


class RabbitConnection:
    def __init__(self, properties):
        self.exchange = properties['exchange']

        params = ConnectionParameters(host=properties['host'],
                                      heartbeat_interval=600,
                                      blocked_connection_timeout=300)
        connection = BlockingConnection(params)
        self.channel = connection.channel()

        self.channel.exchange_declare(self.exchange, exchange_type='fanout')


class RabbitProducer(RabbitConnection):
    def __init__(self, properties):
        super().__init__(properties)

    def produce(self, event):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key='',
                                   body=event)


class RabbitConsumer(RabbitConnection):
    def __init__(self, properties):
        self.queue = properties['queue']

        super().__init__(properties)

        self.channel.queue_declare(queue=self.queue)
        self.channel.queue_bind(queue=self.queue, exchange=self.exchange)

    def on_event(self, action):
        def callback(ch, method, properties, body):
            payload = transpose_event(body)
            action(payload)

        self.channel.basic_consume(queue=self.queue,
                                   consumer_callback=callback,
                                   no_ack=True)
        self.channel.start_consuming()
