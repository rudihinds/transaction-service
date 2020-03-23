import pika


def channel():
    host = '5672'
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    return channel


def consume(channel, callback):
    channel.basic_consume(callback, queue='hello', no_ack=True)
    channel.start_consuming()
