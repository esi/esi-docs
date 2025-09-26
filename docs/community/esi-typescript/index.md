---
search:
  exclude: true

title: EVE API for TypeScript
type: resource
description: TypeScript client library for EVE Online API (ESI).
maintainer:
  name: Leigh Griffin
  github: lgriffin
---

# ESI.ts

[![npm version](https://badge.fury.io/js/%40lgriffin%2Fesi.ts.svg)](https://badge.fury.io/js/%40lgriffin%2Fesi.ts)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.5%2B-blue)](https://www.typescriptlang.org/)

A modern, type-safe TypeScript implementation for the [EVE Online ESI API](https://esi.evetech.net/). Built with clean architecture principles, comprehensive error handling, and extensive testing.

## 🚀 Features

- **Type-Safe**: Full TypeScript support with comprehensive type definitions
- **Clean Architecture**: Separation of concerns with dependency injection
- **Resilient**: Built-in error handling, retry logic, and circuit breakers
- **High Performance**: Intelligent ETag caching for optimal bandwidth usage
- **Testable**: Extensive test coverage with BDD scenarios
- **Modern**: Uses latest TypeScript features and best practices
- **Comprehensive**: Covers all ESI API endpoints with organized client structure

## 📦 Installation

```bash
npm install @lgriffin/esi.ts
```

## 🔧 Getting Started

ESI.ts offers multiple ways to use the API depending on your needs:

### 1. Full ESI Client (All APIs)

The complete `EsiClient` gives you access to all ESI endpoints:

```typescript
import { EsiClient } from '@lgriffin/esi.ts';

// Full client with all APIs available
const client = new EsiClient({
  clientId: 'your-app-name',
  accessToken: 'your-access-token', // Optional - required for authenticated endpoints
  timeout: 30000,                   // Optional - request timeout in ms
  retryAttempts: 3                  // Optional - number of retry attempts
});
```

### 2. Custom Lightweight Client (Selected APIs)

Create a lightweight client with only the APIs you need:

```typescript
import { CustomEsiClient } from '@lgriffin/esi.ts';

// Lightweight client with only specific APIs
const customClient = new CustomEsiClient({
  clientId: 'my-trading-bot',
  clients: ['characters', 'market', 'universe'] // Only load what you need
});

// Access your selected APIs
const character = await customClient.characters?.getCharacterPublicInfo(123456);
const prices = await customClient.market?.getMarketPrices();
```

### 3. Builder Pattern for Custom Clients

Use the builder pattern for more readable client construction:

```typescript
import { EsiClientBuilder } from '@lgriffin/esi.ts';

// Build a custom client step by step
const client = new EsiClientBuilder()
  .addClient('characters')
  .addClient('corporations')
  .addClients(['market', 'universe'])
  .withClientId('my-corp-manager')
  .withAccessToken('your-token')
  .build();
```

### 4. Individual API Clients (Ultra Lightweight)

Create standalone clients for single API groups:

```typescript
import { EsiApiFactory } from '@lgriffin/esi.ts';

// Just the Character API
const characterClient = EsiApiFactory.createCharacterClient({
  clientId: 'character-lookup-tool'
});

const character = await characterClient.getCharacterPublicInfo(123456);

// Just the Market API
const marketClient = EsiApiFactory.createMarketClient({
  clientId: 'market-analyzer'
});

const prices = await marketClient.getMarketPrices();
```

### 5. Direct API Class Instantiation

For maximum control, instantiate API clients directly:

```typescript
import { CharacterClient, ApiClient, ApiClientBuilder } from '@lgriffin/esi.ts';

// Create the underlying API client
const apiClient = new ApiClientBuilder()
  .withClientId('direct-api-client')
  .withBaseUrl('https://esi.evetech.net')
  .build();

// Create the Character client directly
const characterClient = new CharacterClient(apiClient);
const character = await characterClient.getCharacterPublicInfo(123456);
```

## 📊 Client Architecture

### Available Client Types

All approaches above give you access to these organized API clients:

```typescript
// Available clients:
client.alliance      // Alliance information
client.characters    // Character data
client.corporations  // Corporation management
client.market        // Market data and trading
client.universe      // Universe information (systems, stations, items)
client.fleets        // Fleet management
client.industry      // Manufacturing and industry
client.mail          // In-game mail
client.contacts      // Contact management
client.assets        // Asset management
client.wallet        // Wallet operations
client.killmails     // Killmail data
client.location      // Character location
client.skills        // Character skills (if available)
client.factions      // Faction warfare
client.wars          // War information
client.sovereignty   // Sovereignty data
client.incursions    // Incursion information
client.opportunities // Opportunities system
client.fittings      // Ship fittings
client.clones        // Clone management
client.loyalty       // Loyalty points
client.bookmarks     // Bookmark management
client.calendar      // Calendar events
client.contracts     // Contract system
client.insurance     // Insurance information
client.route         // Route planning
client.search        // Search functionality
client.status        // Server status
client.ui            // UI interactions
```

## 🎯 Choosing the Right Approach

### When to Use Each Method

| Approach | Best For | Memory Usage | Startup Time |
|----------|----------|--------------|--------------|
| **Full EsiClient** | Complete applications, multiple API usage | High | Slower |
| **CustomEsiClient** | Focused applications, selected APIs | Medium | Medium |
| **EsiApiFactory** | Single-purpose tools, microservices | Low | Fast |
| **Direct Instantiation** | Libraries, embedded usage | Minimal | Fastest |

### Practical Examples by Use Case

#### Character Lookup Tool (Ultra Lightweight)

```typescript
import { EsiApiFactory } from '@lgriffin/esi.ts';

const characterClient = EsiApiFactory.createCharacterClient({
  clientId: 'character-lookup-v1'
});

// Just character operations
const character = await characterClient.getCharacterPublicInfo(123456);
const portrait = await characterClient.getCharacterPortrait(123456);
console.log(`${character.body.name} - ${portrait.body.px128x128}`);
```

#### Trading Bot (Selected APIs)

```typescript
import { EsiClientBuilder } from '@lgriffin/esi.ts';

const tradingBot = new EsiClientBuilder()
  .addClients(['market', 'characters', 'universe', 'wallet'])
  .withClientId('trading-bot-v2')
  .withAccessToken(process.env.EVE_ACCESS_TOKEN)
  .build();

// Only the APIs you need are loaded
const prices = await tradingBot.market?.getMarketPrices();
const wallet = await tradingBot.wallet?.getCharacterWallet(characterId);
```

#### Corporation Management Dashboard (Custom Client)

```typescript
import { CustomEsiClient } from '@lgriffin/esi.ts';

const corpManager = new CustomEsiClient({
  clientId: 'corp-dashboard',
  accessToken: directorToken,
  clients: ['corporations', 'characters', 'assets', 'wallet', 'mail']
});

// Efficient corp management with only needed APIs
const corp = await corpManager.corporations?.getCorporationInfo(corpId);
const members = await corpManager.corporations?.getCorporationMembers(corpId);
```

## 📋 Common Usage Patterns

### Public Data (No Authentication Required)

```typescript
// Get alliance information
const alliance = await client.alliance.getAllianceById(99005338);
console.log(`Alliance: ${alliance.name} [${alliance.ticker}]`);

// Get character public information
const character = await client.characters.getCharacterPublicInfo(1689391488);
console.log(`Character: ${character.name}`);

// Get corporation information
const corporation = await client.corporations.getCorporationInfo(98742334);
console.log(`Corporation: ${corporation.name} [${corporation.ticker}]`);

// Get market prices
const prices = await client.market.getMarketPrices();
console.log(`Found ${prices.length} market prices`);

// Get solar system information
const system = await client.universe.getSystemById(30000142);
console.log(`System: ${system.name} (Security: ${system.security_status})`);
```

### Authenticated Data (Access Token Required)

```typescript
// Initialize with access token
const authenticatedClient = new EsiClient({
  clientId: 'your-app-name',
  accessToken: 'your-character-access-token'
});

const characterId = 1689391488;

// Get character's assets
const assets = await authenticatedClient.assets.getCharacterAssets(characterId);
console.log(`Character has ${assets.length} assets`);

// Get character's wallet balance
const wallet = await authenticatedClient.wallet.getCharacterWallet(characterId);
console.log(`Wallet balance: ${wallet.toLocaleString()} ISK`);

// Get character's mail
const mail = await authenticatedClient.mail.getCharacterMail(characterId);
console.log(`Character has ${mail.length} mail messages`);

// Get character's market orders
const orders = await authenticatedClient.market.getCharacterOrders(characterId);
console.log(`Character has ${orders.length} active market orders`);
```

### Complex Workflows

```typescript
// Character Profile Assembly
async function getCompleteCharacterProfile(characterId: number) {
  const [character, portrait, corporation, location] = await Promise.all([
    client.characters.getCharacterPublicInfo(characterId),
    client.characters.getCharacterPortrait(characterId),
    client.characters.getCharacterPublicInfo(characterId).then(char => 
      client.corporations.getCorporationInfo(char.corporation_id)
    ),
    client.location.getCharacterLocation(characterId)
  ]);

  return {
    character,
    portrait,
    corporation,
    location
  };
}

// Market Analysis
async function analyzeMarketData(regionId: number, typeId: number) {
  const [prices, orders, history] = await Promise.all([
    client.market.getMarketPrices(),
    client.market.getMarketOrders(regionId, { type_id: typeId }),
    client.market.getMarketHistory(regionId, typeId)
  ]);

  const currentPrice = prices.find(p => p.type_id === typeId)?.average_price;
  const buyOrders = orders.filter(o => o.is_buy_order);
  const sellOrders = orders.filter(o => !o.is_buy_order);

  return {
    currentPrice,
    bestBuyPrice: Math.max(...buyOrders.map(o => o.price)),
    bestSellPrice: Math.min(...sellOrders.map(o => o.price)),
    dailyVolume: history[0]?.volume || 0
  };
}
```

## 📊 Error Handling

The library provides comprehensive error handling with specific error types:

```typescript
import { ApiError, ApiErrorType } from '@lgriffin/esi.ts';

try {
  const alliance = await client.alliance.getAllianceById(99999999); // Invalid ID
} catch (error) {
  if (error instanceof ApiError) {
    switch (error.type) {
      case ApiErrorType.NOT_FOUND:
        console.log('Alliance not found');
        break;
      case ApiErrorType.RATE_LIMITED:
        console.log('Rate limited - retry after:', error.retryAfter);
        break;
      case ApiErrorType.SERVER_ERROR:
        console.log('ESI server error:', error.statusCode);
        break;
      case ApiErrorType.NETWORK_ERROR:
        console.log('Network connectivity issue');
        break;
      case ApiErrorType.AUTHENTICATION_ERROR:
        console.log('Invalid or expired access token');
        break;
      default:
        console.log('Unexpected error:', error.message);
    }
  }
}
```

### Graceful Error Handling in Complex Workflows

```typescript
async function safeCharacterLookup(characterId: number) {
  try {
    // Use Promise.allSettled for partial success scenarios
    const results = await Promise.allSettled([
      client.characters.getCharacterPublicInfo(characterId),
      client.characters.getCharacterPortrait(characterId),
      client.location.getCharacterLocation(characterId)
    ]);

    const profile: any = {};

    if (results[0].status === 'fulfilled') {
      profile.character = results[0].value;
    }
    
    if (results[1].status === 'fulfilled') {
      profile.portrait = results[1].value;
    }
    
    if (results[2].status === 'fulfilled') {
      profile.location = results[2].value;
    } else if (results[2].status === 'rejected') {
      console.log('Location unavailable (character may be offline)');
    }

    return profile;
  } catch (error) {
    console.error('Failed to get character data:', error);
    return null;
  }
}
```

## ⚡ Performance & Caching

### Intelligent ETag Caching

ESI.ts includes a sophisticated ETag caching system that automatically optimizes API calls by avoiding unnecessary data transfers. This feature is **enabled by default** and works transparently with all GET requests.

#### How ETag Caching Works

ETags (Entity Tags) are unique identifiers returned by ESI servers that represent the current version of a resource. When data hasn't changed, the server returns a `304 Not Modified` status instead of the full data, dramatically reducing bandwidth usage and improving response times.

#### Basic Usage (Automatic)

```typescript
import { EsiClient } from '@lgriffin/esi.ts';

// ETag caching is enabled by default
const client = new EsiClient({
  clientId: 'my-eve-app'
});

// First call - downloads and caches data
const alliances1 = await client.alliance.getAlliances();

// Second call - returns cached data if unchanged (304 response)
const alliances2 = await client.alliance.getAlliances(); // ⚡ Lightning fast!
```

#### Custom Cache Configuration

```typescript
const client = new EsiClient({
  clientId: 'my-eve-app',
  enableETagCache: true, // Default: true
  etagCacheConfig: {
    maxEntries: 1000,      // Max cached responses (default: 1000)
    defaultTtl: 300000,    // Cache TTL in ms (default: 5 minutes)
    cleanupInterval: 60000, // Cleanup frequency (default: 1 minute)
    persistToStorage: true, // Save to localStorage (default: false)
    storageKey: 'my-esi-cache' // Custom storage key
  }
});
```

#### Cache Management

```typescript
// Get cache statistics
const stats = client.getCacheStats();
console.log(`Cache: ${stats.totalEntries}/${stats.maxEntries} entries`);
console.log(`Hit rate optimization: ${stats.hitRate}%`);

// Clear cache manually
client.clearCache();

// Update cache settings at runtime
client.updateCacheConfig({
  maxEntries: 2000,
  defaultTtl: 600000 // 10 minutes
});

// Disable caching for specific use cases
const client = new EsiClient({
  enableETagCache: false // Disable caching entirely
});
```

#### Performance Benefits

- **🚀 Faster Response Times**: Cached responses return instantly
- **📉 Reduced Bandwidth**: Avoid downloading unchanged data
- **🔋 Server-Friendly**: Reduces load on ESI servers
- **💰 Cost Effective**: Lower data usage for mobile/metered connections
- **🎯 Smart Caching**: Only caches GET requests with ETags

#### Cache Behavior

| Scenario | Behavior | Performance Impact |
|----------|----------|-------------------|
| First API call | Downloads data, stores ETag | Normal speed |
| Data unchanged | Returns cached data (304) | ⚡ **~95% faster** |
| Data changed | Downloads new data, updates cache | Normal speed |
| Cache expired | Downloads fresh data | Normal speed |
| Cache full | Evicts oldest entries automatically | Minimal impact |

#### Advanced ETag Features

```typescript
// Monitor cache performance
client.on('cacheHit', (url, etag) => {
  console.log(`Cache hit for ${url} with ETag ${etag}`);
});

client.on('cacheMiss', (url) => {
  console.log(`Cache miss for ${url} - downloading fresh data`);
});

// Programmatic cache inspection
const cache = client.getETagCache();
if (cache) {
  const entry = cache.get('https://esi.evetech.net/latest/alliances');
  if (entry) {
    console.log(`Cached data age: ${Date.now() - entry.timestamp}ms`);
    console.log(`ETag: ${entry.etag}`);
  }
}
```

#### When ETag Caching Helps Most

- **📊 Market Data**: Price lists that update periodically
- **🏢 Corporation/Alliance Info**: Relatively static organizational data  
- **🌌 Universe Data**: Star system, station, and type information
- **👥 Character Lists**: Member rosters and public information
- **📈 Statistics**: Aggregate data that updates on intervals

#### Implementation Details

- **Architecture**: Implemented at the core `ApiRequestHandler` level
- **Scope**: Works with ALL GET requests automatically
- **Compatibility**: Fully backward compatible - existing code works unchanged
- **Thread Safety**: Uses atomic operations for cache management
- **Memory Efficient**: Automatic cleanup and size management
- **Storage Options**: In-memory (default) or persistent localStorage

## 🔧 Advanced Configuration

### Custom Timeout and Retry Logic

```typescript
const client = new EsiClient({
  clientId: 'my-eve-app',
  timeout: 60000,      // 60 second timeout
  retryAttempts: 5,    // Retry up to 5 times
  baseUrl: 'https://esi.evetech.net' // Custom ESI endpoint (optional)
});
```

### Using Environment Variables

```typescript
// Set environment variables
// ESI_CLIENT_ID=your-app-name
// ESI_ACCESS_TOKEN=your-token
// ESI_TIMEOUT=30000

const client = new EsiClient({
  clientId: process.env.ESI_CLIENT_ID,
  accessToken: process.env.ESI_ACCESS_TOKEN,
  timeout: parseInt(process.env.ESI_TIMEOUT || '30000')
});
```

## 🚀 Real-World Examples

### EVE Market Trading Bot (Lightweight Version)

```typescript
import { EsiClientBuilder } from '@lgriffin/esi.ts';

class MarketBot {
  private client: any; // CustomEsiClient

  constructor(accessToken: string) {
    // Only load the APIs we actually need
    this.client = new EsiClientBuilder()
      .addClients(['market', 'universe'])
      .withClientId('market-bot-v1')
      .withAccessToken(accessToken)
      .build();
  }

  async findArbitrageOpportunities(regionId: number, typeId: number) {
    try {
      const [orders, history] = await Promise.all([
        this.client.market.getMarketOrders(regionId, { type_id: typeId }),
        this.client.market.getMarketHistory(regionId, typeId)
      ]);

      const buyOrders = orders.filter(o => o.is_buy_order).sort((a, b) => b.price - a.price);
      const sellOrders = orders.filter(o => !o.is_buy_order).sort((a, b) => a.price - b.price);

      if (buyOrders.length > 0 && sellOrders.length > 0) {
        const spread = buyOrders[0].price - sellOrders[0].price;
        const spreadPercent = (spread / sellOrders[0].price) * 100;

        return {
          profitable: spread > 0,
          spread,
          spreadPercent,
          bestBuy: buyOrders[0],
          bestSell: sellOrders[0],
          dailyVolume: history[0]?.volume || 0
        };
      }

      return null;
    } catch (error) {
      console.error('Failed to analyze market:', error);
      return null;
    }
  }
}
```

### Corporation Management Dashboard (Custom Client)

```typescript
import { CustomEsiClient } from '@lgriffin/esi.ts';

class CorporationManager {
  private client: CustomEsiClient;

  constructor(accessToken: string) {
    // Only load corporation-related APIs
    this.client = new CustomEsiClient({
      clientId: 'corp-manager',
      accessToken,
      clients: ['corporations', 'characters', 'wallet']
    });
  }

  async getCorporationOverview(corporationId: number) {
    try {
      const [corp, members, wallets] = await Promise.all([
        this.client.corporations.getCorporationInfo(corporationId),
        this.client.corporations.getCorporationMembers(corporationId),
        this.client.wallet.getCorporationWallets(corporationId)
      ]);

      return {
        corporation: corp,
        memberCount: members.length,
        totalBalance: wallets.reduce((sum, wallet) => sum + wallet.balance, 0)
      };
    } catch (error) {
      if (error instanceof ApiError && error.type === ApiErrorType.AUTHENTICATION_ERROR) {
        throw new Error('Insufficient permissions to access corporation data');
      }
      throw error;
    }
  }
}
```

### Simple Character Lookup (Direct API)

```typescript
import { EsiApiFactory } from '@lgriffin/esi.ts';

// Ultra-lightweight: just one API, one function
async function lookupCharacter(characterId: number) {
  const characterClient = EsiApiFactory.createCharacterClient({
    clientId: 'simple-lookup'
  });

  const character = await characterClient.getCharacterPublicInfo(characterId);
  return character.body.name;
}

// Usage
const name = await lookupCharacter(1689391488);
console.log(name); // "deiseman"
```

### Direct API Class Usage

```typescript
import { CharacterClient, ApiClientBuilder } from '@lgriffin/esi.ts';

// Maximum control - build exactly what you need
const apiClient = new ApiClientBuilder()
  .setClientId('direct-usage')
  .setLink('https://esi.evetech.net')
  .build();

const characterClient = new CharacterClient(apiClient);

// Direct usage without any wrapper
const character = await characterClient.getCharacterPublicInfo(123456);
const portrait = await characterClient.getCharacterPortrait(123456);
```

### Microservice Example (Single Responsibility)

```typescript
import { EsiApiFactory } from '@lgriffin/esi.ts';

// A microservice that only needs market data
class PriceService {
  private marketClient;

  constructor() {
    // Only load what this service needs
    this.marketClient = EsiApiFactory.createMarketClient({
      clientId: 'price-service-v1'
    });
  }

  async getCurrentPrice(typeId: number): Promise<number> {
    const prices = await this.marketClient.getMarketPrices();
    const price = prices.body.find((p: any) => p.type_id === typeId);
    return price?.average_price || 0;
  }

  async getBestPrices(regionId: number, typeId: number) {
    const orders = await this.marketClient.getMarketOrders(regionId, { type_id: typeId });
    
    const buyOrders = orders.body.filter((o: any) => o.is_buy_order);
    const sellOrders = orders.body.filter((o: any) => !o.is_buy_order);
    
    return {
      bestBuy: Math.max(...buyOrders.map((o: any) => o.price)),
      bestSell: Math.min(...sellOrders.map((o: any) => o.price))
    };
  }
}
```

## 🧪 Testing

### Running Tests

```bash
# Run unit tests
npm test

# Run unit tests with coverage
npm run coverage

# Run BDD tests (behavioral scenarios)
npm run bdd

# Run specific BDD test suites
npm run bdd:alliance
npm run bdd:character
npm run bdd:market

# Run all tests
npm run test:all
```

## 🚀 Working Examples

### Try the Examples

ESI.ts includes working examples that demonstrate real API usage:

```bash
# Run the complete character profile example
npm run example

# Run flexible API usage examples (all 5 approaches)
npm run examples:flexible
```

### Character Profile Example

The main example (`npm run example`) demonstrates:
- ✅ Complete character profile assembly
- ✅ Parallel API calls for efficiency
- ✅ Error handling and graceful degradation
- ✅ Resource cleanup
- ✅ Performance timing

**Sample Output:**
```
🚀 ESI.ts Character Profile Example
=====================================

🔍 Gathering complete profile for character ID: 1689391488
📋 Fetching basic character information...
🚀 Fetching detailed profile data in parallel...

============================================================
🎯 CHARACTER PROFILE SUMMARY
============================================================
👤 Name: deiseman
🆔 Character ID: 1689391488
🎂 Birthday: 2/3/2008
⚖️  Security Status: 0.16

🏢 Corporation: Brittas Empire [BREMP]
👥 Members: 360
🤝 Alliance: Pandemic Horde [REKTD]
📊 Founded: 2/4/2015

🖼️  Portrait URLs:
   📱 64x64: https://images.evetech.net/characters/1689391488/portrait?tenant=tranquility&size=64
   🖥️  128x128: https://images.evetech.net/characters/1689391488/portrait?tenant=tranquility&size=128
   🖼️  256x256: https://images.evetech.net/characters/1689391488/portrait?tenant=tranquility&size=256
   📺 512x512: https://images.evetech.net/characters/1689391488/portrait?tenant=tranquility&size=512

📍 Current Location: Unavailable (character may be offline)
============================================================

⏱️  Total execution time: 154ms
✅ Character profile retrieved successfully!
```

### Flexible API Examples

The flexible examples (`npm run examples:flexible`) demonstrate:
- ✅ Full ESI Client (all APIs)
- ✅ Custom lightweight client (selected APIs)
- ✅ Builder pattern usage
- ✅ Individual API clients
- ✅ Direct API class instantiation
- ✅ Performance comparisons
- ✅ Microservice example

**Sample Output:**
```
🚀 ESI.ts Flexible API Usage Examples
=====================================

1️⃣  Full ESI Client (All APIs)
✅ Character: deiseman (using full client)

2️⃣  Custom Lightweight Client (Selected APIs)
✅ Character: deiseman (using custom client)
📊 Enabled clients: characters, corporations

3️⃣  Builder Pattern
✅ Character: deiseman (using builder pattern)

4️⃣  Individual API Client (Ultra Lightweight)
✅ Character: deiseman (using standalone client)

5️⃣  Direct API Class Instantiation
✅ Character: deiseman (using direct instantiation)

🎯 Performance Comparison
=========================
⏱️  Startup time comparison:
   Full Client: 1ms
   Custom Client (1 API): 0ms
   Individual Client: 0ms

💰 Microservice Example: Price Service
======================================
💎 Tritanium average price: 3.78 ISK
```

### Example Files

| File | Purpose | Command |
|------|---------|---------|
| `src/index.ts` | Character profile assembly | `npm run example` |
| `demo/flexible-examples.ts` | All flexible API patterns | `npm run examples:flexible` |

### Learning Path

1. **Start Here**: Run `npm run example` to see a complete real-world workflow
2. **Explore Options**: Run `npm run examples:flexible` to see all the different ways to use the API
3. **Choose Your Approach**: Pick the method that best fits your use case
4. **Build Your App**: Use the examples as templates for your own application

### Testing Your Applications

```typescript
import { EsiClient } from '@lgriffin/esi.ts';
import { TestDataFactory } from '@lgriffin/esi.ts';

describe('My EVE Application', () => {
  let client: EsiClient;

  beforeEach(() => {
    client = new EsiClient({
      clientId: 'test-client'
    });
  });

  afterEach(async () => {
    await client.shutdown();
  });

  it('should handle character lookup', async () => {
    // Mock data for testing
    jest.spyOn(client.characters, 'getCharacterPublicInfo')
      .mockResolvedValue(TestDataFactory.createCharacterInfo({
        character_id: 123456,
        name: 'Test Character'
      }));

    const character = await client.characters.getCharacterPublicInfo(123456);
    expect(character.name).toBe('Test Character');
  });
});
```

## 🛠️ Resource Management

### Proper Cleanup

```typescript
// Always clean up resources when done
async function myApplication() {
  const client = new EsiClient({
    clientId: 'my-app'
  });

  try {
    // Your application logic here
    const alliance = await client.alliance.getAllianceById(99005338);
    console.log(alliance.name);
  } finally {
    // Important: Always shutdown the client
    await client.shutdown();
  }
}

// Or use a try-with-resources pattern
class EsiClientManager {
  private client: EsiClient;

  constructor(config: any) {
    this.client = new EsiClient(config);
  }

  async use<T>(callback: (client: EsiClient) => Promise<T>): Promise<T> {
    try {
      return await callback(this.client);
    } finally {
      await this.client.shutdown();
    }
  }
}

// Usage
const manager = new EsiClientManager({ clientId: 'my-app' });
const result = await manager.use(async (client) => {
  return await client.alliance.getAllianceById(99005338);
});
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass: `npm test && npm run bdd`
5. Open a Pull Request

## 📄 License

GPL-3.0-or-later - see the [LICENSE](LICENSE) file for details.

---

**Happy coding, capsuleers! o7**
