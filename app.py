import web
import json
import requests
import time
import logging
from datetime import datetime
import os

try:
    user = os.environ["GH_USER"]
    cred = os.environ["GH_TOKEN"]
except:
    print("ERROR: You must set GH_USER and GH_TOKEN variables before executing this script")
    exit()


urls = (
    '/', "webhook"
)


class webhook:
    def __init__(self):
        self.session = requests.session()
        self.session.auth = (user, cred)

    def POST(self):
        currentdatetime = datetime.now()
        print("Received webhook POST at:", currentdatetime)
        logging.info("Received webhook POST")
        payload = json.loads(web.data())

        # Verify the repo was created
        try:
            if payload["action"] == "created":
                # Create branch protection for the main branch of the repo
                logging.info("Created branch for Organization: " +
                             payload["organization"]["login"] + " - in Repository: " + payload["repository"]["name"])
                print("Created branch for Organization: " +
                      payload["organization"]["login"], " - in Repository: " + payload["repository"]["name"])
                self.url = payload["repository"]["url"]
                self.protect_branch()
                self.create_issue()
        except KeyError:
            # There was a problem with the payload
            logging.warning("unexpected payload received: " + payload)
            print("unexpected payload received: ", payload)

    def protect_branch(self):
        print("Protecting branch")
        logging.info("Protecting branch")
        url = self.url + "/branches/main/protection"

        payload = json.dumps({
            "required_status_checks": {
                "strict": True,
                "contexts": [
                    "default"
                ]
            },
            "enforce_admins": False,
            "required_pull_request_reviews": None,
            "restrictions": None
        })

        response = self.session.put(
            url,
            payload,
        )

        if response.status_code == 200:
            print("Branch protection created successfully. Status code: ",
                  response.status_code)
            logging.info(
                "Branch protection created successfully. Status code: " + str(response.status_code))
        else:
            print("ERROR PROTECTING BRANCH!!! Status code: ", response.status_code)
            logging.warning(
                "ERROR PROTECTING BRANCH!!! Status code: " + str(response.status_code))
        return "OK"

    def create_issue(self):
        url = self.url + "/issues"
        logging.info("creating issue")
        payload = json.dumps({
            "title": "New Protection Added",
            "body": "@gabrielorce A new branch protection was added to the main branch."
        })
        response = self.session.post(
            url,
            payload,
        )

        if response.status_code == 201:
            print(
                "Issue created. Status code: ",
                response.status_code,
            )
            logging.info(
                "Issue created. Status code: " + str(response.status_code))

        else:
            print("ERROR CREATING ISSUE!!! Status code: ",
                  response.status_code,
                  )
            logging.warning(
                "ERROR CREATING ISSUE!!! Status code: " + str(response.status_code))
        return "OK"


# Create log directory if it does not already exist
if not os.path.exists("./log"):
    os.makedirs("./log")

# Set logging parameters
logging.basicConfig(
    filename="./log/actions.log",
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
