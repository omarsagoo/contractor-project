from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId
from datetime import datetime


sample_dream_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_dream = {
    'title': 'My dream',
    'body': 'It was a dream',
    'tag': 'Funny',
    'created_at': datetime.now()
}

sample_form_data = {
    'title': sample_dream['title'],
    'body': sample_dream['body'],
    'tag': sample_dream['tag'],
    'created_at': sample_dream['created_at']
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

        result = self.client.get(f'/dreams/{sample_dream_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'My dream', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_dream(self, mock_find):
        """Test editing a single dream."""
        mock_find.return_value = sample_dream

        result = self.client.get(f'/dreams/{sample_dream_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'My dream', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_dream(self, mock_insert):
        """Test submitting a new dream."""
        result = self.client.post('/dreams', data=sample_form_data)

        # After submitting, should redirect to that dreams's page
        self.assertEqual(result.status, '302 FOUND')

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_dream(self, mock_update):
        result = self.client.post(f'/dreams/{sample_dream_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_dream(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/dreams/{sample_dream_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_dream_id})

if __name__ == '__main__':
    unittest_main()