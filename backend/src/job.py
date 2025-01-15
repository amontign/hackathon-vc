import uuid
from dataclasses import dataclass
from model import Status


@dataclass
class Job(object):
    uuid: uuid.UUID
    status: Status
    progress: float
    result: str
    message: str

    @classmethod
    def create(cls):
        return cls(
            uuid=uuid.uuid4(),
            status=Status.COLLECTING,
            progress=0.0,
            result="",
            message="",
        )


jobs: dict[uuid, Job] = {}
