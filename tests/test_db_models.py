import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base, User, FinancialData

class TestDbModels(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        # Clean up the database after each test
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_user(self):
        # Test creating a User record
        user = User(name='John Doe', email='john@example.com')
        self.session.add(user)
        self.session.commit()
        retrieved_user = self.session.query(User).filter_by(email='john@example.com').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.name, 'John Doe')

    def test_create_financial_data(self):
        # Test creating a FinancialData record
        financial_data = FinancialData(user_id=1, amount=100.0, category='Food')
        self.session.add(financial_data)
        self.session.commit()
        retrieved_data = self.session.query(FinancialData).filter_by(user_id=1).first()
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(retrieved_data.amount, 100.0)
        self.assertEqual(retrieved_data.category, 'Food')

if __name__ == "__main__":
    unittest.main()
