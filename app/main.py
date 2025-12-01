from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import members,trainers,admin


app = FastAPI(
    title="Gym Management System",
    description="Health and Fitness Club Management API",
    version="1.0.0"
)
app.include_router(members.router)
# CORS middleware for frontend (we'll need this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(trainers.router)
app.include_router(admin.router)
@app.get("/")
def root():
    return {"message": "Gym Management System API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}