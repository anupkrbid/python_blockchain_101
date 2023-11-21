class Printable:
    """A base class which implements printing functionality."""

    def __repr__(self) -> str:
        return str(self.__dict__)
