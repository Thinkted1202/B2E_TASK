from flask import current_app
from hashids import Hashids

class HashidsHelper(object):
    salt = 'Test'
    min_length = 8

    def __init__(self, **kwargs):
        self.obj = Hashids(salt=self.salt,min_length=self.min_length)

    def hashid(self,source):
        return self.obj.encode(source)
