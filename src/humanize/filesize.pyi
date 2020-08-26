from typing import Any, Dict, SupportsFloat, Tuple, Union

suffixes: Dict[str, Tuple[str, ...]]

def naturalsize(
    value: Union[str, SupportsFloat],
    binary: bool = ...,
    gnu: bool = ...,
    format: str = ...
) -> str: ...
