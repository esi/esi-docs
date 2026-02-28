// Your first ESI call — check the EVE server status.

interface ServerStatus {
  players: number;
  server_version: string;
  start_time: string;
}

const BASE_URL = "https://esi.evetech.net";
const USER_AGENT = "EVE Getting Started Guide/1.0 (your@email.com)";

const response = await fetch(`${BASE_URL}/v2/status/`, {
  headers: { "User-Agent": USER_AGENT },
});

if (!response.ok) {
  throw new Error(`HTTP ${response.status}: ${response.statusText}`);
}

const serverStatus: ServerStatus = await response.json();
console.log(`Players online: ${serverStatus.players}`);
console.log(`Server version: ${serverStatus.server_version}`);
console.log(`Started at:     ${serverStatus.start_time}`);

export {};
