from abc import ABC, abstractmethod


class AbstractBaseHandler(ABC):
    """All Handlers must inherit from this AbstractBaseHandler class."""

    @classmethod
    @abstractmethod
    def handle(cls):
        """
        All Handlers must override the `handle` method,
        which must return a Comment object.
        """
        pass


class HandlerError(Exception):
    pass
