import base64
import random
import requests
import string
import urllib

client_id = "your_client_id"
client_secret = "your_client_secret"


def request_token(authorization_code):
    """
    Takes an authorization code and exchanges it for an access token and refresh token.

    :param str authorization_code: The authorization code received from the SSO
    :returns: A dictionary containing the access token and refresh token
    """
    basic_auth = base64.urlsafe_b64encode(
        f"{client_id}:{client_secret}".encode("utf-8")
    ).decode()
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
    }
    response = requests.post(
        "https://login.eveonline.com/v2/oauth/token", headers=headers, data=payload
    )
    response.raise_for_status()

    return response.json()


def redirect_to_sso(scopes, redirect_uri):
    """
    Generates a URL to redirect the user to the SSO for authentication.

    :param list[str] scopes: A list of scopes that the application is requesting access to
    :param str redirect_uri: The URL where the user will be redirected back to after the authorization flow is complete
    :returns: A tuple containing the URL and the state parameter that was used
    """
    state = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    query_params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "state": state,
    }
    query_string = urllib.parse.urlencode(query_params)
    return (f"https://login.eveonline.com/v2/oauth/authorize?{query_string}", state)
