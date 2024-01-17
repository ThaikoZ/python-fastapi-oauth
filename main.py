from fastapi import FastAPI
from users import models
from core.database import engine
import uvicorn
from users.routes import router as users_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router)
# app.include_router(auth)

if __name__ == '__main__':
  uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
