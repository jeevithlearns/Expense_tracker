import gradio as gr
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Backend API URL - Change this to your deployed FastAPI URL
API_BASE_URL = "http://0.0.0.0:8000"  # Replace with your actual API URL

def add_transaction(message):
    """Add a new transaction"""
    if not message.strip():
        return "⚠️ Please enter a transaction description", None, ""
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/add", 
            json={"message": message},
            timeout=10
        )
        result = response.json()
        
        if result.get("success"):
            return (
                result["message"],
                f"✅ **Transaction Added Successfully!**\n\n"
                f"**Amount:** ₹{result['transaction']['Amount']}\n"
                f"**Category:** {result['transaction']['Category']}\n"
                f"**Type:** {result['transaction']['Type']}\n"
                f"**Date:** {result['transaction']['Date']}",
                ""  # Clear the input
            )
        else:
            return result["message"], f"❌ **Error:** {result['message']}", message
            
    except requests.exceptions.RequestException as e:
        return f"🔌 **Connection Error:** Unable to reach the server. Make sure your API is running.", "", message
    except Exception as e:
        return f"❌ **Error:** {str(e)}", "", message

def get_summary():
    """Get financial summary with charts"""
    try:
        response = requests.get(f"{API_BASE_URL}/summary", timeout=10)
        data = response.json()["data"]
        
        # Create summary text
        summary_text = f"""
## 📊 **Financial Summary**

### 💰 **Overview**
- **Total Income:** ₹{data['total_income']:,.2f}
- **Total Expenses:** ₹{data['total_expense']:,.2f}
- **Current Balance:** ₹{data['balance']:,.2f}
- **Total Records:** {data['total_records']}

### 📈 **Status**
{get_status_emoji(data['balance'])} **{get_balance_status(data['balance'])}**
        """
        
        # Create expense pie chart
        expense_chart = None
        income_chart = None
        
        if data['expenses_by_category']:
            expense_fig = px.pie(
                values=list(data['expenses_by_category'].values()),
                names=list(data['expenses_by_category'].keys()),
                title="💸 Expenses by Category",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            expense_fig.update_layout(
                font_size=14,
                title_font_size=18,
                showlegend=True
            )
            expense_chart = expense_fig
        
        # Create income pie chart
        if data['income_by_category']:
            income_fig = px.pie(
                values=list(data['income_by_category'].values()),
                names=list(data['income_by_category'].keys()),
                title="💰 Income by Source",
                color_discrete_sequence=px.colors.qualitative.Pastel1
            )
            income_fig.update_layout(
                font_size=14,
                title_font_size=18,
                showlegend=True
            )
            income_chart = income_fig
        
        return summary_text, expense_chart, income_chart
        
    except requests.exceptions.RequestException as e:
        return "🔌 **Connection Error:** Unable to reach the server.", None, None
    except Exception as e:
        return f"❌ **Error:** {str(e)}", None, None

def get_transactions():
    """Get all transactions as a formatted table"""
    try:
        response = requests.get(f"{API_BASE_URL}/transactions", timeout=10)
        data = response.json()["data"]
        
        if not data:
            return "📭 No transactions found."
        
        # Convert to DataFrame for better display
        df = pd.DataFrame(data)
        df['Amount'] = df['Amount'].apply(lambda x: f"₹{x:,.2f}")
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d %b %Y')
        
        # Reorder columns
        df = df[['Date', 'Type', 'Category', 'Amount']]
        
        return df
        
    except requests.exceptions.RequestException as e:
        return "🔌 **Connection Error:** Unable to reach the server."
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

def delete_transaction(index):
    """Delete a transaction by index"""
    if index is None or index < 0:
        return "⚠️ Please enter a valid transaction index (0 or greater)"
    
    try:
        response = requests.delete(
            f"{API_BASE_URL}/transaction",
            json={"index": int(index)},
            timeout=10
        )
        result = response.json()
        
        if result.get("success"):
            return f"✅ {result['message']}"
        else:
            return f"❌ {result['message']}"
            
    except requests.exceptions.RequestException as e:
        return "🔌 **Connection Error:** Unable to reach the server."
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

def reset_data():
    """Reset all data"""
    try:
        response = requests.post(f"{API_BASE_URL}/reset", timeout=10)
        result = response.json()
        
        if result.get("success"):
            return "✅ All data has been reset successfully!"
        else:
            return f"❌ {result['message']}"
            
    except requests.exceptions.RequestException as e:
        return "🔌 **Connection Error:** Unable to reach the server."
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

def get_status_emoji(balance):
    """Get emoji based on balance"""
    if balance > 1000:
        return "🟢"
    elif balance > 0:
        return "🟡"
    else:
        return "🔴"

def get_balance_status(balance):
    """Get balance status text"""
    if balance > 1000:
        return "Great! You're in good financial shape."
    elif balance > 0:
        return "You're doing okay, but watch your spending."
    else:
        return "Warning: You're spending more than you earn!"

# Custom CSS
css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.gr-button-primary {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
}
.gr-button-secondary {
    background: linear-gradient(45deg, #95E1D3, #F8B500) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
}
"""

# Create Gradio interface
with gr.Blocks(css=css, title="💰 Personal Expense Tracker", theme=gr.themes.Soft()) as app:
    
    gr.Markdown("# 💰 Personal Expense Tracker")
    gr.Markdown("Track your expenses and income with natural language! Just describe your transaction and let the AI handle the rest.")
    
    with gr.Tab("➕ Add Transaction"):
        gr.Markdown("### Add a New Transaction")
        gr.Markdown("**Examples:**\n- 'I spent 150 on groceries'\n- 'Received 5000 salary from company'\n- 'Paid 80 for dinner at restaurant'")
        
        with gr.Row():
            transaction_input = gr.Textbox(
                placeholder="Describe your transaction... (e.g., 'I spent 100 on groceries')",
                label="Transaction Description",
                scale=3
            )
            add_btn = gr.Button("Add Transaction", variant="primary", scale=1)
        
        add_output = gr.Textbox(label="Result", interactive=False)
        transaction_details = gr.Markdown()
        
        add_btn.click(
            add_transaction,
            inputs=[transaction_input],
            outputs=[add_output, transaction_details, transaction_input]
        )
    
    with gr.Tab("📊 Financial Summary"):
        gr.Markdown("### Your Financial Overview")
        
        summary_btn = gr.Button("Get Summary", variant="primary", size="lg")
        
        with gr.Row():
            summary_text = gr.Markdown()
        
        with gr.Row():
            expense_chart = gr.Plot(label="Expenses Breakdown")
            income_chart = gr.Plot(label="Income Sources")
        
        summary_btn.click(
            get_summary,
            outputs=[summary_text, expense_chart, income_chart]
        )
    
    with gr.Tab("📋 Transaction History"):
        gr.Markdown("### All Your Transactions")
        
        transactions_btn = gr.Button("Load Transactions", variant="secondary")
        transactions_output = gr.Dataframe(
            label="Transaction History",
            interactive=False,
            wrap=True
        )
        
        transactions_btn.click(
            get_transactions,
            outputs=[transactions_output]
        )
    
    with gr.Tab("🗑️ Manage Data"):
        gr.Markdown("### Manage Your Data")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("#### Delete Transaction")
                delete_index = gr.Number(
                    label="Transaction Index (from Transaction History)",
                    value=0,
                    precision=0
                )
                delete_btn = gr.Button("Delete Transaction", variant="secondary")
                delete_output = gr.Textbox(label="Delete Result", interactive=False)
            
            with gr.Column():
                gr.Markdown("#### Reset All Data")
                gr.Markdown("⚠️ **Warning:** This will delete ALL your transactions!")
                reset_btn = gr.Button("Reset All Data", variant="stop")
                reset_output = gr.Textbox(label="Reset Result", interactive=False)
        
        delete_btn.click(
            delete_transaction,
            inputs=[delete_index],
            outputs=[delete_output]
        )
        
        reset_btn.click(
            reset_data,
            outputs=[reset_output]
        )
    
    with gr.Tab("ℹ️ Help"):
        gr.Markdown("""
        ### How to Use This App
        
        #### ➕ Adding Transactions
        Simply describe your transaction in natural language:
        - **Expenses**: "I spent 100 on groceries", "Paid 50 for lunch", "Bought clothes for 200"
        - **Income**: "Received 5000 salary", "Got 500 from freelance work", "Earned 100 from side project"
        
        #### 📊 Understanding Your Summary
        - **Green Status** 🟢: Great financial health (balance > ₹1000)
        - **Yellow Status** 🟡: Doing okay (balance > ₹0)
        - **Red Status** 🔴: Spending more than earning (negative balance)
        
        #### 🗑️ Managing Data
        - **Delete Transaction**: Use the index number from the transaction history
        - **Reset Data**: Removes all transactions (cannot be undone!)
        
        #### 💡 Tips
        - Be specific about amounts and categories for better tracking
        - Check your summary regularly to understand spending patterns
        - Use the charts to visualize where your money goes
        
        #### 🔧 Technical Notes
        - Make sure your FastAPI backend is running
        - Update the `API_BASE_URL` in the code to your deployed API
        - For free hosting, deploy this on Hugging Face Spaces
        """)

# Launch the app
if __name__ == "__main__":
    app.launch(
        share=True,  # Creates a public link
        server_name="0.0.0.0",
        server_port=7860
    )