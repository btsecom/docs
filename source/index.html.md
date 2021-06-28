---
title: BTSE Spot API
language_tabs:
  - shell: Shell
  - java: Java
  - python: Python
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v3.6.6 -->

<section>
<h1 id="btse-spot-api">BTSE Spot API v2.1</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

# Overview
## Generating API Key
You will need to create an API key on the BTSE platform before you can use authenticated APIs. To create API keys, you can follow the steps below:
1. Login with your username / email and password into the BTSE website
2. Click on “Account” on the top right hand corner
3. Select the API tab
4. Click on “New API” button to create an API key and passphrase. (Note: the passphrase will only appear once)
5. Use your API key and passphrase to construct a signature.

Base URLs:

* undefined - <a href="https://api.btse.com/spot">https://api.btse.com/spot</a>

* undefined - <a href="https://testapi.btse.io/spot">https://testapi.btse.io/spot</a>

</section>

<section>

# Authentication

* API Key (btse-sign)
    - Parameter Name: **btse-sign**, in: header. A composite signature produced based on the following algorithm: ```Signature=Sha384 (secretkey, (urlpath + btse-nonce + bodyStr))```

* API Key (btse-api)
    - Parameter Name: **btse-api**, in: header. API key is obtained from BTSE platform as a string

* API Key (btse-nonce)
    - Parameter Name: **btse-nonce**, in: header. Representation of current timestamp in long format

</section>

<section>
<h1 id="btse-spot-api-public-endpoints">Public Endpoints</h1>

<section>

## High level market overview

<a id="opIdgetMarketSummaryUsingGET_1"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.btse.com/spot/v2/market_summary \
  -H 'Accept: application/json'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/market_summary");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.btse.com/spot/v2/market_summary', params={

}, headers = headers)

print r.json()

```

`GET /v2/market_summary`

This API provides a high level overview of the market. Provides you with information such as the best bid/ask, price movements over the last day and volume information.

> Example responses

> 200 Response

```json
{
  "symbol": {
    "high24hr": "string",
    "highest_bid": "string",
    "last": "string",
    "low24hr": "string",
    "lowest_ask": "string",
    "percent_change": "string",
    "volume": "string"
  }
}
```

<section>
<h3 id="high-level-market-overview-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="high-level-market-overview-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» symbol|[MarketSummary](#schemamarketsummary)|false|none|none|
|»» high24hr|string|false|none|none|
|»» highest_bid|string|false|none|none|
|»» last|string|false|none|none|
|»» low24hr|string|false|none|none|
|»» lowest_ask|string|false|none|none|
|»» percent_change|string|false|none|none|
|»» volume|string|false|none|none|

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="success">
This operation does not require authentication
</aside>

</section>

<section>

## Market information

<a id="opIdgetMarkets"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.btse.com/spot/v2/markets \
  -H 'Accept: application/json'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/markets");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.btse.com/spot/v2/markets', params={

}, headers = headers)

print r.json()

```

`GET /v2/markets`

Gets information on the available markets

> Example responses

> 200 Response

```json
[
  {
    "base_currency": "string",
    "base_increment_size": 0,
    "base_max_size": 0,
    "base_min_size": 0,
    "id": "string",
    "quote_currency": "string",
    "quote_increment": 0,
    "quote_min_price": 0,
    "status": "string"
  }
]
```

<section>
<h3 id="market-information-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="market-information-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[MarketModel](#schemamarketmodel)]|false|none|none|
|» MarketModel|[MarketModel](#schemamarketmodel)|false|none|none|
|»» base_currency|string|false|none|none|
|»» base_increment_size|number(double)|false|none|none|
|»» base_max_size|number(double)|false|none|none|
|»» base_min_size|number(double)|false|none|none|
|»» id|string|false|none|none|
|»» quote_currency|string|false|none|none|
|»» quote_increment|number(double)|false|none|none|
|»» quote_min_price|number(double)|false|none|none|
|»» status|string|false|none|none|

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="success">
This operation does not require authentication
</aside>

</section>

<section>

## Gets Orderbook

<a id="opIdgetOrderBookUsingGET_1"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.btse.com/spot/v2/orderbook/{symbol} \
  -H 'Accept: application/json'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/orderbook/{symbol}");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.btse.com/spot/v2/orderbook/{symbol}', params={

}, headers = headers)

print r.json()

