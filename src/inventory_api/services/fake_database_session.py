class FakeDatabaseSession:
    def __init__(self):
        self.closed=False

    def close(self):
        self.closed=True