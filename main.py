from fastapi import FastAPI
# from .users import models
# from database import engine
import uvicorn

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(router)
@app.get('/')
async def health_check():
  return {"message": "Hello world"} 

if __name__ == '__main__':
  uvicorn.run(app=app, host='127.0.0.1', port='8000')