```

`GET /v2/orderbook/{symbol}`

Gets Orderbook for a given symbol

<section>
<h3 id="gets-orderbook-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|group|query|integer(int32)|false|Decimal grouping|
|limit_asks|query|integer(int32)|false|Restricts the depth of orderbook to return|
|limit_bids|query|integer(int32)|false|Restricts the depth of orderbook to return|
|symbol|path|string|true|Symbol representing the market|

</section>

> Example responses

> 200 Response

```json
{
  "buyQuote": [
    {
      "price": "string",
      "size": "string"
    }
  ],
  "sellQuote": [
    {
      "price": "string",
      "size": "string"
    }
  ],
  "symbol": "string",
  "timestamp": 0
}
```

<section>
<h3 id="gets-orderbook-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[OrderBookResponse](#schemaorderbookresponse)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="gets-orderbook-responseschema">Response Schema</h3>

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="success">
This operation does not require authentication
</aside>

</section>

<section>

## Ticker Information

<a id="opIdgetTicker"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.btse.com/spot/v2/ticker/{symbol} \
  -H 'Accept: application/json'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/ticker/{symbol}");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.btse.com/spot/v2/ticker/{symbol}', params={

}, headers = headers)

print r.json()

```

`GET /v2/ticker/{symbol}`

Retrieves bid, asks, and other information of the ticker

<section>
<h3 id="ticker-information-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|symbol|path|string|true|symbol|

</section>

> Example responses

> 200 Response

```json
{
  "ask": "string",
  "bid": "string",
  "price": "string",
  "size": "string",
  "time": "string",
  "volume": "string"
}
```

<section>
<h3 id="ticker-information-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[TickerModel](#schematickermodel)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="ticker-information-responseschema">Response Schema</h3>

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="success">
This operation does not require authentication
</aside>

</section>

<section>

## Gets market statistics

<a id="opIdHour24StatsUsingGET_1"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.btse.com/spot/v2/stats/{symbol} \
  -H 'Accept: application/json'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/stats/{symbol}");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.btse.com/spot/v2/stats/{symbol}', params={

}, headers = headers)

print r.json()

```

`GET /v2/stats/{symbol}`

Gets market statistics over the past 24hours

<section>
<h3 id="gets-market-statistics-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|symbol|path|string|true|symbol|

</section>

> Example responses

> 200 Response

```json
{
  "close": "string",
  "high": "string",
  "low": "string",
  "open": "string",
  "time": "string",
  "volume": "string"
}
```

<section>
<h3 id="gets-market-statistics-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[Hour24Stats](#schemahour24stats)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="gets-market-statistics-responseschema">Response Schema</h3>

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="success">
This operation does not require authentication
</aside>

</section>

<section>

## Gets list of recent trades

<a id="opIdapiTradeHistoryUsingGET_1"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.btse.com/spot/v2/trades/{symbol} \
  -H 'Accept: application/json'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/trades/{symbol}");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.btse.com/spot/v2/trades/{symbol}', params={

}, headers = headers)

print r.json()

```

`GET /v2/trades/{symbol}`

Gets list of most recent trades for a given symbol

<section>
<h3 id="gets-list-of-recent-trades-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|symbol|path|string|true|Symbol representing the market|

</section>

> Example responses

> 200 Response

```json
[
  {
    "amount": 0,
    "price": 0,
    "serial_id": "string",
    "symbol": "string",
    "time": "string",
    "type": "string"
  }
]
```

<section>
<h3 id="gets-list-of-recent-trades-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="gets-list-of-recent-trades-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[TradeModel](#schematrademodel)]|false|none|none|
|» TradeModel|[TradeModel](#schematrademodel)|false|none|none|
|»» amount|number(double)|false|none|none|
|»» price|number(double)|false|none|none|
|»» serial_id|string|false|none|none|
|»» symbol|string|false|none|none|
|»» time|string|false|none|none|
|»» type|string|false|none|none|

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="success">
This operation does not require authentication
</aside>

</section>

<section>

## Get Server time

<a id="opIdgetServerTimeUsingGET_1"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.btse.com/spot/v2/time \
  -H 'Accept: application/json'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/time");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.btse.com/spot/v2/time', params={

}, headers = headers)

print r.json()

