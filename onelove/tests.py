from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from .models import User, Fleet
from django.contrib.auth.models import Group


class APITest(APITestCase):
    def setUp(self):
        """
        Setup token
        """
        user = User.objects.get(email='admin@example.com')
        self.token, created = Token.objects.get_or_create(user=user)

    def test_v1_get_fleets(self):
        """
        GET on 'fleet-list' URL with anonymous and authenticated user
        """
        endpoint = 'fleet-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_v1_get_groups(self):
        """
        GET on 'group-list' URL with anonymous and authenticated user
        """
        endpoint = 'group-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_v1_get_applications(self):
        """
        GET on 'application-list' URL with anonymous and authenticated
        user
        """
        endpoint = 'application-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_v1_get_providers(self):
        """
        GET on 'provider-list' URL with anonymous and authenticated
        user
        """
        endpoint = 'provider-list'
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(path=reverse(endpoint))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_v1_post_groups(self):
        """
        POST on 'group-list' URL with anonymous and authenticated user
        """
        endpoint = 'group-list'
        data = {
            'name': u'group',
            'permissions': [],
        }
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['id'] = response.data['id']
        data['fleets'] = []
        self.assertEqual(dict(response.data), data)

    def test_v1_post_fleets(self):
        """
        POST on 'fleet-list' URL with anonymous and authenticated user
        """
        endpoint = 'fleet-list'
        group = Group.objects.create(name='wordpress')
        data = {
            'name': u'fleet',
            'url': u'http://onelove.org/',
            'group': group.pk,
        }
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['applications'] = []
        data['id'] = response.data['id']
        data['providers'] = []
        self.assertEqual(dict(response.data), data)

    def test_v1_post_applications(self):
        """
        POST on 'application-list' URL with anonymous and authenticated
        user
        """
        endpoint = 'application-list'
        group = Group.objects.create(name='wordpress')
        fleet = Fleet.objects.create(group=group)
        data = {
            'name': u'application',
            'repo': u'https://github.com/one-love/wordpress.git',
            'fleet': fleet.id,
        }
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['id'] = response.data['id']
        self.assertEqual(dict(response.data), data)

    def test_v1_post_providers(self):
        """
        POST on 'provider-list' URL with anonymous and authenticated
        user
        """
        endpoint = 'provider-list'
        group = Group.objects.create(name='wordpress')
        fleet = Fleet.objects.create(group=group)
        data = {
            'name': u'provider',
            'access_key': u'sdfvsdvdsf',
            'security_key': u'vsdfvdsfgrvvfsdfvd',
            'fleet': fleet.id,
        }
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            path=reverse(endpoint),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['id'] = response.data['id']
        self.assertEqual(dict(response.data), data)
