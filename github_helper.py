import csv
import json
import logging
from base64 import b64encode
from datetime import datetime
from os import getenv

import requests
from nacl import encoding, public


logger = logging.getLogger("github")


class GithubHelper:
    def __init__(self):
        self.GH_CSV = getenv("GH_CSV", "")

        if self.GH_CSV == "":
            logger.warning("GH_CSV not set")
            exit(0)

        reader = csv.reader(self.GH_CSV.split('\\n'), delimiter=',')
        gh_csv = list(reader)

        self.gh_json = []
        for line in gh_csv:
            self.gh_json.append(
                {
                    "owner": line[0],
                    "name": line[1],
                    "token": line[2]
                }
            )

        self.today_date = datetime.now().strftime("%Y-%m-%d")
        self.personal_urn = None
        self.access_token = None

        self.get_repo_keys()

        logger.debug("Github inizializzato!")

    def get_repo_keys(self):
        for gh in self.gh_json:
            url = f"https://api.github.com/repos/{gh['owner']}/{gh['name']}/actions/secrets/public-key"
            response = requests.get(
                url,
                headers={
                    'Accept': 'application/vnd.github+json',
                    'Authorization': f'Bearer {gh["token"]}',
                    'X-GitHub-Api-Version': '2022-11-28'
                }
            )

            if response.status_code == 200:
                response_json = response.json()

                gh['key_id'] = response_json['key_id']
                gh['key'] = response_json['key']
            else:
                raise Exception(f"GithubHelper.get_repo_keys error: {response.status_code}\n{response.text}")

    def encrypt(self, public_key, secret_value):  # noqa
        public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())  # noqa
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))

        return b64encode(encrypted).decode("utf-8")

    def update_secret(self, gh, secret_name, encoded_secret_value):  # noqa
        logger.debug(f"Updating secret {secret_name}...")
        url = f"https://api.github.com/repos/{gh['owner']}/{gh['name']}/actions/secrets/{secret_name}"

        logger.debug(f"{url=} {encoded_secret_value=} - {gh['key_id']=}")
        response = requests.put(
            url,
            json={
                "encrypted_value": encoded_secret_value,
                "key_id": gh['key_id']
            },
            headers={
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {gh['token']}',
                'X-GitHub-Api-Version': '2022-11-28'
            }
        )

        if response.status_code == 201 or response.status_code == 204:
            logger.debug(f"Secret {secret_name} updated successfully!")
        else:
            raise Exception(f"GithubHelper.update_secret error: {response.status_code}\n{response.text}")

    def post_credentials(self):
        with open(f'{self.today_date}.json', 'r') as f:
            string_json_code = f.readline()
            json_code = json.loads(string_json_code)

            self.personal_urn = json_code['personal_urn']
            self.access_token = json_code['access_token']

        for gh in self.gh_json:
            encoded_ac = self.encrypt(gh['key'], self.access_token)
            self.update_secret(gh, 'ACCESS_TOKEN', encoded_ac)

            encoded_pu = self.encrypt(gh['key'], self.personal_urn)
            self.update_secret(gh, 'PERSONAL_URN', encoded_pu)
