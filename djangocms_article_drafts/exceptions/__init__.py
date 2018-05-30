class UnregisteredModelError(Exception):
    """A class is not registered with the publisher model class pool."""
    pass


class DraftDoesNotExist(Exception):
    pass


class NotPublished(Exception):
    pass
