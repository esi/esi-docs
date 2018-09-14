"""Revokes a given refresh token.

Prerequisites:
    * Have a Python 3 environment available to you (possibly by using a
      virtual environment: https://virtualenv.pypa.io/en/stable/)
    * Run pip install -r requirements.txt with this directory as your root.

This can be run by doing

>>> python revoke_refresh_token.py

and entering the data prompted for.
"""
import sys

import requests


def _retrieve_sso_meta(base_uri):
    sso_meta_path = ".well-known/oauth-authorization-server"
    sso_meta_endpoint = "{}/{}".format(base_uri, sso_meta_path)

    res = requests.get(sso_meta_endpoint)
    res.raise_for_status()

    return res.json()


def revoke_refresh_token(refresh_token, client_id, secret_key):
    """Revokes a refresh token from EVE's SSO.

    Args:
        refresh_token: A refresh token originating from the EVE SSO
        client_id: Your application's client ID
        secret_key: Your application's secret key
    """

    base_sso_uri = "https://login.eveonline.com"
    sso_meta = _retrieve_sso_meta(base_sso_uri)

    try:
        revocation_endpoint = sso_meta["revocation_endpoint"]
    except KeyError:
        print("The sso meta endpoint did not include the expected key "
              "revocation_endpoint. \nSSO meta info received is: "
              "{}".format(sso_meta))
        sys.exit(1)

    body = {
        "token": refresh_token,
        "token_type_hint": "refresh_token"
    }

    res = requests.post(
        revocation_endpoint,
        json=body,
        auth=(client_id, secret_key)
    )

    print("Made a request to {} with body: {} using basic "
          "authentication".format(revocation_endpoint, body))

    if res.status_code != 200:
        print("Something went wrong with the request to revoke your token. "
              "\nThe status code from EVE SSO is {} \nThe response body "
              "is {}".format(res.status_code, res.json()))
        sys.exit(1)

    return res.status_code


def main():
    """Manually input a refresh token to be revoked."""

    refresh_token = input("Copy and paste the refresh token you want to "
                          "revoke here: ")
    client_id = input("Copy and paste your application's client ID here: ")
    secret_key = input("Copy and paste your application's secret key here: ")

    revoke_status_code = revoke_refresh_token(
        refresh_token,
        client_id,
        secret_key
    )

    if revoke_status_code == 200:
        print("Success! Your token has been revoked!")


if __name__ == "__main__":
    main()
