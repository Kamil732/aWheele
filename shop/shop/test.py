from django.test import TestCase, override_settings

# class MulitDomainTestCase(TestCase):
#     @override_settings(ALLOWED_HOSTS=['otherserver'])
#     def test_other_domain(self):
#         response = self.client.get('http://otherserver/accounts/login')
#         self.assertEqual(response.status_code, 200)