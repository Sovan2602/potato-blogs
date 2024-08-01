from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import auth
import uvicorn


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# backend/
# │
# ├── app/
# │   ├── __init__.py
# │   ├── main.py
# │   ├── models.py
# │   ├── schemas.py
# │   ├── database.py
# │   ├── auth.py
# │   ├── crud.py
# │   ├── config.py
# │   ├── utils.py
# │   └── routers/
# │       ├── __init__.py
# │       ├── auth.py
# │       └── users.py
# │
# ├── env/  # virtual environment
# ├── requirements.txt
# └── .env
