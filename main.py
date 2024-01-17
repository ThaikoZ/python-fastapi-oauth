from fastapi import FastAPI
from users import models
from core.database import engine
import uvicorn
from users.routes import router as guest_router, user_router
from auth.route import router as auth_router
from core.security import JWTAuth
from starlette.middleware.authentication import AuthenticationMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)

# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

if __name__ == '__main__':
  uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
