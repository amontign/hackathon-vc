from typing import Any, List

import settings

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_307_TEMPORARY_REDIRECT

from uuid import UUID
from job import jobs, Job

from workflow import Workflow
import asyncio

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


@app.get("/create", response_model=dict[str, Any])
async def create_flow(term: str = Query(..., description="The domain to research (e.g., 'LegalTech')")):
    if not term:
        raise HTTPException(status_code=400, detail="Term parameter is required")
    job = Job.create()
    jobs[job.uuid] = job
    print(term)

    workflow = Workflow(search_term=term)
    asyncio.create_task(workflow.run(job))
    return {"uuid": str(job.uuid)}


@app.get("/status", response_model=Job)
async def get_status(uuid: UUID = Query(..., description="UUID of the research flow")):
    try:
        return jobs[uuid]
    except KeyError:
        raise HTTPException(status_code=404, detail="Research flow not found")


@app.get("/result", response_model=dict[str,str])
async def get_result(uuid: UUID = Query(..., description="UUID of the research flow")):
    try:
        return {'result': jobs[uuid].result}
    except KeyError:
        raise HTTPException(status_code=404, detail="Research flow not found")


@app.get("/overview_topics", response_model=List[str])
async def get_overview_topics():
    prompts_dir = settings.SRC_DIR / 'prompts' / 'overview'
    try:
        # Get all txt files in the prompts directory
        topics = [file.stem for file in prompts_dir.glob('*.txt')]
        return topics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading topics: {str(e)}")



# Any other request - redirect to web
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    # Redirect to your web interface
    return RedirectResponse(
        url=settings.WEB_URL,
        status_code=HTTP_307_TEMPORARY_REDIRECT
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
