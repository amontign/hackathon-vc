from fastapi import FastAPI

app = FastAPI()

# Catch-all route that matches any path
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return {"message": "Hello World"}

# Root path handler
@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
