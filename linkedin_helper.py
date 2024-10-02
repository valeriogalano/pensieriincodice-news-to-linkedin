import json
import time
import os
from datetime import datetime
from os import getenv
from multiprocessing import Process

import requests
from selenium import webdriver

from flask_server import run_server


class LinkedinHelper:
    def __init__(self):
        self.today_date = datetime.now().strftime("%Y-%m-%d")
        self.server_thread = None

        self.CLIENT_ID = getenv("CLIENT_ID", None)
        self.CLIENT_SECRET = getenv("CLIENT_SECRET", None)
        self.CALLBACK_PROTOCOL = getenv("CALLBACK_URL_PROTOCOL", 'http')
        self.CALLBACK_URL = getenv("CALLBACK_URL", f'localhost')
        self.CALLBACK_PORT = int(getenv("CALLBACK_URL_PORT", "8000"))
        self.COMPLETE_CALLBACK_URL = f"{self.CALLBACK_PROTOCOL}://{self.CALLBACK_URL}:{self.CALLBACK_PORT}"
        self.SCOPE = getenv("SCOPE", 'w_member_social openid profile')

        self.access_token = getenv("ACCESS_TOKEN", None)
        self.personal_urn = getenv("PERSONAL_URN", None)

    def auth(self):
        try:
            # cancello il file se è già stato fatto un tentativo di login
            # nello stesso giorno ed è andato a male (o serve un secondo access token)
            os.remove(f'{self.today_date}.json')
        except Exception:  # noqa
            # se il file non esiste non sollevo eccezione
            pass

        self.start_local_server()

        # questa funzione richiede un desktop environment per essere eseguita
        url = (
            "https://www.linkedin.com/oauth/v2/authorization?response_type=code"
            f"&client_id={self.CLIENT_ID}"
            f"&redirect_uri={self.COMPLETE_CALLBACK_URL}"
            f"&scope={self.SCOPE}"
        )

        driver = webdriver.Chrome()
        driver.get(url)
        mainwindow = driver.window_handles[0]  # noqa

        condition = True
        json_code = None
        while condition:
            time.sleep(10)

            try:
                if os.path.exists(f'{self.today_date}.json'):
                    with open(f'{self.today_date}.json', 'r') as f:
                        string_json_code = f.readline()
                        json_code = json.loads(string_json_code)
                        if json_code['code'] is not None:
                            condition = False
            except Exception:  # noqa
                pass

        driver.close()
        self.stop_local_server()

        if json_code is None:
            raise Exception("LinkedinHelper.auth error: json_code is None")

        self.access_token = self.code_for_access_token(json_code['code'])['access_token']
        self.personal_urn = self.get_personal_urn()['sub']
        json_code['personal_urn'] = self.personal_urn
        json_code['access_token'] = self.access_token

        with open(f'{self.today_date}.json', 'w') as f:
            string_json = json.dumps(json_code, indent=4)
            f.write(string_json)

    def start_local_server(self):
        self.server_thread = Process(target=run_server)
        self.server_thread.start()

    def stop_local_server(self):
        self.server_thread.terminate()
        self.server_thread.join()

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
            print(response.json())
            return response.json()

        raise Exception(f"LinkedinHelper.code_for_access_token error: {response.status_code}\n{response.text}")

    def post(self, text):
        pass
