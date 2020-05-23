import base64
import requests
import datetime


class SpotipieAuth(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_uri = 'https://accounts.spotify.com/api/token'

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
        token_uri = self.token_uri
        data = self.get_token_data()
        headers = self.get_token_header()
        r = requests.post(token_uri, data=data, headers=headers)
        response = r.json()
        if r.status_code not in range(200, 299):
            raise Exception("client was not authenticated")
        now = datetime.datetime.now()
        access_token = response['access_token']
        expires_in = response['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires_in
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
