class MockEvents:
    def __init__(self):
        self.last_event = None
        self.action = None

    def produce(self, event):
        self.last_event = event
        if self.action is not None:
            self.action(event)

    def on_event(self, action):
        self.action = action
