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
from jose.exceptions import ExpiredSignatureError, JWTError, JWTClaimsError


def validate_eve_jwt(jwt_token):
    """Validate a JWT token retrieved from the EVE SSO.

    Args:
        jwt_token: A JWT token originating from the EVE SSO
    Returns
        dict: The contents of the validated JWT token if there are no
              validation errors
    """

    jwk_set_url = "https://login.eveonline.com/oauth/jwks"

    res = requests.get(jwk_set_url)
    res.raise_for_status()

    data = res.json()

    try:
        jwk_sets = data["keys"]
    except KeyError as e:
        print("Something went wrong when retrieving the JWK set. The returned "
              "payload did not have the expected key {}. \nPayload returned "
              "from the SSO looks like: {}".format(e, data))
        sys.exit(1)

    jwk_set = next((item for item in jwk_sets if item["alg"] == "RS256"))

    try:
        return jwt.decode(
            jwt_token,
            jwk_set,
            algorithms=jwk_set["alg"],
            issuer="login.eveonline.com"
        )
    except ExpiredSignatureError:
        print("The JWT token has expired: {}")
        sys.exit(1)
    except JWTError as e:
        print("The JWT signature was invalid: {}").format(str(e))
        sys.exit(1)
    except JWTClaimsError as e:
        try:
            return jwt.decode(
                        jwt_token,
                        jwk_set,
                        algorithms=jwk_set["alg"],
                        issuer="https://login.eveonline.com"
                    )
        except JWTClaimsError as e:
            print("The issuer claim was not from login.eveonline.com or "
                  "https://login.eveonline.com: {}".format(str(e)))
            sys.exit(1)


def main():
    """Manually input a JWT token to be validated."""

    token = input("Enter an access token to validate: ")
    validated_jwt = validate_eve_jwt(token)

    print("\nThe contents of the access token are: {}".format(validated_jwt))


if __name__ == "__main__":
    main()
