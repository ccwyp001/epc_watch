class IdentityFormater(object):
    _DELIMITER = ':'

    @classmethod
    def load(cls, identity):
        return identity.split(cls._DELIMITER)

    @classmethod
    def dump(cls, name, role):
        return cls._DELIMITER.join([name, role])
