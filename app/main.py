from fastapi import FastAPI

from routers import user

app = FastAPI()


app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
        host="localhost", port=8000, reload=True)