```

`GET /v2/time`

Get Server time

> Example responses

> 200 Response

```json
{
  "iso": "string",
  "epoch": 0
}
```

<section>
<h3 id="get-server-time-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="get-server-time-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» iso|string|false|none|Date timestamp|
|» epoch|number|false|none|Long timestamp|

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="success">
This operation does not require authentication
</aside>

</section>

</section>

<section>
<h1 id="btse-spot-api-authenticated-endpoints">Authenticated Endpoints</h1>

<section>

## Get Account Information

<a id="opIdgetAccountUsingGET_1"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.btse.com/spot/v2/account \
  -H 'Accept: application/json' \
  -H 'btse-api: API_KEY'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/account");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Accept': 'application/json',
  'btse-api': 'API_KEY'
}

r = requests.get('https://api.btse.com/spot/v2/account', params={

}, headers = headers)

print r.json()

```

`GET /v2/account`

Get account information and balances

> Example responses

> 200 Response

```json
[
  {
    "available": "string",
    "currency": "string",
    "total": "string"
  }
]
```

<section>
<h3 id="get-account-information-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="get-account-information-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[ApiAccountModel](#schemaapiaccountmodel)]|false|none|none|
|» ApiAccountModel|[ApiAccountModel](#schemaapiaccountmodel)|false|none|none|
|»» available|string|false|none|none|
|»» currency|string|false|none|none|
|»» total|string|false|none|none|

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
btse-api, btse-sign, btse-nonce
</aside>

</section>

<section>

## Order Placement

<a id="opIdplaceAnOrderUsingPOST_1"></a>

> Code samples

```shell
# You can also use wget
curl -X POST https://api.btse.com/spot/v2/order \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'btse-api: API_KEY'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/order");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'btse-api': 'API_KEY'
}

r = requests.post('https://api.btse.com/spot/v2/order', params={

}, headers = headers)

print r.json()

```

`POST /v2/order`

Sends Limit orders to BTSE

> Body parameter

```json
{
  "amount": 0,
  "client_oid": 0,
  "created_at": 0,
  "funds": 0,
  "id": "string",
  "post_only": true,
  "price": 0,
  "symbol": "string",
  "side": "string",
  "status": "string",
  "stop": "string",
  "stop_price": 0,
  "stp": "string",
  "tag": "string",
  "time_in_force": "string",
  "type": "string"
}
```

<section>
<h3 id="order-placement-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[ApiOrderModel](#schemaapiordermodel)|true|apiOrderModel|

</section>

> Example responses

> 200 Response

```json
{
  "id": "string"
}
```

<section>
<h3 id="order-placement-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="order-placement-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» id|string|false|none|none|

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
btse-api, btse-sign, btse-nonce
</aside>

</section>

<section>

## Gets pending orders

<a id="opIdgetPendingOrderUsingGET_1"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.btse.com/spot/v2/pending \
  -H 'Accept: application/json' \
  -H 'btse-api: API_KEY'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/pending");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Accept': 'application/json',
  'btse-api': 'API_KEY'
}

r = requests.get('https://api.btse.com/spot/v2/pending', params={

}, headers = headers)

print r.json()

```

`GET /v2/pending`

Gets all pending orders for the market

<section>
<h3 id="gets-pending-orders-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|symbol|query|string|false|symbol|

</section>

> Example responses

> 200 Response

```json
[
  {
    "amount": 0,
    "created_at": "string",
    "id": "string",
    "price": 0,
    "symbol": "string",
    "side": 0,
    "status": "string",
    "tag": "string",
    "type": 0
  }
]
```

<section>
<h3 id="gets-pending-orders-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="gets-pending-orders-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[PendingOrderModel](#schemapendingordermodel)]|false|none|none|
|» PendingOrderModel|[PendingOrderModel](#schemapendingordermodel)|false|none|none|
|»» amount|number(double)|false|none|none|
|»» created_at|string|false|none|none|
|»» id|string|false|none|none|
|»» price|number(double)|false|none|none|
|»» symbol|string|false|none|none|
|»» side|integer(int32)|false|none|none|
|»» status|string|false|none|none|
|»» tag|string|false|none|none|
|»» type|integer(int32)|false|none|none|

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
btse-api, btse-sign, btse-nonce
</aside>

</section>

<section>

## Get order fills

<a id="opIdgetFillsUsingPOST"></a>

> Code samples

```shell
# You can also use wget
curl -X POST https://api.btse.com/spot/v2/fills \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'btse-api: API_KEY'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/fills");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'btse-api': 'API_KEY'
}

r = requests.post('https://api.btse.com/spot/v2/fills', params={

}, headers = headers)

