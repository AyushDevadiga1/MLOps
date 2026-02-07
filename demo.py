from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {
                'message':'Hello EveryNyan !!!'
            }

@app.get("/about")
def hello():
    return {
                'message':' I can speak Engrishu ....  '
            }
