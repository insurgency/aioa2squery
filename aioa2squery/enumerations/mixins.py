__all__ = (
    'BooleanEnumMixin',
    'OrdinalByteRepresentationMixin',
    'SimpleMemberNameStringMixin',
    'TryLowercaseValueWhenMissingMixin',
)


# noinspection PyUnresolvedReferences
class BooleanEnumMixin(object):
    """
    TODO
    """

    def __bool__(self) -> bool:
        return bool(self.value)


# noinspection PyUnresolvedReferences
class OrdinalByteRepresentationMixin(object):
    """
    An enumeration mixin to implement :meth:`__repr__() <object.__repr__>` using the character of the member's ordinal
    value.

    >>> from enum import IntEnum
    >>> class SomeEnum(OrdinalByteRepresentationMixin, IntEnum):
    >>>     MEMBER = ord('X')
    >>>
    >>> repr(SomeEnum)
    """

    def __repr__(self):
        # TODO: self._value_ uppercase if context var is goldsource
        return '<%s.%s: %r>' % (self.__class__.__name__, self._name_, chr(self._value_))


# noinspection PyUnresolvedReferences
class SimpleMemberNameStringMixin(object):
    """
    Enumeration mixin to implement :meth:`__str__`  from using it's own member name

    .. note::

        Performs simple string substitution and titles case of member name string.
    """

    def __str__(self) -> str:
        return self.name.replace('_', ' ').title()


# noinspection PyProtectedMember,PyUnresolvedReferences,PyArgumentList
class TryLowercaseValueWhenMissingMixin(object):
    """
    An enumeration mixin that allows either the uppercase or lowercase ordinal character value to be used.

    >>> from enum import IntEnum
    >>> class SomeEnum(TryLowercaseValueWhenMissingMixin, IntEnum):
    >>>     DEDICATED_SERVER = ord('x')
    >>>
    >>> SomeEnum('X') == SomeEnum('x')
    """

    @classmethod
    def _missing_(cls, value):
        value = ord(chr(value).lower())

        if value in cls.__members__.values():
            return cls(value)

        return super()._missing_(value)


class MissingEnumeratorValueMixin(object):
    pass
