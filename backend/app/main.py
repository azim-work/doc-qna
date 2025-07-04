from fastapi.middleware.cors import CORSMiddleware


from fastapi import FastAPI
from app.api.v1.endpoints import router as api_router

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the versioned API
app.include_router(api_router, prefix="/api/v1")
