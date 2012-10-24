from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.models import ApiKey
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication

from django.contrib.auth.models import User
from sapling.api import api


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['username', 'first_name', 'last_name', 'date_joined']
        filtering = {
            'username': ALL,
            'first_name': ALL,
            'last_name': ALL,
            'date_joined': ALL,
        }

class ApiKeyResource(ModelResource):
    class Meta:
        queryset = ApiKey.objects.all()
        resource_name = "api_key"
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()

class UserWithApiKeyResource(ModelResource):
    api_key = fields.ForeignKey('users.api.ApiKeyResource', 
                                'api_key', null=True, readonly=True)
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users_with_apikey'
        fields = ['username', 'api_key', 'email']
        filtering = {
            'username': ALL,
            'api_key': ALL,
            'email': ALL,
        }
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()

api.register(UserResource())
api.register(ApiKeyResource())
api.register(UserWithApiKeyResource())
