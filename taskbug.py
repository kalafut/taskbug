history = []

class Track:
    def __init__(self, task=None):
        self.tasks = []
        self.push(task)


    def push(self, task):
        if task:
            self.tasks.append(task)

    def pop(self):
        return self.tasks.pop()

    def top(self):
        if self.count() > 0:
            return self.tasks[-1]
        else:
            return None

    def count(self):
        return len(self.tasks)

class TrackCollection:
    def __init__(self):
        self.tracks = [Track()]
        self.current_track = 0
        self.last_track = 0

    def current(self):
        return self.tracks[self.current_track]

    def add(self, task):
        self.tracks.append(Track(task))
        self.current_track = len(self.tracks) - 1

    def delete(self):
        pass


tc = TrackCollection()

while True:
    t = tc.current()
    print t.top()
    cmd = raw_input('>' * (t.count() + 1))
    if cmd == "done":
        history.append(t.pop())
    elif cmd == "hist":
        print history
    elif cmd.startswith("n "):
        tc.add(cmd)
    elif cmd == "q":
        pass


    else:
        t.push(cmd)

    print
