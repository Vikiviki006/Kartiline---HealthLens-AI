from fastapi import FastAPI
from api.upload import router as upload_router

app = FastAPI(
    title="HealthLens AI",
    version="1.0.0"
)

app.include_router(upload_router)

@app.get("/")
def home():
    return {
        "message": "HealthLens AI Backend Running"
    }