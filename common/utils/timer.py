import time
from typing import Callable, TypeVar, Tuple

T = TypeVar("T")

def time_ms(fn: Callable[..., T], *args, **kwargs) -> Tuple[T, int]:
    """
    Times how long a function takes to execute and returns (result, elapsed_ms).
    """
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed_ms = int((time.perf_counter() - start) * 1000)
    return result, elapsed_ms
