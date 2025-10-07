from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def handle(self, request):
        pass

class Middleware(Handler):
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)

    def handle(self, request):
        for handler in self.handlers:
            request = handler.handle(request)
            if request is None:
                break
        return request