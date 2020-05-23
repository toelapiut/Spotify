import base64
import requests
import datetime
from urllib.parse import urlencode

base_url = 'https://api.spotify.com/v1'


class Spotipie(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__ (self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials (self):
        """
        encodes your client_id and client_secret
        :return: base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id is None or client_secret is None:
            raise Exception("client_id and client_secret are required")
        client_credential = f'{client_id}:{client_secret}'
        b64_encoded_client = base64.b64encode(client_credential.encode())
        return b64_encoded_client.decode()

    def get_token_data (self):
        return {
            "grant_type": "client_credentials"
        }

    def get_token_header (self):
        """
        :return: Authorization headers with encoded credentials
        """
        encoded_credential = self.get_client_credentials()
        return {
            "Authorization": f"Basic {encoded_credential}"
        }

    def auth_process (self):
        """
        :return: Boolean that indicates whether you've been granted access(True) or not(False)
        """
        token_url = self.token_url
        data = self.get_token_data()
        headers = self.get_token_header()
        r = requests.post(token_url, data=data, headers=headers)
        response = r.json()
        if r.status_code not in range(200, 299):
            raise Exception("client was not authenticated")
        now = datetime.datetime.now()
        access_token = response['access_token']
        expires_in = response['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token (self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.auth_process()
            return self.get_access_token()
        elif token is None:
            self.auth_process()
            return self.get_access_token()
        return token

    def get_resource_header (self):
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}"
        }

    def get_resource (self, _id, resources, v='v1'):
        headers = self.get_resource_header()
        resource_url = f'{base_url}/{v}/{resources}/{_id}',
        request = requests.get(resource_url, headers=headers)
        if request.status_code not in range(200, 299):
            return {}
        return request.json()

    def get_album (self, _id):
        return self.get_resource(_id, resources='album')

    def get_artist (self, _id):
        return self.get_resource(_id, resources='artist')

    def search (self, query, query_type, v='v1'):
        headers = self.get_resource_header()
        search_url = f'{base_url}/{v}/search'
        query_param = urlencode({"q": query, "type": query_type.lower()})
        query_string = f'{search_url}?{query_param}'
        request = requests.get(query_string, headers=headers)
        print(request.json())
        if request.status_code not in range(200, 299):
            return {}
        return request.json()
