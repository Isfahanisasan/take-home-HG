# server.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import random
import os
import uvicorn

app = FastAPI()

# Configurable parameters
TOTAL_DELAY_SECONDS = int(os.getenv("TOTAL_DELAY_SECONDS", "30"))  # Total delay in seconds
ERROR_CHANCE = float(os.getenv("ERROR_CHANCE", "0.1"))  # 10% chance of error
RESET_INTERVAL_SECONDS = int(os.getenv("RESET_INTERVAL_SECONDS", "20"))  # Time before resetting job

# Global variables to simulate job status
job_start_time = datetime.now()
job_completed = False
job_result = "pending"

def reset_job():
    """
    Resets the job to the initial state.
    """
    global job_start_time, job_completed, job_result
    job_start_time = datetime.now()
    job_completed = False
    job_result = "pending"

@app.get("/status")
async def get_status():
    global job_completed
    global job_result

    now = datetime.now()
    elapsed_time = (now - job_start_time).total_seconds()

    if not job_completed:
        if elapsed_time >= TOTAL_DELAY_SECONDS:
            # Job is completed
            job_completed = True
            # Randomly decide if the job succeeded or failed
            if random.random() < ERROR_CHANCE:
                job_result = "error"
            else:
                job_result = "completed"
        else:
            job_result = "pending"
    else:
        # Check if reset interval has passed since the job completed
        if elapsed_time >= TOTAL_DELAY_SECONDS + RESET_INTERVAL_SECONDS:
            reset_job()

    return JSONResponse(content={"result": job_result})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
