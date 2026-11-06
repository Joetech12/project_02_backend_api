
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from routers.messages import router as messages_router


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):

    # STARTUP
    print(f"Starting {settings.APP_NAME}...")

    app.state.settings = settings

    yield

    # SHUTDOWN
    print(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Professional backend development with FastAPI",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def request_timer(request: Request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = str(process_time)

    print(
        f"{request.method} {request.url.path} "
        f"- {process_time:.4f} seconds"
    )

    return response


# Register routers
app.include_router(messages_router)


@app.get("/")
def home():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
