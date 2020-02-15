"""The abstract base Handler class which all Handlers must subclass."""

from abc import ABC, abstractmethod
from comment import Comment


class AbstractBaseHandler(ABC):
    """All Handlers must inherit from this AbstractBaseHandler class."""

    @classmethod
    @abstractmethod
    def handle(cls, url) -> Comment:
        """
        All Handlers must override the `handle` method,
        which must return a Comment object.
        """


class HandlerError(Exception):
    """An Error exception raised during the operation of a Handler."""
