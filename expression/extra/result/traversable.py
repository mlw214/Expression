"""Data structures that can be traversed from left to right, performing an action on each element."""
from typing import Callable, Generator, List, TypeVar, Union, cast, overload

from expression import effect
from expression.collections import seq
from expression.core import Ok, Result, identity, pipe

TSource = TypeVar("TSource")
TResult = TypeVar("TResult")
TError = TypeVar("TError")


@overload
def traverse(
    fn: Callable[[Result[TResult, TError]], Result[TResult, TError]], lst: List[Result[TResult, TError]]
) -> Result[List[TResult], TError]:
    ...


def traverse(fn: Callable[[TSource], Result[TResult, TError]], lst: List[TSource]) -> Result[List[TResult], TError]:
    """Traverses a list of items.

    Threads an applicative computation though a list of items.
    """

    @effect.result
    def folder(
        head: TSource, tail: Result[List[TResult], TError]
    ) -> Generator[Union[List[TResult], TResult], Union[List[TResult], TResult], List[TResult]]:
        """Same as:
        >>> fn(head).bind(lambda head: tail.bind(lambda tail: Ok([head] + tail)))
        """
        h = yield from fn(head)
        t = yield from tail

        h = cast("TResult", h)
        t = cast(List[TResult], t)
        return [h] + t

    state: Result[List[TSource], TError] = Ok([])
    return pipe(state, seq.fold_back(folder, lst))


def sequence(lst: List[Result[TSource, TError]]) -> Result[List[TSource], TError]:
    """Execute a sequence of result returning commands and collect the
    sequence of their response."""

    return traverse(identity, lst)
