from rest_framework.authentication import TokenAuthentication as BaseAuthToken

class TokenAuthentication(BaseAuthToken):
    keyword = 'Bearer'