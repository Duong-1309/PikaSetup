import pika


class Publisher:
    def __init__(self, config):
        self.config = config
        
    def publish(self, routing_key, message):       
        connection = self.create_connection()
        # Create a new channel with the next available channel number or pass in a channel number to use
        channel = connection.channel()
        # Creates an exchange if it does not already exist, and if the exchange exists,
        # verifies that it is of the correct and expected class.
        channel.queue_declare('test_queue')
        channel.exchange_declare(exchange=self.config['exchange'], exchange_type='topic')
        channel.queue_bind('test_queue', exchange=self.config['exchange'], routing_key='test.*')
        
        #Publi shes message to the exchange with the given routing key
        channel.basic_publish(exchange=self.config['exchange'], routing_key=routing_key, body=message)
        print('[x] Sent message %r for %r' % (message,routing_key))
    
    
    # Create new connection
    def create_connection(self):
        param = pika.ConnectionParameters(host=self.config['host'], port=self.config['port']) 
        return pika.BlockingConnection(param)
    
config = { 'host': 'localhost','port': 5672, 'exchange' : 'my_exchange'}
publisher = Publisher(config)
for i in range(100):
    publisher.publish('test.nifty', f'New Data {i}')
