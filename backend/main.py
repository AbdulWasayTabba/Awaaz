from fastapi import FastAPI
from routers import auth, children, content, invites, therapist
from routers import auth

app = FastAPI(title="Awaaz")
app.include_router(auth.router)
app.include_router(children.router)
app.include_router(invites.router)
app.include_router(therapist.router)
app.include_router(content.router)

@app.get("/")
def root():
    return {"message": "Awaaz backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


...
