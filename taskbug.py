#!/usr/bin/env python

import inspect
import os
import readline

history = []
commands = {}
tracks=[ [] ]
track = tracks[0]


def command(keyword):
    def decorator(f):
        assert keyword not in commands
        commands[keyword] = f
        def wrapper(*args, **kwargs):
            print keyword
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
    for k,f in commands.iteritems():
        print "{} - {}".format(k, f[1])

@command('__DEFAULT__')
def add(line):
    track.insert(0, line)

@command('d')
def drop(track):
    if len(track) > 0:
        del track[0:1]

@command('l')
def list(line, track):
    for t in track:
        print t

@command('t')
def select_track(line):
    global track
    tnum = int(line)
    if tnum < len(tracks):
        tracks.insert(0,tracks.pop(tnum))

    track = tracks[0]

@command('lt')
def list_tracks(line):
    for t in reversed(tracks):
        print t[0]

@command('nt')
def new_track(rem):
    global track
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
            'track': track
        }

        func = commands['__DEFAULT__']
        for k,fn in commands.iteritems():
            if cmd == k:
                func = fn
                break
        invoke(func, args)

def invoke(fn, params):
    args = inspect.getargspec(fn).args
    target_args = []
    for i,arg in enumerate(args):
        target_args.append(params[arg])
    fn(*target_args)


while True:
    if len(track) > 0:
        print track[0]
    cmd = raw_input('{} > '.format(len(track)))
    parse(cmd)
    print
