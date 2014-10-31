import cPickle as pickle

class Upgradeable(object):
    def __getstate__(self):
        self.version = self.class_version()
        return self.__dict__

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

        if self.version < self.class_version():
            self.upgrade(self.version)
            self.version = self.class_version()
        elif self.version > self.class_version():
            raise Exception("Can't downgrade versions")

    def upgrade(self, from_version):
        raise Exception("upgrade() not implemented")

    def class_version(self):
        return self.__class__.version
