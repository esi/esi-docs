""" Python 3 Web Application OAuth 2.0 example.

This example can be run from the command line and will show you how the
OAuth 2.0 flow should be handled if you are a web based application.

Prerequisites:
    * Create an SSO application at developers.eveonline.com with the scope
      "esi-characters.read_blueprints.v1" and the callback URL
      "https://localhost/callback/". Note: never use localhost as a callback
      in released applications.
    * Have a Python 3 environment available to you (possibly by using a
      virtual environment: https://virtualenv.pypa.io/en/stable/).
    * Run pip install -r requirements.txt with this directory as your root.

To run this example, make sure you have completed the prerequisites and then
run the following command from this directory as the root:

>>> python esi_oauth_web.py

then follow the prompts.
"""
import base64

from shared_flow import print_auth_url
from shared_flow import send_token_request
from shared_flow import handle_sso_token_response


def main():
    """ Takes you through a local example of the OAuth 2.0 web flow."""

    print("This program will take you through an example OAuth 2.0 flow "
          "that you should be using if you are building a web based "
          "application. Follow the prompts and enter the info asked for.")

    client_id = input("\nCopy your SSO application's client ID and enter it "
                      "here: ")

    print_auth_url(client_id)

    auth_code = input("Copy the \"code\" query parameter and enter it here: ")
    app_secret = input("Copy your SSO application's secret key and enter it "
                       "here: ")

    # Basic auth can be taken care of by the requests library by passing in
    # the kwarg "auth=(client_id, app_secret)" but it's best to show how it's
    # done without it for this example.
    user_pass = "{}:{}".format(client_id, app_secret)
    basic_auth = base64.urlsafe_b64encode(user_pass.encode('utf-8')).decode()
    auth_header = "Basic {}".format(basic_auth)

    body = {
        "grant_type": "authorization_code",
        "code": auth_code,
    }

    headers = {"Authorization": auth_header}

    print("\nThe following request uses basic authentication, as a web based "
          "app you should do the same.")

    input("\nPress any key to continue:")

    res = send_token_request(body, add_headers=headers)

    handle_sso_token_response(res)


if __name__ == "__main__":
    main()
