// Token refresh utilities for EVE SSO.

const SSO_TOKEN = "https://login.eveonline.com/v2/oauth/token";
const USER_AGENT = "EVE Getting Started Guide/1.0 (your@email.com)";

/** Check if a JWT access token is expired or will expire soon. */
function isTokenExpired(accessToken: string, bufferSeconds = 60): boolean {
  const payload = JSON.parse(
    Buffer.from(accessToken.split(".")[1], "base64url").toString()
  );
  return Date.now() / 1000 >= payload.exp - bufferSeconds;
}

/** Exchange a refresh token for a new access token. */
async function refreshAccessToken(
  refreshToken: string,
  clientId: string,
  clientSecret: string
): Promise<{ access_token: string; refresh_token: string }> {
  const credentials = Buffer.from(`${clientId}:${clientSecret}`).toString(
    "base64"
  );
  const response = await fetch(SSO_TOKEN, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${credentials}`,
      "User-Agent": USER_AGENT,
    },
    body: new URLSearchParams({
      grant_type: "refresh_token",
      refresh_token: refreshToken,
    }),
  });
  if (!response.ok) {
    throw new Error(`Token refresh failed: ${response.status}`);
  }
  return response.json();
}

/** Return a valid access token, refreshing if needed. */
async function ensureValidToken(
  accessToken: string,
  refreshToken: string,
  clientId: string,
  clientSecret: string
): Promise<[string, string]> {
  if (!isTokenExpired(accessToken)) {
    return [accessToken, refreshToken];
  }
  const tokens = await refreshAccessToken(refreshToken, clientId, clientSecret);
  return [tokens.access_token, tokens.refresh_token];
}
