from django.test import TestCase, Client
from lesson import models
import ddt

from unittest import mock

# Create your tests here.


@ddt.ddt
class MaterialTestCase(TestCase):

    def setUp(self):
        super(MaterialTestCase, self).setUp()
        self.client = Client()
        self.user = models.User(first_name='testuser')
        self.user.save()

    def test_material_created_return_200(self):
        response = self.client.post(
            '/create/',
            {'title': 'testtitle',
             'body': 'testbody',
             'material_type': 'practice'},
        )
        self.assertEqual(response.status_code, 200)

    def test_created_one_material(self):
        response = self.client.post(
            '/create/',
            {'title': 'testtitle',
             'body': 'testbody',
             'material_type': 'practice'},
        )
        mat = models.Material.objects.get()
        self.assertEqual(mat.title, 'testtitle')

    @ddt.data('slug1', 'slug2', 'slug3')
    def test_slug_created(self, title):
        response = self.client.post(
            '/create/',
            {'title': title,
             'body': 'testbody',
             'material_type': 'practice'},
        )
        mat = models.Material.objects.get()
        self.assertEqual(mat.slug, title)

    @ddt.data(
        ("sl ug1", "sl-ug1"),
        ("sl u g1", "sl-u-g1"),
        ("sl u g 1", "sl-u-g-1"),
    )
    @ddt.unpack
    def test_slug_created_correctly(self, title, expected_slug):
        """test slug for title "{}" created correctly "{}\""""
        response = self.client.post(
            '/create/',
            {'title': title,
             'body': 'testbody',
             'material_type': 'practice'},
        )
        mat = models.Material.objects.get()
        self.assertEqual(mat.slug, expected_slug)

    def test_send_mail(self):
        material = models.Material(slug='slug',
                                   author=self.user,
                                   body='mybody')
        material.save()

        with mock.patch('lesson.views.send_mail') as mail_mock:
            response = self.client.post(
                '/' + str(material.id) + '/share/',
                {
                    "name": "test_name",
                    "my_email": "email@tt.ru",
                    "to_email": "email@tt.ru",
                    "comment": "test comment",
                }
            )
        mail_mock.assert_called_once()

    @mock.patch('lesson.views.send_mail')
    def test_send_mail_args(self, mail_mock):
        material = models.Material(slug='slug',
                                   author=self.user,
                                   body='mybody')
        material.save()

        with mock.patch('lesson.views.send_mail') as mail_mock:
            response = self.client.post(
                '/' + str(material.id) + '/share/',
                {
                    "name": "test_name",
                    "my_email": "email@tt.ru",
                    "to_email": "email@tt.ru",
                    "comment": "test comment",
                }
            )
            response = self.client.post(
                '/' + str(material.id) + '/share/',
                {
                    "name": "test_name",
                    "my_email": "email@tt.ru",
                    "to_email": "email@tt.ru",
                    "comment": "test comment",
                }
            )
        # mail_mock.assert_called_once()
        # mail_mock.assert_called_with('test_name (email@tt.ru) recommends you ', ' at http://testserver/2020/4/25/slug/\n\n test_name recommends you with comment:\n\ntest comment', 'admin@mysite.com', ['email@tt.ru'])
        self.assertEqual(mail_mock.call_args_list[0][0][2], "admin@mysite.com")