print r.json()

```

`POST /v2/fills`

Get order fills

> Body parameter

```json
{
  "after": 0,
  "before": 0,
  "limit": 0,
  "order_id": "string",
  "symbol": "string",
  "username": "string"
}
```

<section>
<h3 id="get-order-fills-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[FillQueryModel](#schemafillquerymodel)|true|fillQueryModel|

</section>

> Example responses

> 200 Response

```json
[
  {
    "amount": 0,
    "created_at": "yyyy-MM-dd HH:mm:ss",
    "fee": 0,
    "id": 0,
    "order_id": "string",
    "price": 0,
    "symbol": "string",
    "side": "string",
    "tag": "string",
    "trade_id": "string"
  }
]
```

<section>
<h3 id="get-order-fills-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="get-order-fills-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[FillModel](#schemafillmodel)]|false|none|none|
|» FillModel|[FillModel](#schemafillmodel)|false|none|none|
|»» amount|number(double)|false|none|none|
|»» created_at|string|false|none|none|
|»» fee|number(double)|false|none|none|
|»» id|integer(int64)|false|none|none|
|»» order_id|string|false|none|none|
|»» price|number(double)|false|none|none|
|»» symbol|string|false|none|none|
|»» side|string|false|none|none|
|»» tag|string|false|none|none|
|»» trade_id|string|false|none|none|

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
btse-api, btse-sign, btse-nonce
</aside>

</section>

<section>

## Cancel order

<a id="opIdcancelOrderUsingPOST"></a>

> Code samples

```shell
# You can also use wget
curl -X POST https://api.btse.com/spot/v2/deleteOrder \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'btse-api: API_KEY'

```

```java
URL obj = new URL("https://api.btse.com/spot/v2/deleteOrder");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'btse-api': 'API_KEY'
}

r = requests.post('https://api.btse.com/spot/v2/deleteOrder', params={

}, headers = headers)

print r.json()

```

`POST /v2/deleteOrder`

Cancel order

> Body parameter

```json
{
  "coin_name": "string",
  "order_id": "string",
  "symbol": "string"
}
```

<section>
<h3 id="cancel-order-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[CancelOrderModel](#schemacancelordermodel)|true|none|

</section>

> Example responses

> 200 Response

```json
[
  {
    "code": 0,
    "data": {},
    "msg": "string",
    "success": true,
    "time": 0
  }
]
```

<section>
<h3 id="cancel-order-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|
|503|[Service Unavailable](https://tools.ietf.org/html/rfc7231#section-6.6.4)|Service Unavailable|Inline|

<h3 id="cancel-order-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[ReturnResult](#schemareturnresult)]|false|none|none|
|» ReturnResult|[ReturnResult](#schemareturnresult)|false|none|none|
|»» code|integer(int32)|false|none|none|
|»» data|object|false|none|none|
|»» msg|string|false|none|none|
|»» success|boolean|false|none|none|
|»» time|integer(int64)|false|none|none|

Status Code **400**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **401**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **403**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **500**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

Status Code **503**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer(int32)|false|none|none|
|» errorCode|integer(int32)|false|none|none|
|» message|string|false|none|none|

</section>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
btse-api, btse-sign, btse-nonce
</aside>

</section>

</section>

<section>

# Schemas

<section>
<h2 id="tocS_TickerModel">TickerModel</h2>
<!-- backwards compatibility -->
<a id="schematickermodel"></a>
<a id="schema_TickerModel"></a>
<a id="tocStickermodel"></a>
<a id="tocstickermodel"></a>

```json
{
  "ask": "string",
  "bid": "string",
  "price": "string",
  "size": "string",
  "time": "string",
  "volume": "string"
}

```

TickerModel

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|ask|string|false|none|none|
|bid|string|false|none|none|
|price|string|false|none|none|
|size|string|false|none|none|
|time|string|false|none|none|
|volume|string|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_ApiAccountModel">ApiAccountModel</h2>
<!-- backwards compatibility -->
<a id="schemaapiaccountmodel"></a>
<a id="schema_ApiAccountModel"></a>
<a id="tocSapiaccountmodel"></a>
<a id="tocsapiaccountmodel"></a>

```json
{
  "available": "string",
  "currency": "string",
  "total": "string"
}

