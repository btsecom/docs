---
title: BTSE API Documentation
language_tabs:
  - json
toc_footers: []
includes: []
search: true
highlight_theme: darkula
code_clipboard: true
headingLevel: 2

---

# Change Log

## Version 1.0.0 (10th July 2025)

* Release V2.3 API. This change will take effect on 16th July, 2025.

# Overview

## Migration from v3.2 to v3.3

We are updating several order-related API endpoints to improve consistency and clarity in size-related fields. Please review the following changes carefully, as some existing fields will be deprecated and replaced with new ones.

### Updated Fields for Order Actions 

For the following endpoints, the fields `size`, `fillSize`, `originalSize` and `remainingSize` will be deprecated and replaced with the following:

  * `originalOrderBaseSize`
  * `originalOrderQuoteSize`
  * `currentOrderBaseSize`
  * `currentOrderQuoteSize`
  * `remainingOrderBaseSize`
  * `remainingOrderQuoteSize`
  * `filledBaseSize`
  * `totalFilledBaseSize`
  * `orderCurrency` ("base" or "quote")

**Affected Endpoints**

  * [`Create New Order`](#create-new-order)
    * Both `POST /api/v3.3/order` and `POST /api/v3.3/order/peg`
  * [`Amend Order`](#amend-order)
  * [`Cancel Order`](#cancel-order)

### Updated Fields for Order Query Endpoints 

To improve data structure clarity and consistency, the following legacy fields will be deprecated:

  * `size`
  * `filledSize`
  * `remainingSize` 
  * In some endpoints: `fillSize` as well

They will be replaced with the following enhanced fields:

  * `originalOrderBaseSize`
  * `originalOrderQuoteSize`
  * `currentOrderBaseSize`
  * `currentOrderQuoteSize`
  * `remainingOrderBaseSize`
  * `remainingOrderQuoteSize`
  * `totalFilledBaseSize`
  * `orderCurrency` ("base" or "quote")

**Affected Endpoints**

  * [`Query Order`](#query-order) - Replacing `size`, `filledSize`, `remainingSize` 
  * [`Query Open Orders`](#query-open-orders) - Replacing `size`, `fillSize`, `filledSize`, `remainingSize` 


## Generating API Key

You will need to create an API key on the BTSE platform before you can use authenticated APIs. To create API keys, you can follow the steps below:

* Login with your username / email and password into the BTSE website
* Click on `Account` on the top right hand corner
* Select the API tab
* Click on `New API` button to create an API key and passphrase. (Note: the passphrase will only appear once)
* Use your API key and passphrase to construct a signature.

## Endpoints

* Production
  * HTTP
     * `https://api.btse.com/spot`
  * Websocket
     * `wss://ws.btse.com/ws/spot`
  * Websocket (for orderbook stream)
     * `wss://ws.btse.com/ws/oss/spot` (Used for Orderbook incremental update stream)
* Testnet
  * HTTP
     * `https://testapi.btse.io/spot`
  * Websocket
     * `wss://testws.btse.io/ws/spot`
  * Websocket (for orderbook stream)
     * `wss://testws.btse.io/ws/oss/spot` (Used for Orderbook incremental update stream)

## Authentication

* API Key (request-api)
  * Parameter Name: `request-api`, in: header. API key is obtained from BTSE platform as a String

* API Key (request-nonce)
  * Parameter Name: `request-nonce`, in: header. Representation of current timestamp in Long format

* API Key (request-sign)
  * Parameter Name: `request-sign`, in: header. A composite signature produced based on the following algorithm: Signature=HMAC.Sha384 (secretkey, (urlpath + request-nonce + bodyStr)) (note: bodyStr = '' when no data):

### Example 1: Place an order

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v3.3/order1624985375123{\"postOnly\":false,\"price\":8500.0,\"side\":\"BUY\",\"size\":0.002,\"stopPrice\":0.0,\"symbol\":\"BTC-USD\",\"time_in_force\":\"GTC\",\"trailValue\":0.0,\"triggerPrice\":0.0,\"txType\":\"LIMIT\",\"type\":\"LIMIT\"}" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)=e9cd0babdf497b536d1e48bc9cf1fadad3426b36406b5747d77ae4e3cdc9ab556863f2d0cf78e0228c39a064ad43afb7
```

* Endpoint to place an order is `https://api.btse.com/spot/api/v3.3/order`
* Assume we have the values as follows:
  * request-nonce: `1624985375123`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v3.3/order`
  * Body: `{"postOnly":false,"price":8500.0,"side":"BUY","size":0.002,"stopPrice":0.0,"symbol":"BTC-USD","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
  * Encrypted Text: `/api/v3.3/order1624985375123{"postOnly":false,"price":8500.0,"side":"BUY","size":0.002,"stopPrice":0.0,"symbol":"BTC-USD","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
* Generated signature will be:
  * request-sign: `e9cd0babdf497b536d1e48bc9cf1fadad3426b36406b5747d77ae4e3cdc9ab556863f2d0cf78e0228c39a064ad43afb7`

## Rate Limits

* The following rate limits are enforced:

Rate limits for BTSE is as follows:

**Query**

* Per API: `15 requests/second`
* Per User: `30 requests/second`

**Orders**

* Per API: `75 requests/second`
* Per User: `75 requests/second`

### Mechanism Description

Our system implements a tiered blocking mechanism with three distinct durations: **1 second**, **5 minutes**, and **15 minutes**. The duration of the block begins calculation from the moment the first block is imposed.
Additionally, the calculation duration will be reset if the IP address or user does not exceed the rate limit within a span of 1 hour or the 15 mins blocking duration is ended.

A `Retry-After` header is included with a 429 response and will give the unlocked timestamp.

#### Rate limit tiers

* 1 sec
* 5 min
* 15 min

## API Status Codes

Each API will return one of the following HTTP status:

* 200 - API request was successful, refer to the specific API response for expected payload
* 400 - Bad Request. Server will not process this request. This is usually due to invalid parameters sent in request
* 401 - Unauthorized request. Server will not process this request as it does not have valid authentication credentials
* 403 - Forbidden request. Credentials were provided but they were insufficient to perform the request
* 404 - Not found. Indicates that the server understood the request but could not find a correct representation for the target resource
* 405 - Method not allowed. Indicates that the request method is not known to the requested server
* 408 - Request timeout. Indicates that the server did not complete the request. BTSE API timeouts are set at 30secs
* 429 - Too many requests. Indicates that the client has exceeded the rates limits set by the server. Refer to Rate Limits for more details
* 500 - Internal server error. Indicates that the server encountered an unexpected condition resulting in not being able to fulfill the request

## API Enum

When connecting up the BTSE API, you will come across Double codes that represents different states or status types in BTSE. The following section provides a list of codes that you are expecting to see.

* -1: TIMEOUT= Request timeout, please check the order status
* 1: MARKET_UNAVAILABLE = Futures market is unavailable
* 2: ORDER_INSERTED = Order is inserted successfully
* 4: ORDER_FULLY_TRANSACTED = Order is fully transacted
* 5: ORDER_PARTIALLY_TRANSACTED = Order is partially transacted
* 6: ORDER_CANCELLED = Order is cancelled successfully
* 7: ORDER_REFUNDED = Order is refunded
* 8: INSUFFICIENT_BALANCE = Insufficient balance in account
* 9: TRIGGER_INSERTED = Trigger Order is inserted successfully
* 10: TRIGGER_ACTIVATED = Trigger Order is activated successfully
* 11: ERROR_INVALID_CURRENCY
* 12: ERROR_UPDATE_RISK_LIMIT = Error in updating risk limit
* 13: ERROR_INVALID_LEVERAGE
* 15: ORDER_REJECTED = Order is rejected
* 16: ORDER_NOTFOUND = Order is not found with the order ID or clOrderID provided
* 17: REQUEST_FAILED = Failed to complete the request, please check order status
* 20: SUCCESS = Action succeeded.
* 21: FREEZE_SUCCESSFUL
* 27: TRANSFER_SUCCESSFUL = Transfer funds between futures and spot is successful
* 28: TRANSFER_UNSUCCESSFUL = Transfer funds between spot and futures is unsuccessful
* 29: QUERY_GET_ORDERS
* 31: QUERY_GET_POSITIONS
* 33: QUERY_GET_ALL_POSITIONS_ORDERS
* 34: QUERY_WALLET
* 36: QUERY_FUTURES_MARGIN
* 41: ERROR_INVALID_RISK_LIMIT = Invalid risk limit was specified
* 51: QUERY_GET_ORDERS_WITH_LIMIT
* 64: STATUS_LIQUIDATION = Account is undergoing liquidation
* 65: STATUS_ACITVE = Order is active
* 66: MODE_BUY
* 76: ORDER_TYPE_LIMIT = Limit order
* 77: ORDER_TYPE_MARKET = Market order
* 80: ORDER_TYPE_PEG = Peg/Algo order
* 81: ORDER_TYPE_OTC = Otc order
* 83: MODE_SELL
* 85: STATUS_PROCESSING = Order is inactive
* 88: STATUS_INACTIVE = Order is inactive
* 101: FUTURES_ORDER_PRICE_OUTSIDE_LIQUIDATION_PRICE = Futures order is outside of liquidation price
* 110: FUTURES_FUNDING
* 123: AMEND_ORDER = Order amended
* 124: UNFREEZE_SUCCESSFUL
* 300: ERROR_MAX_ORDER_SIZE_EXCEEDED
* 301: ERROR_INVALID_ORDER_SIZE
* 302: ERROR_INVALID_ORDER_PRICE
* 303: ERROR_RATE_LIMITS_EXCEEDED
* 304: ERROR_MAX_OPEN_ORDER_EXCEEDED
* 1003: ORDER_LIQUIDATION = Order is undergoing liquidation
* 1004: ORDER_ADL = Order is undergoing ADL
* 30410: BLOCK_TRADE_COMPLETE_SUCCESS


# Public Endpoints

## Market Summary

> Response

```json
[
  {
    "symbol": "BTC-USD",
    "last": 36976,
    "lowestAsk": 37012,
    "highestBid": 36972,
    "percentageChange": -4.633438649,
    "volume": 81456627.51106991,
    "high24Hr": 39478.5,
    "low24Hr": 36821.5,
    "base": "BTC",
    "quote": "USD",
    "active": true,
    "size": 2117.88522,
    "minValidPrice": 0.01,
    "minPriceIncrement": 0.5,
    "minOrderSize": 0.00001,
    "maxOrderSize": 2000,
    "minSizeIncrement": 0.00001,
    "openInterest": 0,
    "openInterestUSD": 0,
    "contractStart": 0,
    "contractEnd": 0,
    "timeBasedContract": false,
    "openTime": 0,
    "closeTime": 0,
    "startMatching": 0,
    "inactiveTime": 0,
    "fundingRate": 0,
    "contractSize": 0,
    "maxPosition": 0,
    "minRiskLimit": 0,
    "maxRiskLimit": 0,
    "availableSettlement": null,
    "futures": false,
    "isMarketOpenToOtc": false,
    "isMarketOpenToSpot": true
  }
]
```

`GET /api/v3.3/market_summary`

Gets market summary information. If no symbol parameter is sent, then all markets will be retrieved.

### Request Parameters

| name     | type     | required   | description     |
| -------- | -------- | ---------- | --------------- |
| symbol   | String   | no         | market symbol   |

### Response Content

| Name                | Type     | Required   | Description                                                 |
| ------------------  | -------- | ---------- | -------------                                               |
| symbol              | String   | Yes        | Market symbol                                               |
| last                | Double   | Yes        | Last price                                                  |
| lowestAsk           | Double   | Yes        | Lowest ask price in the orderbook                           |
| highestBid          | Double   | Yes        | Highest bid price in the orderbook                          |
| percentageChange    | Double   | Yes        | Percentage change against the price within the last 24hours |
| volume              | Double   | Yes        | Transacted volume                                           |
| high24Hr            | Double   | Yes        | Highest price over the last 24hours                         |
| low24Hr             | Double   | Yes        | Lowest price over the last 24hours                          |
| base                | String   | Yes        | Base currency                                               |
| quote               | String   | Yes        | Quote currency                                              |
| active              | Boolean  | Yes        | Indicator if market is active                               |
| size                | Double   | Yes        | Transacted size                                             |
| minValidPrice       | Double   | Yes        | Minimum valid price                                         |
| minPriceIncrement   | Double   | Yes        | Price increment                                             |
| minOrderSize        | Double   | Yes        | Minimum tick size                                           |
| minSizeIncrement    | Double   | Yes        | Tick size                                                   |
| maxOrderSize        | Double   | Yes        | Maximum order size                                          |
| openInterest        | Double   | No         | Not valid for spot                                          |
| openInterestUSD     | Double   | No         | Not valid for spot                                          |
| contractStart       | date     | No         | Not valid for spot                                          |
| contractEnd         | date     | No         | Not valid for spot                                          |
| timeBasedContract   | Boolean  | No         | Not valid for spot                                          |
| openTime            | date     | Yes        | Market opening time                                         |
| closeTime           | date     | Yes        | Market closing time                                         |
| startMatching       | date     | Yes        | Matching start time                                         |
| inactiveTime        | date     | Yes        | Time where market is inactive                               |
| fundingRate         | Double   | No         | Not valid for spot                                          |
| contractSize        | Double   | No         | Not valid for spot                                          |
| maxPosition         | Double   | No         | Not valid for spot                                          |
| minRiskLimit        | Double   | No         | Not valid for spot                                          |
| maxRiskLimit        | Double   | No         | Not valid for spot                                          |
| availableSettlement | Array    | No         | Not valid for spot                                          |
| futures             | Boolean  | Yes        | Indicator if symbol is a futures contract                   |
| isMarketOpenToOtc   | Boolean  | Yes        | Indicator if market is open to otc                          |
| isMarketOpenToSpot  | Boolean  | Yes        | Indicator if market is open to spot                         |

## Charting Data

> Response

```json
[
  [
    1624987380,
    36477,
    36477,
    36473.5,
    36473.5,
    693.049
  ],
  [
    1624987320,
    36476.5,
    36481.5,
    36466,
    36466,
    2370.8095
  ]
]
```

`GET /api/v3.3/ohlcv`

Gets candle stick charting data. Default of 300 data points will be returned at any one time.

### Request Parameters

| name       | type   | required | description                                                                                                                         |
| ---        | ---    | ---      | ---                                                                                                                                 |
| symbol     | String | yes      | market symbol                                                                                                                       |
| start      | Long   | no       | starting time in milliseconds (eg. 1624987283000)                                                                                   |
| end        | Long   | no       | ending time in milliseconds (eg. 1624987283000)                                                                                     |
| resolution | String | yes      | supported resolutions are: <br/> 1: 1 min<br/> 5: 5 mins<br/> 15: 15 mins<br/>30: 30 mins<br/>60: 60 mins<br/>240: 4 hours<br/>360: 6 hours<br/>1440: 1day<br/>10080: 1 week<br/>43200: 1 month |


### Response Content

Returns a 2D array with the indexes described in the table below

| Index | Type   | Required | Description   |
| ---   | ---    | ---      | ---           |
| 0     | Long   | Yes      | Unix time     |
| 1     | Double | Yes      | Open price    |
| 2     | Double | Yes      | High Price    |
| 3     | Double | Yes      | Low price     |
| 4     | Double | Yes      | Closing price |
| 5     | Double | Yes      | Volume        |


## Query Market price

> Response

```json
[
  {
    "symbol": "BTC-USD",
    "indexPrice": 36288.949684967,
    "lastPrice": 36286.5,
    "markPrice": 0
  }
]
```

`GET /api/v3.3/price`

Retrieve current prices on the platform. If no symbol specified, all symbols will be returned.

### Request Parameters

| Name   | Type   | Required | Description   |
| ---    | ---    | ---      | ---           |
| symbol | String | Yes      | Market symbol |


### Response Content

| Name       | Type   | Required | Description           |
| ---        | ---    | ---      | ---                   |
| symbol     | Double | Yes      | Market symbol         |
| indexPrice | Double | Yes      | Index price           |
| lastPrice  | Double | Yes      | Last transacted price |
| markPrice  | Double | Yes      | Not valid for spot    |

## Orderbook (By grouping)

> Response

```json
{
  "buyQuote": [
    {
      "price": "36371.0",
      "size": "0.01485"
    }
  ],
  "sellQuote": [
    {
      "price": "36380.5",
      "size": "0.01782"
    }
  ],
  "timestamp": 1624989459489,
  "symbol": "BTC-USD"
}
```

`GET /api/v3.3/orderbook`

Retrieves a Level 2 snapshot of the orderbook and allows you to specify grouping and also bid / asks depth

### Request Parameters

| Name       | Type    | Required | Description                                                                                                                                                                                             |
| ---        | ---     | ---      |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol     | String  | Yes      | Market symbol                                                                                                                                                                                           |
| group      | Integer | No       | Orderbook grouping. Valid values are: <br/>0-8 where 0 indicates level 0 grouping (eg. for BTC, it will be 0.1)<br/>Level 1 grouping for BTC would be 0.5<br/>Level 1 grouping for BTC would be 1<br/>  |
| limit_bids | Integer | No       | Orderbook depth on the bid side                                                                                                                                                                         |
| limit_asks | Integer | No       | Orderbook depth on the ask side                                                                                                                                                                         |

### Response Content

#### Orderbook

| Name      | Type   | Required | Description            |
| ---       | ---    | ---      | ---                    |
| symbol    | String | Yes      | Market symbol          |
| buyQuote  | Quote  | Yes      | Array of Buy quotes    |
| sellQuote | Quote  | Yes      | Array of Sell quotes   |
| timestamp | Double | Yes      | Timestamp of orderbook |

#### Quote

| Name  | Type   | Required | Description |
| ---   | ---    | ---      | ---         |
| price | Double | Yes      | order price |
| size  | Double | Yes      | order size  |


## Orderbook

> Response

```json
{
  "buyQuote": [
    {
      "price": "36235.0",
      "size": "7.67500"
    }
  ],
  "sellQuote": [
    {
      "price": "36241.5",
      "size": "0.60200"
    }
  ],
  "timestamp": 1624989977940,
  "symbol": "BTC-USD"
}
```

`GET /api/v3.3/orderbook/L2`

Retrieves a Level 2 snapshot of the orderbook

### Request Parameters

| Name   | Type    | Required | Description     |
| ---    | ---     | ---      | ---             |
| symbol | String  | Yes      | Market symbol   |
| depth  | Integer | No       | Orderbook depth |

### Response Content

#### Orderbook

| Name      | Type   | Required | Description            |
| ---       | ---    | ---      | ---                    |
| symbol    | String | Yes      | Market symbol          |
| buyQuote  | Quote  | Yes      | Array of Buy quotes    |
| sellQuote | Quote  | Yes      | Array of Sell quotes   |
| timestamp | Double | Yes      | Timestamp of orderbook |

#### Quote

| Name  | Type   | Required | Description |
| ---   | ---    | ---      | ---         |
| price | Double | Yes      | order price |
| size  | Double | Yes      | order size  |


## Query Trades Fills

> Response

```json
[
  {
    "price": 36164,
    "size": 0.035,
    "side": "SELL",
    "symbol": "BTC-USD",
    "serialId": 85997835,
    "timestamp": 1624990097000
  }
]
```

`GET /api/v3.3/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

| Name      | Type    | Required | Description                                       |
| ---       | ---     | ---      | ---                                               |
| symbol    | String  | Yes      | Market symbol                                     |
| startTime | Long    | No       | Starting time in milliseconds (eg. 1624987283000) |
| endTime   | Long    | No       | Ending time in milliseconds (eg. 1624987283000)   |
| count     | Integer | No       | Number of records to return                       |

* maximum days of trade fills

| Time Interval       | Maximum Days  | Explanation                                                                             |
| :---:               | ---:          | :---:                                                                                   |
| startTime / endTime | 30            | Maximum **30** days within the specified interval                                       |
| startTime /    -    | 3             | If the **end time** is not specified, then **3** days after the **start time**          |
|      -    / endTime | 3             | If the **start time** is not specified, then **3** days before the **end time**         |
|      -    /    -    | 3             | If neither start nor end time is specified, then **3** days before the **current time** |

### Response Content

| Name      | Type   | Required | Description                             |
| ---       | ---    | ---      | ---                                     |
| symbol    | String | Yes      | Market symbol                           |
| side      | String | Yes      | Trade side. Values are: [`BUY`, `SELL`] |
| price     | Double | Yes      | Transacted price                        |
| size      | Double | Yes      | Transacted size                         |
| serialId  | Double | Yes      | Serial Id, running sequence Double      |
| timestamp | Double | Yes      | Transacted timestamp                    |


## Query Server Time

> Response

```json
{
  "iso": "2021-06-29T18:14:30.886Z",
  "epoch": 1624990470
}
```

`GET /api/v3.3/time`

Gets server time

### Response Content

| Name  | Type | Required | Description                            |
| ---   | ---  | ---      | ---                                    |
| iso   | Long | Yes      | Time in YYYY-MM-DDTHH24:MI:SS.Z format |
| epoch | Long | Yes      | Returns epoch timestamp                |


# Trade Endpoints

## Create New Order

> Request (create `MARKET` order)

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "side": "BUY",
  "type": "MARKET"
}
```

> Request (create `MARKET STOP` order)

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "side": "BUY",
  "type": "MARKET",
  "txType": "Stop",
  "triggerPrice": 32000
}
```

> Request (create `LIMIT` order)

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "price": 34000,
  "side": "BUY",
  "type": "LIMIT"
}
```

> Request (create `LIMIT STOP` order)

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "price": 34000,
  "side": "BUY",
  "type": "LIMIT",
  "txType": "Stop",
  "triggerPrice": 32000
}
```

> Request (create `OCO` order)

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "price": 24000,
  "side": "BUY",
  "type": "OCO",
  "txType": "LIMIT",
  "stopPrice": 40010,
  "triggerPrice": 40000
}
```

> Request (create `PEG` order)

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "price": 25000,
  "side": "BUY",
  "type": "PEG",
  "deviation": -10,
  "stealth": 10
}
```

> Response (general)

```json
[
  {
    "status": 4,
    "symbol": "BTC-USD",
    "orderType": 77,
    "price": 111370.40932,
    "side": "BUY",
    "orderID": "c7884abe-21e6-4728-9825-157298cad88f",
    "timestamp": 1752129037800,
    "triggerPrice": 0,
    "stopPrice": null,
    "trigger": false,
    "message": "",
    "clOrderID": null,
    "stealth": 1,
    "deviation": 1,
    "postOnly": false,
    "orderDetailType": null,
    "originalOrderBaseSize": 0.0001,
    "originalOrderQuoteSize": null,
    "currentOrderBaseSize": 0.0001,
    "currentOrderQuoteSize": null,
    "remainingOrderBaseSize": 0,
    "remainingOrderQuoteSize": null,
    "filledBaseSize": 0.0001,
    "totalFilledBaseSize": 0.0001,
    "orderCurrency": "base",
    "avgFilledPrice": 111370.40932,
    "time_in_force": "GTC"
  }
]
```

> Response (for `Quote Buy`)
```json
[
  {
    "status": 5,
    "symbol": "BTC-USD",
    "orderType": 77,
    "price": 111381.34601685,
    "side": "BUY",
    "orderID": "f4aa8d57-c062-4ba9-b22e-09c4249d53f5",
    "timestamp": 1752129085233,
    "triggerPrice": 0,
    "stopPrice": null,
    "trigger": false,
    "message": "",
    "clOrderID": null,
    "stealth": 1,
    "deviation": 1,
    "postOnly": false,
    "orderDetailType": null,
    "originalOrderBaseSize": null,
    "originalOrderQuoteSize": 100,
    "currentOrderBaseSize": null,
    "currentOrderQuoteSize": 100,
    "remainingOrderBaseSize": null,
    "remainingOrderQuoteSize": 0.870602045,
    "filledBaseSize": 0.00089,
    "totalFilledBaseSize": 0.00089,
    "orderCurrency": "quote",
    "avgFilledPrice": 111381.34601685,
    "time_in_force": "GTC"
  }
]
```

> Response (for `OCO` order)

```json
[
  {
    "status": 2,
    "symbol": "BTC-USDT",
    "orderType": 76,
    "price": 110000,
    "side": "BUY",
    "orderID": "54b3ab22-132b-4df0-9378-beacdc808e5c",
    "timestamp": 1752129347246,
    "triggerPrice": 0,
    "stopPrice": null,
    "trigger": false,
    "message": "",
    "clOrderID": "_W_mcjffli1752129293688",
    "stealth": 1,
    "deviation": 1,
    "postOnly": false,
    "orderDetailType": null,
    "originalOrderBaseSize": 0.0001,
    "originalOrderQuoteSize": null,
    "currentOrderBaseSize": 0.0001,
    "currentOrderQuoteSize": null,
    "remainingOrderBaseSize": 0.0001,
    "remainingOrderQuoteSize": null,
    "filledBaseSize": 0,
    "totalFilledBaseSize": 0,
    "orderCurrency": "base",
    "avgFilledPrice": 0,
    "time_in_force": "GTC"
  },
  {
    "status": 9,
    "symbol": "BTC-USDT",
    "orderType": 76,
    "price": 111318.3,
    "side": "BUY",
    "orderID": "fae47714-4c75-4956-9e6a-832cbf2d9a09",
    "timestamp": 1752129347246,
    "triggerPrice": 120000,
    "stopPrice": null,
    "trigger": true,
    "message": "",
    "clOrderID": "_W_mcjffli1752129293688",
    "stealth": 1,
    "deviation": 1,
    "postOnly": false,
    "orderDetailType": null,
    "originalOrderBaseSize": 0.0001,
    "originalOrderQuoteSize": null,
    "currentOrderBaseSize": 0.0001,
    "currentOrderQuoteSize": null,
    "remainingOrderBaseSize": 0,
    "remainingOrderQuoteSize": null,
    "filledBaseSize": 0,
    "totalFilledBaseSize": 0,
    "orderCurrency": "base",
    "avgFilledPrice": 0,
    "time_in_force": "GTC"
  }
]
```

`POST /api/v3.3/order` or `POST /api/v3.3/order/peg` (The 2 endpoints work identically)

Creates a new order. Requires `Trading` permission. Please note that Index Order only supports USD quotes.

### Request Parameters

| Name          | Type    | Required | Description                                                                                                                                                                                                                                                                                                                                                        |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                                                                                |
| symbol        | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                                                                                      |
| price         | Double  | No       | Mandatory unless creating a MARKET order. Minimum price for a sell order, this is the lowest price that a user is willing to sell at. Maximum price for a buy order, this is the maximum price a user is willing to buy at.                                                                                                                                        |
| size          | Double  | Yes      | Order size                                                                                                                                                                                                                                                                                                                                                         |
| side          | String  | Yes      | 'BUY' or 'SELL'                                                                                                                                                                                                                                                                                                                                                    |
| time_in_force | String  | No       | Time validity of the order<br/>GTC: Good till Cancel<br/>IOC: Immediate or Cancel<br/>FOK: Fill or Kill<br/>HALFMIN: Order valid for 30 seconds<br/>FIVEMIN: Order valid for 5 mins<br/> HOUR: Order valid for an hour<br/>TWELVEHOUR: Order valid for 12 hours<br/>DAY: Order valid for a day<br/>WEEK: Order valid for a week<br/>MONTH: Order valid for a month |
| type          | String  | Yes      | Order type<br/>LIMIT: Limit Orders<br/>MARKET: Market Orders<br/>OCO: One cancel the other<br/>PEG: price is according to a deviation to the Index price                                                                                                                                                                                                           |
| txType        | String  | No       | Used for Stop orders or trigger orders<br/>STOP: Stop Order, `triggerPrice` is mandatory<br/>TRIGGER: Trigger order, `triggerPrice` is mandatory<br/>LIMIT: Default, used when its not a Stop order nor Trigger order                                                                                                                                                 |
| stopPrice     | Double  | No       | Mandatory when creating an OCO order. Indicates the stop price                                                                                                                                                                                                                                                                                              |
| triggerPrice  | Double  | No       | Mandatory when creating a Stop, Trigger or OCO order. Indicates the trigger price                                                                                                                                                                                                                                                                                        |
| trailValue    | Double  | No       | Trail value                                                                                                                                                                                                                                                                                                                                                        |
| postOnly      | Boolean | No       | Boolean to indicate if this is a post only order. For post only orders, traders are charged maker fees                                                                                                                                                                                                                                                             |
| clOrderID     | String  | No       | Custom order Id                                                                                                                                                                                                                                                                                                                                                    |
| stealth       | Double  | No       | Mandatory when creating a PEG order. How many percent of the order is to be displayed on the orderbook.                                                                                                                                                                                                                                                            |
| deviation     | Double  | No       | For PEG order. How much should the order price deviate from index price. Value is in percentage and can range from `-10` to `10`                                                                                                                                                                                                                                   |


### Response Content

| Name             | Type    | Required | Description                                                                                                                                                                                                                                                                                         |
| ---              | ---     | ---      | ---                                                                                                                                                                                                                                                                                                 |
| symbol           | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                       |
| clOrderID        | String  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                                                      |
| orderID          | String  | Yes      | Order ID                                                                                                                                                                                                                                                                                            |
| orderType        | Integer  | Yes      | Order type <br/>76: Limit order<br/>77: Market order<br/>80: Peg/Algo order                                                                                                                                                                                                                         |
| postOnly         | Boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                                             |
| price            | Double  | Yes      | Order price                                                                                                                                                                                                                                                                                         |
| side             | String  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                                                          |
| status           | Integer | Yes      | Order status<br/>	2: Order Inserted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>8: Insufficient Balance<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found<br/>17: Request Failed |
| stopPrice        | Double  | Yes      | Stop price                                                                                                                                                                                                                                                                                          |
| time_in_force    | String  | Yes      | Order validity                                                                                                                                                                                                                                                                                      |
| timestamp        | Long  | Yes      | Order timestamp                                                                                                                                                                                                                                                                                     |
| trigger          | Boolean  | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                                               |
| triggerPrice     | Double  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                                                      |
| avgFilledPrice | Double  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                                              |
| message          | String  | Yes      | Trade messages                                                                                                                                                                                                                                                                                      |
| stealth          | Double  | Yes      | Stealth value of order                                                                                                                                                                                                                                                                              |
| deviation        | Double  | Yes      | Deviation value of order                                                                                                                                                                                                                                                                            |
| originalOrderBaseSize                 | Double  | Yes      | The original order quantity in base currency. This value will not change even if adjustments are made later.                                                                           |
| originalOrderQuoteSize                 | Double  | Yes      | The original order quantity in quote currency. This value will not change even if adjustments are made later.                                                                           |
| currentOrderBaseSize                 | Double  | Yes      | The latest order quantity in base currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| currentOrderQuoteSize                 | Double  | Yes      | The latest order quantity in quote currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| remainingOrderBaseSize                 | Double  | Yes      | The remaining order quantity in base currency = Current Order Base Size - Filled Base Size.                                                                           |
| remainingOrderQuoteSize                 | Double  | Yes      | The remaining order quantity in quote currency = Current Order Quote Size - Filled Quote Size.                                                                           |
| filledBaseSize                 | Double  | Yes      | The quantity of the order in base currency that has been filled.                                                                           |
| totalFilledBaseSize                 | Double  | Yes      | Cumulative filled quantity of this order in base currency.                                                                           |
| orderCurrency                 | Double  | Yes      | "base" or "quote"                                                                           |

## Query Order

> Response

```json
{
  "orderID": "54b3ab22-132b-4df0-9378-beacdc808e5c",
  "orderType": 76,
  "price": 110000,
  "side": "BUY",
  "orderValue": 11.004378,
  "pegPriceMin": 0,
  "pegPriceMax": 0,
  "pegPriceDeviation": 0,
  "timestamp": 1752129347245,
  "triggerOrder": false,
  "triggerPrice": 0,
  "triggerOriginalPrice": 0,
  "triggerOrderType": 0,
  "triggerTrailingStopDeviation": 0,
  "triggerStopPrice": 0,
  "symbol": "BTC-USDT",
  "trailValue": 0,
  "quote": "USDT",
  "clOrderID": "_W_mcjffli1752129293688",
  "status": 2,
  "timeInForce": "GTC",
  "originalOrderBaseSize": 0.0001,
  "originalOrderQuoteSize": null,
  "currentOrderBaseSize": 0.0001,
  "currentOrderQuoteSize": null,
  "remainingOrderBaseSize": 0.0001,
  "remainingOrderQuoteSize": null,
  "totalFilledBaseSize": 0,
  "orderCurrency": "base",
  "avgFilledPrice": 0,
  "triggered": true
}
```


`GET /api/v3.3/order`

Query order detail for a specified orderID/clOrderID, for the open orders and cancelled order which is cancelled in 30 minutes only.
Please note that this API is `Trading` permission required.

### Request Parameters

| Name      | Type   | Required | Description                                                                                                                  |
| ---       | ---    | ---      | ---                                                                                                                          |
| orderID   | String | No       | Unique identifier for an order. Mandatory when clOrderID is not provided. If orderID is provided, clOrderID will be ignored. |
| clOrderID | String | No       | Client custom order ID. Mandatory when orderID is not provided.                                                              |

### Response Content

| Name                          | Type    | Required | Description                                                                            |
| ---                           | ---     | ---      | ---                                                                                    |
| orderID                       | String  | Yes      | Order ID                                                                               |
| symbol                        | String  | Yes      | Market symbol                                                                          |
| quote                         | String  | Yes      | Quote symbol                                                                           |
| orderType                     | Integer | Yes      | Order type                                                                             |
| side                          | String  | Yes      | Order side                                                                             |
| price                         | Double  | Yes      | Order price                                                                            |
| orderValue                    | Double  | Yes      | Total value of of this order                                                           |
| pegPriceMin                   | Double  | Yes      | Minimum possible peg price this takes precedence over pegPriceDeviation                |
| pegPriceMax                   | Double  | Yes      | Peg Price Max (New Entry)                                                              |
| pegPriceDeviation             | Double  | Yes      | Percentage deviation from Index price                                                  |
| timestamp                     | Long    | Yes      | Order timestamp                                                                        |
| triggerOrder                  | Boolean | Yes      | Indicator if order is a trigger order                                                  |
| triggerPrice                  | Double  | Yes      | Order trigger price, returns 0 if order is not a trigger order                         |
| triggerOriginalPrice          | Double  | Yes      | Price of the original order. Only valid if it's a triggered order                      |
| triggerOrderType              | Integer | Yes      | Order type                                                                             |
| triggerTrailingStopDeviation  | Double  | Yes      | Percentage deviation from stop price                                                   |
| triggerStopPrice              | Double  | Yes      | Stop price, Algo Order only                                                            |
| triggered                     | Boolean | Yes      | Indicate whether the order is triggered                                                |
| trailValue                    | Double  | Yes      | Trail value                                                                            |
| clOrderID                     | String  | Yes      | Customer tag sent in by trader                                                         |
| avgFilledPrice              | Double  | Yes      | Average filled price. Returns the average filled price for partially transacted orders |
| originalOrderBaseSize                 | Double  | Yes      | The original order quantity in base currency. This value will not change even if adjustments are made later.                                                                           |
| originalOrderQuoteSize                 | Double  | Yes      | The original order quantity in quote currency. This value will not change even if adjustments are made later.                                                                           |
| currentOrderBaseSize                 | Double  | Yes      | The latest order quantity in base currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| currentOrderQuoteSize                 | Double  | Yes      | The latest order quantity in quote currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| remainingOrderBaseSize                 | Double  | Yes      | The remaining order quantity in base currency = Current Order Base Size - Filled Base Size.                                                                           |
| remainingOrderQuoteSize                 | Double  | Yes      | The remaining order quantity in quote currency = Current Order Quote Size - Filled Quote Size.                                                                           |
| totalFilledBaseSize                 | Double  | Yes      | Cumulative filled quantity of this order in base currency.                                                                           |
| orderCurrency                 | Double  | Yes      | "base" or "quote"                                                                           |
| status                        | Integer | Yes      | Order status. Please refer to [`API Enum`](#api-enum)                                  |
| timeInForce                   | String  | Yes      | Order validity                                                                         |

## Amend Order

> Request (amend price)

```json
{
  "symbol": "BTC-USD",
  "orderID": "25248336-66d8-41ff-99fd-83489c4e6029",
  "type": "PRICE",
  "value": 35000
}

```
> Request (amend size)

```json
{
  "orderID": "689bf733-4879-4e32-8d1f-cb81f63d24d4",
  "type": "SIZE",
  "value": 10.05,
  "symbol": "BTC-USD"
}
```

> Request (amend trigger price)

```json
{
  "orderID": "cb2785b0-558e-4b30-bf1f-8a8c56174d0c",
  "type": "TRIGGERPRICE",
  "value": 40020,
  "symbol": "BTC-USD"
}
```

> Request (amend multiple attributes)

```json
{
  "symbol": "BTC-USD",
  "orderID": "cb2785b0-558e-4b30-bf1f-8a8c56174d0c",
  "type": "ALL",
  "orderPrice": 40010,
  "orderSize": 10.05,
  "triggerPrice": 40000
}
```

> Response

```json
[
  {
    "status": 123,
    "symbol": "BTC-USDT",
    "orderType": 76,
    "price": 90000,
    "side": "BUY",
    "orderID": "56c03da5-3d7b-4c5c-8b13-1b3de5be2e33",
    "timestamp": 1752129948157,
    "triggerPrice": 0,
    "stopPrice": null,
    "trigger": false,
    "message": "",
    "clOrderID": "_W_ejrojwq1752129916234",
    "stealth": 0,
    "deviation": 0,
    "postOnly": true,
    "orderDetailType": null,
    "originalOrderBaseSize": 0.00001,
    "originalOrderQuoteSize": null,
    "currentOrderBaseSize": 0.00001,
    "currentOrderQuoteSize": null,
    "remainingOrderBaseSize": 0.00001,
    "remainingOrderQuoteSize": null,
    "filledBaseSize": 0,
    "totalFilledBaseSize": 0,
    "orderCurrency": "base",
    "avgFilledPrice": 0,
    "originalPrice": 90000,
    "time_in_force": "GTC"
  }
]
```

`PUT /api/v3.3/order`

Amend the price or size or trigger price of an order. For trigger orders, if the order has already been triggered, the trigger price cannot be further amended. Amend order _does not_ apply to algo orders. Requires `Trading` permission.

### Request Parameters

| Name         | Type    | Required | Description                                                                                                                                                        |
| ---          | ---     | ---      | ---                                                                                                                                                                |
| symbol       | String  | Yes      | Market symbol                                                                                                                                                      |
| orderID      | String  | No       | Internal order ID. Mandatory when `clOrderID` is not provided. If `orderID` is provided, `clOrderID` will be ignored.                                              |
| clOrderID    | String  | No       | Custom order ID. Mandatory when `orderID` is not provided.                                                                                                         |
| type         | String  | Yes      | Type of amendment.<br/>`PRICE`: To amend order price<br/>`SIZE`: To amend order size<br/>`TRIGGERPRICE`: To amend trigger price for trigger orders only.<br/>`ALL`: To amend multiple fields. Note that the `TRIGGERPRICE` can only be amended if the order is a trigger order. Don't include `TRIGGERPRICE` if it is not a trigger order. |
| value        | Double  | No       | Mandatory for types: `PRICE`, `SIZE`, `TRIGGERPRICE`. The value to be amended to. Value depends on the type being set.                                             |
| orderPrice   | Double  | No       | For type: `ALL`, order price to be amended                                                                                                                         |
| orderSize    | Double  | No       | For type: `ALL`, order size to be amended                                                                                                                          |
| triggerPrice | Double  | No       | For type: `ALL`, trigger price to be amended                                                                                                                       |

### Response Content

| Name             | Type    | Required | Description                                                                                                                                                                                                                                                                                         |
| ---              | ---     | ---      | ---                                                                                                                                                                                                                                                                                                 |
| symbol           | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                       |
| clOrderID        | String  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                                                      |
| orderID          | String  | Yes      | Order ID                                                                                                                                                                                                                                                                                            |
| orderType        | Integer  | Yes      | Order type <br/>76: Limit order<br/>77: Market order<br/>80: Peg/Algo order                                                                                                                                                                                                                         |
| postOnly         | Boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                                             |
| price            | Double  | Yes      | Order price                                                                                                                                                                                                                                                                                         |
| side             | String  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                                                          |
| status           | Integer | Yes      | Order status<br/>	2: Order Inserted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>8: Insufficient Balance<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found<br/>17: Request Failed |
| stopPrice        | Double  | Yes      | Stop price                                                                                                                                                                                                                                                                                          |
| time_in_force    | String  | Yes      | Order validity                                                                                                                                                                                                                                                                                      |
| timestamp        | Long  | Yes      | Order timestamp                                                                                                                                                                                                                                                                                     |
| trigger          | Boolean  | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                                               |
| triggerPrice     | Double  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                                                      |
| avgFilledPrice | Double  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                                              |
| message          | String  | Yes      | Trade messages                                                                                                                                                                                                                                                                                      |
| stealth          | Double  | Yes      | Stealth value of order                                                                                                                                                                                                                                                                              |
| deviation        | Double  | Yes      | Deviation value of order                                                                                                                                                                                                                                                                            |
| originalOrderBaseSize                 | Double  | Yes      | The original order quantity in base currency. This value will not change even if adjustments are made later.                                                                           |
| originalOrderQuoteSize                 | Double  | Yes      | The original order quantity in quote currency. This value will not change even if adjustments are made later.                                                                           |
| currentOrderBaseSize                 | Double  | Yes      | The latest order quantity in base currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| currentOrderQuoteSize                 | Double  | Yes      | The latest order quantity in quote currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| remainingOrderBaseSize                 | Double  | Yes      | The remaining order quantity in base currency = Current Order Base Size - Filled Base Size.                                                                           |
| remainingOrderQuoteSize                 | Double  | Yes      | The remaining order quantity in quote currency = Current Order Quote Size - Filled Quote Size.                                                                           |
| filledBaseSize                 | Double  | Yes      | The quantity of the order in base currency that has been filled.                                                                           |
| totalFilledBaseSize                 | Double  | Yes      | Cumulative filled quantity of this order in base currency.                                                                           |
| orderCurrency                 | Double  | Yes      | "base" or "quote"                                                                           |


## Cancel Order

> Request

```
/api/v3.3/order?symbol=BTC-USD&clOrderID=my-order-id
```

> Response (general)

```json
[
  {
    "status": 6,
    "symbol": "BTC-USDT",
    "orderType": 76,
    "price": 90000,
    "side": "BUY",
    "orderID": "56c03da5-3d7b-4c5c-8b13-1b3de5be2e33",
    "timestamp": 1752130038115,
    "triggerPrice": 0,
    "stopPrice": null,
    "trigger": false,
    "message": "",
    "clOrderID": "_W_ejrojwq1752129916234",
    "stealth": 1,
    "deviation": 1,
    "postOnly": true,
    "orderDetailType": null,
    "originalOrderBaseSize": 0.00001,
    "originalOrderQuoteSize": null,
    "currentOrderBaseSize": 0.00001,
    "currentOrderQuoteSize": null,
    "remainingOrderBaseSize": 0.00001,
    "remainingOrderQuoteSize": null,
    "filledBaseSize": 0,
    "totalFilledBaseSize": 0,
    "orderCurrency": "base",
    "avgFilledPrice": 0,
    "time_in_force": "GTC"
  }
]
```
> Response (for `OCO` order)

```json
[
  {
    "status": 6,
    "symbol": "BTC-USDT",
    "orderType": 76,
    "price": 110000,
    "side": "BUY",
    "orderID": "54b3ab22-132b-4df0-9378-beacdc808e5c",
    "timestamp": 1752133730711,
    "triggerPrice": 0,
    "stopPrice": null,
    "trigger": false,
    "message": "",
    "clOrderID": "_W_mcjffli1752129293688",
    "stealth": 1,
    "deviation": 1,
    "postOnly": false,
    "orderDetailType": null,
    "originalOrderBaseSize": 0.0001,
    "originalOrderQuoteSize": null,
    "currentOrderBaseSize": 0.0001,
    "currentOrderQuoteSize": null,
    "remainingOrderBaseSize": 0.0001,
    "remainingOrderQuoteSize": null,
    "filledBaseSize": 0,
    "totalFilledBaseSize": 0,
    "orderCurrency": "base",
    "avgFilledPrice": 0,
    "time_in_force": "GTC"
  },
  {
    "status": 6,
    "symbol": "BTC-USDT",
    "orderType": 76,
    "price": 0,
    "side": "BUY",
    "orderID": "fae47714-4c75-4956-9e6a-832cbf2d9a09",
    "timestamp": 1752133730710,
    "triggerPrice": 120000,
    "stopPrice": null,
    "trigger": true,
    "message": "",
    "clOrderID": "_W_mcjffli1752129293688",
    "stealth": 1,
    "deviation": 1,
    "postOnly": false,
    "orderDetailType": null,
    "originalOrderBaseSize": 0.0001,
    "originalOrderQuoteSize": null,
    "currentOrderBaseSize": 0.0001,
    "currentOrderQuoteSize": null,
    "remainingOrderBaseSize": 0,
    "remainingOrderQuoteSize": null,
    "filledBaseSize": 0,
    "totalFilledBaseSize": 0,
    "orderCurrency": "base",
    "avgFilledPrice": 0,
    "time_in_force": "GTC"
  }
]
```

`DELETE /api/v3.3/order`

Cancels pending orders that has not yet been transacted. The `orderID` is a unique identifier to cancel a particular order. `clOrderID` is a custom ID sent in by the trader. When cancel by `clOrderID`, all orders having the same ID will be cancelled. If `orderID` and `clOrderID` is not sent in, then cancellation will be for all orders in the current market. Requires `Trading` permission.

### Request Parameters

| Name      | Type   | Required | Description                                                                                                                        |
| ---       | ---    | ---      | ---                                                                                                                                |
| symbol    | String | Yes      | Market symbol                                                                                                                      |
| orderID   | String | No       | Unique identifier for an order. Mandatory when `clOrderID` is not provided. If `orderID` is provided, `clOrderID` will be ignored. |
| clOrderID | String | No       | Client custom order ID. Mandatory when `orderID` is not provided.                                                                  |

### Response Content

| Name             | Type    | Required | Description                                                                                                                                                                                                                                                                                     |
| ---              | ---     | ---      | ---                                                                                                                                                                                                                                                                                             |
| symbol           | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                   |
| clOrderID        | String  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                                                  |
| orderID          | String  | Yes      | Order ID                                                                                                                                                                                                                                                                                        |
| orderType        | Integer  | Yes      | Order type <br/>76: Limit order<br/>77: Market order<br/>80: Peg/Algo order                                                                                                                                                                                                                     |
| postOnly         | Boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                                         |
| price            | Double  | Yes      | Order price                                                                                                                                                                                                                                                                                     |
| side             | String  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                                                      |
| status           | Integer | Yes      | Order status<br/>	2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found<br/>17: Request failed |
| stopPrice        | Double  | Yes      | Stop price                                                                                                                                                                                                                                                                                      |
| time_in_force    | String  | Yes      | Order validity                                                                                                                                                                                                                                                                                  |
| timestamp        | Long  | Yes      | Order timestamp                                                                                                                                                                                                                                                                                 |
| trigger          | Boolean  | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                                           |
| triggerPrice     | Double  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                                                  |
| avgFilledPrice | Double  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                                          |
| message          | String  | Yes      | Trade messages                                                                                                                                                                                                                                                                                  |
| stealth          | Double  | Yes      | Stealth value of order                                                                                                                                                                                                                                                                          |
| deviation        | Double  | Yes      | Deviation value of order                                                                                                                                                                                                                                                                        |
| originalOrderBaseSize                 | Double  | Yes      | The original order quantity in base currency. This value will not change even if adjustments are made later.                                                                           |
| originalOrderQuoteSize                 | Double  | Yes      | The original order quantity in quote currency. This value will not change even if adjustments are made later.                                                                           |
| currentOrderBaseSize                 | Double  | Yes      | The latest order quantity in base currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| currentOrderQuoteSize                 | Double  | Yes      | The latest order quantity in quote currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| remainingOrderBaseSize                 | Double  | Yes      | The remaining order quantity in base currency = Current Order Base Size - Filled Base Size.                                                                           |
| remainingOrderQuoteSize                 | Double  | Yes      | The remaining order quantity in quote currency = Current Order Quote Size - Filled Quote Size.                                                                           |
| filledBaseSize                 | Double  | Yes      | The quantity of the order in base currency that has been filled.                                                                           |
| totalFilledBaseSize                 | Double  | Yes      | Cumulative filled quantity of this order in base currency.                                                                           |
| orderCurrency                 | Double  | Yes      | "base" or "quote"                                                                           |

## Dead Man's Switch (Cancel All After)

> Request

```json
{
  "timeout": 60000
}
```

`POST /api/v3.3/order/cancelAllAfter`

Dead-man's switch allows the trader to send in a timeout value which is a Time to live (TTL) value for an order. Extension of the timeout is done by sending another `cancelAllAfter` request. If the server does not receive another request before the timeout is reached, all orders will be cancelled. Requires `Trading` permission.

### Request Parameters

| Name    | Type | Required | Description                   |
| ---     | ---  | ---      | ---                           |
| timeout | Long | Yes      | Timeout value in milliseconds |


### Response Content

* If set correctly, a HTTP 200 response code will be returned

## Query Open Orders

> Response

```json
[
    {
        "orderID": "fae47714-4c75-4956-9e6a-832cbf2d9a09",
        "requestId": 9018830890442560439,
        "vendorName": null,
        "botID": null,
        "orderType": 76,
        "price": 111318.3,
        "side": "BUY",
        "orderValue": 11.136338391,
        "pegPriceMin": 0,
        "pegPriceMax": 0,
        "pegPriceDeviation": 0,
        "cancelDuration": 0,
        "timestamp": 1752129347246,
        "triggerOrder": true,
        "triggerPrice": 120048.6,
        "triggerOriginalPrice": 120000,
        "triggerOrderType": 1001,
        "triggerTrailingStopDeviation": 0,
        "triggerStopPrice": 0,
        "symbol": "BTC-USDT",
        "trailValue": 0,
        "quote": "USDT",
        "clOrderID": "_W_mcjffli1752129293688",
        "orderState": "STATUS_ACTIVE",
        "timeInForce": "GTC",
        "orderDetailType": null,
        "orderDetail": null,
        "originalOrderBaseSize": 0.0001,
        "originalOrderQuoteSize": null,
        "currentOrderBaseSize": 0.0001,
        "currentOrderQuoteSize": null,
        "remainingOrderBaseSize": 0.0001,
        "remainingOrderQuoteSize": null,
        "totalFilledBaseSize": 0,
        "orderCurrency": "base",
        "avgFilledPrice": 0,
        "triggered": false
    },
    {
        "orderID": "54b3ab22-132b-4df0-9378-beacdc808e5c",
        "requestId": 3237203630362690520,
        "vendorName": null,
        "botID": null,
        "orderType": 76,
        "price": 110000,
        "side": "BUY",
        "orderValue": 11.004455,
        "pegPriceMin": 0,
        "pegPriceMax": 0,
        "pegPriceDeviation": 0,
        "cancelDuration": 0,
        "timestamp": 1752129347245,
        "triggerOrder": false,
        "triggerPrice": 0,
        "triggerOriginalPrice": 0,
        "triggerOrderType": 0,
        "triggerTrailingStopDeviation": 0,
        "triggerStopPrice": 0,
        "symbol": "BTC-USDT",
        "trailValue": 0,
        "quote": "USDT",
        "clOrderID": "_W_mcjffli1752129293688",
        "orderState": "STATUS_ACTIVE",
        "timeInForce": "GTC",
        "orderDetailType": null,
        "orderDetail": null,
        "originalOrderBaseSize": 0.0001,
        "originalOrderQuoteSize": null,
        "currentOrderBaseSize": 0.0001,
        "currentOrderQuoteSize": null,
        "remainingOrderBaseSize": 0.0001,
        "remainingOrderQuoteSize": null,
        "totalFilledBaseSize": 0,
        "orderCurrency": "base",
        "avgFilledPrice": 0,
        "triggered": true
    }
]
```

`GET /api/v3.3/user/open_orders`

Retrieves open orders that have not yet been matched or matched recently. Requires `Trading` permission.

### Request Parameters

| Name      | Type   | Required | Description                                                                         |
| ---       | ---    | ---      | ---                                                                                 |
| symbol    | String | No       | Market symbol                                                                       |
| orderID   | String | No       | Query using internal order ID                                                       |
| clOrderID | String | No       | Query using custom order ID. If `orderID` is provided, `clOrderID` will be ignored. |


### Response Content

| Name                       | Type   | Required | Description                                                                            |
| ---                          | ---    | ---      | ---                                                                                  |
| orderType                  | Integer | Yes      | Order type <br/>76: Limit order<br/>77: Market order<br/>80: Peg/Algo order            |
| price                      | Double | Yes      | Order price                                                                            |
| side                       | String | Yes      | Order side<br/>`BUY` or `SELL`                                                         |
| orderValue                 | Double | Yes      | Total value of of this order                                                           |
| pegPriceMin                | Double | Yes      | Minimum possible peg price this takes precedence over pegPriceDeviation                |
| pegPriceMax                | Double | Yes      | Maximum possible peg price this takes precedence over pegPriceDeviation                |
| pegPriceDeviation          | Double | Yes      | Percentage deviation from Index price                                                  |
| cancelDuration             | Double | Yes      | Order expiration time if not 0                                                         |
| timestamp                  | Long | Yes      | Order placement time                                                                   |
| orderID                    | String | Yes      | Order Id                                                                               |
| triggerOrder               | Boolean   | Yes      | Indicator if order is a trigger order                                                  |
| triggerPrice               | Double | Yes      | Order trigger price, returns 0 if order is not a trigger order                         |
| triggerOriginalPrice       | Double | Yes      | Price of the original order. Only valid if it's a triggered order                      |
| triggerOrderType           | Double | Yes      | Order type <br/>`76: Limit order`<br/>`77: Market order`<br/>`80: Peg/Algo order`      |
| triggerTrailingStopDeviation | Double | Yes      | Percentage deviation from stop price                                                 |
| triggerStopPrice           | Double | Yes      | Stop price, Algo Order only                                                            |
| symbol                     | String | Yes      | Market name (e.g. BTC-USD)                                                             |
| trailValue                 | Double | Yes      | Trail value                                                                            |
| avgFilledPrice           | Double | Yes      | Average filled price. Returns the average filled price for partially transacted orders |
| clOrderID                  | String | Yes      | Customer order ID                                                                      |
| orderState                 | String | Yes      | `STATUS_ACTIVE`, `STATUS_INACTIVE`                                                     |
| timeInForce                | String | Yes      | Order validity                                                                         |
| triggered                  | Boolean   | Yes      | Indicate whether the order is triiggered                                               |
 originalOrderBaseSize                 | Double  | Yes      | The original order quantity in base currency. This value will not change even if adjustments are made later.                                                                           |
| originalOrderQuoteSize                 | Double  | Yes      | The original order quantity in quote currency. This value will not change even if adjustments are made later.                                                                           |
| currentOrderBaseSize                 | Double  | Yes      | The latest order quantity in base currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| currentOrderQuoteSize                 | Double  | Yes      | The latest order quantity in quote currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| remainingOrderBaseSize                 | Double  | Yes      | The remaining order quantity in base currency = Current Order Base Size - Filled Base Size.                                                                           |
| remainingOrderQuoteSize                 | Double  | Yes      | The remaining order quantity in quote currency = Current Order Quote Size - Filled Quote Size.                                                                           |
| totalFilledBaseSize                 | Double  | Yes      | Cumulative filled quantity of this order in base currency.                                                                           |
| orderCurrency                 | Double  | Yes      | "base" or "quote"                                                                           |

## Query User Trades Fills

> Response

```json
[
  {
    "tradeId": "a85de513-4ddf-489b-8601-b1aa96d97ad6",
    "orderId": "f4aa8d57-c062-4ba9-b22e-09c4249d53f5",
    "clOrderID": null,
    "username": "btse",
    "side": "BUY",
    "orderType": 77,
    "triggerType": 0,
    "price": 111381.3460167,
    "size": 100,
    "filledPrice": 111381.3460167,
    "filledSize": 0.00089,
    "triggerPrice": 0,
    "base": "BTC",
    "quote": "USD",
    "symbol": "BTC-USD",
    "feeCurrency": "BTC",
    "feeAmount": 5.34e-7,
    "wallet": "SPOT@",
    "realizedPnl": 0,
    "total": 0,
    "serialId": 926957588,
    "timestamp": 1752129085233,
    "avgFilledPrice": 111381.3460167
  }
]
```

`GET /api/v3.3/user/trade_history`

Retrieves a user's trade history which includes funding fee data. Requires `Read` permission.

### Request Parameters

| Name          | Type    | Required | Description                                                                                 |
| ---           | ---     | ---      | ---                                                                                         |
| symbol        | String  | Yes      | Market symbol                                                                               |
| startTime     | Long    | No       | Starting time in milliseconds (eg. 1624987283000)                                           |
| endTime       | Long    | No       | Ending time in milliseconds (eg. 1624987283000)                                             |
| count         | Integer | No       | Number of records to return                                                                 |
| clOrderID     | String  | No       | Query trade history by custom order ID                                                      |
| orderID       | String  | No       | Query trade history by order ID                                                             |
| isMatchSymbol | Boolean | No       | Exact match on `symbol`. If this sets to true, will only match records for that symbol only |

* maximum days of trade history

| Time Interval       | Maximum Days  | Explanation                                                                             |
| :---:               | ---:          | :---:                                                                                   |
| startTime / endTime | 7            | Maximum **7** days within the specified interval. If specified interval exceeds **7** days, the **start time** will be set to **7** days before the **end time**                                    |
| startTime /    -    | 7             | If the **end time** is not specified, then **7** days after the **start time**          |
|      -    / endTime | 7             | If the **start time** is not specified, then **7** days before the **end time**         |
|      -    /    -    | 7             | If neither start nor end time is specified, then **7** days before the **current time** |

### Response Content

| Name            | Type   | Required | Description                             |
| ---             | ---    | ---      |-----------------------------------------|
| symbol          | String | Yes      | Market symbol                           |
| side            | String | Yes      | Trade side. Values are: [`BUY`, `SELL`] |
| price           | Double | yes      | Transacted price                        |
| size            | Double | yes      | Original order size                   |
| serialId        | Long   | yes      | Serial id, running sequence Double      |
| tradeId         | String | yes      | Trade identifier                        |
| timestamp       | Long   | yes      | Transacted timestamp                    |
| base            | Long   | yes      | Base currency                           |
| quote           | Long   | yes      | Quote currency                          |
| clOrderID       | Long   | yes      | Custom order id                         |
| orderId         | Long   | yes      | Order id                                |
| feeAmount       | Long   | yes      | Fee amount                              |
| feeCurrency     | Long   | yes      | Fee currency                            |
| filledPrice     | Long   | yes      | Filled price                            |
| filledSize      | Long   | yes      | Filled size                             |
| orderType       | Integer| yes      | Order type                              |
| realizedPnl     | Long   | yes      | Not used in spot                        |
| total           | Long   | yes      | Not used in spot                        |
| triggerType     | Integer| yes      | 1001: Stop Loss 1002: Take Profit       |
| triggerPrice    | Double | yes      | Trigger price                           |
| wallet          | String | yes      | SPOT@ for spot transactions             |
| avgFilledPrice| String | yes      | Average fill price                      |
| username        | String | yes      | Username                                |


## query account fees

> response

```json
{
  "makerfee": 0,
  "symbol": "btc-usd",
  "takerfee": 0
}
```

`GET /api/v3.3/user/fees`

Retrieve user's trading fees. Requires `Read` permission.

### request parameters

| name     | type     | required | description                                   |
| -------- | -------- | -------- | --------------------------------------------- |
| symbol   | String   | no       | market symbol to filter for specific market   |

### response content

| name     | type   | required | description   |
| ---      | ---    | ---      | ---           |
| symbol   | String | yes      | market symbol |
| makerfee | Double | yes      | maker fees    |
| takerfee | Double | yes      | taker fees    |


# Investment Endpoints

## Query Investment Products

> response

```json
[
  {
    "id": "openeth00001",
    "name": "eth flex savings",
    "currency": "eth",
    "type": "flex",
    "startdate": 1610685918000,
    "intereststartdate": 1610719200000,
    "rates":
    [
      {
        "days": 1,
        "rate": 1.15
      }
    ],
    "compounding": true,
    "autorenewsupported": false,
    "dailylimit": 10.0,
    "minsize": 1.00000000,
    "incrementalsize": 1.00000000
  }
]
```

`GET /api/v3.3/invest/products`

Get all investment products. Requires `Read` permission.

### request parameters

(none)

### response content

| name               | type         | required | description                              |
| ---                | ---          | ---      | ---                                      |
| id                 | String       | yes      | product id                               |
| name               | String       | yes      | product name                             |
| currency           | String       | yes      | currency                                 |
| type               | String       | yes      | product type                             |
| startdate          | Long         | yes      | inventment start date                    |
| intereststartdate  | Long         | yes      | interest start date                      |
| rates              | rateobject[] | yes      | interest rate information                |
| compounding        | Double       | yes      | is product compounding                   |
| autorenewsupported | Double       | yes      | is product supported renew automatically |
| dailylimit         | Double       | yes      | daily invent amount limit                |
| minsize            | Double       | yes      | minimum invest size                      |
| incrementalsize    | Double       | yes      | invest step size                         |

### rateobject

| name | type    | required | description      |
| ---  | ---     | ---      | ---              |
| days | Integer | yes      | duration in days |
| rate | Double  | yes      | interest rate    |


## Deposit Investment

> request

```json
{
    "productId": "openusdt0001",
    "amount": 100.99
}
```

`POST /api/v3.3/invest/deposit`

Deposit an investment. Requires `Wallet` permission.

### request parameters

| name      | type    | required | description         |
| ---       | ---     | ---      | ---                 |
| productId | String  | yes      | invest product id   |
| amount    | Double  | yes      | invest amount       |


## Renew Investment

> request

```json
{
    "orderId": 1,
    "autoRenew": false
}
```

> response

```json
{
    "orderId": 1,
    "autoRenew": false
}
```

`POST /api/v3.3/invest/renew`

Renew an investment order. Requires `Wallet` permission.

### request parameters

| name      | type    | required | description         |
| ---       | ---     | ---      | ---                 |
| orderId   | Integer | yes      | investment order id |
| autoRenew | Boolean | yes      | renew automatically |

### response content

| name      | type    | required | description              |
| ---       | ---     | ---      | ---                      |
| orderId   | Integer | yes      | investment order id      |
| autoRenew | Boolean | yes      | status of autoRenew flag |


## Redeem Investment

> request

```json
{
    "orderId": 1,
    "amount": 12.34
}
```

`POST /api/v3.3/invest/redeem`

Redeem an investment order. Requires `Wallet` permission.

### request parameters

| name    | type    | required | description         |
| ---     | ---     | ---      | ---                 |
| orderId | Integer | yes      | investment order id |
| amount  | Double  | yes      | redeem amount       |


## Query Investment Orders

> response

```json
[
  {
    "id": 456,
    "name": "eth flex savings",
    "currency": "eth",
    "type": "flex",
    "rate": 1.15,
    "investamt": 10.00000000,
    "interestearned": 0.00031507,
    "nextinterestpayouttime": 1610632800000,
    "starttime": 0,
    "endtime": 0,
    "duration": 86400000,
    "payoutlocktime": 300000,
    "autorenew": false,
    "compounding": true,
    "autorenewsupported": false,
    "dailylimit": 0,
    "redemptionprocessing": false
  }
]
```

`GET /api/v3.3/invest/orders`

Query investment orders. Requires `Wallet` permission.

### response content

| name                   | type    | required | description                      |
| ---                    | ---     | ---      | ---                              |
| id                     | Integer | yes      | order id                         |
| name                   | String  | yes      | product name                     |
| currency               | String  | yes      | currency                         |
| type                   | String  | yes      | product type                     |
| rate                   | Double  | yes      | interest rate                    |
| investment             | Double  | yes      | amount                           |
| interestearned         | Double  | yes      | intereset earned                 |
| nextinterestpayouttime | Integer | yes      | next interest payout time        |
| starttime              | Integer | yes      | start time                       |
| endtime                | Integer | yes      | end time                         |
| duration               | Integer | yes      | duration                         |
| payoutlocktime         | Integer | yes      | lock time of payout              |
| autorenew              | Boolean | yes      | renew automatically              |
| compounding            | Boolean  | yes      | is compounding                   |
| autorenewsupported     | Boolean | yes      | is renew automatically supported |
| redemptionprocessing   | Boolean | yes      | is redemption processing         |


## Query Investment History

> response

```json
[
  {
    "txntime": 1598918400000,
    "name": "usdt flex savings",
    "currency": "usdt",
    "rate": 0.5,
    "type": "flex",
    "txntype": "invest_service_type_deposit",
    "amount": 100,
    "totalamount": 2000,
    "interestearned": 1.22,
    "duration": 0
  }
]
```

`GET /api/v3.3/invest/history`

Query investment history. Requires `Wallet` permission.

### response content

| name           | type    | required | description                    |
| ---            | ---     | ---      | ---                            |
| txntime        | Integer | yes      | transaction time               |
| name           | String  | yes      | product name                   |
| currency       | String  | yes      | currency                       |
| rate           | String  | yes      | interest rate                  |
| type           | Boolean | yes      | product type                   |
| txntype        | String  | yes      | transaction type               |
| amount         | Double  | yes      | transaction amount             |
| totalamount    | Double  | yes      | total amount of the investment |
| interestearned | Double  | yes      | interest earned                |
| duration       | Boolean | yes      | duration                       |


# Order Book Websocket Streams

## Endpoints
  * Production
     * `wss://ws.btse.com/ws/oss/spot`
  * Testnet
     * `wss://testws.btse.io/ws/oss/spot`

## OSS L1 Snapshot

> Request

```json
{
  "op": "subscribe",
  "args": [
    "snapshotL1:BTC-USD"
  ]
}

{
  "op": "unsubscribe",
  "args": [
    "snapshotL1:BTC-USD"
  ]
}
```

> Response

```json
{
  "topic": "snapshotL1:BTC-USD",
  "data": {
    "bids": [
      [
          "28016.7",
          "1.48063"
      ]
    ],
    "asks": [
      [
          "28033.6",
          "1.34133"
      ]
    ],
    "type": "snapshotL1",
    "symbol": "BTC-USD",
    "timestamp": 1680750154232
  }
}
```

Subscribe to the Level 1 Orderbook through the endpoint `wss://ws.btse.com/ws/oss/spot`. The format to subscribe to will be `symbol`.

* `symbol` indicates the market symbol

### Response Content

#### Orderbook Object

| Name  | Type        | Required | Description                |
| ---   | ---         | ---      | ---                        |
| topic | String      | Yes      | Websocket topic            |
| data  | Data Object | Yes      | Refer to data object below |

#### Data Object

| Name      | Type         | Required | Description         |
| ---       | ---          | ---      | ---                 |
| bids      | Quote Object | Yes      | Bid quotes          |
| asks      | Quote Object | Yes      | Asks quotes         |
| symbol    | String       | Yes      | Market symbol       |
| type      | String       | Yes      | `snapshotL1` - L1 data refers to the best bid / best ask of a trading pair’s order book.   |
| timestamp | Long         | Yes      | Orderbook timestamp |

## Orderbook Incremental Updates

> Request

```json
{
  "op": "subscribe",
  "args": [
    "update:BTC-USD_0"
  ]
}
```

```json
{
  "op": "unsubscribe",
  "args": [
    "update:BTC-USD_0"
  ]
}
```

> Response

```json
{
  "topic": "update:BTC-USD_0",
  "data": {
    "bids": [
      [
        "59252.5",
        "0.06865"
      ],
      [
        "59249.0",
        "0.24000"
      ],
      [
        "59235.5",
        "0.16073"
      ],
      [
        "59235.0",
        "0.26626"
      ],
      [
        "59233.0",
        "0.50000"
      ]
    ],
    "asks": [
      [
        "59292.0",
        "0.50000"
      ],
      [
        "59285.5",
        "0.24000"
      ],
      [
        "59285.0",
        "0.15598"
      ],
      [
        "59282.5",
        "0.06829"
      ],
      [
        "59278.5",
        "0.01472"
      ]
    ],
    "seqNum": 628282,
    "prevSeqNum": 628281,
    "type": "snapshot",
    "timestamp": 1565135165600,
    "symbol": "BTC-USD"
  }
}
```

```json
{
  "topic": "update:BTC-USD",
  "data": {
    "bids": [],
    "asks": [
      [
        "59367.5",
        "2.15622"
      ],
      [
        "59325.5",
        "0"
      ]
    ],
    "seqNum": 628283,
    "prevSeqNum": 628282,
    "type": "delta",
    "timestamp": 1565135165600,
    "symbol": "BTC-USD"
  }
}
```

Subscribe to Orderbook incremental updates through the endpoint `wss://ws.btse.com/ws/oss/spot`. The format of topic will be `update:symbol_grouping` (eg. `update:BTC-USD_0`). The first response received will be a snapshot of the current orderbook (this is indicated in the `type` field) and 50 levels will be returned. Incremental updates will be sent in subsequent packets with type `delta`.

Bids and asks will be sent in `price` and `size` tuples. The size sent will be the new updated size for the price. If a value of `0` is sent, the price should be removed from the local copy of the orderbook.

To ensure that the updates are received in sequence, `seqNum` indicates the current sequence and `prevSeqNum` refers to the packet before. `seqNum` will always be one after the `prevSeqNum`. If the sequence is out of order, you will need to unsubscribe and re-subscribe to the topic again.

Also if [crossed orderbook](https://en.wikipedia.org/wiki/Order_book#Crossed_book) ever occurs when the best bid higher or equal to the best ask, please unsubscribe and re-subscribe to the topic again.

### Response Content

#### Orderbook Object

| Name  | Type        | Required | Description                |
| ---   | ---         | ---      | ---                        |
| topic | String      | Yes      | Websocket topic            |
| data  | Data Object | Yes      | Refer to data object below |

#### Data Object

| Name       | Type         | Required | Description                                                                                                 |
| ---        | ---          | ---      | ---                                                                                                         |
| bids       | Quote Object | Yes      | Bid quotes                                                                                                  |
| asks       | Quote Object | Yes      | Asks quotes                                                                                                 |
| seqNum     | Integer          | Yes      | Current sequence Double                                                                                     |
| prevSeqNum | Integer          | Yes      | Previous sequence Double                                                                                    |
| type       | String       | Yes      | `snapshot` - Snapshot of the orderbook with a maximum of 50 levels<br/> `delta` -  Updates of the orderbook |
| timestamp  | Long         | Yes      | Timestamp of the orderbook                                                                                  |
| symbol     | String       | Yes      | Orderbook symbol                                                                                            |

#### Orderbook Error Response

| Error Code | Message                                                                                |
| ---        | ---                                                                                    |
| 1000       | Market pair provided is currently not supported.                                       |
| 1001       | Operation provided is currently not supported.                                         |
| 1002       | Invalid request. Please check again your request and provide all information required. |
| 1005       | Topic provided does not exist.                                                         |
| 1007       | User message buffer is full.                                                           |
| 1008       | Reached maximum failed attempts, closing the session.                                  |

# Websocket Streams

## Endpoints
  * Production
    * `wss://ws.btse.com/ws/spot`
  * Testnet
    * `wss://testws.btse.io/ws/spot`

## Ping/Pong
For all our WebSocket servers, simply send a 'ping' message, and the WebSocket server will respond with a 'pong' message if the WebSocket connection is established and active.
> Request

```
ping
```

> Response

```
pong
```

## Subscription

> request

```json
{
  "op": "subscribe",
  "args": [
    "tradeHistoryApi:BTC-USD"
  ]
}
```

> response

```json
{
  "event": "subscribe",
  "channel": [
    "tradeHistoryApi:BTC-USD"
  ]
}
```

to subscribe to a websocket public trade fill

### request parameters

| name | type   | required | description                                                                                                            |
| ---  | ---    | ---      | ---                                                                                                                    |
| op   | String | yes      | operation. `subscribe` will subscribe to the topics provided in `args`. `unsubscribe` will unsubscribe from the topics |
| args | Array  | yes      | topics to subscribe to.                                                                                                |

### response content

| Name    | Type   | Required | Description                                   |
| ---     | ---    | ---      | ---                                           |
| event   | String | Yes      | Respond with the event type                   |
| channel | Array  | Yes      | Topics which have been sucessfully subscribed |




## Public Trade Fills

> Request

```json
{
  "op": "subscribe",
  "args": [
    "tradeHistoryApi:BTC-USD"
  ]
}
```

> Response

```json
{
  "topic": "tradeHistoryApi:BTC-USD",
  "data": [
  {
    "symbol": "BTC-USD",
    "side": "SELL",
    "size": 0.007,
    "price": 5302.8,
    "tradeId": 118974855,
    "timestamp": 1584446020295
  }
  ]
}
```

Subscribe to recent trade feed for a market. The topic will be `tradeHistoryApi:<market>` where `<market>` is the market symbol.

### Response Content

#### TradeHistory Object

| Name  | Type        | Required | Description                |
| ---   | ---         | ---      | ---                        |
| topic | String      | Yes      | Websocket topic            |
| data  | Data Object | Yes      | Refer to data object below |

#### Data Object

| Name      | Type   | Required | Description             |
| ---       | ---    | ---      | ---                     |
| symbol    | String | Yes      | Market symbol           |
| side      | String | Yes      | Trade Side, BUY or SELL |
| size      | Double | Yes      | Transacted size         |
| price     | Double | Yes      | Transacted price        |
| tradeId   | Long   | Yes      | Trade sequence Id       |
| timestamp | Long   | Yes      | Trade timestamp         |

## Authentication

> Request

```json
{
  "op":"authKeyExpires",
  "args":["APIKey", "nonce", "signature"]
}
```

Authenticate the websocket session to subscribe to authenticated websocket topics. Assume we have values as follows:

* `request-nonce`: 1624985375123
* `request-api`: 4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x
* `secret`: 848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx

Our subscription request will be:

```
{
  "op":"authKeyExpires",
  "args":["4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x", "1624985375123", "c410d38c681579adb335885800cff24c66171b7cc8376cfe43da1408c581748156b89bcc5a115bb496413bda481139fb"]
}
```

### Request Parameters

Below details the arguments needed to be sent in.

| Index | Type   | Required | Description                          |
| ---   | ---    | ---      | ---                                  |
| 0     | String | Yes      | First argument is the API key        |
| 1     | Long   | Yes      | Nonce which is the current timestamp |
| 2     | String | Yes      | Generated signature                  |

> Generating a signature

```shell
echo -n "/ws/spot1624985375123"  | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= c410d38c681579adb335885800cff24c66171b7cc8376cfe43da1408c581748156b89bcc5a115bb496413bda481139fb
```


## Notifications

> Request

```json
{
  "op": "subscribe",
  "args": [
    "notificationApiV3"
  ]
}
```

> Response

```json
{
  "topic": "notificationApiV3",
  "data": {
    "symbol": "BTC-USDT",
    "orderID": "789b05fa-dd43-43e8-8626-e229ae216ead",
    "side": "MODE_BUY",
    "orderType": 77,
    "txType": 0,
    "price": 111131,
    "triggerPrice": 0,
    "pegPriceDeviation": 1,
    "stealth": 1,
    "status": 5,
    "timestamp": 1752147703368,
    "avgFilledPrice": 111131,
    "clOrderID": "_W_bjvf1752147703280",
    "maker": false,
    "postOnly": false,
    "orderUserInitiated": true,
    "originalOrderBaseSize": 0,
    "originalOrderQuoteSize": 1000,
    "currentOrderBaseSize": 0,
    "currentOrderQuoteSize": 1000,
    "filledBaseSize": 0.00899,
    "totalFilledBaseSize": 0.00899,
    "remainingBaseSize": 0,
    "remainingQuoteSize": 0.93231,
    "orderCurrency": "USDT",
    "time_in_force": "GTC"
  }
}
```

Receive trade notifications by subscribing to the topic `notificationApiV3`. The websocket feed will push trade level notifications to the subscriber. If topic is subscribed without being authenticated, no messages will be sent.

### Response Content

| Name              | Type    | Required | Description                                                                   |
| ---               | ---     | ---      | ---                                                                           |
| symbol            | String  | Yes      | Market symbol                                                                 |
| orderID           | String  | Yes      | Internal order ID                                                             |
| side              | String  | Yes      | Trade side. BUY or SELL                                                       |
| orderType              | Integer     | Yes      | Order type. Valid values are:<br/>76: Limit order<br/>77: Market order<br/>80: Peg/Algo order  |
| price             | Double  | Yes      | Order price or transcated price                                               |
| avgFilledPrice    | Double  | Yes      | Average filled price                                                          |
| status            | Integer | Yes      | Status with values as follows:<br/>1: MARKET_UNAVAILABLE, Market is currently unavailable<br/>2: ORDER_INSERTED, Order is inserted successfully<br/>4: ORDER_FULLY_TRANSACTED, Order is fully transacted<br/>5: ORDER_PARTIALLY_TRANSACTED, Order is partially transacted<br/>6: ORDER_CANCELLED, Order is cancelled successfully<br/>8: INSUFFICIENT_BALANCE, Insufficient balance in account<br/>9: TRIGGER_INSERTED, Trigger Order is inserted successfully<br/>10: TRIGGER_ACTIVATED, Trigger Order is activated successfully<br/>12: ERROR_UPDATE_RISK_LIMIT, Error in updating risk limit<br/>15: ORDER_REJECTED, Change made to the order was unsuccessful<br/>27: TRANSFER_SUCCESSFUL, Transfer funds between futures and spot is successful<br/>28: TRANSFER_UNSUCCESSFUL, Transfer funds between spot and futures is unsuccessful<br/>41: ERROR_INVALID_RISK_LIMIT, Invalid risk limit was specified<br/>64: STATUS_LIQUIDATION, Account is undergoing liquidation<br/>101: FUTURES_ORDER_PRICE_OUTSIDE_LIQUIDATION_PRICE, Futures order is outside of liquidation price<br/>1003: ORDER_LIQUIDATION, Order is undergoing liquidation<br/>1004: ORDER_ADL, Order is undergoing ADL |
| clOrderID         | String  | Yes      | Custom order ID                                                               |
| maker             | Boolean | Yes      | Indicator to indicate if trade is a maker trade                               |
| remainingSize     | Double  | Yes      | Remaining size on the order                                                   |
| time_in_force     | String  | Yes      | Validity of the order                                                         |
| timestamp         | Long    | Yes      | Order timestamp or transacted timestamp                                       |
| stealth           | Double  | Yes      | Percentage of orders to show on orderbook. Only for Algo orders               |
| pegPriceDeviation | Double  | Yes      | Deviation percentage. Only for Algo orders                                    |
| triggerPrice      | Double  | Yes      | Trigger Price                                                                 |
| txType            | Integer  | Yes      | Used by trigger or OCO orders. </br>0: Limit</br>1: Stop</br>2: Trigger</br>3: OCO</br>STOP indicates its a Stop order, TAKEPROFIT indicates its a take profit order, and LIMIT is when its not any of the above    |
| originalOrderBaseSize                 | Double  | Yes      | The original order quantity in base currency. This value will not change even if adjustments are made later.                                                                           |
| originalOrderQuoteSize                 | Double  | Yes      | The original order quantity in quote currency. This value will not change even if adjustments are made later.                                                                           |
| currentOrderBaseSize                 | Double  | Yes      | The latest order quantity in base currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| currentOrderQuoteSize                 | Double  | Yes      | The latest order quantity in quote currency, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                           |
| remainingOrderBaseSize                 | Double  | Yes      | The remaining order quantity in base currency = Current Order Base Size - Filled Base Size.                                                                           |
| remainingOrderQuoteSize                 | Double  | Yes      | The remaining order quantity in quote currency = Current Order Quote Size - Filled Quote Size.                                                                           |
| filledBaseSize                 | Double  | Yes      | The quantity of the order in base currency that has been filled.                                                                           |
| totalFilledBaseSize                 | Double  | Yes      | Cumulative filled quantity of this order in base currency.                                                                           |
| orderCurrency                 | Double  | Yes      | "base" or "quote"                                                                           |

## User Trade Fills

> Request

```json
{
    "op":"subscribe",
    "args":["fills"]
}

```

> Response

```json
{
  "topic": "fills",
  "data": [{
    "orderId": "order id",
    "serialId": "serial ID after insertion into DB",
    "clOrderId": "Client Order ID",
    "type": "order type",
    "symbol": "ex: BTC-USD",
    "side": "BUY|SELL",
    "price": "filled price",
    "size": "filled size",
    "feeAmount": "Fees charged to user, value to be String on API",
    "feeCurrency": "Fee currency, eg. Buy would be BTC, Sell would be USD",
    "base": "Base currency, eg. BTC",
    "quote": "Quote currency eg. USD",
    "maker": "maker or taker",
    "timestamp": "Time trade was matched in the engine",
    "tradeId": "Trade Unique ID"
  }]
}


```

When a trade has been transacted, this topic will send the trade information back to the subscriber.

### Response Content

| Name        | Type    | Required | Description                                                                                   |
| ---         | ---     | ---      | ---                                                                                           |
| symbol      | String  | Yes      | Market symbol                                                                                 |
| orderId     | String  | Yes      | Internal order ID                                                                             |
| clOrderId   | String  | Yes      | Custom order ID                                                                               |
| serialId    | String  | Yes      | Trade sequence ID                                                                             |
| tradeId     | String  | Yes      | Trade unique identifier                                                                       |
| type        | Integer     | Yes      | Order type. Valid values are:<br/>76: Limit order<br/>77: Market order<br/>80: Peg/Algo order |
| side        | String  | Yes      | Trade side. BUY or SELL                                                                       |
| price       | Double  | Yes      | Transcated price                                                                              |
| size        | Double  | Yes      | Transacted size                                                                               |
| feeAmount   | Double  | Yes      | Fee amount charged                                                                            |
| feeCurrency | String  | Yes      | Fee currency                                                                                  |
| base        | String  | Yes      | Base currency                                                                                 |
| quote       | String  | Yes      | Quote currency                                                                                |
| maker       | Boolean | Yes      | Indicator to indicate if trade is a maker trade                                               |
| timestamp   | Long    | Yes      | Order timestamp or transacted timestamp                                                       |

</section>
