import queue

from abc import ABC, abstractmethod
 
class Publisher:
    def __init__(self):
        self.message_queue = queue.Queue()
        self.subscribers = []
 
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
 
    def publish_and_execute(self, message):
        self.message_queue.put(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)
    


# interface
class Subscriber(ABC):
    @abstractmethod
    def receive(self, message):
        ...
 