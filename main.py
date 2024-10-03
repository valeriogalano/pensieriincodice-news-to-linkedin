from linkedin_helper import LinkedinHelper

if __name__ == "__main__":
    linkedin = LinkedinHelper()

    linkedin.auth()
    linkedin.post("Hello LinkedIn! This is my first post using the API.")
