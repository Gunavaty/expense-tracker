import unittest
import tempfile
import os
from app import app, db, Expense

class ExpenseTrackerTest(unittest.TestCase):
    
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Expenses', response.data)
    
    def test_add_expense(self):
        response = self.app.post('/add', data={
            'date': '2024-01-15',
            'amount': '25.50',
            'category': 'Food',
            'description': 'Lunch'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        with app.app_context():
            expense = Expense.query.filter_by(amount=25.50).first()
            self.assertIsNotNone(expense)
            self.assertEqual(expense.amount, 25.50)

if __name__ == '__main__':
    unittest.main()