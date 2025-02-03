import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="rnd_fastapi_server.server:app",
        host="0.0.0.0",
        port=6000,
        reload=True,
    )