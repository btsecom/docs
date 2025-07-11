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

## Migration from v2.2 to v2.3

We are updating several order-related API endpoints to improve consistency and clarity in size-related fields. Please review the following changes carefully, as some existing fields will be deprecated and replaced with new ones.

### Updated Fields for Order Actions 

For the following endpoints, the fields `size`, `fillSize` and `originalSize` will be deprecated and replaced with the following:

  * `originalOrderSize`
  * `currentOrderSize`
  * `filledSize`
  * `totalFilledSize`

**Affected Endpoints**

  * [`Create New Order`](#create-new-order)
  * [`Amend Order`](#amend-order)
  * [`Cancel Order`](#cancel-order)
  * [`Create New Algo Order`](#create-new-algo-order)
  * [`Bind TP/SL`](#bind-tp-sl)
  * [`Close Position`](#close-position)

### Updated Fields for Order Query

For the following endpoints, `size` and `filledSize` will be deprecated, and replaced by:

  * `originalOrderSize`
  * `currentOrderSize`
  * `totalFilledSize`

**Affected Endpoints**

  * [`Query Order`](#query-order)
  * [`Query Open Orders`](#query-open-orders)

**Updated Fields for Notifications** 

For [`Notifications`](#notifications), the fields `size`, `fillSize`, `originalSize` will be deprecated and replaced with:

* `originalOrderSize`
* `currentOrderSize`
* `filledSize`
* `totalFilledSize`

### WebSocket Consistency Update

We are also improving consistency across WebSocket topics between subscription requests and data notifications.


## Generating API Key

You will need to create an API key on the BTSE platform before you can use authenticated APIs. To create API keys, you can follow the steps below:

* Login with your username / email and password into the BTSE website
* Click on “Account” on the top right hand corner
* Select the API tab
* Click on “New API” button to create an API key and passphrase. (Note: the passphrase will only appear once)
* Use your API key and passphrase to construct a signature.

## Endpoints

* Production
  * HTTP
     * `https://api.btse.com/futures`
  * Websocket
     * `wss://ws.btse.com/ws/futures`
  * Websocket (for orderbook stream)
     * `wss://ws.btse.com/ws/oss/futures` (Used for Orderbook incremental update stream)
* Testnet
  * HTTP
     * `https://testapi.btse.io/futures`
  * Websocket
     * `wss://testws.btse.io/ws/futures`
  * Websocket (for orderbook stream)
     * `wss://testws.btse.io/ws/oss/futures` (Used for Orderbook incremental update stream)

## Authentication

* API Key (request-api)
  * Parameter Name: `request-api`, in: header. API key is obtained from BTSE platform as a string

* API Key (request-nonce)
  * Parameter Name: `request-nonce`, in: header. Representation of current timestamp in long format

* API Key (request-sign)
  * Parameter Name: `request-sign`, in: header. A composite signature produced based on the following algorithm: Signature=HMAC.Sha384 (secretkey, (urlpath + request-nonce + bodyStr)) (note: bodyStr = '' when no data):

### Example 1: Get Wallet

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v2.3/user/wallet1624984297330" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 2c41ab59d24d4e807ab035ef2fd4619c928320cac319751e7be2ecd03e5bf6dd31a4c85db88535bbe3e012b22d312290
```

* Endpoint to get wallet is `https://api.btse.com/futures/api/v2.3/user/wallet`
* Assume we have the values as follows:
  * request-nonce: `1624984297330`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v2.3/user/wallet`
* Generated signature will be:
  * request-sign: `2c41ab59d24d4e807ab035ef2fd4619c928320cac319751e7be2ecd03e5bf6dd31a4c85db88535bbe3e012b22d312290`

### Example 2: Place an order

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v2.3/order1624985375123{\"postOnly\":false,\"price\":8500.0,\"reduceOnly\":false,\"side\":\"BUY\",\"size\":1,\"stopPrice\":0.0,\"symbol\":\"BTC-PERP\",\"time_in_force\":\"GTC\",\"trailValue\":0.0,\"triggerPrice\":0.0,\"txType\":\"LIMIT\",\"type\":\"LIMIT\"}" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 1794da8c6090ed2d97a85f5b3bae89d7993b4f2db809da7abe24be5fb70b63fea7320b321929c4ee9e3eda083ecf837f
```

* Endpoint to place an order is `https://api.btse.com/futures/api/v2.3/order`
* Assume we have the values as follows:
  * request-nonce: `1624985375123`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v2.3/order`
  * Body: `{"postOnly":false,"price":8500.0,"reduceOnly":false,"side":"BUY","size":1,"stopPrice":0.0,"symbol":"BTC-PERP","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
  * Encrypted Text: `/api/v2.3/order1624985375123{"postOnly":false,"price":8500.0,"reduceOnly":false,"side":"BUY","size":1,"stopPrice":0.0,"symbol":"BTC-PERP","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
* Generated signature will be:
  * request-sign: `1794da8c6090ed2d97a85f5b3bae89d7993b4f2db809da7abe24be5fb70b63fea7320b321929c4ee9e3eda083ecf837f`


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
* 451 - Unavailable For Legal Reasons. Indicates that the client has been banned because abnormal behavior
* 500 - Internal server error. Indicates that the server encountered an unexpected condition resulting in not being able to fulfill the request

## API Enum

When connecting up the BTSE API, you will come across Double codes that represents different states or status types in BTSE. The following section provides a list of codes that you are expecting to see.

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
* 129: FUTURES_CONFIG_MODE_CHANGE
* 131: FUTURES_STATUS_PROCESSING_LEVERAGE
* 132: FUTURES_STATUS_PROCESSING_RISK_LIMIT
* 133: FUTURES_POSITION_MODE_INVALID
* 134: POSITION_MODE_UNCHANGEABLE
* 138: POSITION_MODE_CHANGE_PROCESSING
* 300: ERROR_MAX_ORDER_SIZE_EXCEEDED
* 301: ERROR_INVALID_ORDER_SIZE
* 302: ERROR_INVALID_ORDER_PRICE
* 303: ERROR_RATE_LIMITS_EXCEEDED
* 304: ERROR_MAX_OPEN_ORDER_EXCEEDED
* 305: ERROR_ORDER_PRICE_OUT_OF_PRICE_PROTECTION_RANGE
* 1003: ORDER_LIQUIDATION = Order is undergoing liquidation
* 1004: ORDER_ADL = Order is undergoing ADL
* 30410: BLOCK_TRADE_COMPLETE_SUCCESS

## Spam Orders

Spam orders are large number of small order sizes that is placed. In order to ensure that the platform and user's interests are protected from malicious players, we will apply the following for users placing small sized orders.

[Spam Order Detection Mechanism : BTSE Support](https://support.btse.com/en/support/solutions/articles/43000720904-spam-order-detection-mechanism)

* Orders with a notional value below 5 USDT will be marked as a spam order and will automatically become hidden orders.
* Orders marked as spam always pay the taker fee.
* Post-Only API orders marked as spam will be rejected instead of being hidden.
* Too many spam orders may be grounds to temporarily ban an account from trading.
* API accounts placing >= 4 resting orders, with total size less than 20 USDT are at risk of being marked as a spam account.
* Accounts marked as spam may have limitations placed on the account, including order rate limits, position limits, or have API functions disabled. For questions regarding the new spam order mechanism, please email mm@btse.com.

# Public Endpoints

## Market Summary

> Response

```json
[
  {
    "symbol": "BTC-PERP",
    "last": 36365,
    "lowestAsk": 36377,
    "highestBid": 36376,
    "percentageChange": 4.973731309,
    "volume": 172418318.7575521,
    "high24Hr": 36447,
    "low24Hr": 33989.5,
    "base": "BTC",
    "quote": "USDT",
    "active": true,
    "size": 4916.8266,
    "minValidPrice": 0.5,
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
    "fundingIntervalMinutes": 480,
    "fundingTime": 1699347600000
  }
]
```

`GET /api/v2.3/market_summary`

Gets market summary information. If no symbol parameter is sent, then all markets will be retrieved.

### Request Parameters

| Name               | Type    | Required | Description                                                            |
| ---                | ---     | ---      | ---                                                                    |
| symbol             | String  | No       | Market symbol                                                          |
| listFullAttributes | Boolean | No       | True to return all attributes of the market summary |

### Response Content

| Name                | Type    | Required | Description                                                                                           |
| ---                 | ---     | ---      | ---                                                                                                   |
| symbol              | String  | Yes      | Market symbol                                                                                         |
| last                | Double  | Yes      | Last price                                                                                            |
| lowestAsk           | Double  | Yes      | Lowest ask price in the orderbook                                                                     |
| highestBid          | Double  | Yes      | Highest bid price in the orderbook                                                                    |
| percentageChange    | Double  | Yes      | Percentage change against the price within the last 24hours                                           |
| volume              | Double  | Yes      | Transacted volume                                                                                     |
| high24Hr            | Double  | Yes      | Highest price over the last 24hours                                                                   |
| low24Hr             | Double  | Yes      | Lowest price over the last 24hours                                                                    |
| base                | String  | Yes      | Base currency                                                                                         |
| quote               | String  | Yes      | Quote currency                                                                                        |
| active              | Boolean | Yes      | Indicator if market is active                                                                         |
| size                | Double  | Yes      | Transacted size                                                                                       |
| minValidPrice       | Double  | Yes      | Minimum valid price                                                                                   |
| minPriceIncrement   | Double  | Yes      | Price increment                                                                                       |
| minOrderSize        | Double  | Yes      | Minimum tick size                                                                                     |
| minSizeIncrement    | Double  | Yes      | Tick size                                                                                             |
| maxOrderSize        | Double  | Yes      | Maximum order size                                                                                    |
| openInterest        | Double  | No       | Number of open positions in the futures market                                                        |
| openInterestUSD     | Double  | No       | Number of open positions in the futures market in USD notional value                                  |
| contractStart       | Long    | No       | Contract start time                                                                                   |
| contractEnd         | Long    | No       | Contract end time                                                                                     |
| timeBasedContract   | Boolean | No       | Indicator to indicate if it is a time based contract                                                  |
| openTime            | Long    | Yes      | Market opening time                                                                                   |
| closeTime           | Long    | Yes      | Market closing time                                                                                   |
| startMatching       | Long    | Yes      | Matching start time                                                                                   |
| inactiveTime        | Long    | Yes      | Time where market is inactive                                                                         |
| fundingRate         | Double  | No       | The funding rate                                                                      |
| contractSize        | Double  | No       | Size of one contract                                                                                  |
| maxPosition         | Double  | No       | Maximum position a user is allowed to have `Will no longer be applicable after risk limit adjustment` |
| minRiskLimit        | Double  | No       | Minimum risk limit in contract size  `Will be changed to USD value`                                   |
| maxRiskLimit        | Double  | No       | Maximum risk limit Integer contract size `Will be changed to USD value`                                   |
| availableSettlement | Array   | No       | Currencies available for settlement                                                                   |
| futures             | Boolean | Yes      | Indicator if symbol is a futures contract                                                             |
| fundingIntervalMinutes             | Integer | No      | Funding interval, only display when param `listFullAttributes` is true|
| fundingTime             | Long | No      | Next funding time, only display when param `listFullAttributes` is true|

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

`GET /api/v2.3/ohlcv`

Gets candle stick charting data. Default of 300 data points will be returned at any one time.

### Request Parameters

| Name               | Type    | Required | Description                                                                                                                                                                                          |
| ---                | ---     | ---      |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol             | String  | Yes      | Market symbol                                                                                                                                                                                        |
| start              | Long    | No       | Starting time in milliseconds (eg. 1624987283000)                                                                                                                                                    |
| end                | Long    | No       | Ending time in millisecond (eg. 1624987283000)                                                                                                                                                       |
| resolution         | String  | Yes      | Supported resolutions are: <br/> 1: 1 min<br/> 5: 5 mins<br/> 15: 15 mins<br/>30: 30 mins<br/>60: 60 mins<br/>240: 4 hours<br/>360: 6 hours<br/>1440: 1day<br/>10080: 1 week<br/>43200: 1 month |


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
    "symbol": "BTC-PERP",
    "indexPrice": 36288.949684967,
    "lastPrice": 36286.5,
    "markPrice": 0
  }
]
```

`GET /api/v2.3/price`

Retrieve current prices on the platform. If no symbol specified, all symbols will be returned.

### Request Parameters

| Name               | Type    | Required | Description                                                     |
| ---                | ---     | ---      | ---                                                             |
| symbol             | String  | Yes      | Market symbol                                                   |

### Response Content

| Name       | Type   | Required | Description           |
| ---        | ---    | ---      | ---                   |
| symbol     | Double | Yes      | Market symbol         |
| indexPrice | Double | Yes      | Index price           |
| lastPrice  | Double | Yes      | Last transacted price |
| markPrice  | Double | Yes      | Mark price            |

## Orderbook (By grouping)

> Response

```json
{
  "buyQuote": [
    {
      "price": "36371.0",
      "size": "100"
    }
  ],
  "sellQuote": [
    {
      "price": "36380.5",
      "size": "100"
    }
  ],
  "timestamp": 1624989459489,
  "symbol": "BTC-PERP"
}
```

`GET /api/v2.3/orderbook`

Retrieves a snapshot of the orderbook.

### Request Parameters

| Name               | Type    | Required | Description                                                                                                                                                                                                           |
|--------------------| ---     | ---      |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol             | String  | Yes      | Market symbol, entered as a path variable                                                                                                                                                                             |
| group              | Integer | No       | Orderbook grouping. Valid values are: <br/>0-8 where 0 indicates level 0 grouping (eg. for BTC-PERP, it will be 0.1)<br/>Level 1 grouping for BTC-PERP would be 0.5<br/>Level 2 grouping for BTC-PERP would be 1<br/> |

### Response Content

#### Orderbook

| Name      | Type          | Required | Description            |
| ---       | ---           | ---      | ---                    |
| symbol    | String        | Yes      | Market symbol          |
| buyQuote  | Quote Object  | Yes      | Array of Buy quotes    |
| sellQuote | Quote Object  | Yes      | Array of Sell quotes   |
| timestamp | Long          | Yes      | Timestamp of orderbook |

#### Quote Object

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
      "size": "700"
    }
  ],
  "sellQuote": [
    {
     "price": "36241.5",
      "size": "600"
    }
  ],
  "timestamp": 1624989977940,
  "symbol": "BTC-PERP"
}
```

`GET /api/v2.3/orderbook/L2`

Retrieves a Level 2 snapshot of the orderbook

### Request Parameters

| Name               | Type    | Required | Description                                                            |
| ---                | ---     | ---      | ---                                                                    |
| symbol             | String  | Yes      | Market symbol                                                          |
| depth              | Long    | No       | Orderbook depth                                                        |

### Response Content

#### Orderbook

| Name      | Type          | Required | Description            |
| ---       | ---           | ---      | ---                    |
| symbol    | String | Yes  | Market symbol          |
| buyQuote  | Quote Object  | Yes      | Array of Buy quotes    |
| sellQuote | Quote Object  | Yes      | Array of Sell quotes   |
| timestamp | Long          | Yes      | Timestamp of orderbook |

#### Quote Object

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
    "size": 100,
    "side": "SELL",
    "symbol": "BTC-PERP",
    "serialId": 85997835,
    "timestamp": 1624990097000
  }
]
```

`GET /api/v2.3/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

| Name               | Type    | Required | Description                                                                       |
| ---                | ---     | ---      | ---                                                                               |
| symbol             | String  | Yes      | Market symbol                                                                     |
| startTime          | Long    | No       | Starting time in milliseconds (eg. 1624987283000)                                 |
| endTime            | Long    | No       | Ending time in milliseconds (eg. 1624987283000)                                   |
| beforeSerialId     | Long  | No      | Used for pagination to retrieve records when the order volume exceeds **500 per millisecond**. For typical scenarios, it is recommended to use the `startTime` and `endTime` parameters instead. |
| afterSerialId      | Long  | No      | Used for pagination to retrieve records when the order volume exceeds **500 per millisecond**. For typical scenarios, it is recommended to use the `startTime` and `endTime` parameters instead. |
| count              | Long    | Yes      | Number of records to return                                                       |
| includeOld         | Boolean | Yes      | Retrieve trade  history records past 7 days                                       |

### Response Content

| Name      | Type   | Required | Description                             |
| ---       | ---    | ---      | ---                                     |
| symbol    | String | Yes      | Market symbol                           |
| side      | String | Yes      | Trade side. Values are: [`Buy`, `SELL`] |
| price     | Double | Yes      | Transacted price                        |
| size      | Double | Yes      | Transacted size                         |
| serialId  | Long   | Yes      | Serial Id, running sequence Long      |
| timestamp | Long   | Yes      | Transacted timestamp                    |


## Funding History

> Response

```json
{
  "BTC-PERP": [
    {
      "time": 1706515200,
      "rate": 0.000011405,
      "symbol": "BTC-PERP"
    }
  ]
}
```

`GET /api/v2.3/funding_history`

Get funding rate history for certain symbols

### Request Parameters

| Name               | Type    | Required | Description                                                                        |
| ---                | ---     | ---      | ---                                                                                |
| symbol             | String  | No       | Market symbol (e.g., BTC-PERP)                                                     |
| count              | Integer     | No       | Number of records to return (mutually exclusive with from/to)                      |
| from               | Long    | No       | Starting time in milliseconds (e.g., 1624987283000; mutually exclusive with count) |
| to                 | Long    | No       | Ending time in milliseconds (e.g., 1624987283000; mutually exclusive with count)   |

### Response Content

| Name      | Type   | Required | Description                                       |
| ---       | ---    | ---      | ---                                               |
| symbol    | String | Yes      | Market symbol                                     |
| time      | Long   | Yes      | The epoch timestamp in second of the funding rate |
| rate      | Double | Yes      | Funding rate                                      |


## Market Risk Limit Setting

> Response ( Successful )

```json
{
    "code": 1,
    "msg": "Success",
    "time": 1747207591721,
    "data": [
        {
            "symbol": "SOL-PERP",
            "riskLevel": 1,
            "riskLimitValue": 10000,
            "initialMarginRate": 0.02,
            "maintenanceMarginRate": 0.015,
            "maxLeverage": 50
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 2,
            "riskLimitValue": 20000,
            "initialMarginRate": 0.025,
            "maintenanceMarginRate": 0.02,
            "maxLeverage": 40
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 3,
            "riskLimitValue": 30000,
            "initialMarginRate": 0.03,
            "maintenanceMarginRate": 0.025,
            "maxLeverage": 33.33
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 4,
            "riskLimitValue": 40000,
            "initialMarginRate": 0.035,
            "maintenanceMarginRate": 0.03,
            "maxLeverage": 28.57
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 5,
            "riskLimitValue": 50000,
            "initialMarginRate": 0.04,
            "maintenanceMarginRate": 0.035,
            "maxLeverage": 25
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 6,
            "riskLimitValue": 60000,
            "initialMarginRate": 0.045,
            "maintenanceMarginRate": 0.04,
            "maxLeverage": 22.22
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 7,
            "riskLimitValue": 70000,
            "initialMarginRate": 0.05,
            "maintenanceMarginRate": 0.045,
            "maxLeverage": 20
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 8,
            "riskLimitValue": 80000,
            "initialMarginRate": 0.055,
            "maintenanceMarginRate": 0.05,
            "maxLeverage": 18.18
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 9,
            "riskLimitValue": 90000,
            "initialMarginRate": 0.06,
            "maintenanceMarginRate": 0.055,
            "maxLeverage": 16.67
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 10,
            "riskLimitValue": 100000,
            "initialMarginRate": 0.065,
            "maintenanceMarginRate": 0.06,
            "maxLeverage": 15.38
        }
    ],
    "success": true
}
```

> Response ( Failed to find the market )

```json
{
    "code": -2,
    "msg": "Invalid request parameters",
    "time": 1747207833879,
    "data": null,
    "success": false
}
```

`GET /api/v2.3/market/risk_limit`

Gets all default market settings, including initial margin and maintenance margin by each market and each risk limit level. You'll retrieve all markets if no symbol parameter is sent.

### Request Parameters

| Name               | Type    | Required | Description                                                            |
| ---                | ---     | ---      | ---                                                                    |
| symbol             | String  | No       | Market symbol              |

### Response Content

| Name                     | Type     | Required | Description                                                                                           |
| ---                      | ---      | ---      | ---                                                                                                   |
| code                     | Integer   | Yes     | Response code                                                                                                  |
| msg                      | Integer  | Yes      | Response message                                                                                               |
| time                     | Integer  | Yes      | Response Time                                                                                                  |
| data                     | Object   | No       |  Refer to data object below                                                                                                 |
| success                  | Boolean   | Yes      | Whether or not query is successful                                                                                                  |

### Data Object

| Name                     | Type     | Required | Description                                                                                           |
| ---                      | ---      | ---      | ---                                                                                                   |
| symbol                   | String   | Yes      | Market symbol                                                                                                |
| riskLevel                | Integer  | Yes      | Risk level                                                                                                 |
| riskLimitValue           | Integer  | Yes      | Risk limit value for current risk level in coin size                                                                                                  |
| initialMarginRate        | Double   | Yes      | Initial margin rate                                                                                     |
| maintenanceMarginRate    | Double   | Yes      | Maintenance margin rate                                                                                                  |
| maxLeverage              | Double   | Yes      | Max leverage for current risk level                                                                                                  |


# Trade Endpoints

## Create New Order

> Request (create `MARKET` order)

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "side": "BUY",
  "type": "MARKET"
}
```
> Request (create `LIMIT` order)

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "price": 21000,
  "side": "BUY",
  "type": "LIMIT"
}
```
> Request (create `LIMIT` `TRIGGER` order)

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "price": 21000,
  "side": "BUY",
  "type": "LIMIT",
  "txType": "TRIGGER",
  "triggerPrice": 30000
}
```
> Request (create `LIMIT` `STOP` order)

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "price": 21000,
  "side": "BUY",
  "type": "LIMIT",
  "txType": "STOP",
  "triggerPrice": 30000
}
```
> Request (create `OCO` order)

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "price": 21000,
  "side": "BUY",
  "type": "OCO",
  "txType": "LIMIT",
  "trigger": "markPrice",
  "stopPrice": 30010,
  "triggerPrice": 30000
}
```

> Request (create `Limit` order with `TP/SL`)

```json
{
    "symbol": "BTC-PERP",
    "size": 10,
    "price": 29000,
    "side": "BUY",
    "type": "LIMIT",
    "takeProfitPrice": 31000,
    "takeProfitTrigger": "markPrice",
    "stopLossPrice": 27000,
    "stopLossTrigger": "lastPrice"
}
```
> Request (create `Limit` order with `TP` only)

```json
{
    "symbol": "BTC-PERP",
    "size": 10,
    "price": 29000,
    "side": "BUY",
    "type": "LIMIT",
    "takeProfitPrice": 31000,
    "takeProfitTrigger": "markPrice"
}
```

> Request (create `Limit` order with `SL` only)

```json
{
    "symbol": "BTC-PERP",
    "size": 10,
    "price": 29000,
    "side": "BUY",
    "type": "LIMIT",
    "stopLossPrice": 27000,
    "stopLossTrigger": "lastPrice"
}
```

> Request (create hedge mode long position `MARKET` order)

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "side": "BUY",
  "type": "MARKET",
  "positionMode": "HEDGE"
}
```


> Request (create hedge mode short position `MARKET` reduce order)

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "side": "BUY",
  "type": "MARKET",
  "reduceOnly": true,
  "positionMode": "HEDGE"
}
```

> Response (general)

```json
[
  {
    "status": 4,
    "symbol": "BTC-PERP",
    "orderType": 77,
    "price": 111199.8,
    "side": "BUY",
    "orderID": "52cdd4ce-bf2e-4b8c-b286-4129ad1ab662",
    "timestamp": 1752138139421,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 111199.8,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 1,
    "totalFilledSize": 1,
    "remainingSize": 0,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

> Response (for `OCO` order)

```json
[
  {
    "status": 9,
    "symbol": "BTC-PERP",
    "orderType": 76,
    "price": 111255.6,
    "side": "BUY",
    "orderID": "977e8486-64c3-4faa-9d44-ed187785f594",
    "timestamp": 1752138472048,
    "triggerPrice": 111255.6,
    "trigger": true,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 0,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  },
  {
    "status": 2,
    "symbol": "BTC-PERP",
    "orderType": 76,
    "price": 111055.6,
    "side": "BUY",
    "orderID": "9c1dea07-e7b7-448a-a16d-40c11809cee1",
    "timestamp": 1752138472047,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 1,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

> Response (for hedge mode order)

```j[
  {
    "status": 2,
    "symbol": "BTC-PERP",
    "orderType": 76,
    "price": 110078.1,
    "side": "BUY",
    "orderID": "738ef757-88e1-46d4-87b2-b24dd43e01db",
    "timestamp": 1752141497172,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 1,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "HEDGE",
    "positionDirection": "LONG",
    "positionId": "BTC-PERP-USDT|LONG",
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.3/order`

Creates a new order. Requires `Trading` permission.

### Request Parameters

| Name          | Type    | Required | Description                                                                                                                                                                                                                                                                                                                                                        |
|---------------| ---     | ---      |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol        | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                                                                                      |
| price         | Double  | No       | Mandatory unless creating a MARKET order. Order price                                                                                                                                                                                                                                                                                                              |
| size          | Long    | Yes      | Order size in `contract size` (this remains unchanged even after risk limit adjustment)                                                                                                                                                                                                                                                                            |
| side          | String  | Yes      | 'BUY' or 'SELL'                                                                                                                                                                                                                                                                                                                                                    |
| time_in_force | String  | No       | Time validity of the order<br/>GTC: Good till Cancel<br/>IOC: Immediate or Cancel<br/>FOK: Fill or Kill<br/>HALFMIN: Order valid for 30 seconds<br/>FIVEMIN: Order valid for 5 mins<br/> HOUR: Order valid for an hour<br/>TWELVEHOUR: Order valid for 12 hours<br/>DAY: Order valid for a day<br/>WEEK: Order valid for a week<br/>MONTH: Order valid for a month |
| type          | String  | Yes      | Order type<br/>LIMIT: Limit Orders<br/>MARKET: Market Orders<br/>OCO: One cancel the other                                                                                                                                                                                                                                                                         |
| txType        | String  | No       | Used for Stop orders or trigger orders<br/>STOP: Stop Order, `triggerPrice` is mandatory<br/>TRIGGER: Trigger order, `triggerPrice` is mandatory<br/>LIMIT: Default, used when its not a Stop order nor Trigger order                                                                                                                                              |
| stopPrice     | Double  | No       | Mandatory when creating an OCO order. Indicates the stop price                                                                                                                                                                                                                                                                                                     |
| triggerPrice  | Double  | No       | Mandatory when creating a Stop, Trigger, OCO order. Indicates the trigger price                                                                                                                                                                                                                                                                                    |
| trailValue    | Double  | No       | Trail value                                                                                                                                                                                                                                                                                                                                                        |
| postOnly      | Boolean | No       | Boolean to indicate if this is a post only order. For post only orders, traders are charged maker fees                                                                                                                                                                                                                                                             |
| reduceOnly    | Boolean | No       | Boolean to indicate if this is a reduce only order, if in hedge mode, it is used to reduce the specified position, ex: sell to reduce Long position, buy to reduce short position.                                                                                                                                                                                 |
| clOrderID     | String  | No       | Custom order Id                                                                                                                                                                                                                                                                                                                                                    |
| trigger       | String  | No       | For creating order with txType: `STOP` or `TRIGGER`. Valid options: `markPrice` (default) or `lastPrice`|
| takeProfitPrice  | Double  | No       | Mandatory when creating new order with take profit order. Indicates the trigger price
| takeProfitTrigger       | String  | No       | For creating order with take profit order. Valid options: `markPrice` (default) or `lastPrice`|
| stopLossPrice  | Double  | No       | Mandatory when creating new order with stop loss order. Indicates the trigger price
| stopLossTrigger       | String  | No       | For creating order with stop loss order. Valid options: `markPrice` (default) or `lastPrice`|
| positionMode  | String  | No       | For creating order and wanting to specify the positionMode. Valid options: `ONE_WAY` (default) , `HEDGE` , `ISOLATED`                                                                                                                                                                                                                                                          |

### Response Content

| Name              | Type    | Required | Description                                                                                                                                                                                                                                                                                     |
|-------------------| ---     |----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol            | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                   |
| clOrderID         | String  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                                                  |
| orderID           | String  | Yes      | Order ID                                                                                                                                                                                                                                                                                        |
| orderType         | Integer  | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                                                                         |
| postOnly          | Boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                                         |
| price             | Double  | Yes      | Order price                                                                                                                                                                                                                                                                                     |
| side              | String  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                                                      |
| status            | Integer    | Yes      | Order status<br/> 2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found<br/>17: Request failed |
| time_in_force     | String  | Yes      | Order validity                                                                                                                                                                                                                                                                                  |
| timestamp         | Long    | Yes      | Order timestamp                                                                                                                                                                                                                                                                                 |
| trigger           | Boolean | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                                           |
| triggerPrice      | Double  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                                                  |
| avgFilledPrice      | Double  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                                          |
| message           | String  | Yes      | Trade messages                                                                                                                                                                                                                                                                                  |
| stealth           | Double  | Yes      | Only valid for Algo orders                                                                                                                                                                                                                                                                      |
| deviation         | Double  | Yes      | Only valid for Algo orders                                                                                                                                                                                                                                                                      |
| remainingSize     | Integer  | Yes      | The remaining order quantity = Current order size - Filled size.                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | The original order quantity. This value will not change even if adjustments are made later.                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | The latest order quantity, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                                                                                                                                                                                                                             |
| filledSize          | Integer  | Yes      | The quantity of the order that has been filled.                                                                                                                                                                                                                                                                               |
| totalFilledSize      | Integer  | Yes      | Cumulative filled quantity of this order.                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | Position mode<br/>ONE_WAY, HEDGE or ISOLATED                                                                                                                                                                                                                                                    |
| positionDirection | String  | Yes      | Position direction                                                                                                                                                                                                                                                                              |
| positionId        | String  | Yes      | The current order belongs to the id of position.                                                                                                                                                                                                                                                |

## Create New Algo Order

> Request

```json
{
  "symbol": "BTC-PERP",
  "price": 21500,
  "size": 10,
  "side": "BUY",
  "clOrderID": "60a30188-f2a2-4498-b061-7d72126c18c2",
  "stealth": 10,
  "deviation": -10
}
```

> Response

```json
[
  {
    "status": 2,
    "symbol": "BTC-PERP",
    "orderType": 80,
    "price": 111541.9,
    "side": "BUY",
    "orderID": "7080613e-2d15-42fd-ba25-340c755065fa",
    "timestamp": 1752214790589,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 10,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 1,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.3/order/peg`

Creates a new algo order. Algo order is an order that price will change according to market price. To create an algo order, user will need to enter additional parameters:

* `price`: What is the min price (for a sell order) or maximum price (for a buy order) that a user will be willing to list his order at
* `deviation`: How much should the order price deviate from index price. Value is in percentage and can range from `-10` to `10`
* `stealth`: How many percent of the order is to be displayed on the orderbook.

This API Requires `Trading` permission.

### Request Parameters

| Name         | Type   | Required | Description                                                                                                                                                                       |
|--------------| ---    | ---      | ---                                                                                                                                                                               |
| symbol       | String | Yes      | Market symbol                                                                                                                                                                     |
| price        | Double | Yes      | Minimum price for a sell order, this is the lowest price that a user is willing to sell at. Maximum price for a buy order, this is the maximum price a user is willing to buy at. |
| size         | Long   | Yes      | Order size                                                                                                                                                                        |
| side         | String | Yes      | Order side<br/>BUY or SELL                                                                                                                                                        |
| clOrderID    | String | No       | Custom order Id                                                                                                                                                                   |
| deviation    | Double | No       | How much should the order price deviate from index price. Value is in percentage and can range from `-10` to `10`                                                                 |
| stealth      | Double | No       | How many percent of the order is to be displayed on the orderbook.                                                                                                                |
| positionMode | String  | No       | For creating order and wanting to specify the positionMode. Valid options: `ONE_WAY` (default) , `HEDGE` , `ISOLATED`                                                                                                                                                                                                                                                         |

### Response Content

| Name              | Type    | Required | Description                                                                                                                                                                                                                                                                                     |
|-------------------| ---     | ---      |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol            | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                   |
| clOrderID         | String  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                                                  |
| orderID           | String  | Yes      | Order ID                                                                                                                                                                                                                                                                                        |
| orderType         | Integer  | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                                                                         |
| postOnly          | Boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                                         |
| price             | Double  | Yes      | Order price                                                                                                                                                                                                                                                                                     |
| side              | String  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                                                      |
| status            | Integer    | Yes      | Order status<br/> 2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found<br/>17: Request failed |
| time_in_force     | String  | Yes      | Order validity                                                                                                                                                                                                                                                                                  |
| timestamp         | Long    | Yes      | Order timestamp                                                                                                                                                                                                                                                                                 |
| trigger           | Boolean | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                                           |
| triggerPrice      | Double  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                                                  |
| avgFilledPrice      | Double  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                                          |
| message           | String  | Yes      | Trade messages                                                                                                                                                                                                                                                                                  |
| stealth           | Double  | Yes      | Stealth value of order                                                                                                                                                                                                                                                                          |
| deviation         | Double  | Yes      | Deviation value of order                                                                                                                                                                                                                                                                        |
| remainingSize     | Integer  | Yes      | The remaining order quantity = Current order size - Filled size.                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | The original order quantity. This value will not change even if adjustments are made later.                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | The latest order quantity, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                                                                                                                                                                                                                             |
| filledSize          | Integer  | Yes      | The quantity of the order that has been filled.                                                                                                                                                                                                                                                                               |
| totalFilledSize      | Integer  | Yes      | Cumulative filled quantity of this order.                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | Position mode<br/>ONE_WAY, HEDGE or ISOLATED                                                                                                                                                                                                                                                    |
| positionDirection | String  | Yes  | Position direction                                                                                                                                                                                                                                                                              |
| positionId        | String  | Yes      | The current order belongs to the id of position.                                                                                                                                                                                                                                                |

## Query Order

> Response

```json
{
    "orderType": 80,
    "price": 111541.9,
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "totalFilledSize": 1,
    "remainingSize": 0,
    "side": "BUY",
    "orderValue": 1.115419,
    "pegPriceMin": 1,
    "pegPriceMax": 111541.9,
    "pegPriceDeviation": 0.1,
    "timestamp": 1752138591588,
    "orderID": "956a4e97-c229-42e8-a065-54c8b96f0732",
    "stealth": 1,
    "triggerOrder": false,
    "triggered": false,
    "triggerPrice": 0,
    "triggerOriginalPrice": 0,
    "triggerOrderType": 0,
    "triggerTrailingStopDeviation": 0,
    "triggerStopPrice": 0,
    "symbol": "BTC-PERP",
    "trailValue": 0,
    "clOrderID": "",
    "reduceOnly": false,
    "status": 4,
    "triggerUseLastPrice": false,
    "avgFilledPrice": 111126.6,
    "contractSize": 0.00001,
    "timeInForce": "GTC",
    "closeOrder": false
}

```

`GET /api/v2.3/order`

Query order detail for a specified orderID/clOrderID, please note that a canceled order will only exist for 30 minutes. Requires `Trading` permission.

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
| originalOrderSize             | Integer  | Yes      | The original order quantity. This value will not change even if adjustments are made later.                                              |
| currentOrderSize              | Integer  | Yes      | The latest order quantity, which means the sum of the filled quantity and the remaining unfilled quantity.                             |
| totalFilledSize               | Integer  | Yes      | Cumulative filled quantity of this order.                                              |
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
| remainingSize                 | Integer  | Yes      | remainingSize                                                                          |
| status                        | Integer | Yes      | Order status. Please refer to [`API Enum`](#api-enum)                                  |
| takeProfitOrder               | TakeProfitOrder object | No | Take profit order info |
| stopLossOrder                 | StopLossOrder object   | No | Stop loss order info |
| closeOrder                    | Boolean   | Yes      | Whether it is an order to close this position |
| timeInForce                   | String  | Yes      | Order validity                                                                         |
| contractSize                  | Double  | Yes      | The order contract size                                                                |

## Amend Order

> Request (Amend price)

```json
{
  "symbol": "BTC-PERP",
  "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
  "type": "PRICE",
  "value": 22000
}
```

> Request (Amend size)

```json
{
  "symbol": "BTC-PERP",
  "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
  "type": "SIZE",
  "value": 100
}
```

> Request (Amend all - trigger Order.)

```json
{
  "symbol": "BTC-PERP",
  "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
  "type": "ALL",
  "orderPrice": 30010,
  "orderSize": 10,
  "triggerPrice": 30000
}
```

> Request (Amend all - Not trigger order.)

```json
{
  "symbol": "BTC-PERP",
  "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
  "type": "ALL",
  "orderPrice": 30010,
  "orderSize": 10
}
```

> Response

```json
[
    {
        "status": 123,
        "symbol": "BTC-PERP",
        "orderType": 76,
        "price": 10104.1,
        "side": "BUY",
        "orderID": "39ff44d2-513a-4ea6-858c-e07498d424fd",
        "timestamp": 1752138774052,
        "triggerPrice": 0,
        "trigger": false,
        "deviation": 100,
        "stealth": 100,
        "message": "",
        "avgFilledPrice": 0,
        "clOrderID": "",
        "originalOrderSize": 1,
        "currentOrderSize": 1,
        "filledSize": 0,
        "totalFilledSize": 0,
        "remainingSize": 1,
        "postOnly": false,
        "orderDetailType": null,
        "positionMode": "ONE_WAY",
        "positionDirection": null,
        "positionId": "BTC-PERP-USDT",
        "time_in_force": "GTC"
    }
]
```

`PUT /api/v2.3/order`

Amend the price or size or trigger price of an order. For trigger orders, if the order has already been triggered, the trigger price cannot be further amended. Amend order _does not_ apply to algo orders

### Request Parameters

| Name         | Type    | Required | Description                                                                                                                                                        |
| ---          | ---     | ---      | ---                                                                                                                                                                |
| symbol       | String  | Yes      | Market symbol                                                                                                                                                      |
| orderID      | String  | No       | Internal order ID. Mandatory when `clOrderID` is not provided. If `orderID` is provided, `clOrderID` will be ignored.                                              |
| clOrderID    | String  | No       | Custom order ID. Mandatory when `orderID` is not provided.                                                                                                         |
| type         | String  | Yes      | Type of amendment.<br/>`PRICE`: To amend order price<br/>`SIZE`: To amend order size<br/>`TRIGGERPRICE`: To amend trigger price for trigger orders only.<br/>`ALL`: To amend multiple fields. Note that the `TRIGGERPRICE` can only be amended if the order is a trigger order. Don't include `TRIGGERPRICE` if it is not a trigger order. |
| value        | Double  | Yes      | The value to be amended to. Value depends on the type being set.                                                                                                   |
| orderPrice   | Double  | No       | For type: `ALL`, order price to be amended.                                                                                                                         |
| orderSize    | Double  | No       | For type: `ALL`, order size in contract size to be amended.                                                                                                         |
| triggerPrice | Double  | No       | For type: `ALL`, trigger price to be amended.                                                                                                                       |


### Response Content

| Name              | Type    | Required | Description                                                                                                                                                                                                                                                                                     |
|-------------------| ---     |----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol            | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                   |
| clOrderID         | String  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                                                  |
| orderID           | String  | Yes      | Order ID                                                                                                                                                                                                                                                                                        |
| orderType         | Integer | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                                                                         |
| postOnly          | Boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                                         |
| price             | Double  | Yes      | Order price                                                                                                                                                                                                                                                                                     |
| side              | String  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                                                      |
| status            | Status    | Yes      | Order status<br/> 2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found<br/>17: Request faile<br/> For more status, please refer to [`API Enum`](#api-enum) |
| time_in_force     | String  | Yes      | Order validity                                                                                                                                                                                                                                                                                  |
| timestamp         | Long    | Yes      | Order timestamp                                                                                                                                                                                                                                                                                 |
| trigger           | String  | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                                           |
| triggerPrice      | String  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                                                  |
| avgFilledPrice      | String  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                                          |
| message           | String  | Yes      | Trade messages                                                                                                                                                                                                                                                                                  |
| stealth           | Double  | Yes      | Stealth value of order                                                                                                                                                                                                                                                                          |
| deviation         | String  | Yes      | Deviation value of order                                                                                                                                                                                                                                                                        |
| remainingSize     | Integer  | Yes      | The remaining order quantity = Current order size - Filled size.                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | The original order quantity. This value will not change even if adjustments are made later.                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | The latest order quantity, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                                                                                                                                                                                                                             |
| filledSize          | Integer  | Yes      | The quantity of the order that has been filled.                                                                                                                                                                                                                                                                               |
| totalFilledSize      | Integer  | Yes      | Cumulative filled quantity of this order.                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | Position mode<br/>ONE_WAY, HEDGE or ISOLATED                                                                                                                                                                                                                                                    |
| positionDirection | String  | Yes      | Position direction                                                                                                                                                                                                                                                                              |
| positionId        | String  | Yes      | The current order belongs to the id of position.                                                                                                                                                                                                                                                |

## Cancel Order

> Request

```
/api/v2.3/order?symbol=BTC-PERP&clOrderID=my-order-id
```

> Response

```json
[
  {
    "status": 6,
    "symbol": "BTC-PERP",
    "orderType": 76,
    "price": 100090.6,
    "side": "BUY",
    "orderID": "7a64ab37-313e-4313-bf1b-e909ebe9b976",
    "timestamp": 1752139128547,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 1,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

`DELETE /api/v2.3/order`

Cancels pending orders that has not yet been transacted. The `orderID` is a unique identifier to cancel a particular order. `clOrderID` is a custom ID sent in by the trader. When cancel by `clOrderID`, all orders having the same ID will be cancelled. If `orderID` and `clOrderID` is not sent in, then cancellation will be for all orders in the current market.
Requires `Trading` permission.

### Request Parameters

| Name      | Type   | Required | Description                                                                                                                        |
| ---       | ---    | ---      | ---                                                                                                                                |
| symbol    | String | Yes      | Market symbol                                                                                                                      |
| orderID   | String | No       | Unique identifier for an order. Mandatory when `clOrderID` is not provided. If `orderID` is provided, `clOrderID` will be ignored. |
| clOrderID | String | No       | Client custom order ID. Mandatory when `orderID` is not provided.                                                                  |


### Response Content

| Name              | Type    | Required | Description                                                                                                                                                                                                                                                                                     |
|-------------------| ---     |----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol            | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                   |
| clOrderID         | String  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                                                  |
| orderID           | String  | Yes      | Order ID                                                                                                                                                                                                                                                                                        |
| orderType         | Integer | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                                                                         |
| postOnly          | Boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                                         |
| price             | Double  | Yes      | Order price                                                                                                                                                                                                                                                                                     |
| side              | String  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                                                      |
| status            | Integer    | Yes      | Order status<br/> 2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found<br/>17: Request failed<br/> For more status, please refer to [`API Enum`](#api-enum) |
| time_in_force     | String  | Yes      | Order validity                                                                                                                                                                                                                                                                                  |
| timestamp         | Long    | Yes      | Order timestamp                                                                                                                                                                                                                                                                                 |
| trigger           | Boolean | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                                           |
| triggerPrice      | Double  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                                                  |
| avgFilledPrice      | Double  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                                          |
| message           | String  | Yes      | Trade messages                                                                                                                                                                                                                                                                                  |
| stealth           | Double  | Yes      | Stealth value of order                                                                                                                                                                                                                                                                          |
| deviation         | Double  | Yes      | Deviation value of order                                                                                                                                                                                                                                                                        |
| remainingSize     | Integer  | Yes      | The remaining order quantity = Current order size - Filled size.                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | The original order quantity. This value will not change even if adjustments are made later.                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | The latest order quantity, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                                                                                                                                                                                                                             |
| filledSize          | Integer  | Yes      | The quantity of the order that has been filled.                                                                                                                                                                                                                                                                               |
| totalFilledSize      | Integer  | Yes      | Cumulative filled quantity of this order.                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | Position mode<br/>ONE_WAY, HEDGE or ISOLATED                                                                                                                                                                                                                                                    |
| positionDirection | String  | Yes      | Position direction                                                                                                                                                                                                                                                                              |
| positionId        | String  | Yes      | The current order belongs to the id of position.                                                                                                                                                                                                                                                |

## Dead Man's Switch (Cancel All After)

> Request

```json
{
  "timeout": 60000
}
```

`POST /api/v2.3/order/cancelAllAfter`

Dead-man's switch allows the trader to send in a timeout value which is a Time to live (TTL) value for an order. Extension of the timeout is done by sending another `cancelAllAfter` request. If the server does not receive another request before the timeout is reached, all orders will be cancelled. Requires `Trading` permission.

### Request Parameters

| Name    | Type | Required | Description                   |
| ---     | ---  | ---      | ---                           |
| timeout | Long | Yes      | Timeout value in milliseconds |


### Response Content

* If set correctly, a HTTP 200 response code will be returned

## Query Open Orders

> Request

```
/api/v2.3/user/open_orders?symbol=BTC-PERP
```

> Response

```json
[
  {
    "vendorName": null,
    "botID": null,
    "orderType": 76,
    "price": 10104.1,
    "side": "BUY",
    "orderValue": 0.101041,
    "pegPriceMin": 0,
    "pegPriceMax": 0,
    "pegPriceDeviation": 1,
    "cancelDuration": 0,
    "timestamp": 1752138665358,
    "orderID": "39ff44d2-513a-4ea6-858c-e07498d424fd",
    "stealth": 1,
    "triggerOrder": false,
    "triggered": false,
    "triggerPrice": 0,
    "triggerOriginalPrice": 0,
    "triggerOrderType": 0,
    "triggerTrailingStopDeviation": 0,
    "triggerStopPrice": 0,
    "symbol": "BTC-PERP",
    "trailValue": 0,
    "contractSize": 0.00001,
    "clOrderID": "",
    "reduceOnly": false,
    "orderState": "STATUS_ACTIVE",
    "triggerUseLastPrice": false,
    "avgFilledPrice": 0,
    "timeInForce": "GTC",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "totalFilledSize": 0,
    "remainingSize": 1,
    "orderDetailType": null,
    "takeProfitOrder": null,
    "stopLossOrder": null,
    "closeOrder": false,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT"
  }
]
```

`GET /api/v2.3/user/open_orders`

Retrieves open orders that have not yet been matched or matched recently. Requires `Read` permission.

### Request Parameters

| Name               | Type    | Required | Description                                                                         |
| ---                | ---     | ---      | ---                                                                                 |
| symbol             | String  | No       | Market symbol                                                                       |
| orderID            | String  | No       | Query using internal order ID                                                       |
| clOrderID          | String  | No       | Query using custom order ID. If `orderID` is provided, `clOrderID` will be ignored. |

### Response Content

| Name                         | Type   | Required | Description                                                                            |
| ---                          | ---    | ---      |----------------------------------------------------------------------------------------|
| symbol                       | String | Yes      | Market symbol                                                                          |
| clOrderID                    | String | Yes      | Customer tag sent in by trader                                                         |
| orderValue                   | Double | Yes      | Notional value                                                                         |
| pegPriceMin                  | Double | Yes      | peg price min                                                                          |
| pegPriceMax                  | Double | Yes      | peg price max                                                                          |
| pegPriceDeviation            | Double | Yes      | Deviation percentage. Only for Algo orders                                             |
| cancelDuration               | Long   | Yes      | Expire in milliseconds. <br/>0: GTC<br/>-1: IOC                                        |
| orderID                      | String | Yes      | Order ID                                                                               |
| orderType                    | Integer| Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                |
| timeInForce                  | String | Yes      | Order validity                                                                         |
| price                        | Double | Yes      | Order price                                                                            |
| side                         | String | Yes      | Order side<br/>BUY or SELL                                                             |
| originalOrderSize             | Integer  | Yes      | The original order quantity. This value will not change even if adjustments are made later.                                              |
| currentOrderSize              | Integer  | Yes      | The latest order quantity, which means the sum of the filled quantity and the remaining unfilled quantity.                             |
| totalFilledSize               | Integer  | Yes      | Cumulative filled quantity of this order.                                              |
| timestamp                    | Long   | Yes      | Order timestamp                                                                        |
| triggerOrder                 | Boolean   | Yes      | Indicate if this is a trigger order                                                    |
| triggered                    | Boolean   | Yes      | Indicate if this order has been triggered                                              |
| triggerUseLastPrice          | Boolean   | Yes      | Indicate if this trigger order uses last price                                         |
| triggerPrice                 | Double | Yes      | Order trigger price, returns 0 if order is not a trigger order                         |
| triggerOriginalPrice         | Double | Yes      | Original trigger price                                                                 |
| triggerOrderType             | String | Yes      | Trigger order type <br/>1001: Trigger stop loss <br/>1002: Trigger take profit         |
| triggerTrailingStopDeviation | Double | Yes      | Percentage deviation from stop price                                                                     |
| triggerStopPrice             | Double | Yes      | Stop price attribute                                                                     |
| trailValue                   | Double | Yes      | Trail value attribute                                                                     |
| reduceOnly                   | Boolean   | Yes      | Indicate if this order is reduce only                                                  |
| avgFilledPrice               | Double | Yes      | Average filled price. Returns the average filled price for partially transacted orders |
| stealth                      | Double | Yes      | Stealth value of order                                                                 |
| orderState                   | String | Yes      | `STATUS_ACTIVE`, `STATUS_INACTIVE`                                                     |
| takeProfitOrder              | TakeProfitOrder object | No | Take profit order info                                                                 |
| stopLossOrder                | StopLossOrder object   | No | Stop loss order info                                                                   |
| closeOrder                   | Boolean   | Yes      | Whether it is an order to close this position                                          |
| positionMode                 | String   | Yes      | Position mode<br/>ONE_WAY, HEDGE or ISOLATED                                           |
| positionDirection            | String   | Yes      | Position direction                                                                     |
| positionId                   | String   | Yes      | The current order belongs to the id of position.                                       |
| contractSize                 | Double   | Yes      | The order contract size                                                              |

## Query Trades Fills

> Request

```
/api/v2.3/user/trade_history?symbol=BTC-PERP
```

> Response

```json
[
  {
    "tradeId": "9d661ee3-eaf8-4068-8d6a-5d3dfef6ef5f",
    "orderId": "bf07eeff-afdc-433a-a0ca-f41a2433e323",
    "username": "xxx",
    "side": "SELL",
    "orderType": 77,
    "triggerType": null,
    "price": 0,
    "size": 99,
    "filledPrice": 100000,
    "filledSize": 99,
    "triggerPrice": 0,
    "base": "BTC",
    "quote": "USDT",
    "symbol": "BTC-PERP",
    "feeCurrency": "USDT",
    "feeAmount": 0.0198,
    "wallet": "VIRTUAL|1@BTC-PERP-USDT#1",
    "realizedPnl": -0.99,
    "total": -1.0098,
    "serialId": 374029591,
    "timestamp": 1752204538247,
    "orderDetailType": null,
    "contractSize": 0.00001,
    "clOrderID": "_W_pip1752204538116",
    "positionId": "BTC-PERP-USDT",
    "avgFilledPrice": 100000
  }
]
```

`GET /api/v2.3/user/trade_history`

Retrieves a user's trade history. Requires `Read` permission.

### Request Parameters

| Name               | Type    | Required | Description                                                                       |
| ---                | ---     | ---      | ---                                                                               |
| symbol             | String  | No       | Market symbol                                                                     |
| startTime          | Long    | No       | Starting time (eg. 1624987283000)                                                 |
| endTime            | Long    | No       | Ending time (eg. 1624987283000)                                                   |
| beforeSerialId     | Long  | No       | Used for pagination to retrieve records when the order volume exceeds **500 per millisecond**. For typical scenarios, it is recommended to use the `startTime` and `endTime` parameters instead. |
| afterSerialId      | Long  | No       | Used for pagination to retrieve records when the order volume exceeds **500 per millisecond**. For typical scenarios, it is recommended to use the `startTime` and `endTime` parameters instead. |
| count              | Long    | No       | Number of records to return                                                       |
| includeOld         | Boolean | No       | Retrieve trade  history records past 7 days                                       |
| orderID            | String  | No       | Query trade history by order ID                                            |
| clOrderID          | String  | No       | Query trade history by custom order ID                                            |


* maximum days of trade history

| Time Interval       | Maximum Days  | Explanation                                                                             |
| :---:               | ---:          | :---:                                                                                   |
| startTime / endTime | 7            | Maximum **7** days within the specified interval. If specified interval exceeds **7** days, the **start time** will be set to **7** days before the **end time**                                    |
| startTime /    -    | 7             | If the **end time** is not specified, then **7** days after the **start time**          |
|      -    / endTime | 7             | If the **start time** is not specified, then **7** days before the **end time**         |
|      -    /    -    | 7             | If neither start nor end time is specified, then **7** days before the **current time** |


### Response Content

| Name             | Type    | Required | Description                                                                                                                                                                             |
|------------------| ---     | ---      |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol           | String  | Yes      | Market symbol                                                                                                                                                                           |
| side             | String  | Yes      | Trade side. Values are: [`BUY`, `SELL`]                                                                                                                                                 |
| price            | Double  | Yes      | Transacted price                                                                                                                                                                        |
| size             | Long    | Yes      | Original order size                                                                                                                                                                     |
| serialId         | Long    | Yes      | Serial Id, running sequence Long                                                                                                                                                      |
| tradeId          | String  | Yes      | Trade identifier                                                                                                                                                                        |
| timestamp        | Long    | Yes      | Transacted timestamp                                                                                                                                                                    |
| base             | String  | Yes      | Base currency                                                                                                                                                                           |
| quote            | String  | Yes      | Quote currency                                                                                                                                                                          |
| wallet           | String  | Yes      | Wallet name<br/>`CROSS@`: Cross wallet<br/>`ISOLATED@market`: Market refers to the current symbol with `-USDT` appended. Eg. BTC-PERP isolated wallet would be `ISOLATED@BTC-PERP-USDT` |
| clOrderID        | String  | Yes      | Custom order ID                                                                                                                                                                         |
| orderId          | String  | Yes      | Order ID                                                                                                                                                                                |
| username         | String  | Yes      | btse username                                                                                                                                                                           |
| triggerType      | Long    | Yes      | Trigger type<br/>1001: Stop Loss<br/>1002: Take Profit                                                                                                                                  |
| feeAmount        | Double    | Yes      | Fee amount                                                                                                                                                                              |
| feeCurrency      | String    | Yes      | Fee currency                                                                                                                                                                            |
| filledPrice      | Double  | Yes      | Filled price                                                                                                                                                                            |
| avgFilledPrice | Double  | Yes      | Average filled price                                                                                                                                                                    |
| triggerPrice     | Double  | Yes      | Trigger price                                                                                                                                                                           |
| filledSize       | Long    | Yes      | Filled size                                                                                                                                                                             |
| orderType        | Integer | Yes      | Order Type                                                                                                                                                                              |
| realizedPnL      | Double  | Yes      | Not used in Spot                                                                                                                                                                        |
| total            | Long    | Yes      | Not used in Spot                                                                                                                                                                        |
| positionId       | String  | Yes      | The current order belongs to the id of position.                                                                                                                                        |
| contractSize     | Double  | Yes      | The trade contract size                                                                                                                                                                 |


## Query Position

> Request

```
/api/v2.3/user/positions
```

> Response

```json
[
  {
    "marginType": 0,
    "entryPrice": 0,
    "markPrice": 29286.4,
    "symbol": "BTC-PERP",
    "side": "BUY",
    "orderValue": 441.8492,
    "settleWithAsset": "BTC",
    "unrealizedProfitLoss": -0.23538014,
    "totalMaintenanceMargin": 2.366912551,
    "size": 62,
    "liquidationPrice": 0,
    "isolatedLeverage": 25,
    "adlScoreBucket": 2,
    "liquidationInProgress": false,
    "timestamp": 1576661434072,
    "currentLeverage": 0,
    "takeProfitOrder": {
        "orderId": "ea1ab233-c79a-4503-a475-f8633ecc9d79",
        "side": "SELL",
        "triggerPrice": 31000.0,
        "triggerUseLastPrice": false
    },
    "stopLossOrder": {
        "orderId": "48523190-77b9-44ea-bee0-d67a428a51b8",
        "side": "SELL",
        "triggerPrice": 27000.0,
        "triggerUseLastPrice": true
    },
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT"
  },{
     "marginType": 91,
     "entryPrice": 1631.106666667,
     "markPrice": 1630.398947255,
     "symbol": "ETH-PERP",
     "side": "BUY",
     "orderValue": 48.9119684176,
     "settleWithAsset": "USDT",
     "unrealizedProfitLoss": -0.02123158,
     "totalMaintenanceMargin": 0.254871114,
     "size": 3,
     "liquidationPrice": 0,
     "isolatedLeverage": 0,
     "adlScoreBucket": 2,
     "liquidationInProgress": false,
     "timestamp": 0,
     "takeProfitOrder": null,
     "stopLossOrder": null,
     "positionMode": "HEDGE",
     "positionDirection": "LONG",
     "positionId": "ETH-PERP-USDT|LONG",
     "currentLeverage": 0.0340349245,
     "takeProfitOrder": null,
     "stopLossOrder": null
     }
]
```

`GET /api/v2.3/user/positions`

Queries user's current position. When no symbol is specified, positions for all markets will be returned.
Requires `Read` permission.

### Request Parameters

| Name               | Type    | Required | Description                                                     |
| ---                | ---     | ---      | ---                                                             |
| symbol             | String  | No       | Market symbol                                                   |

### Response Content

| Name                   | Type    | Required | Description                                                                 |
|------------------------|---------|----------|-----------------------------------------------------------------------------|
| symbol                 | String  | Yes      | Market symbol                                                               |
| side                   | String  | Yes      | Position side. Values are: [`Buy`, `SELL`]                                  |
| size                   | Long    | Yes      | Position size                                                               |
| entryPrice             | Double  | Yes      | Entry price                                                                 |
| markPrice              | Double  | Yes      | Mark price                                                                  |
| marginType             | Integer | Yes      | Margin Type. Values as follows<br/>91: CROSS wallet<br/>92: Isolated wallet |
| orderValue             | Double  | Yes      | Notional value                                                              |
| settleWithAsset        | String  | Yes      | Settlement currency                                                         |
| totalMaintenanceMargin | Double  | Yes      | Maintenance margin                                                          |
| unrealizedProfitLoss   | Double  | Yes      | Unrealized profit and loss                                                  |
| liquidationPrice       | Double  | Yes      | Liquidation Price                                                           |
| isolatedLeverage       | Double  | Yes      | Isolated leverage value                                                     |
| adlScoreBucket         | Double  | Yes      | ADL Score probability                                                       |
| liquidationInProgress  | Boolean | Yes      | Indicator if liquidation is in progress                                     |
| currentLeverage        | Double  | Yes      | Current leverage                                                            |
| timestamp              | Long    | Yes      | Timestamp when position was queried                                         |
| takeProfitOrder        | TakeProfitOrder object | No | Take profit order info                                                      |
| stopLossOrder          | StopLossOrder object   | No | Stop loss order info                                                        |
| positionMode           | String  | Yes      | Position mode<br/>ONE_WAY, HEDGE or ISOLATED                                |
| positionDirection      | String  | Yes      | Position direction                                                          |
| positionId             | String  | Yes      | Position id                                                                 |


## Close Position

> Request

```json
{
  "price": 0,
  "symbol": "BTC-PERP",
  "type": "MARKET"
}
```
> Request(For hedge mode position)

```json
{
  "price": 0,
  "symbol": "BTC-PERP",
  "type": "MARKET",
  "positionId": "BTC-PERP-USDT|LONG"
}
```
> Response

```json
[
  {
    "status": 4,
    "symbol": "ETH-PERP",
    "orderType": 77,
    "price": 3900,
    "side": "SELL",
    "orderID": "21d2de4d-b133-4e22-81ae-afde5c95d227",
    "timestamp": 1752205761546,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 3900,
    "clOrderID": "_W_mizmtpf1752205761471",
    "postOnly": false,
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "totalFilledSize": 1,
    "remainingSize": 0,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "ETH-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.3/order/close_position`

Closes a user's position for the particular market as specified by symbol. If type is specified as LIMIT, then price is mandatory. When type is MARKET, it closes the position at market price. Requires `Trading` permission.

### Request Parameters

| Name               | Type    | Required | Description                                                                                             |
|--------------------| ---     | ---      |---------------------------------------------------------------------------------------------------------|
| symbol             | String  | Yes      | Market symbol                                                                                           |
| type               | String  | Yes      | Close position type with values:<br/>LIMIT: Close at `price`<br/>MARKET: Close at market price          |
| price              | Double  | No       | Close price. Mandatory when type is `LIMIT`                                                             |
| postOnly           | Boolean | No       | Boolean to indicate if this is a post only order. For post only orders, traders are charged maker fees  |
| positionId         | String  | No       | The position ID that you want to close. Mandatory when positionMode is `HEDGE` or `ISOLATED`                          |

### Response Content

| Name              | Type    | Required | Description                                                                                                                                                                                                                                                                                     |
|-------------------| ---     |----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol            | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                   |
| clOrderID         | String  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                                                  |
| orderID           | String  | Yes      | Order ID                                                                                                                                                                                                                                                                                        |
| orderType         | Integer | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                                                                         |
| postOnly          | Boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                                         |
| price             | Double  | Yes      | Order price                                                                                                                                                                                                                                                                                     |
| side              | String  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                                                      |
| status            | Integer    | Yes      | Order status<br/> 2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found<br/>17: Request failed<br/> For more status, please refer to [`API Enum`](#api-enum) |
| time_in_force     | String  | Yes      | Order validity                                                                                                                                                                                                                                                                                  |
| timestamp         | Long    | Yes      | Order timestamp                                                                                                                                                                                                                                                                                 |
| trigger           | String  | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                                           |
| triggerPrice      | String  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                                                  |
| avgFilledPrice      | String  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                                          |
| message           | String  | Yes      | Trade messages                                                                                                                                                                                                                                                                                  |
| stealth           | Double  | Yes      | Stealth value of order                                                                                                                                                                                                                                                                          |
| deviation         | String  | Yes      | Deviation value of order                                                                                                                                                                                                                                                                        |
| remainingSize     | Integer  | Yes      | The remaining order quantity = Current order size - Filled size.                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | The original order quantity. This value will not change even if adjustments are made later.                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | The latest order quantity, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                                                                                                                                                                                                                             |
| filledSize          | Integer  | Yes      | The quantity of the order that has been filled.                                                                                                                                                                                                                                                                               |
| totalFilledSize      | Integer  | Yes      | Cumulative filled quantity of this order.                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | Position mode<br/>ONE_WAY, HEDGE or ISOLATED                                                                                                                                                                                                                                                    |
| positionDirection | String  | Yes      | Position direction                                                                                                                                                                                                                                                                              |
| positionId        | String  | Yes      | Position id                                                                                                                                                                                                                                                                                     |


## Get Risk Limit

> Request

```
/api/v2.3/risk_limit?symbol=BTC-PERP
```

> Response

```json
{
    "symbol": "BTC-PERP",
    "riskLimit": 100000
}
```
`GET /api/v2.3/risk_limit`

Query risk limit for the specified market. Requires `Read` permission.

### Request Parameters

| Name               | Type    | Required | Description |
| ---                | ---     | ---      | --- |
| symbol             | String  | Yes      | Market symbol  |

### Response Content

| Name      | Type    | Required | Description|
| ---       | ---     | ---      | --- |
| symbol    | String  | Yes      | Market symbol  |
| riskLimit | Long    | Yes      | Risk limit value now in position size, but will be changed to USD value along with futures market name change |

## Set Risk Limit

> Request

```json
{
  "symbol": "BTC-PERP",
  "riskLimit": 0
}
```

> Request (When positionMode is `HEDGE` or `ISOLATED`)

```json
{
    "symbol": "BTC-PERP",
    "riskLimit": 100000,
    "positionMode": "HEDGE"
}
```

> Response

```json
{
  "symbol": "BTC-PERP",
  "timestamp": 1577093486551,
  "status": 20,
  "type": 94,
  "message": "false"
}
```

`POST /api/v2.3/risk_limit`

Changes risk limit for the specified market. Requires `Trading` permission.

### Request Parameters

| Name               | Type    | Required | Description                                                                               |
| ---                | ---     | ---      |-------------------------------------------------------------------------------------------|
| symbol             | String  | Yes      | Market symbol                                                                             |
| riskLimit          | Long    | Yes      | Risk limit value now in position size, but it will be changed to USD value in the future. |
| positionMode       | String  | no       | ONE_WAY(default) or HEDGE. Mandatory when positionMode is `HEDGE` or `ISOLATED`                         |

### Response Content

| Name      | Type    | Required | Description                                                                                                                                     |
| ---       | ---     | ---      | ---                                                                                                                                             |
| symbol    | String  | Yes      | Market symbol                                                                                                                                   |
| status    | Integer    | Yes      | Status of the request. Values are: <br/>8: Insufficient Balance<br/>12: Error in updating risk limit<br/>20: Success<br/>41: Invalid risk limit |
| type      | Double  | Yes      | Value will be 94 indicating that type is `Risk Limit`                                                                                           |
| timestamp | Long    | Yes      | Timestamp where risk limit was set                                                                                                              |
| message   | Long    | Yes      | Message                                                                                                                                         |

## Set Leverage

> Request

```json
{
  "symbol": "BTC-PERP",
  "leverage": 0,
  "marginMode": "CROSS"
}
```

> Request (When positionMode is `HEDGE` or `ISOLATED`)

```json
{
    "symbol": "BTC-PERP",
    "leverage": 0,
    "positionMode": "HEDGE",
    "marginMode": "CROSS"
}
```

> Response

```json
{
  "symbol": "BTC-PERP",
  "timestamp": 1660711246942,
  "status": 20,
  "type": 93,
  "message": ""
}
```

`POST /api/v2.3/leverage`

Change leverage values for the specified market. Requires `Trading` permission.

### Request Parameters

| Name               | Type    | Required | Description                                                       |
| ---                | ---     | ---      |-------------------------------------------------------------------|
| symbol             | String  | Yes      | Market symbol                                                     |
| leverage           | Double  | Yes      | Leverage value, 0 means cross maximum leverage                    |
| positionMode       | String  | no       | ONE_WAY(default) or HEDGE. Mandatory when positionMode is `HEDGE` or `ISOLATED` |
| positionId         | String  | no       | The position ID that you want to change. Mandatory when positionMode is `HEDGE` or `ISOLATED` |
| marginMode         | String  | no       | CROSS or ISOLATED(default)                                        |

### Response Content

| Name      | Type    | Required | Description                                                                                                                             |
| ---       | ---     | ---      | ---                                                                                                                                     |
| symbol    | String  | Yes      | Market symbol                                                                                                                           |
| status    | Integer    | Yes      | Status of the request. Values are: <br/>8: Insufficient Balance<br/>13: Invalid leverage<br/>20: Success<br/>64: Undergoing liquidation |
| type      | Double  | Yes      | Value will be 93 indicating that type is `Leverage`                                                                                     |
| timestamp | Long    | Yes      | Timestamp where leverage was set                                                                                                        |
| message   | Long    | Yes      | Message                                                                                                                                 |

## Get Leverage

> Response

```json
[
  {
    "symbol": "BTC-PERP",
    "leverage": 10,
    "marginMode": "ISOLATED",
    "positionDirection": "LONG"
  },
  {
    "symbol": "BTC-PERP",
    "leverage": 3,
    "marginMode": "ISOLATED",
    "positionDirection": "SHORT"
  }
]
```

`Get /api/v2.3/leverage`

Get leverage value for the specified market. Requires `Read` permission.

### Request Parameters

| Name               | Type    | Required | Description |
| ---                | ---     | ---      | --- |
| symbol             | String  | Yes      | Market symbol |

### Response Content

| Name              | Type   | Required | Description                                                                                          |
| ---               | ---    | ---      |------------------------------------------------------------------------------------------------------|
| symbol            | String | Yes      | Market symbol                                                                                        |
| leverage          | Double | Yes      | Current leverage value for the market, return 0 means the leverage is the maximum cross leverage     |
| marginMode        | String | Yes      | Current margin mode                                                                                  |
| positionDirection | String | Yes      | Current position direction when position mode is Hedge else return null                              |

## Change Contract Settlement Currency

> Request

```json
{
  "symbol": "BTC-PERP",
  "currency": "BTC"
}
```

> Request (When positionMode is `HEDGE` or `ISOLATED`)

```json
{
    "symbol": "BTC-PERP",
    "currency": "USDT",
    "positionId": "BTC-PERP-USDT|LONG"
}
```

> Response (only available when an error occurs)

```json
{
  "status": 0,
  "errorCode": 0,
  "message": "String"
}
```

`POST /api/v2.3/settle_in`

Changes the settlement currency for the position in the current market. Requires `Trading` permission.

### Request Parameters

| Name               | Type    | Required | Description                                                                  |
| ---                | ---     | ---      |------------------------------------------------------------------------------|
| symbol             | String  | Yes      | Market symbol                                                                |
| currency           | String  | Yes      | Settlement currency to set                                                   |
| positionId         | String  | No       | The position ID that you want to set. Mandatory when positionMode is `HEDGE` or `ISOLATED` |

### Response Content

| Name      | Type    | Required | Description                                            |
| ---       | ---     | ---      | ---                                                    |
| status    | Integer    | No       | Status. Only available when an error occurs.           |
| errorCode | Long    | No       | Error code. Only available when an error occurs.       |
| message   | String  | No       | Response message. Only available when an error occurs. |

## Query Account Fee

> Response

```json
{
  "makerFee": 0,
  "symbol": "BTC-PERP",
  "takerFee": 0
}
```

`GET /api/v2.3/user/fees`

Retrieve user's trading fees. Requires `Read` permission.

### Request Parameters

| Name               | Type    | Required | Description                                                     |
| ---                | ---     | ---      | ---                                                             |
| symbol             | String  | No       | Market symbol                                                   |

### Response Content

| Name     | Type   | Required | Description   |
| ---      | ---    | ---      | ---           |
| symbol   | String | Yes      | Market symbol |
| makerFee | Double | Yes      | Maker fees    |
| takerFee | Double | Yes      | Taker fees    |


## Bind TP/SL
> Request

```json
{
    "symbol": "BTC-PERP",
    "takeProfitPrice": 31000,
    "takeProfitTrigger": "markPrice",
    "stopLossPrice": 22000,
    "stopLossTrigger": "lastPrice"
}
```

> Response

```json
[
  {
    "status": 9,
    "symbol": "BTC-PERP",
    "orderType": 77,
    "price": 0,
    "side": "SELL",
    "orderID": "00fcb6e9-5c89-4c20-8b85-b9789dc4d2c7",
    "timestamp": 1752140292632,
    "triggerPrice": 50000,
    "trigger": true,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 8,
    "currentOrderSize": 8,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 0,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  },
  {
    "status": 9,
    "symbol": "BTC-PERP",
    "orderType": 77,
    "price": 0,
    "side": "SELL",
    "orderID": "2eb18277-0625-47d6-b4c9-5d898a33e2f7",
    "timestamp": 1752140292632,
    "triggerPrice": 120000,
    "trigger": true,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 8,
    "currentOrderSize": 8,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 8,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.3/order/bind/tpsl`

Bind TP/SL with an existing position. Requires `Trading` permission.

### Request Parameters

| Name               | Type    | Required | Description
| ---                | ---     | ---      | ---
| symbol             | String  | yes       | Market symbol
| side               | String  | yes       | "BUY" or "SELL" Mandatory when positionMode is `HEDGE`, in hedge mode, it is used to clsoe the specified position, ex: sell to close Long position, buy to close short position
| takeProfitPrice    | Double  | No        | Mandatory when creating new order with take profit order. Indicates the trigger price. Must set takeProfitPrice or stopLossPrice at least when using this API. |
| takeProfitTrigger  | String  | No        | For creating order with take profit order. Valid options: `markPrice` (default) or `lastPrice` |
| stopLossPrice      | Double  | No        | Mandatory when creating new order with stop loss order. Indicates the trigger price        |
| stopLossTrigger     | String | No       | For creating order with stop loss order. Valid options: `markPrice` (default) or `lastPrice`|
| positionMode       | String  | no       | ONE_WAY(default) or HEDGE or ISOLATED. Mandatory when positionMode is `HEDGE` or `ISOLATED` |
| positionId         | String  | no       | The position ID that you want to bind. Mandatory when positionMode is `ISOLATED` |

### Response Content

| Name          | Type    | Required | Description                                                                                                                                                                                                                                                                                     |
| ---           | ---     | ---      |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol        | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                   |
| clOrderID     | String  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                                                  |
| orderID       | String  | Yes      | Order ID                                                                                                                                                                                                                                                                                        |
| orderType     | String  | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                                                                         |
| postOnly      | Boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                                         |
| price         | Double  | Yes      | Order price                                                                                                                                                                                                                                                                                     |
| side          | String  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                                                      |
| status        | Integer    | Yes      | Order status<br/> 2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found<br/>17: Request failed<br/> For more status, please refer to [`API Enum`](#api-enum) |
| time_in_force | String  | Yes      | Order validity                                                                                                                                                                                                                                                                                  |
| timestamp     | Long    | Yes      | Order timestamp                                                                                                                                                                                                                                                                                 |
| trigger       | Boolean | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                                           |
| triggerPrice  | Double  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                                                  |
| avgFilledPrice  | Double  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                                          |
| message       | String  | Yes      | Trade messages                                                                                                                                                                                                                                                                                  |
| stealth       | String  | Yes      | Only valid for Algo orders                                                                                                                                                                                                                                                                      |
| deviation     | Double  | Yes      | Only valid for Algo                                                                                                                                                                                                                                                                             |
| remainingSize     | Integer  | Yes      | The remaining order quantity = Current order size - Filled size.                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | The original order quantity. This value will not change even if adjustments are made later.                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | The latest order quantity, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                                                                                                                                                                                                                             |
| filledSize          | Integer  | Yes      | The quantity of the order that has been filled.                                                                                                                                                                                                                                                                               |
| totalFilledSize      | Integer  | Yes      | Cumulative filled quantity of this order.                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | Position mode<br/>ONE_WAY, HEDGE or ISOLATED                                                                                                                                                                                                                                                    |
| positionDirection | String  | Yes      | Position direction                                                                                                                                                                                                                                                                              |
| positionId        | String  | Yes      | Position id                                                                                                                                                                                                                                                                                     |

## Query Position Mode

> Response

```json
[
    {
        "symbol": "ETH-PERP",
        "positionMode": "HEDGE"
    },
    {
        "symbol": "BTC-PERP",
        "positionMode": "ONE_WAY"
    }
]
```

`GET /api/v2.3/position_mode`

Retrieve user's position mode. Requires `Read` permission.

### Request Parameters

| Name               | Type    | Required | Description          |
| ---                | ---     | ---      | ---------------------|
| symbol             | String  | No       | Market symbol        |

### Response Content

| Name         | Type   | Required | Description                |
| ---          | ---    | ---      |----------------------------|
| symbol       | String | Yes      | Market symbol              |
| positionMode | String | Yes      | ONE_WAY, HEDGE or ISOLATED |

## Change Position Mode

> Request

```json
{
  "symbol": "BTC-PERP",
  "positionMode": "HEDGE"
}
```

`POST /api/v2.3/position_mode`

Changes position mode. Requires `Trading` permission.

### Request Parameters

| Name               | Type    | Required | Description                 |
| ---                | ---     | ---      |-----------------------------|
| symbol             | String  | Yes      | Market symbol               |
| positionMode       | String  | Yes      | ONE_WAY, HEDGE or ISOLATED |

### Response Content

| Name      | Type    | Required | Description                                                            |
| ---       | ---     | ---      | -----------------------------------------------------------------------|
| symbol    | String  | Yes      | Market symbol                                                          |
| timestamp | Long    | No       | Timestamp where position mode was set                                  |
| status    | Integer  | No       | Status of the request. Values are: <br>20: Success                     |
| type      | String  | No       | Value will be 129 indicating that type is `Futures Config Mode Change` |
| message   | String  | No       | Message                                                                |

## Query User Initial Margin Percentage And Maintenance Margin Percentage

> Response

```json
[
    {
        "symbol": "ETH-PERP",
        "initialMarginPercentage": 0.01,
        "maintenanceMarginPercentage": 0.005
    },
    {
        "symbol": "BTC-PERP",
        "initialMarginPercentage": 0.01,
        "maintenanceMarginPercentage": 0.005
    }
]
```

`GET /api/v2.3/user/margin_setting`

Queries user's initial margin percentage and maintenance margin percentage. When no symbol is specified, margin percentage for all markets will be returned. Requires `Read` permission.

### Request Parameters

| Name               | Type    | Required | Description   |
| ---                | ---     | ---      | ---           |
| symbol             | String  | No       | Market symbol |

### Response Content

| Name                        | Type   | Required | Description                           |
| ---                         | ---    | ---      | ---                                   |
| symbol                      | String | Yes      | Market symbol                         |
| initialMarginPercentage     | Double | Yes      | Current initial margin percentage     |
| maintenanceMarginPercentage | Double | Yes      | Current maintenance margin percentage |

# Wallet Endpoints

## Query Wallet Balance

> Response

```json
[
  {
    "trackingID": 0,
    "queryType": 0,
    "activeWalletName": "String",
    "wallet": "CROSS@",
    "username": "String",
    "walletTotalValue": 0,
    "totalValue": 100,
    "marginBalance": 100,
    "availableBalance": 100,
    "unrealisedProfitLoss": 0,
    "maintenanceMargin": 0,
    "leverage": 0,
    "openMargin": 0,
    "assets": [
      {
        "balance": 0.20183537,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ],
    "assetsInUse": [
      {
        "balance": 0.01,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ]
  }
]
```

`GET /api/v2.3/user/wallet`

Query user's wallet balance. Requires `Read` permissions on the API key.

### Request Parameters

| Name               | Type    | Required | Description                                                                                                                                                                       |
| ---                | ---     | ---      | ---                                                                                                                                                                               |
| wallet             | String  | Yes      | Wallet name<br/>`CROSS@`: Cross wallet<br/>`ISOLATED@market`: Market refers to the current symbol with `-USDT` appended. Eg. BTC-PERP isolated wallet would be `ISOLATED@BTC-PERP-USDT` |

### Response Content

#### Wallet

| Name                 | Type         | Required | Description                                                                      |
| ---                  | ---          | ---      | ---                                                                              |
| wallet               | String       | Yes      | Wallet name                                                                      |
| activeWalletName     | String       | Yes      | Active wallet name                                                               |
| queryType            | Integer      | Yes      | Query type                                                                       |
| trackingID           | Long         | Yes      | Internal tracking ID, not being used                                             |
| walletTotalValue     | Double       | Yes      | Wallet total value                                                               |
| totalValue           | Double       | Yes      | Total value                                                                      |
| marginBalance        | Double       | Yes      | Margin balance                                                                   |
| availableBalance     | Double       | Yes      | Available Balance                                                                |
| unrealisedProfitLoss | Double       | Yes      | Unrealised Profit / Loss                                                         |
| maintenanceMargin    | Double       | Yes      | Maintenance margin                                                               |
| leverage             | Double       | Yes      | Leverage. In CROSS wallet, this field is current leverage, not leverage setting  |
| openMargin           | Double       | Yes      | Open margin                                                                      |
| assets               | Asset object | Yes      | Assets available                                                                 |
| assetsInUse          | Asset object | Yes      | Assets in use                                                                    |

#### Assets / Asset in Use

| Name       | Type   | Required | Description |
| ---        | ---    | ---      | ---         |
| balance    | Double | Yes      | Balance     |
| assetPrice | Double | Yes      | Asset price |
| currency   | String | Yes      | Currency    |


## Query Wallet History

> Response

```json
[
  {
    "amount": 21.35823825,
    "currency": "USD",
    "description": "String",
    "fees": 0.06,
    "orderId": 20181213000239,
    "status": 10,
    "timestamp": 1571630174639,
    "type": 1,
    "username": "btseUser",
    "wallet": "Wallet",
    "txid": "<Blockchain Transaction ID>",
    "currencyNetwork": "<Blockchain currency network>"
  }
]
```

`GET /api/v2.3/user/wallet_history`

Get user's wallet history records on the futures wallet. Requires `Read` permission.

### Request Parameters

| Name               | Type    | Required | Description                                                                                                                                 |
| ---                | ---     | ---      | ---                                                                                                                                         |
| wallet             | String  | No       | Wallet, if not specified will return all wallets. Valid values are: <br/>`CROSS@`: Cross wallet<br/>`ISOLATED@BTC-PERP-USDT`: Isolated wallets |
| startTime          | Long    | No       | Starting time in milliseconds (eg. 1624987283000)                                                                                           |
| endTime            | Long    | No       | Ending time in milliseconds (eg. 1624987283000)                                                                                             |
| count              | Integer | No       | Number of records to return                                                                                                                 |


### Response Content

| Name        | Type    | Required | Description                                                                                                       |
| ---         | ---     | ---      | ---                                                                                                               |
| currency    | String  | Yes      | Currency                                                                                                          |
| amount      | Double  | Yes      | Amount in the record                                                                                              |
| fees        | Double  | Yes      | Fees charged if any                                                                                               |
| orderId     | String  | Yes      | Internal wallet order ID                                                                                          |
| wallet      | String  | Yes      | Wallet type. For futures will return `CROSS@` or `ISOLATED@`                                                      |
| description | String  | Yes      | Description of the transaction                                                                                    |
| status      | Integer | Yes      | 1: PENDING<br/>2: PROCESSING<br/>10: COMPLETED<br/>16: CANCELLED                                                  |
| type        | Integer | Yes      | 105: Wallet Transfer<br/>106: Wallet Liquidation<br/>108: Realized PnL<br/>110: Funding<br/>121: Asset Conversion |

## Query Unified Wallet Margin

> Response

```json
{
  "symbol": "BTC-PERP",
  "walletTotalValue": 1535.10700567,
  "walletTotalUnrealizedProfitLoss": -49.90799449,
  "futuresTotalAvailableBalance": 1836.521306109,
  "wallets": [
    {
      "activeWalletName": "VIRTUAL|5@BTC-PERP-USDT#4",
      "unrealisedProfitLoss": 49.88502177,
      "walletTotalValue": 956.43166194,
      "marginBalance": 1006.31668371,
      "availableBalance": 993.201492938,
      "maintenanceMargin": 13.115190772
    }
  ]
}
```

`GET /api/v2.3/user/unifiedWallet/margin`

**This API is for the users who have upgraded wallet**

Gets margin information for the specified wallet or position. Requires `Read` permission.


### Request Parameters

| Name               | Type    | Required | Description        |
| ---                | ---     |----------|--------------------|
| symbol             | String  | No       | Market symbol      |
| positionId         | String  | No       | Position unique id |

### Response Contnet

| Name                            | Type          | Require | Description                    |
|---------------------------------|---------------|---------|--------------------------------|
| symbol                          | String        | Yes     | Market symbol                  |
| walletTotalValue                | Double        | Yes     | Wallet total value             |
| walletTotalUnrealizedProfitLoss | Double        | Yes     | Wallet total P&L               |
| futuresTotalAvailableBalance    | Double        | Yes     | Wallet total available balance |
| wallets                         | Wallet Object | Yes     | Wallet details                 |

#### Wallet Details

| Name                 | Type        | Require | Description        |
|----------------------|-------------|---------|--------------------|
| activeWalletName     | String      | Yes     | Wallet name        |
| unrealisedProfitLoss | Double      | Yes     | Wallet P&L         |
| walletTotalValue     | Double      | Yes     | Wallet total P&L   |
| marginBalance        | Double      | Yes     | Margin balance     |
| availableBalance     | Double      | Yes     | Available balance  |
| maintenanceMargin    | Double      | Yes     | Maintenance margin |


## Query Wallet Margin

> Response

```json
[
  {
    "trackingID": 0,
    "requestId": 0,
    "queryType": 0,
    "wallet": "CROSS@",
    "walletTotalValue": 0,
    "totalValue": 100,
    "marginBalance": 100,
    "availableBalance": 100,
    "unrealisedProfitLoss": 0,
    "maintenanceMargin": 0,
    "leverage": 0,
    "openMargin": 0,
    "assets": [
      {
        "balance": 0.20183537,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ],
    "assetsInUse": [
      {
        "balance": 0.01,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ]
  }
]
```

`GET /api/v2.3/user/margin`

The users who have upgraded wallet to unified wallet are not allow to use this API. Please use [`Query Unified Wallet Margin`](#query-unified-wallet-margin).

Gets margin information for the specified wallet so that users can know which wallet they are currently using in the market.
Requires `Read` permission.

### Request Parameters

| Name               | Type    | Required | Description      |
| ---                | ---     | ---      | ---              |
| symbol             | String  | Yes      | Market symbol    |

### Response Content

#### Wallet

| Name                 | Type         | Required | Description                          |
| ---                  | ---          | ---      | ---                                  |
| wallet               | String       | Yes      | Wallet name                          |
| queryType            | Integer      | Yes      | Query type                           |
| trackingID           | Long         | Yes      | Internal tracking ID, not being used |
| requestId            | Long         | Yes      | Internal request ID, not being used  |
| walletTotalValue     | Double       | Yes      | Wallet total value                   |
| totalValue           | Double       | Yes      | Total value                          |
| marginBalance        | Double       | Yes      | Margin balance                       |
| availableBalance     | Double       | Yes      | Available Balance                    |
| unrealisedProfitLoss | Double       | Yes      | Unrealised Profit / Loss             |
| maintenanceMargin    | Double       | Yes      | Maintenance margin                   |
| leverage             | Double       | Yes      | Leverage                             |
| openMargin           | Double       | Yes      | Open margin                          |
| assets               | Asset object | Yes      | Assets available                     |
| assetsInUse          | Asset object | Yes      | Assets in use                        |

#### Assets / Asset in Use

| Name       | Type   | Required | Description |
| ---        | ---    | ---      | ---         |
| balance    | Double | Yes      | Balance     |
| assetPrice | Double | Yes      | Asset price |
| currency   | String | Yes      | Currency    |

## Transfer funds between Futures wallet

> Request

```json
{
  "walletSrc": "",
  "walletSrcType": "SPOT",
  "walletDest": "",
  "walletDestType": "CROSS",
  "apiWallets": [
    {
      "currency": "USD",
      "allBalance": true
    },
    {
      "currency": "BTC",
      "allBalance": true
    }
  ]
}
```

> Response

```json
[
  {
    "trackingID": 0,
    "queryType": 0,
    "activeWalletName": "",
    "wallet": "CROSS@",
    "username": "String",
    "walletTotalValue": 0,
    "totalValue": 100,
    "marginBalance": 100,
    "availableBalance": 100,
    "unrealisedProfitLoss": 0,
    "maintenanceMargin": 0,
    "leverage": 0,
    "openMargin": 0,
    "assets": [
      {
        "balance": 0.20183537,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ],
    "assetsInUse": [
      {
        "balance": 0.01,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ]
  }
]
```

`POST /api/v2.3/user/wallet/transfer`

Transfers funds between user's wallet. User can specify the source and target wallet to transfer funds. Requires `Transfer` permission.

### Request Parameters

#### Wallet Request

| Name           | Type          | Required | Description                                                                                                                                                         |
| ---            | ---           | ---      | ---                                                                                                                                                                 |
| walletSrc      | String        | No       | Source wallet, required if `walletSrcType` is `ISOLATED`                                                                                                            |
| walletSrcType  | String        | Yes      | Source type, valid values are:<br/>`SPOT`: Spot Wallet<br/>`CROSS`: Cross Wallet<br/>`ISOLATED`: Isolated wallet for the market where market the market symbol      |
| walletDest     | String        | No       | Destination wallet, required if `walletDestType` is `ISOLATED`                                                                                                      |
| walletDestType | String        | Yes      | Destination type, valid values are:<br/>`SPOT`: Spot Wallet<br/>`CROSS`: Cross Wallet<br/>`ISOLATED`: Isolated wallet for the market where market the market symbol |
| apiWallets     | Wallet Detail | Yes      | Transfer details                                                                                                                                                    |

#### Wallet Detail Request

| Name       | Type    | Required | Description                                                |
| ---        | ---     | ---      | ---                                                        |
| currency   | String  | Yes      | Wallet Currency                                            |
| allBalance | Boolean | Yes      | Indicator if all wallet balance is to be transferred       |
| balance    | Double  | No       | The value of the balance is to be transferred, example: 10 |


### Response Content

#### Wallet

| Name                 | Type         | Required | Description                          |
| ---                  | ---          | ---      | ---                                  |
| wallet               | String       | Yes      | Wallet name                          |
| activeWalletName     | String       | Yes      | Active wallet name                   |
| queryType            | Integer      | Yes      | Query type                           |
| trackingID           | Long         | Yes      | Internal tracking ID, not being used |
| walletTotalValue     | Double       | Yes      | Wallet total value                   |
| totalValue           | Double       | Yes      | Total value                          |
| marginBalance        | Double       | Yes      | Margin balance                       |
| availableBalance     | Double       | Yes      | Available Balance                    |
| unrealisedProfitLoss | Double       | Yes      | Unrealised Profit / Loss             |
| maintenanceMargin    | Double       | Yes      | Maintenance margin                   |
| leverage             | Double       | Yes      | Leverage                             |
| openMargin           | Double       | Yes      | Open margin                          |
| assets               | Asset object | Yes      | Assets available                     |
| assetsInUse          | Asset object | Yes      | Assets in use                        |

#### Assets / Asset in Use

| Name       | Type   | Required | Description |
| ---        | ---    | ---      | ---         |
| balance    | Double | Yes      | Balance     |
| assetPrice | Double | Yes      | Asset price |
| currency   | String | Yes      | Currency    |


## Sub-Account Wallet Transfer

`POST /api/v2.3/subaccount/wallet/transfer`

Transfers funds between user and sub-account wallet. User can specify the source and target wallet to transfer funds,
`Wallet` permission is required. To get supported currency list please check [Available currency list for action](#query-available-currency-list-for-wallet-action).

### Request Parameters

#### Wallet Request

| Name           | Type          | Required | Description                                                                                                                                                         |
| ---            | ---           | ---      | ---                                                                                                                                                                 |
| walletSrc      | String        | No       | Source wallet, required when `walletSrcType` is `ISOLATED`                                                                                                          |
| walletSrcType  | String        | Yes      | Source type, valid values are:<br/>`SPOT`: Spot Wallet<br/>`CROSS`: Cross Wallet<br/>`ISOLATED`: Isolated wallet for the market where market the market symbol      |
| walletDest     | String        | No       | Destination wallet, required when `walletDestType` is `ISOLATED`                                                                                                    |
| walletDestType | String        | Yes      | Destination type, valid values are:<br/>`SPOT`: Spot Wallet<br/>`CROSS`: Cross Wallet<br/>`ISOLATED`: Isolated wallet for the market where market the market symbol |
| fromUser       | String        | Yes      | Source username                                                                                                                                                     |
| receiver       | String        | Yes      | Receiver username                                                                                                                                                   |
| apiWallets     | Wallet Detail | Yes      | Transfer details                                                                                                                                                    |

#### Wallet Detail Request

| Name       | Type    | Required | Description                                                |
| ---        | ---     | ---      | ---                                                        |
| currency   | String  | Yes      | Wallet Currency                                            |
| allBalance | Boolean | Yes      | Indicator if all wallet balance is to be transferred       |
| balance    | Double  | No       | The value of the balance is to be transferred, example: 10 |


### Response Content

#### Wallet

| Name                 | Type     | Required | Description         |
|----------------------|----------|----------|---------------------|
| code                 | Integer  | Yes      | Response code       |
| msg                  | String   | Yes      | Response message    |
| time                 | Integer  | Yes      | Response Time       |
| data                 | Object   | No       |                     |
| success              | Boolean  | Yes      | Is transfer success |


#### Transfer Error Code

| Code  | Description                                            |
|-------|--------------------------------------------------------|
| -2    | Invalid request parameter                              |
| -1046 | Transfer fromUser Futures asset to DestWallet failed   |
| -1047 | Transfer fromUser to receiver failed                   |
| -1048 | Transfer receiver Spot wallet to Futures wallet failed |



# Order Book Websocket Streams

## Endpoints
  * Production
    * `wss://ws.btse.com/ws/oss/futures`
  * Testnet
    * `wss://testws.btse.io/ws/oss/futures`

## OSS L1 Snapshot (By grouping)

> Request

```json
{
  "op": "subscribe",
  "args": [
    "snapshotL1:BTC-PERP_0"
  ]
}

{
  "op": "unsubscribe",
  "args": [
    "snapshotL1:BTC-PERP_0"
  ]
}
```

> Response

```json
{
  "topic": "snapshotL1:BTC-PERP_0",
  "data": {
    "bids": [
      [
          "28064.9",
          "1268"
      ]
    ],
    "asks": [
      [
          "28065.0",
          "1015"
      ]
    ],
    "type": "snapshotL1",
    "symbol": "BTC-PERP",
    "timestamp": 1680751558529
  }
}
```

Subscribe to the Level 1 Orderbook through the endpoint `wss://ws.btse.com/ws/oss/futures`. The format to subscribe to will be `symbol_grouping`.

* `symbol` indicates the market symbol
* `grouping` indicates the grouping granularity. Valid values are 0-8.

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
    "update:BTC-PERP_0"
  ]
}
```

```json
{
  "op": "unsubscribe",
  "args": [
    "update:BTC-PERP_0"
  ]
}
```

> Response

```json
{
  "topic": "update:BTC-PERP_0",
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
        "59278.5",
        "0.01472"
      ]
    ],
    "seqNum": 628282,
    "prevSeqNum": 628281,
    "type": "snapshot",
    "timestamp": 1565135165600,
    "symbol": "BTC-PERP"
  }
}
```

```json
{
  "topic": "update:BTC-PERP",
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
    "symbol": "BTC-PERP"
  }
}
```

Subscribe to Orderbook incremental updates through the endpoint `wss://ws.btse.com/ws/oss/futures`. The format of topic will be `update:symbol_grouping` (eg. `update:BTC-PERP_0`). The first response received will be a snapshot of the current orderbook (this is indicated in the `type` field) and 50 levels will be returned. Incremental updates will be sent in subsequent packets with type `delta`.

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
     * `wss://ws.btse.com/ws/futures`
  * Testnet
    * `wss://testws.btse.io/ws/futures`

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

Here is an example for topic subscription.

> Request

```json
{
  "op": "subscribe",
  "args": [
    "tradeHistoryApiV3:BTC-PERP"
  ]
}
```

> Response

```json
{
  "event": "subscribe",
  "channel": [
    "tradeHistoryApiV3:BTC-PERP"
  ]
}
```

To subscribe to a websocket public trade fill

### Request Parameters

| Name | Type   | Required | Description                                                                                                            |
| ---  | ---    | ---      | ---                                                                                                                    |
| op   | String | Yes      | Operation. `subscribe` will subscribe to the topics provided in `args`. `unsubscribe` will unsubscribe from the topics |
| args | Array  | Yes      | Topics to subscribe to.                                                                                                |

### Response Content

| Name    | Type   | Required | Description                                   |
| ---     | ---    | ---      | ---                                           |
| event   | String | Yes      | Respond with the event type                   |
| channel | Array  | Yes      | Topics which have been successfully subscribed |




## Public Trade Fills

> Request

```json
{
  "op": "subscribe",
  "args": [
    "tradeHistoryApiV3:BTC-PERP"
  ]
}
```

> Response – Subscription Acknowledged

```json
{
  "event": "subscribe",
  "channel": [
    "tradeHistoryApiV3:BTC-PERP"
  ]
}
```

> Response – Data Notification

```json
{
  "topic": "tradeHistoryApiV3:BTC-PERP",
  "data": [
      {
        "price": 111144.8,
        "size": 152,
        "side": "SELL",
        "symbol": "BTC-PERP",
        "tradeId": 927002515,
        "timestamp": 1752129545326
      }
  ]
}
```

Subscribe to recent trade feed for a market. The topic will be `tradeHistoryApiV3:<market>` where `<market>` is the market symbol.

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
echo -n "/ws/futures1624985375123"  | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= bd8afb8bee58ba0a2c67f84dcfe6e64d0274f55d064bb26ea84a0fe6dd8c621b541b511982fb0c0b8c244e9521a80ea1
```


## Notifications

> Request

```json
{
  "op": "subscribe",
  "args": [
    "notificationApiV4"
  ]
}
```

> Response

```json
{
  "topic": "notificationApiV4",
  "data": [
    {
      "symbol": "BTC-PERP",
      "orderID": "45e8bb8d-d708-4a90-a428-c61583f90efe",
      "side": "BUY",
      "orderType": 77,
      "type": 0,
      "price": 111085.1,
      "triggerPrice": 0,
      "pegPriceDeviation": 1,
      "stealth": 1,
      "status": 4,
      "timestamp": 1752147101805,
      "avgFilledPrice": 111085.1,
      "clOrderID": "",
      "postOnly": false,
      "maker": false,
      "positionId": "BTC-PERP-USDT",
      "orderDetailType": null,
      "orderUserInitiated": true,
      "originalOrderSize": 900,
      "currentOrderSize": 900,
      "filledSize": 900,
      "totalFilledSize": 900,
      "remainingSize": 0,
      "time_in_force": "GTC"
    }
  ]
}

```

To receive trade notifications, subscribe to the `notificationApiV3` or `notificationApiV4` topics. It is recommended to use `notificationApiV4`, which includes structured and clearly defined fields related to order size changes (e.g., original, filled, remaining). This ensures better consistency with recent API field updates. The WebSocket feed will push real-time, trade-level notifications to authenticated subscribers.
Please note, if the topic is subscribed to without proper authentication, no messages will be delivered.

### Response Content

| Name              | Type    | Required | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|-------------------| ---     | ---      |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol            | String  | Yes      | Market symbol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| orderID           | String  | Yes      | Internal order ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| side              | String  | Yes      | Trade side. BUY or SELL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| type              | Integer     | Yes      | Order type. Valid values are:<br/>76: Limit Order<br/>77: Market Order<br/>80: Algo orders                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| price             | Double  | Yes      | Order price or transcated price                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| originalOrdersize              | Integer  | Yes      | The original order quantity. This value will not change even if adjustments are made later.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| currentOrderSize      | Integer  | Yes      | The latest order quantity, which means the sum of the filled quantity and the remaining unfilled quantity.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| avgFilledPrice    | Double  | Yes      | Average filled price                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| filledSize          | Integer  | Yes      | The quantity of the order that has been filled.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| totalFilledSize          | Integer  | Yes      | Cumulative filled quantity of this order.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| status            | Integer | Yes      | Status with values as follows:<br/>1: MARKET_UNAVAILABLE, Market is currently unavailable<br/>2: ORDER_INSERTED, Order is inserted successfully<br/>4: ORDER_FULLY_TRANSACTED, Order is fully transacted<br/>5: ORDER_PARTIALLY_TRANSACTED, Order is partially transacted<br/>6: ORDER_CANCELLED, Order is cancelled successfully<br/>8: INSUFFICIENT_BALANCE, Insufficient balance in account<br/>9: TRIGGER_INSERTED, Trigger Order is inserted successfully<br/>10: TRIGGER_ACTIVATED, Trigger Order is activated successfully<br/>12: ERROR_UPDATE_RISK_LIMIT, Error in updating risk limit<br/>15: ORDER_REJECTED, Change made to the order was unsuccessful<br/>20: SUCCESS, Trade finished successfully<br/>27: TRANSFER_SUCCESSFUL, Transfer funds between futures and spot is successful<br/>28: TRANSFER_UNSUCCESSFUL, Transfer funds between spot and futures is unsuccessful<br/>41: ERROR_INVALID_RISK_LIMIT, Invalid risk limit was specified<br/>64: STATUS_LIQUIDATION, Account is undergoing liquidation<br/>96: FUTURES_CONFIG_SETTLE_WITH_ASSET, Set futures settle currency<br/>101: FUTURES_ORDER_PRICE_OUTSIDE_LIQUIDATION_PRICE, Futures order is outside of liquidation price<br/>305: ERROR_ORDER_PRICE_OUT_OF_PRICE_PROTECTION_RANGE, order price is out of the protection range<br/>1003: ORDER_LIQUIDATION, Order is undergoing liquidation<br/>1004: ORDER_ADL, Order is undergoing ADL<br/> For more status, please refer to [`API Enum`](#api-enum) |
| clOrderID         | String  | Yes      | Custom order ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| maker             | Boolean | Yes      | Indicator to indicate if trade is a maker trade                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| remainingSize     | Integer  | Yes      | Remaining size on the order                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| time_in_force     | String  | Yes      | Validity of the order                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| timestamp         | Long    | Yes      | Order timestamp or transacted timestamp                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| txType            | String  | Yes      | Used by trigger or OCO orders. STOP indicates its a Stop order, TAKEPROFIT indicates its a take profit order, and LIMIT is when its not any of the above                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| stealth           | Double  | Yes      | Percentage of orders to show on orderbook. Only for Algo orders                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| pegPriceDeviation | Double  | Yes      | Deviation percentage. Only for Algo orders                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| positionId        | String  | Yes      | Position ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

## User Trade Fills

> Request

```json
{
  "op":"subscribe",
  "args":["fillsV2"]
}
```

> Response

```json
{
    "topic": "fillsV2",
    "id": "",
    "data": [
        {
            "orderId": "6aa36da1-0ed8-46c1-9327-c9d6313b3d12",
            "serialId": 189349157,
            "clOrderId": "_W_ekxogc1711427518228",
            "type": "77",
            "symbol": "BTC-PERP",
            "side": "BUY",
            "price": "69704.4",
            "size": "1.0",
            "feeAmount": "0.0348522",
            "feeCurrency": "USDT",
            "base": "BTC-PERP",
            "quote": "USDT",
            "maker": false,
            "timestamp": 1711427518338,
            "contractSize": 0.0001,
            "tradeId": "e094117f-9f84-4c82-b55d-d3d2a54d0dca"
        }
    ]
}


```

When a trade has been transacted, this topic will send the trade information back to the subscriber.

### Response Content

| Name        | Type    | Required | Description                                                                                |
| ---         | ---     | ---      | ---                                                                                        |
| symbol      | String  | Yes      | Market symbol                                                                              |
| orderId     | String  | Yes      | Internal order ID                                                                          |
| clOrderId   | String  | Yes      | Custom order ID                                                                            |
| serialId    | Long    | Yes      | Trade sequence ID                                                                          |
| tradeId     | String  | Yes      | Trade unique identifier                                                                    |
| type        | Integer     | Yes      | Order type. Valid values are:<br/>76: Limit Order<br/>77: Market Order<br/>80: Algo orders |
| side        | String  | Yes      | Trade side. BUY or SELL                                                                    |
| price       | Double  | Yes      | Transcated price                                                                           |
| size        | Double  | Yes      | Transacted size                                                                            |
| feeAmount   | Double  | Yes      | Fee amount charged                                                                         |
| feeCurrency | String  | Yes      | Fee currency                                                                               |
| base        | String  | Yes      | Base currency                                                                              |
| quote       | String  | Yes      | Quote currency                                                                             |
| maker       | Boolean | Yes      | Indicator to indicate if trade is a maker trade                                            |
| timestamp   | Long    | Yes      | Order timestamp or transacted timestamp                                                    |

## All Position

> Request

```json
{
  "op":"subscribe",
  "args":["allPositionV4"]
}
```

> Response

```json
{
  "topic": "allPositionV4",
  "data": [
    {
      "requestId": 0,
      "username": "demonleader",
      "userCurrency": null,
      "marketName": "BTC-PERP-USDT",
      "orderType": 90,
      "orderMode": 66,
      "status": 65,
      "originalAmount": 0.00001,
      "maxPriceHeld": 0,
      "pegPriceMin": 0,
      "stealth": 1,
      "baseCurrency": null,
      "quoteCurrency": null,
      "quoteCurrencyFiat": false,
      "parents": null,
      "makerFeesRatio": null,
      "takerFeesRatio": [
        0.00055
      ],
      "orderID": "72528866-cd9b-4472-a06b-b2d5c5766f5f",
      "vendorName": null,
      "botID": null,
      "maxStealthDisplayAmount": 0,
      "sellexchangeRate": 0,
      "tag": null,
      "triggerPrice": 116682.3,
      "closeOrder": true,
      "dbBaseBalHeld": 0,
      "dbQuoteBalHeld": -5.738340149,
      "isFuture": true,
      "liquidationInProgress": false,
      "marginType": 91,
      "entryPrice": 111126,
      "liquidationPrice": 0,
      "markedPrice": 111115.5,
      "marginHeld": 0,
      "unrealizedProfitLoss": -0.094395,
      "totalMaintenanceMargin": 5.643945149,
      "totalContracts": 899,
      "marginChargedLongOpen": 0,
      "marginChargedShortOpen": 0,
      "unchargedMarginLongOpen": 0,
      "unchargedMarginShortOpen": 0,
      "isolatedCurrency": null,
      "isolatedLeverage": 0,
      "totalFees": 0,
      "totalValue": 998.928345,
      "adlScoreBucket": 1,
      "adlScorePercentile": 0.0070422535,
      "orderTypeName": "TYPE_FUTURES_POSITION",
      "orderModeName": "MODE_BUY",
      "marginTypeName": "FUTURES_MARGIN_CROSS",
      "currentLeverage": 0.009991421,
      "contractSize": 0.00001,
      "minimumRequiredMargin": 0,
      "filledSize": 0,
      "takeProfitOrder": {
        "orderId": "72528866-cd9b-4472-a06b-b2d5c5766f5f",
        "side": "SELL",
        "triggerPrice": 116682.3,
        "triggerUseLastPrice": false
      },
      "stopLossOrder": {
        "orderId": "dbd9cdb7-6b04-49e0-990a-7c21a87486e5",
        "side": "SELL",
        "triggerPrice": 110014.7,
        "triggerUseLastPrice": false
      },
      "positionId": "BTC-PERP-USDT",
      "activeWalletName": "CROSS@",
      "positionMode": "ONE_WAY",
      "positionDirection": "LONG",
      "serviceType": 0,
      "avgFilledPrice": 0,
      "future": true,
      "settleWithNonUSDAsset": "USDT"
    }
  ]
}
```

All futures positions will be pushed via this topic once the position changes.

### Response Content

| Name                    | Type    | Required | Description                                    |
| ---                     | ---     | ---      |------------------------------------------------|
| requestId               | Integer | Yes      | request id                                     |
| username                | String  | Yes      | btse username                                  |
| marketName              | String  | Yes      | market name                                    |
| orderType               | Integer | Yes      | 90: Futures Position                           |
| orderTypeName           | String  | Yes      | String representation of orderType             |
| orderMode               | Integer | Yes      | 66: BUY<br/>83: SELL                           |
| orderModeName           | String  | Yes      | String representation of orderModeName         |
| originalAmount          | Double  | Yes      | order amount                                   |
| maxPriceHeld            | Double  | Yes      | max price of all time                          |
| pegPriceMin             | Double  | Yes      | peg price min                                  |
| stealth                 | Double  | Yes      | used for peg order                             |
| orderID                 | String  | Yes      | order id                                       |
| maxStealthDisplayAmount | Double  | Yes      | used for peg order                             |
| sellexchangeRate        | Double  | Yes      |                                                |
| triggerPrice            | Double  | Yes      | OCO order                                      |
| closeOrder              | Boolean | Yes      | whether it has an order to close this position |
| liquidationInProgress   | Boolean | Yes      | whether is in liquidation                      |
| marginType              | Integer | Yes      | WALLET TYPE:<br/>91: CROSS<br/>92: ISOLDATED   |
| marginTypeName          | String  | Yes      | String representation of marginType            |
| entryPrice              | Double  | Yes      | entry price                                    |
| liquidationPrice        | Double  | Yes      | liquidation price                              |
| markPrice               | Double  | Yes      | mark price                                     |
| unrealizedProfitLoss    | Double  | Yes      | unrealized pnl                                 |
| totalMaintenanceMargin  | Double  | Yes      | maintenance margin                             |
| totalContract           | Double  | Yes      | size of the contract                           |
| isolatedLeverage        | Double  | Yes      |                                                |
| totalFees               | Double  | Yes      |                                                |
| totalValue              | Double  | Yes      |                                                |
| adlScoreBucket          | Double  | Yes      |                                                |
| currentLeverage         | Double  | Yes      |                                                |
| avgFilledPrice            | Double  | Yes      |                                                |
| settleWithNonUSDAsset   | String  | Yes      |                                                |
| takeProfitOrder        | TakeProfitOrder object | No | Take profit order info                         |
| stopLossOrder          | StopLossOrder object   | No | Stop loss order info                           |
| positionMode            | String  | Yes      | Position mode<br/>ONE_WAY, HEDGE or ISOLATED   |
| positionDirection       | String  | Yes      | Position direction                             |
| positionId              | String  | Yes      | Position id                                    |
| contractSize            | Double  | Yes      | The position contract size                   |

## Positions

> Request

```json
{
  "op":"subscribe",
  "args":["positionsV3"]
}
```
> Response

```json
{
  "topic": "positionsV3",
  "data": [
    {
      "requestId": 0,
      "username": "demonleader",
      "userCurrency": null,
      "marketName": "QA-PERP-USDT",
      "orderType": 90,
      "orderMode": 66,
      "status": 65,
      "originalAmount": 0.01,
      "maxPriceHeld": 0,
      "pegPriceMin": 0,
      "stealth": 1,
      "baseCurrency": null,
      "quoteCurrency": null,
      "quoteCurrencyFiat": false,
      "parents": null,
      "makerFeesRatio": null,
      "takerFeesRatio": [
        0.00055
      ],
      "orderID": null,
      "vendorName": null,
      "botID": null,
      "maxStealthDisplayAmount": 0,
      "sellexchangeRate": 0,
      "tag": null,
      "triggerPrice": 0,
      "closeOrder": false,
      "dbBaseBalHeld": 0,
      "dbQuoteBalHeld": -56.4435,
      "isFuture": true,
      "liquidationInProgress": false,
      "marginType": 91,
      "entryPrice": 1500,
      "liquidationPrice": 0,
      "markedPrice": 1500,
      "marginHeld": 0,
      "unrealizedProfitLoss": 0,
      "totalMaintenanceMargin": 56.4435,
      "totalContracts": 666,
      "marginChargedLongOpen": 0,
      "marginChargedShortOpen": 0,
      "unchargedMarginLongOpen": 0,
      "unchargedMarginShortOpen": 0,
      "isolatedCurrency": null,
      "isolatedLeverage": 0,
      "totalFees": 0,
      "totalValue": 9990,
      "adlScoreBucket": 2,
      "adlScorePercentile": 0.75,
      "orderTypeName": "TYPE_FUTURES_POSITION",
      "orderModeName": "MODE_BUY",
      "marginTypeName": "FUTURES_MARGIN_CROSS",
      "currentLeverage": 0.0999085912,
      "contractSize": 0.01,
      "minimumRequiredMargin": 0,
      "filledSize": 0,
      "takeProfitOrder": null,
      "stopLossOrder": null,
      "positionId": "QA-PERP-USDT",
      "activeWalletName": "CROSS@",
      "positionMode": "ONE_WAY",
      "positionDirection": "LONG",
      "serviceType": 0,
      "avgFilledPrice": 0,
      "settleWithNonUSDAsset": "USDT",
      "future": true
    }
  ]
}
```

> Response (The position has been closed)

```json
{
  "topic": "positionsV3",
  "data": [
    {
      "requestId": 0,
      "username": "demonleader",
      "userCurrency": null,
      "marketName": "QA-PERP-USDT",
      "orderType": 0,
      "orderMode": 0,
      "status": 65,
      "originalAmount": 0,
      "maxPriceHeld": 0,
      "pegPriceMin": 0,
      "stealth": 0,
      "baseCurrency": null,
      "quoteCurrency": null,
      "quoteCurrencyFiat": false,
      "parents": null,
      "makerFeesRatio": null,
      "takerFeesRatio": null,
      "orderID": null,
      "vendorName": null,
      "botID": null,
      "maxStealthDisplayAmount": 0,
      "sellexchangeRate": 0,
      "tag": null,
      "triggerPrice": 0,
      "closeOrder": false,
      "dbBaseBalHeld": 0,
      "dbQuoteBalHeld": 0,
      "isFuture": false,
      "liquidationInProgress": false,
      "marginType": 0,
      "entryPrice": 0,
      "liquidationPrice": 0,
      "markedPrice": 0,
      "marginHeld": 0,
      "unrealizedProfitLoss": 0,
      "totalMaintenanceMargin": 0,
      "totalContracts": 0,
      "marginChargedLongOpen": 0,
      "marginChargedShortOpen": 0,
      "unchargedMarginLongOpen": 0,
      "unchargedMarginShortOpen": 0,
      "isolatedCurrency": null,
      "isolatedLeverage": 0,
      "totalFees": 0,
      "totalValue": 0,
      "adlScoreBucket": 0,
      "adlScorePercentile": 0,
      "orderTypeName": null,
      "orderModeName": null,
      "marginTypeName": null,
      "currentLeverage": 0,
      "contractSize": 0,
      "minimumRequiredMargin": 0,
      "filledSize": 0,
      "takeProfitOrder": null,
      "stopLossOrder": null,
      "positionId": "QA-PERP-USDT",
      "activeWalletName": null,
      "positionMode": null,
      "positionDirection": null,
      "serviceType": 0,
      "avgFilledPrice": 0,
      "settleWithNonUSDAsset": "USD",
      "future": false
    }
  ]
}
```

All futures positions will be pushed via this topic once the position changes. If the user reduces the position to 0, the topic will push data with the totalContracts value of 0 once.

### Response Content

| Name                    | Type    | Required | Description                                    |
| ---                     | ---     | ---      |------------------------------------------------|
| requestId               | Integer | Yes      | request id                                     |
| username                | String  | Yes      | btse username                                  |
| marketName              | String  | Yes      | market name                                    |
| orderType               | Integer | Yes      | 90: Futures Position                           |
| orderTypeName           | String  | Yes      | String representation of orderType             |
| orderMode               | Integer | Yes      | 66: BUY<br/>83: SELL                           |
| orderModeName           | String  | Yes      | String representation of orderModeName         |
| originalAmount          | Double  | Yes      | order amount                                   |
| maxPriceHeld            | Double  | Yes      | max price of all time                          |
| pegPriceMin             | Double  | Yes      | peg price min                                  |
| stealth                 | Double  | Yes      | used for peg order                             |
| orderID                 | String  | Yes      | order id                                       |
| maxStealthDisplayAmount | Double  | Yes      | used for peg order                             |
| sellexchangeRate        | Double  | Yes      |                                                |
| triggerPrice            | Double  | Yes      | OCO order                                      |
| closeOrder              | Boolean | Yes      | whether it has an order to close this position |
| liquidationInProgress   | Boolean | Yes      | whether is in liquidation                      |
| marginType              | Integer | Yes      | WALLET TYPE:<br/>91: CROSS<br/>92: ISOLDATED   |
| marginTypeName          | String  | Yes      | String representation of marginType            |
| entryPrice              | Double  | Yes      | entry price                                    |
| liquidationPrice        | Double  | Yes      | liquidation price                              |
| markPrice               | Double  | Yes      | mark price                                     |
| unrealizedProfitLoss    | Double  | Yes      | unrealized pnl                                 |
| totalMaintenanceMargin  | Double  | Yes      | maintenance margin                             |
| totalContract           | Double  | Yes      | size of the contract                           |
| isolatedLeverage        | Double  | Yes      |                                                |
| totalFees               | Double  | Yes      |                                                |
| totalValue              | Double  | Yes      |                                                |
| adlScoreBucket          | Double  | Yes      |                                                |
| currentLeverage         | Double  | Yes      |                                                |
| avgFilledPrice          | Double  | Yes      |                                                |
| settleWithNonUSDAsset   | String  | Yes      |                                                |
| takeProfitOrder        | TakeProfitOrder object | No | Take profit order info                         |
| stopLossOrder          | StopLossOrder object   | No | Stop loss order info                           |
| positionMode            | String  | Yes      | Position mode<br/>ONE_WAY, HEDGE or ISOLATED   |
| positionDirection       | String  | Yes      | Position direction                             |
| positionId              | String  | Yes      | Position id                                    |
| contractSize            | Double  | Yes      | The position contract size                   |

</section>
