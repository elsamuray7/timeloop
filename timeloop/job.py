from threading import Thread, Event
from datetime import timedelta

class Job(Thread):
    def __init__(self, interval, execute, initial_delay, *args, **kwargs):
        Thread.__init__(self)
        self.stopped = Event()
        self.interval = interval
        self.delay = initial_delay or timedelta(seconds=0)
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        if not self.stopped.wait(self.delay.total_seconds()):
            self.execute(*self.args, **self.kwargs)
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)
