#!/usr/bin/env python

import inspect
import os
import cPickle as pickle
import pyreadline as readline
from datetime import datetime

storage_version = 2
history = []
commands = {}
tracks=[ [] ]

save_filename = "tb"

class Task(object):
    def __init__(self, text=""):
        self.version = 3
        self.created = datetime.now()
        self.text = text

    def __str__(self):
        return self.text

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

def save():
    with open(save_filename, "wb") as f:
        pickle.dump(storage_version, f)
        pickle.dump(tracks, f)

def load():
    global track
    global tracks
    with open(save_filename, "rb") as f:
        ver = pickle.load(f)

        if ver==1:
            old_tracks = pickle.load(f)
            tracks = []
            for tr in old_tracks:
                tl = []
                for ta in tr:
                    tl.append(Task(ta))
                tracks.append(tl)
        elif ver==storage_version:
            tracks = pickle.load(f)
        else:
            assert("Migration error")



def command(keyword):
    def decorator(f):
        assert keyword not in commands
        commands[keyword] = f
        def wrapper(*args, **kwargs):
            print keyword # What is this??
            return f(*args, **kwargs)
        return wrapper
    return decorator


@command('clear')
def clear(line):
    os.system("clear")

@command('q')
def quit(line):
    exit()

@command('?')
def help(line):
    """ Yay """
    for k,f in commands.iteritems():
        print "{} - {}".format(k, inspect.getdoc(f))

@command('__DEFAULT__')
def add(track, line):
    track.insert(0, Task(line))

@command('d')
def drop(track, tracks):
    if len(track) > 0:
        del track[0:1]
    else:
        if len(tracks) > 1:
            del tracks[0:1]


@command('l')
def list(track):
    for t in reversed(track):
        print t

@command('b')
def bump(track):
    """ Bump task up """
    if len(track) > 1:
        track.insert(1,track.pop(0))

@command('t')
def select_track(rem, tracks):
    tnum = int(rem)
    if tnum < len(tracks):
        tracks.insert(0,tracks.pop(tnum))

@command('lt')
def list_tracks(line):
    for t in reversed(tracks):
        print "{}   {}".format(g(t, 0, '<empty>'), t[0].created)

@command('nt')
def new_track(tracks, rem):
    track = []
    tracks.insert(0, track)

    if rem:
        add(track, rem)

def parse(raw_line):
    line = raw_line.strip()
    if line:
        cmd = line.split()[0]
        rem = line[len(cmd):].strip()
        args = {
            'line': line,
            'cmd': cmd,
            'rem': rem,
            'track': tracks[0],
            'tracks': tracks
        }

        func = commands['__DEFAULT__']
        for k,fn in commands.iteritems():
            if cmd == k:
                func = fn
                break
        invoke(func, args)
        save()

def invoke(fn, params):
    args = inspect.getargspec(fn).args
    target_args = []
    for i,arg in enumerate(args):
        target_args.append(params[arg])
    fn(*target_args)

def g(seq, idx, default):
    return seq[idx] if len(seq) > idx else default

if os.path.exists(save_filename):
    load()

while True:
    track = tracks[0]
    if len(track) > 0:
        print track[0]
    cmd = raw_input('{} > '.format(len(track)))
    parse(cmd)
    print
