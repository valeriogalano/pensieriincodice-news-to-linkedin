import json
import logging
from datetime import datetime
from os import getenv
from urllib.parse import urlparse, parse_qs

import requests

logger = logging.getLogger("linkedin")


class LinkedinHelper:
    def __init__(self):
        self.today_date = datetime.now().strftime("%Y-%m-%d")

        self.CLIENT_ID = getenv("CLIENT_ID", None)
        self.CLIENT_SECRET = getenv("CLIENT_SECRET", None)
        self.CALLBACK_PROTOCOL = getenv("CALLBACK_URL_PROTOCOL", 'http')
        self.CALLBACK_URL = getenv("CALLBACK_URL", 'localhost')
        self.CALLBACK_PORT = getenv("CALLBACK_URL_PORT", "8000")
        self.COMPLETE_CALLBACK_URL = f"{self.CALLBACK_PROTOCOL}://{self.CALLBACK_URL}:{self.CALLBACK_PORT}"
        self.SCOPE = getenv("SCOPE", 'w_member_social openid profile')

        if isinstance(self.CALLBACK_PORT, str):
            self.CALLBACK_PORT = int(self.CALLBACK_PORT)

        self.access_token = getenv("ACCESS_TOKEN", None)
        self.personal_urn = getenv("PERSONAL_URN", None)

        logger.debug("Linkedin inizializzato!")

    def auth(self):
        url = (
            "https://www.linkedin.com/oauth/v2/authorization?response_type=code"
            f"&client_id={self.CLIENT_ID}"
            f"&redirect_uri={self.COMPLETE_CALLBACK_URL}"
            f"&scope={self.SCOPE}"
        )

        print(f"\nApri questo URL nel browser e autorizza l'applicazione:\n\n{url}\n")
        print(f"Dopo l'autorizzazione verrai reindirizzato a {self.COMPLETE_CALLBACK_URL}?code=...")
        print("Copia l'URL completo dalla barra del browser e incollalo qui sotto:\n")

        redirect_url = input("URL di redirect: ").strip()

        parsed = urlparse(redirect_url)
        params = parse_qs(parsed.query)

        if 'code' not in params:
            raise Exception("LinkedinHelper.auth error: 'code' non trovato nell'URL di redirect")

        code = params['code'][0]

        self.access_token = self.code_for_access_token(code)['access_token']
        self.personal_urn = self.get_personal_urn()['sub']

        token_data = {
            'code': code,
            'personal_urn': self.personal_urn,
            'access_token': self.access_token,
            'created_at': self.today_date
        }

        with open(f'{self.today_date}.json', 'w') as f:
            f.write(json.dumps(token_data))

        print(f"\nAutenticazione completata! Token salvato in {self.today_date}.json")

    def get_personal_urn(self):
        response = requests.get(
            'https://api.linkedin.com/v2/userinfo',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )

        if response.status_code == 200:
            return response.json()

        raise Exception(f"LinkedinHelper.get_personal_urn error: {response.status_code}\n{response.text}")

    def code_for_access_token(self, code):
        response = requests.post(
            "https://api.linkedin.com/oauth/v2/accessToken",
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET,
                "redirect_uri": self.COMPLETE_CALLBACK_URL
            }
        )

        if response.status_code == 200:
            return response.json()

        raise Exception(f"LinkedinHelper.code_for_access_token error: {response.status_code}\n{response.text}")

    def post(self, text, post_url=None):
        url = "https://api.linkedin.com/v2/ugcPosts"
        post_data = {
            "author": f"urn:li:person:{self.personal_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        post_type = "NONE"
        if post_url is not None and post_url != "":
            post_type = "ARTICLE"
            post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                {
                    "status": "READY",
                    "originalUrl": post_url,
                }
            ]

        post_data['specificContent']['com.linkedin.ugc.ShareContent']['shareMediaCategory'] = post_type

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'x-li-format': 'json'
        }

        response = requests.post(url, headers=headers, data=json.dumps(post_data))

        if response.status_code == 201:
            logger.debug("Post created successfully!")
        else:
            raise Exception(f"LinkedinHelper.post error: {response.status_code}\n{response.text}")
