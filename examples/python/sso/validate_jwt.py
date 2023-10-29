"""Validates a given JWT access token originating from the EVE SSO.

Prerequisites:
    * Have a Python 3 environment available to you (possibly by using a
      virtual environment: https://virtualenv.pypa.io/en/stable/)
    * Run pip install -r requirements.txt with this directory as your root.

This can be run by doing

> python validate_jwt.py

and passing in a JWT access token that you have retrieved from the EVE SSO.
"""
import sys

import requests
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

SSO_META_DATA_URL = "https://login.eveonline.com/.well-known/oauth-authorization-server"
JWK_ALGORITHM = "RS256"
JWK_ISSUERS = ("login.eveonline.com", "https://login.eveonline.com")
JWK_AUDIENCE = "EVE Online"


def validate_eve_jwt(token: str) -> dict:
    """Validate a JWT access token retrieved from the EVE SSO.

    Args:
        token: A JWT access token originating from the EVE SSO
    Returns:
        The contents of the validated JWT access token if there are no errors
    """
    # fetch JWKs URL from meta data endpoint
    res = requests.get(SSO_META_DATA_URL)
    res.raise_for_status()
    data = res.json()
    try:
        jwks_uri = data["jwks_uri"]
    except KeyError:
        raise RuntimeError(
            f"Invalid data received from the SSO meta data endpoint: {data}"
        ) from None

    # fetch JWKs from endpoint
    res = requests.get(jwks_uri)
    res.raise_for_status()
    data = res.json()
    try:
        jwk_sets = data["keys"]
    except KeyError:
        raise RuntimeError(
            f"Invalid data received from the the jwks endpoint: {data}"
        ) from None

    # pick the JWK with the requested alogorithm
    jwk_set = [item for item in jwk_sets if item["alg"] == JWK_ALGORITHM].pop()

    # try to decode the token and validate it against expected values
    # will raise JWT exceptions if decoding fails or expected values do not match
    contents = jwt.decode(
        token=token,
        key=jwk_set,
        algorithms=jwk_set["alg"],
        issuer=JWK_ISSUERS,
        audience=JWK_AUDIENCE,
    )
    return contents


def main():
    token = input("Enter an access token to validate: ")

    try:
        token_contents = validate_eve_jwt(token)
    except ExpiredSignatureError:
        print("The JWT token has expired")
        sys.exit(1)
    except JWTError as e:
        print(f"The JWT token was invalid: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(str(e))
        sys.exit(1)
    else:
        print(f"\nThe contents of the access token are:\n{token_contents}")


if __name__ == "__main__":
    main()
