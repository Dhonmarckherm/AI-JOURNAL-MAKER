from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World"})

@app.get("/api/health")
async def health():
    return JSONResponse(content={"status": "healthy"})

handler = app
