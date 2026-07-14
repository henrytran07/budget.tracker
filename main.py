from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.budget_tracker_manager import router
import os
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt

app = FastAPI()
os.makedirs("financial_analysis", exist_ok=True)
app.mount("/asset", StaticFiles(directory="asset"), name="asset")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/financial_analysis", StaticFiles(directory="financial_analysis"), name="analysis")
app.include_router(router)