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
    table_startup: list[dict] = None
    table_enterprise: list[dict] = None
    chart_web_trend:  dict = None
    chart_headcount_trend: dict = None
    summary_with_tables: str = ""

    @classmethod
    def create(cls):
        return cls()


jobs: dict[UUID, Job] = {}
