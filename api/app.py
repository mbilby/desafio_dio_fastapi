from fastapi import FastAPI
from api.routers.routers import api_router as router

app = FastAPI(title="WorkoutAPI")
app.include_router(router)



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, log_leve="info", reload=True)