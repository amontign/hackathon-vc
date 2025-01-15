from enum import Enum
from pydantic import BaseModel, UUID4


class Status(str, Enum):
    COLLECTING = "Collecting"
    DONE = "Done"