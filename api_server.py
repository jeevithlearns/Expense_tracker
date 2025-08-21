import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from tracker_agent import (
    save_transaction,
    show_summary,
    reset_data,
    get_transactions,
    delete_transaction
)

app = FastAPI(
    title="Personal Expense Tracker API",
    description="A simple API for tracking personal expenses and income",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body schemas
class TransactionInput(BaseModel):
    message: str

class DeleteTransactionInput(BaseModel):
    index: int

@app.get("/")
def read_root():
    return {
        "message": "🧾 Personal Expense Tracker API is running.",
        "endpoints": {
            "POST /add": "Add a new transaction",
            "GET /summary": "Get financial summary",
            "GET /transactions": "Get all transactions",
            "DELETE /transaction": "Delete a transaction by index",
            "POST /reset": "Reset all data"
        }
    }

@app.post("/add")
def add_transaction(data: TransactionInput):
    """Add a new transaction from natural language input"""
    try:
        result = save_transaction(data.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary")
def get_summary_report():
    """Get financial summary with totals and breakdowns"""
    try:
        result = show_summary()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions")
def get_all_transactions():
    """Get all recorded transactions"""
    try:
        result = get_transactions()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/transaction")
def delete_single_transaction(data: DeleteTransactionInput):
    """Delete a transaction by its index"""
    try:
        result = delete_transaction(data.index)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
def reset_all_data():
    """Reset all transaction data (use with caution!)"""
    try:
        result = reset_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "expense-tracker-api"}

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",  # Import string instead of app object
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    )