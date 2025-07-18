import json

from app import app
from models import db, Plant

class TestPlant:
    '''Flask application in app.py'''

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        # Seed a plant before testing
        with app.app_context():
            plant = Plant(name="Test Plant", image="test.jpg", price=10.0, is_in_stock=True)
            db.session.add(plant)
            db.session.commit()
            plant_id = plant.id
        response = app.test_client().get(f'/plants/{plant_id}')
        assert(response.status_code == 200)

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        with app.app_context():
            plant = Plant(name="Test Plant 2", image="test2.jpg", price=20.0, is_in_stock=True)
            db.session.add(plant)
            db.session.commit()
            plant_id = plant.id
        response = app.test_client().get(f'/plants/{plant_id}')
        data = json.loads(response.data.decode())
        assert(type(data) == dict)
        assert(data["id"]) 
        assert(data["name"])

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        with app.app_context():
            plant_1 = Plant(name="Patch Plant", image="patch.jpg", price=30.0, is_in_stock=True)
            db.session.add(plant_1)
            db.session.commit()
            plant_id = plant_1.id
        response = app.test_client().patch(
            f'/plants/{plant_id}',
            json = {
                "is_in_stock": False,
            }
        )
        data = json.loads(response.data.decode())
        assert(type(data) == dict)
        assert(data["id"])
        assert(data["is_in_stock"] == False)

    def test_plant_by_id_delete_route_deletes_plant(self):
        '''returns JSON representing updated Plant object at "/plants/<int:id>".'''
        with app.app_context():
            lo = Plant(
                name="Live Oak",
                image="https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
                price=250.00,
                is_in_stock=False,
            )
            db.session.add(lo)
            db.session.commit()
            response = app.test_client().delete(f'/plants/{lo.id}')
            data = response.data.decode()
            assert(not data)