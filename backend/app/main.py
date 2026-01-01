from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from motor.motor_asyncio import AsyncIOMotorClient

from .core.config import settings
from .core.sockets import sio, interview_socket, gd_socket

app = FastAPI(title="AI Mock Interview API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
    app.database = app.mongodb_client[settings.MONGO_DATABASE_NAME]

# Routers
from .routers import auth, chatbot, dashboard, resume, hr, interview_review, career_advisor, job_tracker, gd_router, resume_router
from .api.endpoints import streaming

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(gd_router.router, prefix="/api/v1")
app.include_router(hr.router, prefix="/api/v1/hr")
app.include_router(dashboard.router, prefix="/api/v1/dashboard")
app.include_router(interview_review.router, prefix="/api/v1/interview-reviews")
app.include_router(resume_router.router, prefix="/api/v1")
app.include_router(chatbot.router, prefix="/api/v1/chatbot")
app.include_router(streaming.router, prefix="/api/v1/streaming")
app.include_router(career_advisor.router, prefix="/api/v1/career-path")
app.include_router(job_tracker.router, prefix="/api/v1/job-tracker/rankings")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Mock Interview API!"}

# Socket.IO
sio.register_namespace(interview_socket)
sio.register_namespace(gd_socket)

socket_app = socketio.ASGIApp(sio)
app.mount("/socket.io", socket_app)
