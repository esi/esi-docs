"""Validates a given JWT token originating from the EVE SSO.

Prerequisites:
    * Have a Python 3 environment available to you (possibly by using a
      virtual environment: https://virtualenv.pypa.io/en/stable/)
    * Run pip install -r requirements.txt with this directory as your root.

This can be run by doing

>>> python validate_jwt.py

and passing in a JWT token that you have retrieved from the EVE SSO.
"""
import sys

import requests
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError


def validate_eve_jwt(jwt_token: str) -> dict:
    """Validate a JWT token retrieved from the EVE SSO.

    Args:
        jwt_token: A JWT token originating from the EVE SSO
    Returns:
        The contents of the validated JWT token if there are no validation errors
    """
    # fetch JWKs from endpoint
    res = requests.get("https://login.eveonline.com/oauth/jwks")
    res.raise_for_status()
    data = res.json()
    try:
        jwk_sets = data["keys"]
    except KeyError as e:
        print(
            "Something went wrong when retrieving the JWK set. "
            f"The returned payload did not have the expected key {e}.\n"
            f"Payload returned from the SSO looks like: {data}"
        )
        sys.exit(1)

    # pick the JWK with the RS256 alogorithm
    jwk_set = [item for item in jwk_sets if item["alg"] == "RS256"].pop()

    # try to decode the token and validate it against expected values
    # will raise exceptions if decoding fails or expected values do not match
    jwt_token = jwt.decode(
        jwt_token,
        jwk_set,
        algorithms=jwk_set["alg"],
        issuer=("login.eveonline.com", "https://login.eveonline.com"),
        audience="EVE Online",
    )
    return jwt_token


def main():
    """Manually input a JWT token to be validated."""

    token = input("Enter an access token to validate: ")

    try:
        validated_jwt = validate_eve_jwt(token)
    except ExpiredSignatureError:
        print("The JWT token has expired")
        sys.exit(1)
    except JWTError as e:
        print(f"The JWT token was invalid: {e}")
        sys.exit(1)

    print(f"\nThe contents of the access token are: {validated_jwt}")


if __name__ == "__main__":
    main()
