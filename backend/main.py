from fastapi import FastAPI

from routers import auth

app = FastAPI(title="Awaaz API")
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Awaaz backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}