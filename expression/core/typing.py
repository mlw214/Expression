from abc import abstractmethod
from typing import Any, Iterable, Optional, Protocol, Type, TypeVar, cast, get_origin

A = TypeVar("A")
B = TypeVar("B")
TSource = TypeVar("TSource")
TResult = TypeVar("TResult")

Base = TypeVar("Base")
Derived = TypeVar("Derived")


class SupportsLessThan(Protocol):
    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        raise NotImplementedError


class SupportsMatch(Protocol[TSource]):
    """Pattern matching protocol."""

    @abstractmethod
    def __match__(self, pattern: Any) -> Iterable[TSource]:
        """Match pattern with value.

        Return a singleton iterable item (e.g `[ value ]`) if pattern
        matches value , else an empty iterable (e.g. `[]`)."""

        raise NotImplementedError


def upcast(type: Type[Base], expr: Base) -> Base:
    """Upcast expression from a `Derived` to `Base`.

    Note: F# `:>` or `upcast`.
    """
    x: type = expr
    return x


def downcast(type: Type[Derived], expr: Base) -> Derived:
    """Downcast expression `Derived` to `Base`

    Checks at compile time that the type of expression Base is a
    supertype of Derived, and checks at runtime that Base is in fact an
    instance of Derived.

    Note: F# `:?>` or `downcast`.
    """
    assert isinstance(expr, type), f"The type of expression {expr} is not a supertype of {type}"
    return cast(type, expr)


def try_downcast(type_: Type[Derived], expr: Base) -> Optional[Derived]:
    """Downcast expression `Base` to `Derived`.

    Check that the `Derived` type is a supertype of `Base`.

    NOTE: Supports generic types.

    Returns:
        None if `Derived` is not a supertype of `Base`.
    """
    origin: Optional[Type[Derived]] = get_origin(type_) or type_
    if origin is not None and isinstance(expr, origin):
        derived = cast(type(type_), expr)
        return derived
    else:
        return None


__all__ = ["SupportsLessThan", "downcast", "upcast", "try_downcast"]
