# THIS FILE IS GIVEN TO YOU
# YOU DO NOT NEED TO EDIT THIS CODE
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)