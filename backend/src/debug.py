import uvicorn

def main():

    # FastAPI application configuration
    uvicorn.run(
        "app:app",  # Update this path to match your FastAPI app location
        host="0.0.0.0",
        port=30011,
        reload=True,     # Enable auto-reload
        workers=1,       # Use single worker for debugging
        log_level="debug"
    )

if __name__ == "__main__":
    main()
