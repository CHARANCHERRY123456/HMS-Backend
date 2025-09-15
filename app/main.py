from fastapi import FastAPI
from app.routes import user_routes
from app.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes
app.include_router(user_routes.router, prefix="/api", tags=["Users"])
