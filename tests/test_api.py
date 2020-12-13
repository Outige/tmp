import unittest
from fastapi.testclient import TestClient
from fastapi import FastAPI
import json

import os, sys
sys.path.insert(0, os.path.abspath('..'))
import sql_app.main as main
import sql_app.crud as crud
import sql_app.models as models
import sql_app.schemas as schemas


def clean_test_database():
    """This function primes the test database to be ready for the rest of the unit tests
    - I would prefer if all the code could be in main and I could call client.get("/test/") only
    """
    client.get("/test/")
    client.post(
        "/users/",
        json={"email": "tieg@gmail.com", "password": "super secret password", "is_active": True},
    )
    client.post(
        "/users/",
        json={"email": "troy@gmail.com", "password": "super secreter password", "is_active": False},
    )
    client.post(
        "/users/1/items/",
        json={"title": "tiegs pencil", "description": "here lies tieg pencil"},
    )
    client.post(
        "/users/1/items/",
        json={"title": "tiegs pencil", "description": "tiegs backup pencil"},
    )
    client.post(
        "/users/2/items/",
        json={"title": "troys bag", "description": "this is troys bag"},
    )

app = main.app
client = TestClient(app)

clean_test_database()

class test_main(unittest.TestCase):
    def test_read_users(self):
        """This unit test mesures the expected json and expected response against those received.
        """
        expected_json = [
            {"email": "tieg@gmail.com", "id": 1, "is_active": True, "items": [{"title": "tiegs pencil", 
            "description": "here lies tieg pencil", "id": 1, "owner_id": 1}, {"title": "tiegs pencil", "description": "tiegs backup pencil", 
            "id": 2, "owner_id": 1}]},
            {"email": "troy@gmail.com", "id": 2, "is_active": True, "items": [{"title": "troys bag", 
            "description": "this is troys bag", "id": 3, "owner_id": 2}]}
        ]
        expected_response = 200

        response = client.get("/users/")
        self.assertTrue(response.status_code == expected_response)
        self.assertTrue(response.json() == expected_json)
    
    def test_read_user(self):
        expected_json = {"email": "tieg@gmail.com", "id": 1, "is_active": True, "items": [{"title": "tiegs pencil", 
        "description": "here lies tieg pencil", "id": 1, "owner_id": 1}, {"title": "tiegs pencil", 
        "description": "tiegs backup pencil", "id": 2, "owner_id": 1}]}
        expected_response = 200

        response = client.get("/users/1")
        self.assertTrue(response.status_code == expected_response)
        self.assertTrue(response.json() == expected_json)

    def test_read_items(self):
        expected_json = [
            {"title": "tiegs pencil", "description": "here lies tieg pencil", "id": 1, "owner_id": 1}, 
            {"title": "tiegs pencil", "description": "tiegs backup pencil", "id": 2, "owner_id": 1},
            {"title": "troys bag", "description": "this is troys bag", "id": 3, "owner_id": 2}
        ]
        expected_response = 200

        response = client.get("/items/")
        self.assertTrue(response.status_code == expected_response)
        self.assertTrue(response.json() == expected_json)

    def test_create_user(self):
        """This test case tests the creation of new users
        - The reset of the database used to also add in some dummy data. This cause a problem
        with testing the creation of new users. For some reason the index would still be set to 1.
        This is likely due to the mechanism of adding in a user with the route sets the index. So
        now we just add the dummy data with the create tests
        - Unit tests are preformed out of order. Well I haven't done much research, but my tests
        didn't execute in the order that they were layed out
        - This is really not great. Also notice how clean_test_database() needs to be called.
        Which takes a very long time(mostly because of heroku in USA). We need to reset the db for the
        other tests which happen in some other order
        - We should use a sqlite db so that this process will be instant
        """
        expected_json = {"email": "tony@hotmail.com", "id": 3, "is_active": True, "items": []}
        expected_status_code = 200
        response = client.post(
            "/users/",
            json={"email": "tony@hotmail.com", "password": "no password required", "is_active": True},
        )
        self.assertTrue(response.status_code == expected_status_code)
        self.assertTrue(response.json() == expected_json)

        clean_test_database()

    def test_create_item_for_user(self):
        """This test case tests the creation of new users
        - The reset of the database used to also add in some dummy data. This cause a problem
        with testing the creation of new users. For some reason the index would still be set to 1.
        This is likely due to the mechanism of adding in a user with the route sets the index. So
        now we just add the dummy data with the create tests
        """
        expected_json = {"title": "soda", "description": "bicarbonated beverage", "id": 4, "owner_id": 1}
        expected_status_code = 200
        response = client.post(
            "/users/1/items/",
            json={"title": "soda", "description": "bicarbonated beverage"},
        )
        self.assertTrue(response.status_code == expected_status_code)
        self.assertTrue(response.json() == expected_json)

        clean_test_database()