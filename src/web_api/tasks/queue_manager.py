from .interface.queue_connection import I_QueueConnection

class QueueManager:
    def __init__(self, connection: I_QueueConnection):
        self.connection = connection

    def connect(self):
        self.connection.connect()
        return self.connection

    def create_channel(self, channel_name):
        self.connection.create_channel(channel_name)

    def consume(self, channel_name):
        return self.connection.consume(channel_name)

    def publish(self, channel_name, task):
        self.connection.publish(channel_name, task)

    def close(self):
        self.connection.close()