```

ApiAccountModel

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|available|string|false|none|none|
|currency|string|false|none|none|
|total|string|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_ApiOrderModel">ApiOrderModel</h2>
<!-- backwards compatibility -->
<a id="schemaapiordermodel"></a>
<a id="schema_ApiOrderModel"></a>
<a id="tocSapiordermodel"></a>
<a id="tocsapiordermodel"></a>

```json
{
  "amount": 0,
  "client_oid": 0,
  "created_at": 0,
  "funds": 0,
  "id": "string",
  "post_only": true,
  "price": 0,
  "symbol": "string",
  "side": "string",
  "status": "string",
  "stop": "string",
  "stop_price": 0,
  "stp": "string",
  "tag": "string",
  "time_in_force": "string",
  "type": "string"
}

```

ApiOrderModel

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|amount|number|false|none|none|
|client_oid|integer(int64)|false|none|none|
|created_at|integer(int64)|false|none|none|
|funds|number|false|none|none|
|id|string|false|none|none|
|post_only|boolean|false|none|none|
|price|number|false|none|none|
|symbol|string|false|none|none|
|side|string|false|none|none|
|status|string|false|none|none|
|stop|string|false|none|none|
|stop_price|number|false|none|none|
|stp|string|false|none|none|
|tag|string|false|none|none|
|time_in_force|string|false|none|none|
|type|string|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_FillModel">FillModel</h2>
<!-- backwards compatibility -->
<a id="schemafillmodel"></a>
<a id="schema_FillModel"></a>
<a id="tocSfillmodel"></a>
<a id="tocsfillmodel"></a>

```json
{
  "amount": 0,
  "created_at": "yyyy-MM-dd HH:mm:ss",
  "fee": 0,
  "id": 0,
  "order_id": "string",
  "price": 0,
  "symbol": "string",
  "side": "string",
  "tag": "string",
  "trade_id": "string"
}

```

FillModel

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|amount|number(double)|false|none|none|
|created_at|string|false|none|none|
|fee|number(double)|false|none|none|
|id|integer(int64)|false|none|none|
|order_id|string|false|none|none|
|price|number(double)|false|none|none|
|symbol|string|false|none|none|
|side|string|false|none|none|
|tag|string|false|none|none|
|trade_id|string|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_Hour24Stats">Hour24Stats</h2>
<!-- backwards compatibility -->
<a id="schemahour24stats"></a>
<a id="schema_Hour24Stats"></a>
<a id="tocShour24stats"></a>
<a id="tocshour24stats"></a>

```json
{
  "close": "string",
  "high": "string",
  "low": "string",
  "open": "string",
  "time": "string",
  "volume": "string"
}

```

Hour24Stats

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|close|string|false|none|none|
|high|string|false|none|none|
|low|string|false|none|none|
|open|string|false|none|none|
|time|string|false|none|none|
|volume|string|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_CancelOrderModel">CancelOrderModel</h2>
<!-- backwards compatibility -->
<a id="schemacancelordermodel"></a>
<a id="schema_CancelOrderModel"></a>
<a id="tocScancelordermodel"></a>
<a id="tocscancelordermodel"></a>

```json
{
  "coin_name": "string",
  "order_id": "string",
  "symbol": "string"
}

```

CancelOrderModel

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|coin_name|string|false|none|none|
|order_id|string|false|none|none|
|symbol|string|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_FillQueryModel">FillQueryModel</h2>
<!-- backwards compatibility -->
<a id="schemafillquerymodel"></a>
<a id="schema_FillQueryModel"></a>
<a id="tocSfillquerymodel"></a>
<a id="tocsfillquerymodel"></a>

```json
{
  "after": 0,
  "before": 0,
  "limit": 0,
  "order_id": "string",
  "symbol": "string",
  "username": "string"
}

```

FillQueryModel

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|after|integer(int64)|false|none|none|
|before|integer(int64)|false|none|none|
|limit|integer(int32)|false|none|none|
|order_id|string|false|none|none|
|symbol|string|false|none|none|
|username|string|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_PendingOrderModel">PendingOrderModel</h2>
<!-- backwards compatibility -->
<a id="schemapendingordermodel"></a>
<a id="schema_PendingOrderModel"></a>
<a id="tocSpendingordermodel"></a>
<a id="tocspendingordermodel"></a>

```json
{
  "amount": 0,
  "created_at": "string",
  "id": "string",
  "price": 0,
  "symbol": "string",
  "side": 0,
  "status": "string",
  "tag": "string",
  "type": 0
}

