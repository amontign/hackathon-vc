from enum import Enum
from pydantic import BaseModel, UUID4


class Status(str, Enum):
    COLLECTING = "Collecting"
    DONE = "Done"

class SearchType(str, Enum):
    MARKET = "market"
    COMPANY = "company"
