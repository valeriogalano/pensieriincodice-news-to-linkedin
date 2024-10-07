from github_helper import GithubHelper
from linkedin_helper import LinkedinHelper
import logging

logging.basicConfig(level=logging.DEBUG)


def auth():
    linkedin = LinkedinHelper()
    linkedin.auth()


def github_secrets():
    github = GithubHelper()
    github.post_credentials()


if __name__ == "__main__":
    auth()
    github_secrets()
