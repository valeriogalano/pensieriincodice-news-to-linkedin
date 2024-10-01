import time

from linkedin_helper import LinkedinHelper

if __name__ == "__main__":
    linkedin = LinkedinHelper()
    linkedin.start_local_server()
    time.sleep(120)
    linkedin.stop_local_server()
