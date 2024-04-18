import uvicorn
import uvloop
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    uvloop.install()
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=3000,
                root_path='',
                reload=True)