```

PendingOrderModel

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|amount|number(double)|false|none|none|
|created_at|string|false|none|none|
|id|string|false|none|none|
|price|number(double)|false|none|none|
|symbol|string|false|none|none|
|side|integer(int32)|false|none|none|
|status|string|false|none|none|
|tag|string|false|none|none|
|type|integer(int32)|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_ReturnResult">ReturnResult</h2>
<!-- backwards compatibility -->
<a id="schemareturnresult"></a>
<a id="schema_ReturnResult"></a>
<a id="tocSreturnresult"></a>
<a id="tocsreturnresult"></a>

```json
{
  "code": 0,
  "data": {},
  "msg": "string",
  "success": true,
  "time": 0
}

```

ReturnResult

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|code|integer(int32)|false|none|none|
|data|object|false|none|none|
|msg|string|false|none|none|
|success|boolean|false|none|none|
|time|integer(int64)|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_Quote">Quote</h2>
<!-- backwards compatibility -->
<a id="schemaquote"></a>
<a id="schema_Quote"></a>
<a id="tocSquote"></a>
<a id="tocsquote"></a>

```json
{
  "price": "string",
  "size": "string"
}

```

Quote

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|price|string|false|none|none|
|size|string|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_OrderBookResponse">OrderBookResponse</h2>
<!-- backwards compatibility -->
<a id="schemaorderbookresponse"></a>
<a id="schema_OrderBookResponse"></a>
<a id="tocSorderbookresponse"></a>
<a id="tocsorderbookresponse"></a>

```json
{
  "buyQuote": [
    {
      "price": "string",
      "size": "string"
    }
  ],
  "sellQuote": [
    {
      "price": "string",
      "size": "string"
    }
  ],
  "symbol": "string",
  "timestamp": 0
}

```

OrderBookResponse

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|buyQuote|[[Quote](#schemaquote)]|false|none|none|
|sellQuote|[[Quote](#schemaquote)]|false|none|none|
|symbol|string|false|none|none|
|timestamp|integer(int64)|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_TradeModel">TradeModel</h2>
<!-- backwards compatibility -->
<a id="schematrademodel"></a>
<a id="schema_TradeModel"></a>
<a id="tocStrademodel"></a>
<a id="tocstrademodel"></a>

```json
{
  "amount": 0,
  "price": 0,
  "serial_id": "string",
  "symbol": "string",
  "time": "string",
  "type": "string"
}

```

TradeModel

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|amount|number(double)|false|none|none|
|price|number(double)|false|none|none|
|serial_id|string|false|none|none|
|symbol|string|false|none|none|
|time|string|false|none|none|
|type|string|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_MarketModel">MarketModel</h2>
<!-- backwards compatibility -->
<a id="schemamarketmodel"></a>
<a id="schema_MarketModel"></a>
<a id="tocSmarketmodel"></a>
<a id="tocsmarketmodel"></a>

```json
{
  "base_currency": "string",
  "base_increment_size": 0,
  "base_max_size": 0,
  "base_min_size": 0,
  "id": "string",
  "quote_currency": "string",
  "quote_increment": 0,
  "quote_min_price": 0,
  "status": "string"
}

```

MarketModel

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|base_currency|string|false|none|none|
|base_increment_size|number(double)|false|none|none|
|base_max_size|number(double)|false|none|none|
|base_min_size|number(double)|false|none|none|
|id|string|false|none|none|
|quote_currency|string|false|none|none|
|quote_increment|number(double)|false|none|none|
|quote_min_price|number(double)|false|none|none|
|status|string|false|none|none|

</section>
</section>

<section>
<h2 id="tocS_MarketSummary">MarketSummary</h2>
<!-- backwards compatibility -->
<a id="schemamarketsummary"></a>
<a id="schema_MarketSummary"></a>
<a id="tocSmarketsummary"></a>
<a id="tocsmarketsummary"></a>

```json
{
  "high24hr": "string",
  "highest_bid": "string",
  "last": "string",
  "low24hr": "string",
  "lowest_ask": "string",
  "percent_change": "string",
  "volume": "string"
}

```

MarketSummary

<section>

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|high24hr|string|false|none|none|
|highest_bid|string|false|none|none|
|last|string|false|none|none|
|low24hr|string|false|none|none|
|lowest_ask|string|false|none|none|
|percent_change|string|false|none|none|
|volume|string|false|none|none|

</section>
</section>

