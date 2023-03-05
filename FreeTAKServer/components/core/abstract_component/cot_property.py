from typing import Any, Callable, Union


class CoTProperty(property):
    is_cot = True
    
    def __init__(self, fget: Union[Callable[[Any], Any], None] = ...,
        fset: Union[Callable[[Any, Any], None], None] = ...,
        fdel: Union[Callable[[Any], None], None] = ...,
        doc: Union[str, None] = ...,):
        super().__init__(fget, fset, fdel, doc)