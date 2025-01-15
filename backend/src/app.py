from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel, UUID4
import sqlite3
import uuid
from typing import Optional
from enum import Enum
from datetime import datetime

app = FastAPI(
    title="Research Flow API",
    description="API for managing research flows across different domains using AI services",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Status(str, Enum):
    COLLECTING = "Collecting"
    SUMMARIZING = "Summarizing"
    DONE = "Done"

class ResearchFlow(BaseModel):
    uuid: UUID4
    status: Status
    result: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UUIDResponse(BaseModel):
    uuid: UUID4

class StatusResponse(BaseModel):
    status: Status

class ResultResponse(BaseModel):
    result: str

class ErrorResponse(BaseModel):
    error: str

def init_db():
    conn = sqlite3.connect('research.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS research_flows (
            uuid TEXT PRIMARY KEY,
            status TEXT CHECK(status IN ('Collecting', 'Summarizing', 'Done')) NOT NULL,
            result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect('research.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/create", response_model=UUIDResponse, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def create_flow(term: str = Query(..., description="The domain to research (e.g., 'LegalTech')")):
    if not term:
        raise HTTPException(status_code=400, detail="Term parameter is required")

    flow_uuid = str(uuid.uuid4())

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO research_flows (uuid, status) VALUES (?, ?)',
            (flow_uuid, Status.COLLECTING)
        )
        conn.commit()
        conn.close()

        return {"uuid": flow_uuid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status", response_model=StatusResponse, responses={
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def get_status(uuid: UUID4 = Query(..., description="UUID of the research flow")):
    try:
        conn = get_db()
        cursor = conn.cursor()
        result = cursor.execute(
            'SELECT status FROM research_flows WHERE uuid = ?',
            (str(uuid),)
        ).fetchone()
        conn.close()

        if not result:
            raise HTTPException(status_code=404, detail="Research flow not found")

        return {"status": result['status']}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/result", response_model=ResultResponse, responses={
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def get_result(uuid: UUID4 = Query(..., description="UUID of the research flow")):
    try:
        conn = get_db()
        cursor = conn.cursor()
        result = cursor.execute(
            'SELECT status, result FROM research_flows WHERE uuid = ?',
            (str(uuid),)
        ).fetchone()
        conn.close()

        if not result:
            raise HTTPException(status_code=404, detail="Research flow not found")

        if result['status'] != Status.DONE:
            raise HTTPException(
                status_code=400,
                detail=f"Research is not complete yet (status: {result['status']})"
            )

        if not result['result']:
            raise HTTPException(status_code=400, detail="No result available")

        return {"result": result['result']}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root path handler
@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
