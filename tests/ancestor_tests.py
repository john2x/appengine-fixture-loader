"""
Test the one-level, multi-type loader
"""

import datetime
import unittest

# The test will error out if we can't import these items
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from appengine_fixture_loader.loader import load_fixture


class Customer(ndb.Model):
    name = ndb.StringProperty()

class Purchase(ndb.Model):
    price = ndb.IntegerProperty


class AncestorTests(unittest.TestCase):
    """Tests if we can load a JSON file"""
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.customers_data = load_fixture('tests/customers.json', Customer)
        self.purchases_data = load_fixture('tests/purchases.json', Purchase)

    def tearDown(self):
        self.testbed.deactivate()

    def test_loaded_count(self):
        """Make sure we got 2 objects from the JSON file"""
        self.assertEqual(len(self.customers_data), 2)
        self.assertEqual(len(self.purchases_data), 2)

    def test_ancestors(self):
        """Check whether the ancestor of keys we imported match the JSON contents"""
        john = Customer.query(Customer.name == 'John').get()
        self.assertEqual(john.name, 'John')

        john_purchases = Purchase.query(ancestor=john.key)
        self.assertEqual(john_purchases.count(), 1)
        self.assertEqual(john_purchases.get().key.parent(), john.key)


if __name__ == '__main__':
    unittest.main()
