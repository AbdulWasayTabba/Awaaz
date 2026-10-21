from fastapi import FastAPI

app = FastAPI(title="Awaaz API")


@app.get("/")
def root():
    return {"message": "Awaaz backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}