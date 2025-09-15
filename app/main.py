from fastapi import FastAPI

app = FastAPI(title="DiveApp API")

@app.get("/")
def read_root():
    return {"message": "DiveApp funcionando!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}