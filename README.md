# Expense Tracker

This is a simple expense tracker web app built with Flask. It is used to add daily expenses and view them with basic filtering by month and category.

---

## Features

- Add daily expenses (date, amount, category, description)
- View expenses with filters by month and category
- Set monthly budgets for each category
- Get alerts when budget is exceeded

---

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

3. Open browser: `http://localhost:5000`

## Usage

1. **Add Expense**: Click "Add New Expense" button
2. **View Expenses**: Main page shows all expenses
3. **Filter**: Use month/category filters to narrow results
4. **Set Budgets**: Click "Manage Budgets" to set monthly limits
5. **Budget Alerts**: Get warnings when you exceed your budget

## Testing

```bash
python test_app.py
```
