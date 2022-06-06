import pika
import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        print(self.corr_id)
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response1 = fibonacci_rpc.call(30)
print(" [.] Got %r" % response1)

# print(" [x] Requesting fib(40)")
# response2= fibonacci_rpc.call(40)
# print(" [.] Got %r" % response2)

# print(" [x] Requesting fib(50)")
# response3 = fibonacci_rpc.call(50)
# print(" [.] Got %r" % response3)

# print(" [x] Requesting fib(60)") 
# response4 = fibonacci_rpc.call(60)
# print(" [.] Got %r" % response4)