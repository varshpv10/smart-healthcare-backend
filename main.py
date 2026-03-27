from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine
from models import Base
from routers import patient, doctor, login, appointment, admin

import os

app = FastAPI()

# ✅ CORS (needed for mobile + teammates)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create tables (safe for Supabase via SQLAlchemy)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("DB connection error:", e)

# ✅ Fix for uploads folder (VERY IMPORTANT for Railway)
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Root test
@app.get("/")
def root():
    return {"message": "Smart Healthcare Backend Running"}

# ✅ Routers
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(login.router)
app.include_router(appointment.router)
app.include_router(admin.router)
