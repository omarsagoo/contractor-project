from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_dream_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_dream = {
    'title': 'My dream',
    'body': 'It was a dream',
    'tag': 'Funny'
}

sample_form_data = {
    'title': sample_dream['title'],
    'body': sample_dream['body'],
    'tag': sample_dream['Funny']
}

class DreamssTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the dreams homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Dream', result.data)

    def test_new(self):
        """Test the new dream creation page."""
        result = self.client.get('/dreams/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Dream', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_dream(self, mock_find):
        """Test showing a single dream."""
        mock_find.return_value = sample_dream

        result = self.client.get(f'/playlists/{sample_dream_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'My dream', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_dream(self, mock_find):
        """Test editing a single dream."""
        mock_find.return_value = sample_dream

        result = self.client.get(f'/dreams/{sample_dream_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Funny', result.data)

if __name__ == '__main__':
    unittest_main()