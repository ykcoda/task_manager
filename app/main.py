from fastapi import FastAPI


app = FastAPI(title="Task App")


@app.get("/health")
async def health():
    return {"status": "ok"}
