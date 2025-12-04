from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

@app.route('/')
def index():
    # Ensure tables exist
    db.create_all()
    
    # Get filter parameters
    filter_month = request.args.get('month')
    filter_category = request.args.get('category')
    
    # Start with all expenses
    expenses = Expense.query
    
    # Apply filters
    if filter_month:
        year, month = filter_month.split('-')
        expenses = expenses.filter(
            db.extract('year', Expense.date) == int(year),
            db.extract('month', Expense.date) == int(month)
        )
    
    if filter_category:
        expenses = expenses.filter(Expense.category == filter_category)
    
    expenses = expenses.order_by(Expense.date.desc()).all()
    
    # Get unique categories for filter dropdown
    categories = db.session.query(Expense.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('index.html', expenses=expenses, categories=categories)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        expense = Expense(
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            amount=float(request.form['amount']),
            category=request.form['category'],
            description=request.form['description']
        )
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)