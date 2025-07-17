from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import auth, challans

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Transport Department API",
    description="API for managing traffic challans and department operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(challans.router)

@app.get("/")
def root():
    return {"message": "E-Transport Department API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}