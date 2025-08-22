# 💰 Personal Expense Tracker API

A powerful backend API for tracking personal expenses and income using natural language processing. Built with FastAPI and intelligent text processing capabilities.

![Expense Tracker Screenshot](https://img.shields.io/badge/Status-Production%20Ready-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Features

- **Natural Language Processing**: Parse transactions from plain English
  - "I spent 500 on groceries"
  - "Received 15000 from salary"
  - "Paid 2000 for rent"

- **Smart Categorization**: Automatically categorizes transactions
  - Food & Dining, Transportation, Entertainment
  - Salary, Freelance, Business Income

- **Financial Analytics**: Comprehensive summary and reporting
  - Total income, expenses, and balance calculations
  - Category-wise breakdowns and aggregations
  - Transaction history with filtering

- **RESTful API**: Complete backend API with auto-documentation
- **Data Persistence**: CSV-based storage with pandas integration
- **Input Validation**: Robust data validation using Pydantic models

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv expense_tracker_env
   
   # On Windows
   expense_tracker_env\Scripts\activate
   
   # On macOS/Linux
   source expense_tracker_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the API server**
   ```bash
   python api_server.py
   ```

5. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Interactive API: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

## 📁 Project Structure

```
expense_tracker/
├── api_server.py          # FastAPI backend server
├── tracker_agent.py       # Business logic layer
├── tools.py              # NLP text processing engine
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── expense_data.csv     # Data storage (auto-generated)
```

## 🛠️ Technical Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: Lightning-fast ASGI server for production deployment
- **Pydantic**: Data validation and settings management using Python type hints

### Data Processing
- **Pandas**: Powerful data manipulation and analysis library
- **Regular Expressions**: Advanced pattern matching for text extraction
- **Natural Language Processing**: Custom keyword-based transaction classification

### Storage & Persistence
- **CSV Files**: Lightweight, portable data storage
- **File I/O Operations**: Efficient data reading and writing
- **Data Validation**: Comprehensive input validation and sanitization

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API status and available endpoints |
| `POST` | `/add` | Add new transaction from natural language |
| `GET` | `/summary` | Get financial summary with breakdowns |
| `GET` | `/transactions` | Retrieve all recorded transactions |
| `DELETE` | `/transaction` | Delete specific transaction by index |
| `POST` | `/reset` | Reset all transaction data |
| `GET` | `/health` | Health check endpoint |

### Example API Usage

```bash
# Add a transaction
curl -X POST "http://localhost:8000/add" \
     -H "Content-Type: application/json" \
     -d '{"message": "I spent 500 on groceries"}'

# Get financial summary
curl -X GET "http://localhost:8000/summary"

# Delete a transaction
curl -X DELETE "http://localhost:8000/transaction" \
     -H "Content-Type: application/json" \
     -d '{"index": 0}'
```

## 📊 Core Components

### 1. Natural Language Processing Engine (`tools.py`)
- **Text Analysis**: Extracts financial information from plain English
- **Pattern Recognition**: Uses regex patterns for amount and currency detection
- **Smart Categorization**: Maps expenses to predefined categories
- **Keyword Classification**: Distinguishes between income and expenses
- **Fall## 💡 Usage Examples

### Adding Expenses
```bash
curl -X POST "http://localhost:8000/add" \
     -H "Content-Type: application/json" \
     -d '{"message": "I spent 150 on coffee"}'

curl -X POST "http://localhost:8000/add" \
     -H "Content-Type: application/json" \
     -d '{"message": "Paid 2500 for electricity bill"}'
```

### Adding Income
```bash
curl -X POST "http://localhost:8000/add" \
     -H "Content-Type: application/json" \
     -d '{"message": "Received 25000 from salary"}'

curl -X POST "http://localhost:8000/add" \
     -H "Content-Type: application/json" \
     -d '{"message": "Got 5000 from freelance project"}'
```

### Getting Financial Summary
```bash
curl -X GET "http://localhost:8000/summary"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_income": 30000.0,
    "total_expense": 2650.0,
    "balance": 27350.0,
    "income_by_category": {
      "Salary": 25000.0,
      "Freelance": 5000.0
    },
    "expenses_by_category": {
      "Food & Dining": 150.0,
      "Bills & Utilities": 2500.0
    }
  }
}
```

## 🔍 Advanced Features

### Error Handling & Validation
- **Input Sanitization**: Prevents malformed data entry
- **Type Validation**: Ensures data types match expected formats
- **Business Rule Validation**: Checks logical constraints
- **Graceful Degradation**: Handles partial data extraction

### Performance Optimizations
- **Efficient Data Loading**: Optimized pandas operations
- **Memory Management**: Minimal memory footprint
- **Fast Response Times**: Lightweight processing pipeline
- **Scalable Architecture**: Ready for database integration

### Extensibility
- **Modular Design**: Easy to add new features
- **Plugin Architecture**: Custom category handlers
- **API Versioning**: Backward compatibility support
- **Configuration Management**: Environment-based settings

## 📈 Supported Transaction Patterns

### Expense Patterns
- "I spent [amount] on [category]"
- "Paid [amount] for [category]"
- "Bought [category] for [amount]"
- "[Category] cost [amount]"
- "Bill of [amount] for [category]"

### Income Patterns
- "Received [amount] from [source]"
- "Earned [amount] from [source]"
- "Got [amount] from [source]"
- "[Source] paid me [amount]"
- "Income of [amount] from [source]"

### Supported Categories
**Expenses:**
- Food & Dining, Groceries, Transportation
- Entertainment, Shopping, Bills & Utilities
- Health & Medical, Education, Miscellaneous

**Income:**
- Salary, Freelance, Business
- Investment, Gift, Refund, Allowance

## 🚀 Production Deployment

### Environment Setup
```bash
# Production dependencies
pip install fastapi[all] uvicorn[standard] pandas

# Environment variables
export ENVIRONMENT=production
export HOST=0.0.0.0
export PORT=8000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment Options
- **Heroku**: Easy deployment with Procfile
- **AWS Lambda**: Serverless with Mangum adapter
- **DigitalOcean App Platform**: Container deployment
- **Google Cloud Run**: Managed container platform

## 🧪 Testing

### API Testing with pytest
```python
import pytest
from fastapi.testclient import TestClient
from api_server import app

client = TestClient(app)

def test_add_transaction():
    response = client.post("/add", 
        json={"message": "I spent 100 on groceries"})
    assert response.status_code == 200
    assert response.json()["success"] == True
```

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/summary

# Using curl for stress testing
for i in {1..100}; do
  curl -X POST "http://localhost:8000/add" \
       -H "Content-Type: application/json" \
       -d '{"message": "Test transaction '$i'"}'
## 🔧 Development

### Adding Custom Categories
```python
# In tools.py, extend category_keywords dictionary
category_keywords = {
    "Food & Dining": ["food", "restaurant", "lunch"],
    "Custom Category": ["custom", "specific", "keywords"],
    # Add your categories here
}
```

### Environment Configuration
```python
# config.py (create if needed)
import os

CSV_FILE = os.getenv("DATA_FILE", "expense_data.csv")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"
```

### Extending the API
```python
# Add new endpoints in api_server.py
@app.get("/analytics/{category}")
def get_category_analytics(category: str):
    # Custom analytics logic
    return {"category": category, "analytics": {...}}
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Install dev dependencies: `pip install -r requirements-dev.txt`
4. Make your changes and add tests
5. Run tests: `pytest`
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Add docstrings for public methods
- Maintain test coverage above 80%

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI framework for excellent API development experience
- Pandas library for powerful data manipulation capabilities
- Regular expressions for robust text pattern matching
- Open source community for inspiration and best practices

## 📞 Support & Contact

- **Issues**: Please use GitHub Issues for bug reports and feature requests
- **Documentation**: Visit `/docs` endpoint for interactive API documentation
- **Email**: [your-email@domain.com]
- **LinkedIn**: [Your LinkedIn Profile]

---

**Made with ❤️ for better personal finance management**

### 2. Business Logic Layer (`tracker_agent.py`)
- **Transaction Management**: CRUD operations for financial data
- **Data Validation**: Ensures data integrity and consistency
- **Financial Calculations**: Computes summaries, balances, and analytics
- **CSV Operations**: Efficient data persistence and retrieval
- **Error Handling**: Comprehensive exception management

### 3. API Server (`api_server.py`)
- **RESTful Endpoints**: Standard HTTP methods and status codes
- **Request Validation**: Automatic input validation with Pydantic
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Auto Documentation**: OpenAPI/Swagger documentation generation
- **Health Monitoring**: System status and diagnostics

## 🧠 NLP Processing Pipeline

### Transaction Analysis Flow
```
User Input → Text Preprocessing → Pattern Matching → Classification → Validation → Storage
```

1. **Text Preprocessing**
   - Convert to lowercase
   - Tokenization and word splitting
   - Remove unnecessary whitespace

2. **Pattern Matching**
   - Extract monetary amounts using regex
   - Identify currency symbols (₹, Rs, $)
   - Parse decimal values and large numbers

3. **Transaction Classification**
   - Expense keywords: "spent", "paid", "bought", "cost"
   - Income keywords: "received", "earned", "got", "salary"
   - Context-aware categorization

4. **Category Detection**
   - Predefined category mapping
   - Preposition-based extraction ("on", "for", "to")
   - Smart fallback to custom categories

## 💾 Data Architecture

### Storage Schema
```csv
Amount,Category,Type,Date
500.0,Groceries,Expense,2024-01-15
15000.0,Salary,Income,2024-01-01
```

### Data Operations
- **Create**: Add new transactions with validation
- **Read**: Retrieve transactions with filtering options
- **Update**: Modify existing transaction records
- **Delete**: Remove transactions by index
- **Aggregate**: Calculate summaries and statistics