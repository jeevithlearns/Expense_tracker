import os
import pandas as pd
from datetime import datetime
from tools import extract_expense_info

CSV_FILE = "expense_data.csv"

# Initialize CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Amount", "Category", "Type", "Date"]).to_csv(CSV_FILE, index=False)


def save_transaction(user_input: str):
    """Extract transaction info and save to CSV"""
    data = extract_expense_info(user_input)

    if data["Amount"] and data["Category"] and data["Type"]:
        df = pd.read_csv(CSV_FILE)
        new_row = {
            "Amount": data["Amount"],
            "Category": data["Category"].title(),  # Capitalize for consistency
            "Type": data["Type"],
            "Date": datetime.today().strftime('%Y-%m-%d')
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

        return {
            "success": True,
            "message": f"✅ Saved: ₹{data['Amount']} on {data['Category']} ({data['Type']})",
            "transaction": new_row
        }
    else:
        return {
            "success": False,
            "message": "⚠️ Could not understand. Try: 'I spent 100 on groceries' or 'I received 500 from freelance'",
            "extracted": data
        }


def show_summary():
    """Generate financial summary report"""
    try:
        df = pd.read_csv(CSV_FILE)

        if df.empty:
            return {
                "success": True,
                "message": "No records found.",
                "data": {
                    "total_income": 0,
                    "total_expense": 0,
                    "balance": 0,
                    "income_by_category": {},
                    "expenses_by_category": {},
                    "recent_transactions": []
                }
            }

        # Calculate totals
        total_income = df[df["Type"] == "Income"]["Amount"].sum()
        total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
        balance = total_income - total_expense

        # Group by category
        income_by_cat = df[df["Type"] == "Income"].groupby("Category")["Amount"].sum().to_dict()
        expenses_by_cat = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().to_dict()

        # Get recent transactions (last 10)
        recent_transactions = df.tail(10).to_dict('records')

        return {
            "success": True,
            "data": {
                "total_income": float(total_income),
                "total_expense": float(total_expense),
                "balance": float(balance),
                "income_by_category": income_by_cat,
                "expenses_by_category": expenses_by_cat,
                "recent_transactions": recent_transactions,
                "total_records": len(df)
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error generating summary: {str(e)}"
        }


def reset_data():
    """Reset all transaction data"""
    try:
        pd.DataFrame(columns=["Amount", "Category", "Type", "Date"]).to_csv(CSV_FILE, index=False)
        return {
            "success": True,
            "message": "🗑️ All data has been reset."
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error resetting data: {str(e)}"
        }


def get_transactions():
    """Get all transactions"""
    try:
        df = pd.read_csv(CSV_FILE)
        return {
            "success": True,
            "data": df.to_dict('records')
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error fetching transactions: {str(e)}"
        }


def delete_transaction(index: int):
    """Delete a transaction by index"""
    try:
        df = pd.read_csv(CSV_FILE)
        if 0 <= index < len(df):
            deleted_row = df.iloc[index].to_dict()
            df = df.drop(df.index[index])
            df.to_csv(CSV_FILE, index=False)
            return {
                "success": True,
                "message": f"Transaction deleted: ₹{deleted_row['Amount']} on {deleted_row['Category']}",
                "deleted_transaction": deleted_row
            }
        else:
            return {
                "success": False,
                "message": "Invalid transaction index"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting transaction: {str(e)}"
        }