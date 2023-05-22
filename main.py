import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/raw/{category}")
async def get_raw_random(category: str):
    return {"message": f"Hello {category}"}


if __name__ == '__main__':
    uvicorn.run("main:app",
                host="127.0.0.1",
                port=7878, reload=True)