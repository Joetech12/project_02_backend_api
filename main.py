
from fastapi import FastAPI

from routers.messages import router as messages_router


app = FastAPI(
    title="Python Backend API",
    description="Professional backend development with FastAPI",
    version="1.0.0",
)


# Register message routes
app.include_router(messages_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to my Python Backend API",
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
    }
