from fastapi import FastAPI
from db.database import engine, Base
from routers import dashboard, notes, mood, accidents
from services.gemini import gemini
from fastapi_mcp import FastApiMCP

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pegasus Bloom API + MCP",
    description="API for accessing daily notes and user data.",
    version="1.0.0"
)

app.include_router(notes.router)
app.include_router(mood.router)
app.include_router(dashboard.router)
app.include_router(gemini.router)
app.include_router(accidents.router)

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the Pegasus Bloom API. MCP to Follow"}


mcp = FastApiMCP(app, name="Pegasus Bloom MCP", include_tags=["tools"])
mcp.mount()

