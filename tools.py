import re
from typing import Dict, Optional


def extract_expense_info(text: str) -> Dict[str, Optional[str]]:
    """
    Extract expense/income information from natural language text.

    Args:
        text (str): Natural language input describing a transaction

    Returns:
        dict: Contains Amount, Category, and Type fields
    """
    amount = None
    category = None
    transaction_type = None

    # Extract amount (supports formats like 100, 100.50, $100, ₹100)
    amount_pattern = r"(?:₹|rs\.?|inr|usd|\$)?\s*(\d+(?:\.\d{1,2})?)"
    match = re.search(amount_pattern, text.lower())
    if match:
        amount = float(match.group(1))

    text_lower = text.lower()
    words = text_lower.split()

    # Enhanced expense detection keywords
    expense_keywords = [
        "spent", "paid", "bought", "purchased", "ate", "gave", "cost", "costs",
        "bill", "bills", "expense", "expenses", "shopping", "shop", "buy"
    ]

    # Enhanced income detection keywords
    income_keywords = [
        "received", "got", "earned", "salary", "income", "profit", "bonus",
        "refund", "returned", "cashback", "won", "gift", "allowance"
    ]

    # Check for expense indicators
    if any(keyword in text_lower for keyword in expense_keywords):
        transaction_type = "Expense"

        # Try to extract category using various patterns
        category = extract_category_for_expense(text_lower, words)

    # Check for income indicators
    elif any(keyword in text_lower for keyword in income_keywords):
        transaction_type = "Income"

        # Try to extract income source
        category = extract_category_for_income(text_lower, words)

    # If no clear type is found, make educated guess based on context
    elif amount:
        # If amount is mentioned without clear type, try to infer from context
        if any(word in text_lower for word in ["food", "groceries", "restaurant", "fuel", "gas", "movie", "clothes"]):
            transaction_type = "Expense"
            category = extract_category_for_expense(text_lower, words)
        elif any(word in text_lower for word in ["work", "job", "freelance", "project", "client"]):
            transaction_type = "Income"
            category = extract_category_for_income(text_lower, words)

    return {
        "Amount": amount,
        "Category": category,
        "Type": transaction_type
    }


def extract_category_for_expense(text_lower: str, words: list) -> Optional[str]:
    """Extract expense category from text"""
    category = None

    # Common expense categories with their keywords
    category_keywords = {
        "Food & Dining": ["food", "restaurant", "lunch", "dinner", "breakfast", "ate", "pizza", "coffee", "snack"],
        "Groceries": ["groceries", "grocery", "supermarket", "vegetables", "fruits", "milk", "bread"],
        "Transportation": ["fuel", "gas", "petrol", "diesel", "uber", "taxi", "bus", "train", "metro"],
        "Entertainment": ["movie", "movies", "cinema", "game", "games", "party", "concert", "show"],
        "Shopping": ["clothes", "clothing", "shoes", "dress", "shirt", "shopping", "mall"],
        "Bills & Utilities": ["bill", "bills", "electricity", "water", "internet", "phone", "rent"],
        "Health & Medical": ["doctor", "medicine", "hospital", "pharmacy", "medical", "health"],
        "Education": ["books", "course", "class", "tuition", "fees", "school", "college"]
    }

    # Check for predefined categories
    for cat, keywords in category_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            category = cat
            break

    # If no predefined category found, try to extract using prepositions
    if not category:
        for keyword in ["on", "for", "to", "at"]:
            if keyword in words:
                try:
                    idx = words.index(keyword)
                    if idx + 1 < len(words):
                        category = " ".join(words[idx + 1:]).strip()
                        # Clean up common words
                        category = category.replace("the", "").replace("a", "").strip()
                        break
                except:
                    continue

    # If still no category, try to find noun after amount
    if not category and any(char.isdigit() for char in text_lower):
        # Look for words after numbers
        words_after_amount = []
        found_number = False
        for word in words:
            if any(char.isdigit() for char in word):
                found_number = True
            elif found_number:
                words_after_amount.append(word)

        if words_after_amount:
            category = " ".join(words_after_amount[:3]).strip()  # Take first 3 words max

    return category.title() if category else "Miscellaneous"


def extract_category_for_income(text_lower: str, words: list) -> Optional[str]:
    """Extract income source from text"""
    category = None

    # Common income sources
    income_sources = {
        "Salary": ["salary", "job", "work", "employment", "paycheck"],
        "Freelance": ["freelance", "freelancing", "client", "project", "contract"],
        "Business": ["business", "sales", "profit", "revenue"],
        "Investment": ["investment", "dividend", "interest", "stocks", "mutual"],
        "Gift": ["gift", "present", "birthday", "wedding"],
        "Refund": ["refund", "return", "cashback"],
        "Allowance": ["allowance", "pocket money", "parents"]
    }

    # Check for predefined sources
    for source, keywords in income_sources.items():
        if any(keyword in text_lower for keyword in keywords):
            category = source
            break

    # Try to extract using "from" preposition
    if not category and "from" in words:
        try:
            idx = words.index("from")
            if idx + 1 < len(words):
                category = " ".join(words[idx + 1:]).strip()
        except:
            pass

    return category.title() if category else "Other Income"


def validate_transaction_data(amount: float, category: str, transaction_type: str) -> bool:
    """Validate extracted transaction data"""
    if not amount or amount <= 0:
        return False
    if not category or len(category.strip()) == 0:
        return False
    if transaction_type not in ["Income", "Expense"]:
        return False
    return True


def format_currency(amount: float, currency: str = "₹") -> str:
    """Format amount as currency"""
    return f"{currency}{amount:,.2f}"


def parse_date_from_text(text: str) -> Optional[str]:
    """Extract date from text (for future enhancement)"""
    # This can be expanded to parse dates like "yesterday", "last week", etc.
    import datetime

    text_lower = text.lower()

    if "yesterday" in text_lower:
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        return date.strftime('%Y-%m-%d')
    elif "today" in text_lower:
        return datetime.datetime.now().strftime('%Y-%m-%d')

    return None