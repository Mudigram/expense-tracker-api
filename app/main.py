from fastapi import FastAPI
from app.api.v1 import auth_router, expenses_router, category_router, summary_router


app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)

API_V1 = "/api/v1"
app.include_router(auth_router, prefix=API_V1)
app.include_router(expenses_router, prefix=API_V1)
app.include_router(category_router, prefix=API_V1)
app.include_router(summary_router, prefix=API_V1)

@app.get("/health")
def health_check():
    return {"status": "ok"}
