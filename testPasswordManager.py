import unittest
from passwordManager import app, c, conn

class TestVaultAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def tearDown(self):
        c.execute("DELETE FROM credentials WHERE site LIKE 'unittest-%'")
        conn.commit()

    def test_add_get_delete_roundtrip(self):
        site = "unittest-example.com"
        user = "tester"
        pwd  = "TempPass123!"  # or generate locally; not required by API

        r = self.client.post("/add", json={"site": site, "username": user, "password": pwd})
        self.assertEqual(r.status_code, 200)

        r = self.client.get(f"/get/{site}")
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data["username"], user)
        self.assertEqual(data["password"], pwd)

        r = self.client.delete(f"/delete/{site}")
        self.assertEqual(r.status_code, 200)

        r = self.client.get(f"/get/{site}")
        self.assertEqual(r.get_json().get("error"), "not found")

if __name__ == "__main__":
    unittest.main(verbosity=2)
