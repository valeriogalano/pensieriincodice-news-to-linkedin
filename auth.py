from linkedin_helper import LinkedinHelper


def auth():
    linkedin = LinkedinHelper()
    linkedin.auth()


if __name__ == "__main__":
    auth()
