from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import random

app = FastAPI()

# Catch-all route that matches any path
# @app.get("/{full_path:path}")
# async def catch_all(full_path: str):
#     return {"message": "Hello World"}
#
# # Root path handler
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
@app.post("/create")
async def create(term: str):
    generated_uuid = str(uuid.uuid4())
    return {"uuid": generated_uuid}

@app.get("/status")
async def status(uuid: str):
    if not uuid:
        raise HTTPException(status_code=400, detail="uuid parameter is required")
    # Return "Collecting" 99% of the time, "Done" 1% of the time
    status = "Collecting" if random.random() < 0.99 else "Done"
    return {"status": status}

@app.get("/result")
async def result(uuid: str):
    if not uuid:
        raise HTTPException(status_code=400, detail="uuid parameter is required")

    try:
        with open('test_output.md', 'r') as file:
            markdown_content = file.read()

        return {
            "first_part": markdown_content
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Output file not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

