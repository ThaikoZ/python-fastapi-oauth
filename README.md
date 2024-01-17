# Python FastAPI Authentication & Authorization

Basic backend server built with FastAPI and sqlite. This is just an example how to build it by your own.

## Deployment

To deploy this project run

```bash
  docker build -t fastapi-oauth2 .
```

And after previous one, run

```bash
  docker run -d --name backend-container -p 80:80 fastapi-oauth2
```
