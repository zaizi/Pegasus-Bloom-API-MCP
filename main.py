from fastapi import FastAPI
from db.database import engine, Base
from routers import dashboard, notes, mood

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pegasus Bloom API + MCP",
    description="API for accessing daily notes and user data.",
    version="1.0.0"
)

app.include_router(notes.router)
app.include_router(mood.router)
app.include_router(dashboard.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Pegasus Bloom API. MCP to Follow"}