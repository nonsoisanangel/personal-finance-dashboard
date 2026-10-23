import os
import tempfile
import unittest

from app import app, init_db


class FinanceDashboardTests(unittest.TestCase):
    def setUp(self):
        database_file = tempfile.NamedTemporaryFile(delete=False)
        database_file.close()
        self.database_path = database_file.name

        app.config.update(TESTING=True, DATABASE=self.database_path)
        with app.app_context():
            init_db()
        self.client = app.test_client()

    def tearDown(self):
        os.unlink(self.database_path)

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Personal Finance Dashboard", response.data)

    def test_add_edit_and_delete_transaction(self):
        response = self.client.post(
            "/add",
            data={
                "description": "Paycheck",
                "amount": "1200",
                "type": "Income",
                "category": "Salary",
                "transaction_date": "2026-10-22",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Paycheck", response.data)
        self.assertIn(b"$1,200.00", response.data)

        response = self.client.post(
            "/edit/1",
            data={
                "description": "Updated Paycheck",
                "amount": "1300",
                "type": "Income",
                "category": "Salary",
                "transaction_date": "2026-10-22",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Updated Paycheck", response.data)

        response = self.client.post("/delete/1", follow_redirects=True)
        self.assertNotIn(b"Updated Paycheck", response.data)


if __name__ == "__main__":
    unittest.main()
