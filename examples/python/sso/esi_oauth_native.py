""" Python 3 native (desktop/mobile) OAuth 2.0 example.

This example can be run from the command line and will show you how the
OAuth 2.0 flow should be handled if you are a web based application.

Prequisites:
    * Create an SSO application at developers.eveonline.com with the scope
      "esi-characters.read_blueprints.v1" and the callback URL
      "https://localhost/callback/". Note: never use localhost as a callback
      in your real application.
    * Have a Python 3 environment available to you (possibly by using a
      virtual environment: https://virtualenv.pypa.io/en/stable/)
    * Run pip install -r requirements.txt with this directory as your root.

To run this example, make sure you have completed the prerequisites and then
run the following command from this directory as the root:

>>> python esi_oauth_native.py

then follow the prompts.
"""
import base64
import hashlib
import secrets

from shared_flow import print_auth_url
from shared_flow import send_token_request
from shared_flow import handle_sso_token_response


def main():
    """ Takes you through a local example of the OAuth 2.0 native flow."""

    print("This program will take you through an example OAuth 2.0 flow "
          "that you should be using if you are building a desktop or mobile "
          "application. Follow the prompts and enter the info asked for.")

    # Generate the PKCE code challenge
    random = secrets.token_bytes(32)
    m = hashlib.sha256()
    m.update(random)
    d = m.digest()
    code_challenge = base64.urlsafe_b64encode(d).decode().replace('=', '')

    client_id = input("Copy your SSO application's client ID and enter it "
                      "here: ")

    print("\nBecause this is a desktop/mobile application, you should use "
          "the PKCE protocol when contacting the EVE SSO. In this case, that "
          "means sending a base 64 encoded sha256 hashed 32 byte string "
          "called a code challenge. This 32 byte string should be ephemeral "
          "and never stored anywhere. The code challenge string generated for "
          "this program is {} and the hashed code challenge is {}. \nNotice "
          "that the query parameter of the following URL will contain this "
          "code challenge.".format(random, code_challenge))

    input("\nPress any key to continue:")

    print_auth_url(client_id, code_challenge=code_challenge)

    auth_code = input("Copy the \"code\" query parameter and enter it here: ")

    code_verifier = base64.urlsafe_b64encode(random).decode().replace("=", "")

    body = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": auth_code,
        "code_verifier": code_verifier
    }

    print("\nBecause this is using PCKE protocol, your application never has "
          "to share its secret key with the SSO. Instead, this next request "
          "will send the base 64 encoded unhashed value of the code "
          "challenge, called the code verifier, in the request body so EVE's "
          "SSO knows your application was not tampered with since the start "
          "of this process. The code verifier generated for this program is "
          "{} derived from the raw string {}".format(code_verifier, random))

    input("\nPress any key to continue:")

    res = send_token_request(body)

    handle_sso_token_response(res)


if __name__ == "__main__":
    main()
