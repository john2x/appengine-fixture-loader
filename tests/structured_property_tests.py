import datetime
import unittest

# The test will error out if we can't import these items
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from appengine_fixture_loader.loader import load_fixture_flat


class Book(ndb.Model):
    title = ndb.StringProperty()
    date_published = ndb.DateProperty()


class Address(ndb.Model):
    city = ndb.StringProperty()
    state = ndb.StringProperty()
    country = ndb.StringProperty()


class Author(ndb.Model):
    """Our sample class"""
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    born = ndb.DateTimeProperty()
    address = ndb.LocalStructuredProperty(Address)
    books = ndb.StructuredProperty(Book, repeated=True)
    random = ndb.JsonProperty()


class StructuredPropertyTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.authors = load_fixture_flat('tests/authors.json', Author)

    def tearDown(self):
        self.testbed.deactivate()

    def test_structured_property(self):
        self.assertEqual(len(self.authors), 1)

        author = self.authors[0]
        self.assertEqual([b.title for b in author.books], [
            'The Hobbit', 'Fellowship of the Ring'
        ])
        self.assertEqual([b.date_published for b in author.books], [
            datetime.date(1937, 9, 21), datetime.date(1954, 7, 29)
        ])
        self.assertEqual(author.address.city, "Leeds")
        self.assertEqual(author.random, {"data": ["foo", "bar"]})
