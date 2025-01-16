from uuid import uuid4, UUID
from dataclasses import dataclass
from model import Status


@dataclass
class Job(object):
    uuid: UUID = uuid4()
    status: Status = Status.COLLECTING
    progress: float = 0.0
    result: str = ""
    message: str = ""
    search_term: str = ""
    search_type: str = None
    topics: list[str] = None

    @classmethod
    def create(cls):
        return cls()


jobs: dict[UUID, Job] = {}
