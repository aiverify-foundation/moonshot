from ..interface.queue_connection import I_QueueConnection


# Just a placeholder for implementation using RabbitMQ
# Will probably remove this if we don't end up adding the implementation details below

class RabbitMQQueue(I_QueueConnection):
    def connect(self):
        # Connect to RabbitMQ server
        pass

    def create_channel(self, channel_name):
        # Create a RabbitMQ channel
        pass

    def consume(self, channel_name):
        # Consume messages from a RabbitMQ channel
        pass

    def publish(self, channel_name, task):
        # Publish a message to a RabbitMQ channel
        pass

    def close(self):
        # Close the RabbitMQ connection
        pass