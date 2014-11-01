#!/usr/bin/env python

import inspect
import os
from peewee import *
import cPickle as pickle

if os.name=='nt':
    import pyreadline as readline
else:
    import readline
from datetime import datetime
from upgradeable import Upgradeable

commands = {}
db = SqliteDatabase('people.db')

def next_project():
    max_id = -1
    for task in Task.select():
        max_id = max(max_id, task.project)

    return max_id + 1


class Setting(Model):
    keyword = CharField(null=False, unique=True)
    str_value = CharField(null=True)
    int_value = IntegerField(null=True)

    class Meta:
        database = db

    @staticmethod
    def current_project(val=None):
        try:
            s = Setting.get(Setting.keyword == 'current_project')
        except Setting.DoesNotExist:
            s = Setting(keyword='current_project', int_value=0)
            s.save()

        if not val:
            return s.int_value
        else:
            s.int_value = val
            s.save()

class Task(Model):
    description = CharField(null=False, default="")
    created = DateTimeField(default=datetime.utcnow)
    completed = DateTimeField(null=True)
    project = IntegerField(default=0)
    order = IntegerField(null=True)

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

    class Meta:
        database = db

    def __str__(self):
        return self.description



class Database(Upgradeable):
    """Container for data structures, used so we can take advantage
    of easy schema changes."""

    version = 8

    def __init__(self):
        self.tracks = [[]]
        self.history = []

    def upgrade(self, from_version):
        pass


class Task2(Upgradeable):
    version = 5

    def __init__(self, text=""):
        self.created = datetime.utcnow()
        self.completed = None
        self.text = text

    def __str__(self):
        return self.text

    def upgrade(self, from_version):
        pass

class Config(Upgradeable):
    version = 1

    def __init__(self):
        self.auto_clear = False

    def upgrade(self, from_version):
        pass

def save():
    with open(save_filename, "wb") as f:
        pickle.dump(storage_version, f)
        pickle.dump(database, f)

def load():
    global tracks
    global database
    with open(save_filename, "rb") as f:
        ver = pickle.load(f)

        if ver==2:
            database.tracks = pickle.load(f)
        elif ver==storage_version:
            database = pickle.load(f)
        else:
            assert("Migration error")

        tracks = database.tracks


def command(keyword):
    def decorator(f):
        assert keyword not in commands
        commands[keyword] = f
        def wrapper(*args, **kwargs):
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
    p = Setting.current_project()
    t = Task(description = line)
    t.project = p
    t.save()

@command('d')
def drop(track, tracks):
    if len(track) > 0:
        root = track[-1]
        database.history.append( (track[0], root) )
        del track[0:1]
    else:
        if len(tracks) > 1:
            del tracks[0:1]

@command('l')
def list(track):
    for t in Task.select().where(Task.project == Setting.current_project()):
        print t

@command('h')
def history():
    for t in database.history:
        print "{}  ({})".format(t[0], t[1])

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
    p = Setting.current_project() + 1
    Task(description=rem, project=p).save()
    Setting.current_project(val=p)

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

storage_version = 3
history = []
database = Database()

save_filename = "tb"

if os.path.exists(save_filename):
    load()


db.create_tables([Task, Setting], safe=True)

while True:
    track = tracks[0]
    if len(track) > 0:
        print track[0]
    cmd = raw_input('{} > '.format(len(track)))
    parse(cmd)
    print
