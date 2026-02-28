// Complete OAuth2 flow — authenticate and read your character's location.

import * as http from "node:http";
import { URL, URLSearchParams } from "node:url";

// --- Configuration -----------------------------------------------------------
const CLIENT_ID = "your-client-id"; // From developers.eveonline.com
const CLIENT_SECRET = "your-client-secret"; // Keep this secret!
const CALLBACK_URL = "http://localhost:8089/callback";
const SCOPES = "esi-location.read_location.v1";

const BASE_URL = "https://esi.evetech.net";
const SSO_AUTH = "https://login.eveonline.com/v2/oauth/authorize";
const SSO_TOKEN = "https://login.eveonline.com/v2/oauth/token";
const USER_AGENT = "EVE Getting Started Guide/1.0 (your@email.com)";

// --- Step 1: Start a local server to capture the callback -------------------
function waitForCallback(): Promise<string> {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const url = new URL(req.url!, "http://localhost:8089");
      const code = url.searchParams.get("code");
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end("<h1>Login successful!</h1><p>You can close this tab.</p>");
      server.close();
      code ? resolve(code) : reject(new Error("No code in callback"));
    });
    server.listen(8089, () => console.log("Waiting for SSO callback..."));
    setTimeout(() => {
      server.close();
      reject(new Error("Timeout waiting for SSO callback"));
    }, 120_000);
  });
}

// --- Step 2: Open browser for SSO login -------------------------------------
const authParams = new URLSearchParams({
  response_type: "code",
  redirect_uri: CALLBACK_URL,
  client_id: CLIENT_ID,
  scope: SCOPES,
  state: "getting-started",
});

const authUrl = `${SSO_AUTH}?${authParams}`;
console.log(`Open this URL in your browser:\n${authUrl}\n`);

const authCode = await waitForCallback();

// --- Step 3: Exchange the code for tokens -----------------------------------
const credentials = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString(
  "base64"
);

const tokenResponse = await fetch(SSO_TOKEN, {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
    Authorization: `Basic ${credentials}`,
    "User-Agent": USER_AGENT,
  },
  body: new URLSearchParams({
    grant_type: "authorization_code",
    code: authCode,
  }),
});

if (!tokenResponse.ok) {
  throw new Error(`Token exchange failed: ${tokenResponse.status}`);
}

const tokens = (await tokenResponse.json()) as {
  access_token: string;
  refresh_token: string;
};
const accessToken = tokens.access_token;

// --- Step 4: Extract character ID from the JWT ------------------------------
const payload = JSON.parse(
  Buffer.from(accessToken.split(".")[1], "base64url").toString()
);
const characterId = parseInt(payload.sub.split(":").pop()!);
const characterName = payload.name;

// --- Step 5: Call an authenticated endpoint ---------------------------------
const locationResponse = await fetch(
  `${BASE_URL}/v1/characters/${characterId}/location/`,
  {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "User-Agent": USER_AGENT,
    },
  }
);

if (!locationResponse.ok) {
  throw new Error(`Location API failed: ${locationResponse.status}`);
}

const location = (await locationResponse.json()) as {
  solar_system_id: number;
};
console.log(
  `\n${characterName} is in solar system ${location.solar_system_id}`
);
