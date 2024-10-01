from multiprocessing import Process

from flask_server import run_server


class LinkedinHelper:
    def __init__(self):
        self.server_thread = None

    def auth(self):
        pass

    def start_local_server(self):
        self.server_thread = Process(target=run_server)
        self.server_thread.start()

    def stop_local_server(self):
        self.server_thread.terminate()
        self.server_thread.join()

    def get_personal_urn(self):
        pass

    def post(self, text):
        pass
