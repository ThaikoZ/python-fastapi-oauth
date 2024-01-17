from fastapi import FastAPI
from users.models import Base
from core.database import engine
import uvicorn
from users.routes import router as users

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users)

if __name__ == '__main__':
  uvicorn.run(app=app, host='127.0.0.1', port='8000', reload=True)
