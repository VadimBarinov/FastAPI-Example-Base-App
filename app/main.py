import uvicorn
from fastapi import FastAPI


app = FastAPI()


if __name__ == '__main__':
    uvicorn.run(app="main:app", port=8080, host="0.0.0.0", reload=True)
