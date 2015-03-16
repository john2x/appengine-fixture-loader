import datetime
import unittest

# The test will error out if we can't import these items
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from appengine_fixture_loader.loader import load_fixture_flat


class Person(ndb.Model):
    """Our sample class"""
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    born = ndb.DateTimeProperty()
    userid = ndb.IntegerProperty()
    thermostat_set_to = ndb.FloatProperty()
    snores = ndb.BooleanProperty()
    started_school = ndb.DateProperty()
    sleeptime = ndb.TimeProperty()
    favorite_movies = ndb.JsonProperty()
    processed = ndb.BooleanProperty(default=False)


class Product(ndb.Model):
    name = ndb.StringProperty()


class Purchase(ndb.Model):
    price = ndb.FloatProperty(required=True)
    product = ndb.KeyProperty(kind=Product, required=True)


class FlatLoaderTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.persons = load_fixture_flat('tests/hard_coded_id.json', Person)
        self.products = load_fixture_flat('tests/products.json', Product)

    def tearDown(self):
        self.testbed.deactivate()

    def test_loaded_id(self):
        """Check whether the attributes we imported match the JSON contents"""
        # Test if John got in
        john_key = ndb.Key('Person', 'jdoe')
        john = john_key.get()
        self.assertEqual(john.first_name, 'John')
        self.assertEqual(john.last_name, 'Doe')
        self.assertEqual(john.born, datetime.datetime(1968, 3, 3))
        self.assertEqual(john.thermostat_set_to, 18.34)
        self.assertFalse(john.processed)

    def test_loaded_key(self):
        purchases = load_fixture_flat('tests/purchases_key.json', Purchase)

        john_key = ndb.Key('Person', 'jdoe')
        purchases_q = Purchase.query(ancestor=john_key)
        self.assertEqual(purchases_q.count(), len(purchases))
        self.assertEqual(sum([p.price for p in purchases_q.fetch()]), 150)
        self.assertEqual(purchases_q.get().product.get().name, "Product 1")

    def test_loaded_parent(self):
        purchases = load_fixture_flat('tests/purchases_parent.json', {
            'Purchase': Purchase
        })

        john_key = ndb.Key('Person', 'jdoe')
        purchases_q = Purchase.query(ancestor=john_key)
        self.assertEqual(purchases_q.count(), len(purchases))
        self.assertEqual(sum([p.price for p in purchases_q.fetch()]), 150)


if __name__ == '__main__':
    unittest.main()
