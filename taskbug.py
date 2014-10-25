#!/usr/bin/env python

import os
import readline
history = []

commands = {}
tracks=[ [] ]
track = tracks[0]

class Track:
    def __init__(self, task=None):
        self.tasks = []
        self.push(task)

    def push(self, task):
        if task:
            self.tasks.append(task)

    def pop(self):
        if not self.is_empty():
            return self.tasks.pop()

    def top(self):
        if not self.is_empty():
            return self.tasks[-1]
        else:
            return None

    def count(self):
        return len(self.tasks)

    def list(self):
        for t in self.tasks:
            print t

    def is_empty(self):
        return self.count() == 0

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

def command(keyword, helptext=None):
    def decorator(f):
        assert keyword not in commands
        commands[keyword] = (f, helptext)
        def wrapper(*args, **kwargs):
            print keyword
            return f(*args, **kwargs)
        return wrapper
    return decorator

@command('clear', "Clear Screen")
def clear(line):
    os.system("clear")

@command('q')
def quit(line):
    exit()

@command('?')
def help(line):
    for k,f in commands.iteritems():
        print "{} - {}".format(k, f[1])

@command('__DEFAULT__')
def add(line):
    t = tc.current()
    t.push(line)


@command('d')
def drop(line):
    t = tc.current()
    t.pop()

@command('l')
def list(line):
    tc.current().list()

def parse(line):
    for k,f in commands.iteritems():
        if line.startswith(k):
            f[0](line)
            return
    commands['__DEFAULT__'][0](line)

while True:
    t = tc.current()
    print t.top()
    cmd = raw_input('{} > '.format(t.count()))
    parse(cmd)
    print
