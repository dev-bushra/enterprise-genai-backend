from fastapi import FastAPI

app = FastAPI(title="Enterprise GenAI Orchestrator", version="1.0")

@app.get("/")
def read_root():
    return {"msg": "🚀 Backend for GenAI Orchestrator is running!"}
