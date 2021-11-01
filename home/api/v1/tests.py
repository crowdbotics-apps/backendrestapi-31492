from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from subscriptions.models import Plan, Subscription
from apps.models import App
from rest_framework.authtoken.models import Token

class RestApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):

        testPlanFree = Plan.objects.create(name='Free', description='Free Plan', price=0)
        testPlanStd = Plan.objects.create(name='Standard', description='Standard Plan', price=10)
        testPlanPro = Plan.objects.create(name='Pro', description='Pro Plan', price=25)

        testUser1 = User.objects.create_user(username='Test User1', email='tu1@test.com', password='password1')
        testUser2 = User.objects.create_user(username='Test User2', email='tu2@test.com', password='password2')

        testApp1 = App.objects.create(name='App One', description='First Application', type='ty1', framework='fw1',
                                      user=testUser1)
        testApp2 = App.objects.create(name='App Two', description='Second Application', type='ty2', framework='fw2',
                                      user=testUser2)

        testsubs1 = Subscription.objects.create(user=testUser1, plan=testPlanFree, app=testApp1, active=True)
        testsubs2 = Subscription.objects.create(user=testUser2, plan=testPlanStd, app=testApp2, active=False)


    def setUp(self):
        self.token = Token.objects.create(user=User.objects.get(username='Test User1'))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_register(self):
        """
        Ensure we can register users.
        """
        url = reverse('rest_register')
        data = {'username': 'ram', 'email': 'kramsn@gmail.com', 'password': 'password1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_plans(self):
        url = reverse('plans-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data[0]['name']), 'Free')
        self.assertEqual(len(response.data), 3)

    def test_plan_create_not_allowed(self):
        data = {'name':'Test', 'description':'Test Plan', 'price':50}
        url = reverse('plans-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_plan_update_not_allowed(self):
        url = reverse('plans-detail', kwargs={'pk':1})
        response = self.client.get(url)
        response.data['name'] = 'Update Plan Name'
        response = self.client.put(url, dict(response.data), format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_plan_patch_not_allowed(self):
        url = reverse('plans-detail', kwargs={'pk':1})
        response = self.client.get(url)
        response.data['name'] = 'Update Plan Name'
        del response.data['description']
        response = self.client.patch(url, dict(response.data), format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_apps(self):
        url = reverse('apps-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'App One')
        self.assertEqual(len(response.data), 1)

    def test_list_apps_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('apps-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_apps_create(self):
        url = reverse('apps-list')
        data = {
                    'name': 'Test App 10',
                    'description': '10th Application',
                    'type':'ty1',
                    'framework':'fw1',
                    'user':User.objects.get(username='Test User1').id
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test App 10')

    def test_apps_create_unauthorized_user(self):
        url = reverse('apps-list')
        data = {
            'name': 'Test App 10',
            'description': '10th Application',
            'type':'ty1',
            'framework':'fw1',
            'user':User.objects.get(username='Test User2').id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_apps_update(self):
        url = reverse('apps-detail', kwargs={"pk": 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = dict(response.data[0])
        data['description'] = 'Updated description'

        url = reverse('apps-detail', kwargs={"pk": 1})
        resp = self.client.put(url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['description'], 'Updated description')

    def test_apps_update_wrong_user_info(self):
        url = reverse('apps-detail', kwargs={"pk": 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = dict(response.data[0])
        data['description'] = 'wrong user update description'
        data['user'] = 2

        url = reverse('apps-detail', kwargs={"pk": 1})
        resp = self.client.put(url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_apps_patch(self):
        url = reverse('apps-detail', kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = dict(response.data[0])
        data['description'] = 'Patched description'

        del data['type']
        del data['framework']

        url = reverse('apps-detail', kwargs={"pk": 1})
        resp = self.client.patch(url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['description'], 'Patched description')

    def test_apps_patch_wrong_user_info(self):
        url = reverse('apps-detail', kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = dict(response.data[0])
        data['user'] = 2

        del data['type']
        del data['framework']

        url = reverse('apps-detail', kwargs={"pk": 1})
        resp = self.client.patch(url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_app_delete(self):
        url = reverse('apps-detail', kwargs={"pk": 3})
        response = self.client.get(url)
        response = self.client.delete(url, dict(response.data), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_subscription(self):
        url = reverse('subscriptions-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_subscription_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        url = reverse('subscriptions-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscription_create_integrity_constrain(self):
        data = {
            'user':User.objects.get(username='Test User1').id,
            'plan': 1,
            'app': 1,
            'active':'true'
        }
        url = reverse('subscriptions-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscription_create(self):
        data = {
            'user':User.objects.get(username='Test User1').id,
            'plan': 1,
            'app': 2,
            'active':'true'
        }
        url = reverse('subscriptions-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_update(self):
        url = reverse('subscriptions-detail', kwargs={"pk": 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = dict(response.data[0])
        data['active'] = False

        url = reverse('subscriptions-detail', kwargs={"pk": 1})
        resp = self.client.put(url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['active'], False)

    def test_subscription_update_wrong_user_info(self):
        url = reverse('subscriptions-detail', kwargs={"pk": 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = dict(response.data[0])
        data['active'] = False
        data['user'] = 2

        url = reverse('subscriptions-detail', kwargs={"pk": 1})
        resp = self.client.put(url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscription_patch(self):
        url = reverse('subscriptions-detail', kwargs={"pk": 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = dict(response.data[0])
        data['active'] = False

        del data['plan']
        del data['app']

        url = reverse('subscriptions-detail', kwargs={"pk": 1})
        resp = self.client.patch(url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['active'], False)

    def test_subscription_patch_wrong_user_info(self):
        url = reverse('subscriptions-detail', kwargs={"pk": 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = dict(response.data[0])
        data['user'] = 2

        del data['plan']
        del data['app']

        url = reverse('subscriptions-detail', kwargs={"pk": 1})
        resp = self.client.patch(url, data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscription_delete_not_allowed_check(self):
        url = reverse('subscriptions-detail', kwargs={"pk": 3})
        response = self.client.get(url)
        response = self.client.delete(url, dict(response.data), format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login(self):
        data = {'username':'Test User1', 'email':'tu1@test.com', 'password':'password1'}
        url = reverse('rest_login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response,'key')

