#!/usr/bin/env python

import inspect
import os
import cPickle as pickle
import pyreadline as readline

storage_version = 1
history = []
commands = {}
tracks=[ [] ]

save_filename = "tb"

def save():
    with open(save_filename, "wb") as f:
        pickle.dump(storage_version, f)
        pickle.dump(tracks, f)

def load():
    global track
    global tracks
    with open(save_filename, "rb") as f:
        ver = pickle.load(f)
        assert ver==storage_version
        tracks = pickle.load(f)

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
    track.insert(0, line)

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
        print g(t, 0, '<empty>')

@command('nt')
def new_track(tracks, rem):
    track = []
    tracks.insert(0, track)

    if rem:
        track.append(rem)

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
