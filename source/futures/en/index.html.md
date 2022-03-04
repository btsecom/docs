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

## Version 2.3.0 (21st Jan 2022)

* Add new two new response fields `remainingSize` and `originalSize` in [Create new order](#create-new-order), [Create new algo order](#create-new-algo-order), and [Close Position](#close-position) **[NOTE]: This change will be effective on Jan 25th 2022 (UTC+0)**

## Version 2.2.1 (26th Nov 2021)

* Update market name for futures [Orderbook websocket feed](#orderbook-incremental-updates)

## Version 2.2.0 (23rd Nov 2021)

* Addition of orderbook incremental updates [Orderbook websocket feed](#orderbook-incremental-updates)

## Version 2.1.8 (1st July 2021)

* Addition of `fills` websocket topic to subscribe to [user trade fills](#user-trade-fills)
* Addition of attribute `depth` for [Orderbook websocket feed](#orderbook-snapshot-by-depth)

## Version 2.1.7 (4th February 2021)

* Addition of `avgFilledPrice` in open_orders AP


## Version 2.1.6 (29th January 2021)

* Websockets endpoint will be updated to the following:
  * Spot: wss://ws.btse.com/ws/spot
  * Futures: wss://ws.btse.com/ws/futures

  Existing endpoints will continue to be made available.

* Login topic will now respond with a JSON success / failure message {"event":"login","success":true}
* When subscribing or unsubscribing to websocket topics, an acknowledgement will return indicating which topics are successfully subscribed / unsubscribed. Unsuccessful topics will not be returned in the response.
* Websocket notifications will have in addition the following indicators:
  * maker - Boolean indicating if an order is a maker / taker order
  * remainingSize - Value indicating the remaining size on the order
  * time_in_force - Value indicating the time in force set on the order

## Version 2.1.5 (28th September 2020)

* New Amend Order API. Allows users to edit price, size and trigger prices for pending orders

## Version 2.1.4 (24th July 2020)

* New Settle In API added, allows users to set the currency to settle the current position in via API

## Version 2.1.3 (23rd June 2020)

* Introduction of Spam Order detection mechanism
* Websocket topic notificationApiV2 introduced. Topic is meant to standardize response codes returned. Notifications are returned as an Array
* Introduction of API permissions. All current API keys will have Read, Trading and Transfer permissions. Refer to the tags beside the titles to see which category they are classified under

# Overview

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
     * `https://aws-api.btse.com/futures` (Optimised for connection via AWS)
  * Websocket
     * `wss://ws.btse.com/ws/futures`
     * `wss://aws-ws.btse.com/ws/futures` (Optimised for connection via AWS)
* Testnet
  * HTTP
     * `https://testapi.btse.io/futures`
  * Websocket
     * `wss://testws.btse.io/ws/futures`

## Authentication

* API Key (btse-api)
  * Parameter Name: `btse-api`, in: header. API key is obtained from BTSE platform as a string

* API Key (btse-nonce)
  * Parameter Name: `btse-nonce`, in: header. Representation of current timestamp in long format

* API Key (btse-sign)
  * Parameter Name: `btse-sign`, in: header. A composite signature produced based on the following algorithm: Signature=HMAC.Sha384 (secretkey, (urlpath + btse-nonce + bodyStr)) (note: bodyStr = '' when no data):

### Example 1: Get Wallet

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v2.1/user/wallet1624984297330" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= ea4f1f2b43a0f4d750ae560c5274d6214d140fcab3093da5f4a83e36828535bd2ba7b12160cd12199596f422c8883333
```

* Endpoint to get wallet is `https://api.btse.com/futures/api/v2.1/user/wallet`
* Assume we have the values as follows:
  * btse-nonce: `1624984297330`
  * btse-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v2.1/user/wallet`
* Generated signature will be:
  * btse-sign: `ea4f1f2b43a0f4d750ae560c5274d6214d140fcab3093da5f4a83e36828535bd2ba7b12160cd12199596f422c8883333`

### Example 2: Place an order

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v2.1/order1624985375123{\"postOnly\":false,\"price\":8500.0,\"reduceOnly\":false,\"side\":\"BUY\",\"size\":1,\"stopPrice\":0.0,\"symbol\":\"BTCPFC\",\"time_in_force\":\"GTC\",\"trailValue\":0.0,\"triggerPrice\":0.0,\"txType\":\"LIMIT\",\"type\":\"LIMIT\"}" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 943adfce43b609a28506274976b96e08cf4bdc4ea53ca0b4cac0eb2cf0773a7d0807efc0aeab779d47fadcd9a60eea13
```

* Endpoint to place an order is `https://api.btse.com/futures/api/v2.21/order`
* Assume we have the values as follows:
  * btse-nonce: `1624985375123`
  * btse-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v2.1/order`
  * Body: `{"postOnly":false,"price":8500.0,"reduceOnly":false,"side":"BUY","size":5,"stopPrice":0.0,"symbol":"BTCPFC","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
  * Encrypted Text: `/api/v2.1/order1624985375123{"postOnly":false,"price":8500.0,"reduceOnly":false,"side":"BUY","size":5,"stopPrice":0.0,"symbol":"BTCPFC","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
* Generated signature will be:
  * btse-sign: `943adfce43b609a28506274976b96e08cf4bdc4ea53ca0b4cac0eb2cf0773a7d0807efc0aeab779d47fadcd9a60eea13`


## Rate Limits

* The following rate limits are enforced:

Rate limits for BTSE is as follows:

**Query**

* Per API: `15 requests/second`
* Per User: `30 requests/second`

**Orders**

* Per API: `75 requests/second`
* Per User: `75 requests/second`

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

When connecting up the BTSE API, you will come across number codes that represents different states or status types in BTSE. The following section provides a list of codes that you are expecting to see.

* 1: MARKET_UNAVAILABLE = Futures market is unavailable
* 2: ORDER_INSERTED = Order is inserted successfully
* 4: ORDER_FULLY_TRANSACTED = Order is fully transacted
* 5: ORDER_PARTIALLY_TRANSACTED = Order is partially transacted
* 6: ORDER_CANCELLED = Order is cancelled successfully
* 8: INSUFFICIENT_BALANCE = Insufficient balance in account
* 9: TRIGGER_INSERTED = Trigger Order is inserted successfully
* 10: TRIGGER_ACTIVATED = Trigger Order is activated successfully
* 12: ERROR_UPDATE_RISK_LIMIT = Error in updating risk limit
* 15: ORDER_REJECTED = Order is rejected
* 16: ORDER_NOTFOUND = Order is not found with the order ID or clOrderID provided
* 28: TRANSFER_UNSUCCESSFUL = Transfer funds between spot and futures is unsuccessful
* 27: TRANSFER_SUCCESSFUL = Transfer funds between futures and spot is successful
* 41: ERROR_INVALID_RISK_LIMIT = Invalid risk limit was specified
* 64: STATUS_LIQUIDATION = Account is undergoing liquidation
* 65: ORDER_ACITVE = Order is active
* 76: ORDER_TYPE_LIMIT = Limit order
* 77: ORDER_TYPE_MARKET = Market order
* 80: ORDER_TYPE_PEG = Peg/Algo order
* 81: ORDER_TYPE_OTC = Otc order
* 88: ORDER_INACTIVE = Order is inactive
* 101: FUTURES_ORDER_PRICE_OUTSIDE_LIQUIDATION_PRICE = Futures order is outside of liquidation price
* 123: AMEND_ORDER = Order amended
* 1003: ORDER_LIQUIDATION = Order is undergoing liquidation
* 1004: ORDER_ADL = Order is undergoing ADL

## Spam Orders

Spam orders are large number of small order sizes that is placed. In order to ensure that the platform and user's interests are protected from malicious players, we will apply the following for users placing small sized orders.

* Orders equal to or below 5 contracts will be marked as a spam order and will automatically become hidden orders.
* Orders marked as spam always pay the taker fee.
* Post-Only API orders marked as spam will be rejected instead of being hidden.
* Too many spam orders may be grounds to temporarily ban an account from trading.
* API accounts placing >= 4 resting orders, with total size less than 20 contracts are at risk of being marked as a spam account.
* Accounts marked as spam may have limitations placed on the account, including order rate limits, position limits, or have API functions disabled. For questions regarding the new spam order mechanism, please email mm@btse.com.



# Public Endpoints

## Market Summary

> Response

```json
[
  {
    "symbol": "BTCPFC",
    "last": 36365,
    "lowestAsk": 36377,
    "highestBid": 36376,
    "percentageChange": 4.973731309,
    "volume": 172418318.7575521,
    "high24Hr": 36447,
    "low24Hr": 33989.5,
    "base": "BTC",
    "quote": "USD",
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
    "futures": false
  }
]
```

`GET /api/v2.1/market_summary`

Gets market summary information. If no symbol parameter is sent, then all markets will be retrieved.

### Request Parameters

| Name   | Type   | Required | Description   |
| ---    | ---    | ---      | ---           |
| symbol | string | No       | Market symbol |

### Response Content

| Name                | Type    | Required | Description                                                          |
| ---                 | ---     | ---      | ---                                                                  |
| symbol              | string  | Yes      | Market symbol                                                        |
| last                | double  | Yes      | Last price                                                           |
| lowestAsk           | double  | Yes      | Lowest ask price in the orderbook                                    |
| highestBid          | double  | Yes      | Highest bid price in the orderbook                                   |
| percentageChange    | double  | Yes      | Percentage change against the price within the last 24hours          |
| volume              | double  | Yes      | Transacted volume                                                    |
| high24Hr            | double  | Yes      | Highest price over the last 24hours                                  |
| low24Hr             | double  | Yes      | Lowest price over the last 24hours                                   |
| base                | string  | Yes      | Base currency                                                        |
| quote               | string  | Yes      | Quote currency                                                       |
| active              | boolean | Yes      | Indicator if market is active                                        |
| size                | double  | Yes      | Transacted size                                                      |
| minValidPrice       | double  | Yes      | Minimum valid price                                                  |
| minPriceIncrement   | double  | Yes      | Price increment                                                      |
| minOrderSize        | double  | Yes      | Minimum tick size                                                    |
| minSizeIncrement    | double  | Yes      | Tick size                                                            |
| maxOrderSize        | double  | Yes      | Maximum order size                                                   |
| openInterest        | double  | No       | Number of open positions in the futures market                       |
| openInterestUSD     | double  | No       | Number of open positions in the futures market in USD notional value |
| contractStart       | long    | No       | Contract start time                                                  |
| contractEnd         | long    | No       | Contract end time                                                    |
| timeBasedContract   | boolean | No       | Indicator to indicate if it is a time based contract                 |
| openTime            | long    | Yes      | Market opening time                                                  |
| closeTime           | long    | Yes      | Market closing time                                                  |
| startMatching       | long    | Yes      | Matching start time                                                  |
| inactiveTime        | long    | Yes      | Time where market is inactive                                        |
| fundingRate         | double  | No       | Funding rate calculated per hour                                     |
| contractSize        | double  | No       | Size of one contract                                                 |
| maxPosition         | double  | No       | Maximum position a user is allowed to have                           |
| minRiskLimit        | double  | No       | Minimum risk limit                                                   |
| maxRiskLimit        | double  | No       | Maximum risk limit                                                   |
| availableSettlement | array   | No       | Currencies available for settlement                                  |
| futures             | boolean | Yes      | Indicator if symbol is a futures contract                            |

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
  ],
```

`GET /api/v2.1/ohlcv`

Gets candle stick charting data. Default of 300 data points will be returned at any one time.

### Request Parameters

| Name       | Type   | Required | Description                                                                                                                         |
| ---        | ---    | ---      | ---                                                                                                                                 |
| symbol     | string | Yes      | Market symbol                                                                                                                       |
| start      | long   | No       | Starting time (eg. 1624987283000)                                                                                                   |
| end        | long   | No       | Ending time (eg. 1624987283000)                                                                                                     |
| resolution | string | Yes      | Supported resolutions are: <br/> 1: 1min<br/> 5: 5mins<br/> 15: 15mins<br/>30: 30mins<br/>60: 60mins<br/>360: 6hours<br/>1440: 1day |


### Response Content

Returns a 2D array with the indexes described in the table below

| Index | Type   | Required | Description   |
| ---   | ---    | ---      | ---           |
| 0     | long   | Yes      | Unix time     |
| 1     | double | Yes      | Open price    |
| 2     | double | Yes      | High Price    |
| 3     | double | Yes      | Low price     |
| 4     | double | Yes      | Closing price |
| 5     | double | Yes      | Volume        |


## Query Market price

> Response

```json
[
  {
    "symbol": "BTCPFC",
    "indexPrice": 36288.949684967,
    "lastPrice": 36286.5,
    "markPrice": 0
  }
]
```

`GET /api/v2.1/price`

Retrieve current prices on the platform. If no symbol specified, all symbols will be returned.

### Request Parameters

| Name   | Type   | Required | Description   |
| ---    | ---    | ---      | ---           |
| symbol | string | Yes      | Market symbol |


### Response Content

| Name       | Type   | Required | Description           |
| ---        | ---    | ---      | ---                   |
| symbol     | double | Yes      | Market symbol         |
| indexPrice | double | Yes      | Index price           |
| lastPrice  | double | Yes      | Last transacted price |
| markPrice  | double | Yes      | Mark price            |

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
  "symbol": "BTCPFC"
}
```

`GET /api/v2.1/orderbook/{symbol}`

Retrieves a snapshot of the orderbook.

### Request Parameters

| Name   | Type   | Required | Description                               |
| ---    | ---    | ---      | ---                                       |
| symbol | string | Yes      | Market symbol, entered as a path variable |


### Response Content

#### Orderbook

| Name      | Type   | Required | Description            |
| ---       | ---    | ---      | ---                    |
| symbol    | string | Yes      | Market symbol          |
| buyQuote  | Quote  | Yes      | Array of Buy quotes    |
| sellQuote | Quote  | Yes      | Array of Sell quotes   |
| timestamp | double | Yes      | Timestamp of orderbook |

#### Quote

| Name  | Type   | Required | Description |
| ---   | ---    | ---      | ---         |
| price | double | Yes      | order price |
| size  | double | Yes      | order size  |



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
  "symbol": "BTCPFC"
}
```

`GET /api/v2.1/orderbook/L2`

Retrieves a Level 2 snapshot of the orderbook

### Request Parameters

| Name   | Type    | Required | Description     |
| ---    | ---     | ---      | ---             |
| symbol | string  | Yes      | Market symbol   |
| depth  | integer | No       | Orderbook depth |

### Response Content

#### Orderbook

| Name      | Type   | Required | Description            |
| ---       | ---    | ---      | ---                    |
| symbol    | string | Yes      | Market symbol          |
| buyQuote  | Quote  | Yes      | Array of Buy quotes    |
| sellQuote | Quote  | Yes      | Array of Sell quotes   |
| timestamp | double | Yes      | Timestamp of orderbook |

#### Quote

| Name  | Type   | Required | Description |
| ---   | ---    | ---      | ---         |
| price | double | Yes      | order price |
| size  | double | Yes      | order size  |


## Query Trades Fills

> Response

```json
[
  {
    "price": 36164,
    "size": 100,
    "side": "SELL",
    "symbol": "BTCPFC",
    "serialId": 85997835,
    "timestamp": 1624990097000
  }
]
```

`GET /api/v2.1/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

| Name           | Type    | Required | Description                                                                       |
| ---            | ---     | ---      | ---                                                                               |
| symbol         | string  | Yes      | Market symbol                                                                     |
| startTime      | long    | No       | Starting time (eg. 1624987283000)                                                 |
| endTime        | long    | No       | Ending time (eg. 1624987283000)                                                   |
| beforeSerialId | string  | Yes      | Condition to retrieve records before the specified serial Id. Used for pagination |
| afterSerialId  | string  | Yes      | Condition to retrieve records after the specified serial Id. Used for pagination  |
| count          | integer | Yes      | Number of records to return                                                       |
| includeOld     | boolean | Yes      | Retrieve trade  history records past 7 days                                       |


### Response Content

| Name      | Type   | Required | Description                             |
| ---       | ---    | ---      | ---                                     |
| symbol    | string | Yes      | Market symbol                           |
| side      | string | Yes      | Trade side. Values are: [`Buy`, `SELL`] |
| price     | double | Yes      | Transacted price                        |
| size      | double | Yes      | Transacted size                         |
| serialId  | double | Yes      | Serial Id, running sequence number      |
| timestamp | double | Yes      | Transacted timestamp                    |


# Trade Endpoints

## Create new order

> Request

```json
{
  "clOrderID": "string",
  "deviation": 0,
  "postOnly": false,
  "price": 8300,
  "side": "BUY",
  "size": 4,
  "stealth": 0,
  "stopPrice": 0,
  "symbol": "BTCPFC",
  "time_in_force": "GTC",
  "trailValue": 0,
  "triggerPrice": 0,
  "txType": "LIMIT",
  "type": "LIMIT"
}
```

> Response

```json
{
  "averageFillPrice": 0,
  "clOrderID": "string",
  "deviation": 0,
  "fillSize": 0,
  "message": "string",
  "orderID": "string",
  "orderType": 76,
  "price": 0,
  "side": "BUY",
  "size": 4,
  "status": 0,
  "stealth": 0,
  "stopPrice": 8300,
  "symbol": "BTCPFC",
  "timestamp": 1576812000872,
  "trigger": true,
  "triggerPrice": 8300,
  "remainingSize": 2,
  "orginialSize": 4
}
```

`POST /api/v2.1/order`

Creates a new order. Requires `Trading` permission

### Request Parameters

| Name          | Type    | Required | Description                                                                                                                                                                                                                                                                                                                |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                                        |
| symbol        | string  | Yes      | Market symbol                                                                                                                                                                                                                                                                                                              |
| price         | double  | Yes      | Order price                                                                                                                                                                                                                                                                                                                |
| size          | double  | Yes      | Order size                                                                                                                                                                                                                                                                                                                 |
| time_in_force | string  | No       | Time validity of the order<br/>GTC: Good till Cancel<br/>IOC: Immediate or Cancel<br/>FOK: Fill or Kill<br/>FIVEMIN: Order valid for 5 mins<br/> HOUR: Order valid for an hour<br/>TWELVEHOUR: Order valid for 12 hours<br/>DAY: Order valid for a day<br/>WEEK: Order valid for a week<br/>MONTH: Order valid for a month |
| type          | string  | Yes      | Order type<br/>LIMIT: Limit Orders<br/>MARKET: Market Orders<br/>OCO: One cancel the other                                                                                                                                                                                                                                 |
| txType        | string  | Yes      | Used for Stop orders or trigger orders<br/>STOP: Stop Order, `stopPrice` is mandatory<br/>TRIGGER: Trigger order, `triggerPrice` is mandatory<br/>LIMIT: Default, used when its not a Stop order nor Trigger order                                                                                                         |
| stopPrice     | double  | No       | Mandatory when creating a Stop or OCO order. Indicates the stop price                                                                                                                                                                                                                                                      |
| triggerPrice  | double  | Yes      | Mandatory when creating a Trigger or OCO order. Indicates the trigger price                                                                                                                                                                                                                                                |
| trailValue    | double  | Yes      | Trail value                                                                                                                                                                                                                                                                                                                |
| postOnly      | boolean | Yes      | Boolean to indicate if this is a post only order. For post only orders, traders are charged maker fees                                                                                                                                                                                                                     |
| reduceOnly    | boolean | Yes      | Boolean to indicate if this is a reduce only order.                                                                                                                                                                                                                                                                        |
| clOrderID     | string  | Yes      | Custom order Id                                                                                                                                                                                                                                                                                                            |


### Response Content

| Name             | Type    | Required | Description                                                                                                                                                                                                                                      |
| ---              | ---     | ---      | ---                                                                                                                                                                                                                                              |
| symbol           | string  | Yes      | Market symbol                                                                                                                                                                                                                                    |
| clOrderID        | string  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                   |
| fillSize         | string  | Yes      | Trade filled size                                                                                                                                                                                                                                |
| orderID          | string  | Yes      | Order ID                                                                                                                                                                                                                                         |
| orderType        | string  | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                          |
| postOnly         | boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                          |
| price            | double  | Yes      | Order price                                                                                                                                                                                                                                      |
| side             | string  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                       |
| size             | double  | Yes      | Order size                                                                                                                                                                                                                                       |
| status           | integer | Yes      | Order status<br/>	2: Order Inserted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found |
| stopPrice        | string  | Yes      | Stop price                                                                                                                                                                                                                                       |
| time_in_force    | string  | Yes      | Order validity                                                                                                                                                                                                                                   |
| timestamp        | string  | Yes      | Order timestamp                                                                                                                                                                                                                                  |
| trigger          | string  | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                            |
| triggerPrice     | string  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                   |
| averageFillPrice | string  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                           |
| message          | string  | Yes      | Trade messages                                                                                                                                                                                                                                   |
| stealth          | string  | Yes      | Only valid for Algo orders                                                                                                                                                                                                                       |
| deviation        | string  | Yes      | Only valid for Algo orders                                                                                                                                                                                                                       |
| remainingSize    | double  | Yes      | Size left to be transacted                                                                                                                                                                                                                       |
| originalSize     | double  | Yes      | Original order size                                                                                                                                                                                                                              |

## Create new algo order

> Request

```json
{
  "clOrderID": "string",
  "deviation": 0,
  "postOnly": false,
  "price": 8030,
  "side": "BUY",
  "size": 4,
  "stealth": 0,
  "stopPrice": 0,
  "symbol": "BTCPFC",
  "time_in_force": "GTC",
  "trailValue": 0,
  "triggerPrice": 0,
  "txType": "LIMIT",
  "type": "LIMIT"
}
```

> Response

```json
{
  "averageFillPrice": 0,
  "clOrderID": "string",
  "deviation": 0,
  "fillSize": 0,
  "message": "string",
  "orderID": "string",
  "orderType": 76,
  "price": 0,
  "side": "BUY",
  "size": 4,
  "status": 0,
  "stealth": 0,
  "stopPrice": 8030,
  "symbol": "BTCPFC",
  "timestamp": 1576812000872,
  "trigger": true,
  "triggerPrice": 8300,
  "remainingSize": 2,
  "orginialSize": 4
}
```

`POST /api/v3.2/order/peg`

Creates a new algo order. Algo order is an order that price will change according to market price. To create an algo order, user will need to enter additional parameters:

* `price`: What is the min price (for a sell order) or maximum price (for a buy order) that a user will be willing to list his order at
* `size`: Total size of order
* `deviation`: How much should the order price deviate from index price. Value is in percentage and can range from `-10` to `10`
* `stealth`: How many percent of the order is to be displayed on the orderbook.

This API Requires `Trading` permission

### Request Parameters

| Name          | Type    | Required | Description                                                                                                                                                                                                                                                                                                                |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                                        |
| symbol        | string  | Yes      | Market symbol                                                                                                                                                                                                                                                                                                              |
| price         | double  | Yes      | Minimum price for a sell order, this is the lowest price that a user is willing to sell at. Maximum price for a buy order, this is the maximum price a user is willing to buy at.                                                                                                                                          |
| size          | double  | Yes      | Order size                                                                                                                                                                                                                                                                                                                 |
| time_in_force | string  | No       | Time validity of the order<br/>GTC: Good till Cancel<br/>IOC: Immediate or Cancel<br/>FOK: Fill or Kill<br/>FIVEMIN: Order valid for 5 mins<br/> HOUR: Order valid for an hour<br/>TWELVEHOUR: Order valid for 12 hours<br/>DAY: Order valid for a day<br/>WEEK: Order valid for a week<br/>MONTH: Order valid for a month |
| type          | string  | Yes      | Order type<br/>LIMIT: Limit Orders<br/>MARKET: Market Orders<br/>OCO: One cancel the other                                                                                                                                                                                                                                 |
| txType        | string  | Yes      | Used for Stop orders or trigger orders<br/>STOP: Stop Order, `stopPrice` is mandatory<br/>TRIGGER: Trigger order, `triggerPrice` is mandatory<br/>LIMIT: Default, used when its not a Stop order nor Trigger order                                                                                                         |
| stopPrice     | double  | No       | Mandatory when creating a Stop or OCO order. Indicates the stop price                                                                                                                                                                                                                                                      |
| triggerPrice  | double  | Yes      | Mandatory when creating a Trigger or OCO order. Indicates the trigger price                                                                                                                                                                                                                                                |
| trailValue    | double  | Yes      | Trail value                                                                                                                                                                                                                                                                                                                |
| postOnly      | boolean | Yes      | Boolean to indicate if this is a post only order. For post only orders, traders are charged maker fees                                                                                                                                                                                                                     |
| clOrderID     | string  | Yes      | Custom order Id                                                                                                                                                                                                                                                                                                            |
| stealth       | double  | Yes      | How many percent of the order is to be displayed on the orderbook.                                                                                                                                                                                                                                                         |
| deviation     | double  | Yes      | How much should the order price deviate from index price. Value is in percentage and can range from `-10` to `10`                                                                                                                                                                                                          |

### Response Content

| Name             | Type    | Required | Description                                                                                                                                                                                                                                                              |
| ---              | ---     | ---      | ---                                                                                                                                                                                                                                                                      |
| symbol           | string  | Yes      | Market symbol                                                                                                                                                                                                                                                            |
| clOrderID        | string  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                           |
| fillSize         | string  | Yes      | Trade filled size                                                                                                                                                                                                                                                        |
| orderID          | string  | Yes      | Order ID                                                                                                                                                                                                                                                                 |
| orderType        | string  | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                                                  |
| postOnly         | boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                  |
| price            | double  | Yes      | Order price                                                                                                                                                                                                                                                              |
| side             | string  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                               |
| size             | double  | Yes      | Order size                                                                                                                                                                                                                                                               |
| status           | integer | Yes      | Order status<br/>	2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found |
| stopPrice        | string  | Yes      | Stop price                                                                                                                                                                                                                                                               |
| time_in_force    | string  | Yes      | Order validity                                                                                                                                                                                                                                                           |
| timestamp        | string  | Yes      | Order timestamp                                                                                                                                                                                                                                                          |
| trigger          | string  | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                    |
| triggerPrice     | string  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                           |
| averageFillPrice | string  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                   |
| message          | string  | Yes      | Trade messages                                                                                                                                                                                                                                                           |
| stealth          | string  | Yes      | Stealth value of order                                                                                                                                                                                                                                                   |
| deviation        | string  | Yes      | Deviation value of order                                                                                                                                                                                                                                                 |
| remainingSize    | double  | Yes      | Size left to be transacted                                                                                                                                                                                                                                               |
| originalSize     | double  | Yes      | Original order size                                                                                                                                                                                                                                                      |

## Amend Order

> Request

```json
{
  "symbol": "BTCPFC",
  "type": "PRICE",
  "orderID": "Order ID",
  "clOrderID": "Custom Order ID",
  "value": 0,
  "slide": true,
  "orderSize": 12,
  "orderPrice": 40000
}
```

> Response

```json
{
  "averageFillPrice": 0,
  "clOrderID": "string",
  "deviation": -5,
  "fillSize": 0,
  "message": "string",
  "orderID": "string",
  "orderType": 76,
  "price": 0,
  "side": "BUY",
  "size": 4,
  "status": 0,
  "stealth": 10,
  "stopPrice": 8300,
  "symbol": "BTCPFC",
  "timestamp": 1576812000872,
  "trigger": true,
  "triggerPrice": 8300
}
```

`PUT /api/v2.1/order`

Amend the price or size or trigger price of an order. For trigger orders, if the order has already been triggered, the trigger price cannot be further amended. If an order is a POST-ONLY order, and `slide` option is set to true, then price will set to be the best bid/ask price. Amend order _does not_ apply to algo orders

### Request Parameters

| Name         | Type    | Required | Description                                                                                                                                                   |
| ---          | ---     | ---      | ---                                                                                                                                                           |
| symbol       | string  | Yes      | Market symbol                                                                                                                                                 |
| orderID      | string  | No       | Internal order ID                                                                                                                                             |
| clOrderID    | string  | No       | Custom order ID                                                                                                                                               |
| type         | string  | Yes      | Type of amendmend<br/>`PRICE`: To amend order price<br/>`SIZE`: To amend order size<br/>`TRIGGER`: To amend trigger price<br/>`ALL`: to amend multiple fields |
| value        | number  | Yes      | The value to be amended to. Value depends on the type being set.                                                                                              |
| slide        | boolean | No       | Used for Post-Only orders. When set to true will set price to best bid/ask                                                                                    |
| orderPrice   | number  | No       | order price to be amended                                                                                                                                     |
| orderSize    | number  | No       | order size to be amended                                                                                                                                      |
| triggerPrice | number  | No       | trigger price to be amended                                                                                                                                   |


### Response Content

| Name             | Type    | Required | Description                                                                                                                                                                                                                                                              |
| ---              | ---     | ---      | ---                                                                                                                                                                                                                                                                      |
| symbol           | string  | Yes      | Market symbol                                                                                                                                                                                                                                                            |
| clOrderID        | string  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                           |
| fillSize         | string  | Yes      | Trade filled size                                                                                                                                                                                                                                                        |
| orderID          | string  | Yes      | Order ID                                                                                                                                                                                                                                                                 |
| orderType        | string  | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                                                  |
| postOnly         | boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                  |
| price            | double  | Yes      | Order price                                                                                                                                                                                                                                                              |
| side             | string  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                               |
| size             | double  | Yes      | Order size                                                                                                                                                                                                                                                               |
| status           | integer | Yes      | Order status<br/>	2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found |
| stopPrice        | string  | Yes      | Stop price                                                                                                                                                                                                                                                               |
| time_in_force    | string  | Yes      | Order validity                                                                                                                                                                                                                                                           |
| timestamp        | string  | Yes      | Order timestamp                                                                                                                                                                                                                                                          |
| trigger          | string  | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                    |
| triggerPrice     | string  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                           |
| averageFillPrice | string  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                   |
| message          | string  | Yes      | Trade messages                                                                                                                                                                                                                                                           |
| stealth          | string  | Yes      | Stealth value of order                                                                                                                                                                                                                                                   |
| deviation        | string  | Yes      | Deviation value of order                                                                                                                                                                                                                                                 |


## Cancel Order

> Response

```json
[
  {
    "status": 0,
    "symbol": "BTCPFC",
    "orderType": 76,
    "price": 8300,
    "side": "BUY",
    "size": 1,
    "orderID": "string",
    "timestamp": 1576812000872,
    "triggerPrice": 8300,
    "trigger": false,
    "deviation": 0,
    "stealth": 0,
    "message": "false",
    "avgFillPrice": 0,
    "fillSize": 0,
    "clOrderID": "market001"
  }
]
```

`DELETE /api/v2.1/order`

Cancels pending orders that has not yet been transacted. The `orderID` is a unique identifier to cancel a particular order. `clOrderID` is a custom ID sent in by the trader. When cancel by `clOrderID`, all orders having the same ID will be cancelled. If `orderID` and `clOrderID` is not sent in, then cancellation will be for all orders in the current market.

### Request Parameters

| Name      | Type   | Required | Description                    |
| ---       | ---    | ---      | ---                            |
| symbol    | string | Yes      | Market symbol                  |
| orderID   | string | No       | Unique identifier for an order |
| clOrderID | string | No       | Client custom order ID         |


### Response Content

| Name             | Type    | Required | Description                                                                                                                                                                                                                                                              |
| ---              | ---     | ---      | ---                                                                                                                                                                                                                                                                      |
| symbol           | string  | Yes      | Market symbol                                                                                                                                                                                                                                                            |
| clOrderID        | string  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                           |
| fillSize         | string  | Yes      | Trade filled size                                                                                                                                                                                                                                                        |
| orderID          | string  | Yes      | Order ID                                                                                                                                                                                                                                                                 |
| orderType        | string  | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                                                  |
| postOnly         | boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                  |
| price            | double  | Yes      | Order price                                                                                                                                                                                                                                                              |
| side             | string  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                               |
| size             | double  | Yes      | Cancelled size                                                                                                                                                                                                                                                           |
| status           | integer | Yes      | Order status<br/>	2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found |
| stopPrice        | string  | Yes      | Stop price                                                                                                                                                                                                                                                               |
| time_in_force    | string  | Yes      | Order validity                                                                                                                                                                                                                                                           |
| timestamp        | string  | Yes      | Order timestamp                                                                                                                                                                                                                                                          |
| trigger          | string  | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                    |
| triggerPrice     | string  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                           |
| averageFillPrice | string  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                   |
| message          | string  | Yes      | Trade messages                                                                                                                                                                                                                                                           |
| stealth          | string  | Yes      | Stealth value of order                                                                                                                                                                                                                                                   |
| deviation        | string  | Yes      | Deviation value of order                                                                                                                                                                                                                                                 |

## Dead man's switch (Cancel all after)

> Request

```json
{
  "timeout": 60000
}
```

`POST /api/v2.1/order/cancelAllAfter`

Dead-man's switch allows the trader to send in a timeout value which is a Time to live (TTL) value for an order. Extension of the timeout is done by sending another `cancelAllAfter` request. If the server does not receive another request before the timeout is reached, all orders will be cancelled.

### Request Parameters

| Name    | Type | Required | Description                   |
| ---     | ---  | ---      | ---                           |
| timeout | long | Yes      | Timeout value in milliseconds |


### Response Content

* If set correctly, a HTTP 200 response code will be returned

## Query Open Orders

> Response

```json
{
  "averageFillPrice": 0,
  "cancelDuration": 0,
  "clOrderID": "string",
  "fillSize": 0,
  "filledSize": 3,
  "orderID": "string",
  "orderState": "STATUS_ACTIVE",
  "orderType": 0,
  "orderValue": 20.625,
  "pegPriceDeviation": 3,
  "pegPriceMax": 0,
  "pegPriceMin": 0,
  "price": 6875,
  "side": "BUY",
  "size": 4,
  "symbol": "string",
  "timestamp": 0,
  "trailValue": 0,
  "triggerOrder": false,
  "triggerOrderType": 1001,
  "triggerOriginalPrice": 0,
  "triggerPrice": 0,
  "triggerStopPrice": 0,
  "triggerTrailingStopDeviation": 0,
  "triggered": true
}
```

`GET /api/v2.1/user/open_orders`

Retrieves open orders that have not yet been matched. This is also used to check an order for its status. If an order has been cancelled or recently transacted, the `status` field will indicate the state of the order. The state of an order returned in `status` field will only be made available for 30mins. After 30mins, this API will only return if the order is still active. If not it will return that the order is not found.

### Request Parameters

| Name      | Type   | Required | Description                   |
| ---       | ---    | ---      | ---                           |
| symbol    | string | Yes      | Market symbol                 |
| orderID   | string | No       | Query using internal order ID |
| clOrderID | string | No       | Query using custom order ID   |


### Response Content

| Name             | Type   | Required | Description                                                                            |
| ---              | ---    | ---      | ---                                                                                    |
| symbol           | string | Yes      | Market symbol                                                                          |
| clOrderID        | string | Yes      | Customer tag sent in by trader                                                         |
| fillSize         | string | Yes      | Trade filled size                                                                      |
| orderID          | string | Yes      | Order ID                                                                               |
| orderType        | double | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                |
| postOnly         | bool   | Yes      | Indicates if order is a post only order                                                |
| price            | double | Yes      | Order price                                                                            |
| side             | string | Yes      | Order side<br/>BUY or SELL                                                             |
| size             | double | Yes      | Cancelled size                                                                         |
| stopPrice        | double | Yes      | Stop price                                                                             |
| time_in_force    | string | Yes      | Order validity                                                                         |
| timestamp        | string | Yes      | Order timestamp                                                                        |
| trigger          | bool   | Yes      | Indicator if order is a trigger order                                                  |
| triggerPrice     | double | Yes      | Order trigger price, returns 0 if order is not a trigger order                         |
| averageFillPrice | double | Yes      | Average filled price. Returns the average filled price for partially transacted orders |
| message          | string | Yes      | Trade messages                                                                         |
| stealth          | double | Yes      | Stealth value of order                                                                 |
| deviation        | double | Yes      | Deviation value of order                                                               |
| orderState       | string | Yes      | `STATUS_ACTIVE`, `STATUS_INACTIVE`                                                     |

## Query Trades Fills

> Response

```json
{
  "base": "string",
  "clOrderID": "string",
  "feeAmount": 0,
  "feeCurrency": "string",
  "filledPrice": 0,
  "filledSize": 0,
  "orderId": "string",
  "orderType": 0,
  "price": 0,
  "quote": "string",
  "realizedPnl": 0,
  "serialId": 0,
  "side": "string",
  "size": 0,
  "symbol": "string",
  "timestamp": 0,
  "total": 0,
  "tradeId": "string",
  "triggerPrice": 0,
  "triggerType": 0,
  "username": "string",
  "wallet": "string"
}
```

`GET /api/v2.1/user/trade_history`

Retrieves a user's trade history

### Request Parameters

| Name           | Type    | Required | Description                                                                       |
| ---            | ---     | ---      | ---                                                                               |
| symbol         | string  | Yes      | Market symbol                                                                     |
| startTime      | long    | No       | Starting time (eg. 1624987283000)                                                 |
| endTime        | long    | No       | Ending time (eg. 1624987283000)                                                   |
| beforeSerialId | string  | No       | Condition to retrieve records before the specified serial Id. Used for pagination |
| afterSerialId  | string  | No       | Condition to retrieve records after the specified serial Id. Used for pagination  |
| count          | integer | No       | Number of records to return                                                       |
| includeOld     | boolean | Yes      | Retrieve trade  history records past 7 days                                       |
| clOrderID      | string  | No       | Query trade history by custom order ID                                            |
| orderID        | string  | No       | Query trade history by order ID                                                   |


### Response Content

| Name        | Type   | Required | Description                             |
| ---         | ---    | ---      | ---                                     |
| symbol      | string | Yes      | Market symbol                           |
| side        | string | Yes      | Trade side. Values are: [`BUY`, `SELL`] |
| price       | double | Yes      | Transacted price                        |
| size        | double | Yes      | Transacted size                         |
| serialId    | long   | Yes      | Serial Id, running sequence number      |
| tradeId     | string | Yes      | Trade identifier                        |
| timestamp   | double | Yes      | Transacted timestamp                    |
| base        | long   | Yes      | Base currency                           |
| quote       | long   | Yes      | Quote currency                          |
| clOrderID   | long   | Yes      | Custom order ID                         |
| orderID     | long   | Yes      | Order ID                                |
| feeAmount   | long   | Yes      | Fee amount                              |
| feeCurrency | long   | Yes      | Fee currency                            |
| filledPrice | long   | Yes      | Filled price                            |
| filledSize  | long   | Yes      | Filled size                             |
| orderType   | long   | Yes      | Order Type                              |
| realizedPnL | long   | Yes      | Not used in Spot                        |
| total       | long   | Yes      | Not used in Spot                        |


## Query Position

> Response

```json
[
  {
    "marginType": 0,
    "entryPrice": 0,
    "markPrice": 71126.6,
    "symbol": "BTCPFC",
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
    "currentLeverage": 0
  }
]
```

`GET /api/v2.1/user/positions`

Queries user's current position. When no symbol is specified, positions for all markets will be returned.

### Request Parameters

| Name   | Type   | Required | Description   |
| ---    | ---    | ---      | ---           |
| symbol | string | No       | Market symbol |


### Response Content

| Name                   | Type    | Required | Description                                                                 |
| ---                    | ---     | ---      | ---                                                                         |
| symbol                 | string  | Yes      | Market symbol                                                               |
| side                   | string  | Yes      | Position side. Values are: [`Buy`, `SELL`]                                  |
| size                   | double  | Yes      | Position size                                                               |
| entryPrice             | double  | Yes      | Entry price                                                                 |
| markPrice              | double  | Yes      | Mark price                                                                  |
| marginType             | integer | Yes      | Margin Type. Values as follows<br/>91: CROSS wallet<br/>92: Isolated wallet |
| orderValue             | double  | Yes      | Notional value                                                              |
| settleWithAsset        | string  | Yes      | Settlement currency                                                         |
| totalMaintenanceMargin | double  | Yes      | Maintenance margin                                                          |
| unrealizedProfitLoss   | double  | Yes      | Unrealized profit and loss                                                  |
| liquidationPrice       | double  | Yes      | Liquidation Price                                                           |
| isolatedLeverage       | double  | Yes      | Isolated leverage value                                                     |
| adlScoreBucket         | integer | Yes      | ADL Score probability                                                       |
| liquidationInProgress  | boolean | Yes      | Indicator if liquidation is in progress                                     |
| currentLeverage        | double  | Yes      | Current leverage                                                            |
| timestamp              | long    | Yes      | Timestamp when position was queried                                         |


## Close Position

> Request

```json
{
  "price": 0,
  "symbol": "BTCPFC",
  "type": "MARKET"
}
```

> Response

```json
[
  {
    "status": 0,
    "symbol": "BTCPFC",
    "orderType": 76,
    "price": 8300,
    "side": "BUY",
    "size": 4,
    "orderID": "string",
    "timestamp": 1576812000872,
    "triggerPrice": 8300,
    "trigger": false,
    "deviation": 0,
    "stealth": 0,
    "message": "false",
    "avgFillPrice": 0,
    "fillSize": 0,
    "clOrderID": "market001",
    "remainingSize": 2,
    "orginialSize": 4
  }
]
```

`POST /api/v2.1/order/close_position`

Closes a user's position for the particular market as specified by symbol. If type is specified as LIMIT, then price is mandatory. When type is MARKET, it closes the position at market price.

### Request Parameters

| Name   | Type   | Required | Description                                                                                    |
| ---    | ---    | ---      | ---                                                                                            |
| symbol | string | Yes      | Market symbol                                                                                  |
| type   | string | Yes      | Close position type with values:<br/>LIMIT: Close at `price`<br/>MARKET: Close at market price |
| price  | double | No       | Ending time (eg. 1624987283000)                                                                |


### Response Content

| Name             | Type    | Required | Description                                                                                                                                                                                                                                                              |
| ---              | ---     | ---      | ---                                                                                                                                                                                                                                                                      |
| symbol           | string  | Yes      | Market symbol                                                                                                                                                                                                                                                            |
| clOrderID        | string  | Yes      | Customer tag sent in by trader                                                                                                                                                                                                                                           |
| fillSize         | string  | Yes      | Trade filled size                                                                                                                                                                                                                                                        |
| orderID          | string  | Yes      | Order ID                                                                                                                                                                                                                                                                 |
| orderType        | string  | Yes      | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order                                                                                                                                                                                                  |
| postOnly         | boolean | Yes      | Indicates if order is a post only order                                                                                                                                                                                                                                  |
| price            | double  | Yes      | Order price                                                                                                                                                                                                                                                              |
| side             | string  | Yes      | Order side<br/>BUY or SELL                                                                                                                                                                                                                                               |
| size             | double  | Yes      | Cancelled size                                                                                                                                                                                                                                                           |
| status           | integer | Yes      | Order status<br/>	2: Order Inserted<br/>3: Order Transacted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>7: Order Refunded<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found |
| stopPrice        | string  | Yes      | Stop price                                                                                                                                                                                                                                                               |
| time_in_force    | string  | Yes      | Order validity                                                                                                                                                                                                                                                           |
| timestamp        | string  | Yes      | Order timestamp                                                                                                                                                                                                                                                          |
| trigger          | string  | Yes      | Indicator if order is a trigger order                                                                                                                                                                                                                                    |
| triggerPrice     | string  | Yes      | Order trigger price, returns 0 if order is not a trigger order                                                                                                                                                                                                           |
| averageFillPrice | string  | Yes      | Average filled price. Returns the average filled price for partially transacted orders                                                                                                                                                                                   |
| message          | string  | Yes      | Trade messages                                                                                                                                                                                                                                                           |
| stealth          | string  | Yes      | Stealth value of order                                                                                                                                                                                                                                                   |
| deviation        | string  | Yes      | Deviation value of order                                                                                                                                                                                                                                                 |
| remainingSize    | double  | Yes      | Size left to be transacted                                                                                                                                                                                                                                               |
| originalSize     | double  | Yes      | Original order size                                                                                                                                                                                                                                                      |

## Set Risk Limits

> Request

```json
{
  "symbol": "BTCPFC",
  "leverage": 0
}
```

> Response

```json
{
  "symbol": "BTCPFC",
  "timestamp": 1577093486551,
  "status": 20,
  "type": 94,
  "message": "false"
}
```

`POST /api/v2.1/risk_limit`

Changes risk limit for the specified market

### Request Parameters

| Name      | Type    | Required | Description      |
| ---       | ---     | ---      | ---              |
| symbol    | string  | Yes      | Market symbol    |
| riskLimit | integer | Yes      | Risk limit value |


### Response Content

| Name      | Type    | Required | Description                                                                                                                                     |
| ---       | ---     | ---      | ---                                                                                                                                             |
| symbol    | string  | Yes      | Market symbol                                                                                                                                   |
| status    | integer | Yes      | Status of the request. Values are: <br/>8: Insufficient Balance<br/>12: Error in updating risk limit<br/>20: Success<br/>41: Invalid risk limit |
| type      | double  | Yes      | Value will be 94 indicating that type is `Risk Limit`                                                                                           |
| timestamp | double  | Yes      | Timestamp where risk limit was set                                                                                                              |
| message   | long    | Yes      | Message                                                                                                                                         |

## Set Leverage

> Request

```json
{
  "symbol": "BTCPFC",
  "leverage": 0
}
```

> Response

```json
{
  "base": "string",
  "clOrderID": "string",
  "feeAmount": 0,
  "feeCurrency": "string",
  "filledPrice": 0,
  "filledSize": 0,
  "orderId": "string",
  "orderType": 0,
  "price": 0,
  "quote": "string",
  "realizedPnl": 0,
  "serialId": 0,
  "side": "string",
  "size": 0,
  "symbol": "string",
  "timestamp": 0,
  "total": 0,
  "tradeId": "string",
  "triggerPrice": 0,
  "triggerType": 0,
  "username": "string",
  "wallet": "string"
}
```

`POST /api/v2.1/leverage`

Change leverage values for the specified market

### Request Parameters

| Name     | Type    | Required | Description    |
| ---      | ---     | ---      | ---            |
| symbol   | string  | Yes      | Market symbol  |
| leverage | integer | Yes      | Leverage value |


### Response Content

| Name      | Type    | Required | Description                                                                                                                             |
| ---       | ---     | ---      | ---                                                                                                                                     |
| symbol    | string  | Yes      | Market symbol                                                                                                                           |
| status    | integer | Yes      | Status of the request. Values are: <br/>8: Insufficient Balance<br/>13: Invalid leverage<br/>20: Success<br/>64: Undergoing liquidation |
| type      | double  | Yes      | Value will be 93 indicating that type is `Leverage`                                                                                     |
| timestamp | double  | Yes      | Timestamp where leverage was set                                                                                                        |
| message   | long    | Yes      | Message                                                                                                                                 |

## Change contract settlement currency

> Request

```json
{
  "symbol": "BTCPFC",
  "currency": "BTC"
}
```

> Response

```json
{
  "status": 0,
  "errorCode": 0,
  "message": "string"
}
```

`POST /api/v2.1/settle_in`

Changes the settlement currency for the position in the current market

### Request Parameters

| Name     | Type   | Required | Description                |
| ---      | ---    | ---      | ---                        |
| symbol   | string | Yes      | Market symbol              |
| currency | string | Yes      | Settlement currency to set |

### Response Content

| Name      | Type    | Required | Description                                              |
| ---       | ---     | ---      | ---                                                      |
| status    | integer | Yes      | Request status<br/>1: Success<br/>-2: Invalid parameters |
| errorCode | integer | Yes      | Error code                                               |
| message   | string  | Yes      | Response message                                         |

## Query Account Fees

> Response

```json
{
  "makerFee": 0,
  "symbol": "BTCPFC",
  "takerFee": 0
}
```

`GET /api/v2.1/user/fees`

Retrieve user's trading fees
### Response Content

| Name     | Type   | Required | Description   |
| ---      | ---    | ---      | ---           |
| symbol   | string | Yes      | Market symbol |
| makerFee | double | Yes      | Maker fees    |
| takerFee | double | Yes      | Taker fees    |

# Wallet Endpoints

## Query Wallet Balance

> Response

```json
[
  {
    "trackingID": 0,
    "queryType": 0,
    "activeWalletName": "string",
    "wallet": "CROSS@",
    "username": "string",
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

`GET /api/v2.1/user/wallet`

Query user's wallet balance. Requires `Read` permissions on the API key.

### Request Parameters

| Name   | Type   | Required | Description                                                                                                                                                                       |
| ---    | ---    | ---      | ---                                                                                                                                                                               |
| wallet | string | Yes      | Wallet name<br/>`CROSS@`: Cross wallet<br/>`ISOLATED@market`: Market refers to the current symbol with `-USD` appended. Eg. BTCPFC isolated wallet would be `ISOLATED@BTCPFC-USD` |

### Response Content

#### Wallet

| Name                 | Type         | Required | Description                          |
| ---                  | ---          | ---      | ---                                  |
| wallet               | string       | Yes      | Wallet name                          |
| activeWalletName     | string       | Yes      | Active wallet name                   |
| queryType            | integer      | Yes      | Query type                           |
| trackingID           | long         | Yes      | Internal tracking ID, not being used |
| walletTotalValue     | double       | Yes      | Wallet total value                   |
| totalValue           | double       | Yes      | Total value                          |
| marginBalance        | double       | Yes      | Margin balance                       |
| availableBalance     | double       | Yes      | Available Balance                    |
| unrealisedProfitLoss | double       | Yes      | Unrealised Profit / Loss             |
| maintenanceMargin    | double       | Yes      | Maintenance margin                   |
| leverage             | double       | Yes      | Leverage                             |
| openMargin           | double       | Yes      | Open margin                          |
| assets               | Asset object | Yes      | Assets available                     |
| assetsInUse          | Asset object | Yes      | Assets in use                        |

#### Assets / Asset in Use

| Name       | Type   | Required | Description |
| ---        | ---    | ---      | ---         |
| balance    | double | Yes      | Balance     |
| assetPrice | double | Yes      | Asset price |
| currency   | string | Yes      | Currency    |


## Query Wallet History

> Response

```json
[
  {
    "amount": 21.35823825,
    "currency": "USD",
    "description": "string",
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

`GET /api/v2.1/user/wallet_history`

Get user's wallet history records on the futures wallet

### Request Parameters

| Name      | Type    | Required | Description                                                                                                                                 |
| ---       | ---     | ---      | ---                                                                                                                                         |
| wallet    | string  | No       | Wallet, if not specified will return all wallets. Valid values are: <br/>`CROSS@`: Cross wallet<br/>`ISOLATED@BTCPFC-USD`: Isolated wallets |
| startTime | long    | No       | Starting time (eg. 1624987283000)                                                                                                           |
| endTime   | long    | No       | Ending time (eg. 1624987283000)                                                                                                             |
| count     | integer | No       | Number of records to return                                                                                                                 |


### Response Content

| Name        | Type    | Required | Description                                                                                                       |
| ---         | ---     | ---      | ---                                                                                                               |
| currency    | string  | Yes      | Currency                                                                                                          |
| amount      | double  | Yes      | Amount in the record                                                                                              |
| fees        | double  | Yes      | Fees charged if any                                                                                               |
| orderId     | string  | Yes      | Internal wallet order ID                                                                                          |
| wallet      | string  | Yes      | Wallet type. For futures will return `CROSS@` or `ISOLATED@`                                                      |
| description | string  | Yes      | Description of the transaction                                                                                    |
| status      | integer | Yes      | 1: PENDING<br/>2: PROCESSING<br/>10: COMPLETED<br/>16: CANCELLED                                                  |
| type        | integer | Yes      | 105: Wallet Transfer<br/>106: Wallet Liquidation<br/>108: Realized PnL<br/>110: Funding<br/>121: Asset Conversion |

## Query wallet Margin

> Response

```json
[
  {
    "trackingID": 0,
    "queryType": 0,
    "activeWalletName": "string",
    "wallet": "CROSS@",
    "username": "string",
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

`GET /api/v2.1/user/margin`

Gets margin information for the specified wallet so that users can know which wallet they are currently using in the market.

### Request Parameters

| Name      | Type    | Required | Description                                           |
| ---       | ---     | ---      | ---                                                   |
| symbol    | string  | Yes      | Currency, if not specified will return all currencies |
| startTime | long    | No       | Starting time (eg. 1624987283000)                     |
| endTime   | long    | No       | Ending time (eg. 1624987283000)                       |
| count     | integer | No       | Number of records to return                           |


### Response Content

#### Wallet

| Name                 | Type         | Required | Description                          |
| ---                  | ---          | ---      | ---                                  |
| wallet               | string       | Yes      | Wallet name                          |
| activeWalletName     | string       | Yes      | Active wallet name                   |
| queryType            | integer      | Yes      | Query type                           |
| trackingID           | long         | Yes      | Internal tracking ID, not being used |
| walletTotalValue     | double       | Yes      | Wallet total value                   |
| totalValue           | double       | Yes      | Total value                          |
| marginBalance        | double       | Yes      | Margin balance                       |
| availableBalance     | double       | Yes      | Available Balance                    |
| unrealisedProfitLoss | double       | Yes      | Unrealised Profit / Loss             |
| maintenanceMargin    | double       | Yes      | Maintenance margin                   |
| leverage             | double       | Yes      | Leverage                             |
| openMargin           | double       | Yes      | Open margin                          |
| assets               | Asset object | Yes      | Assets available                     |
| assetsInUse          | Asset object | Yes      | Assets in use                        |

#### Assets / Asset in Use

| Name       | Type   | Required | Description |
| ---        | ---    | ---      | ---         |
| balance    | double | Yes      | Balance     |
| assetPrice | double | Yes      | Asset price |
| currency   | string | Yes      | Currency    |

## Transfer funds between Futures wallet

> Request

```json
{
  "walletSrc": "string",
  "walletSrcType": "SPOT",
  "walletDest": "string",
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
    "activeWalletName": "string",
    "wallet": "CROSS@",
    "username": "string",
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

`GET /api/v2.1/wallet/transfer`

Transfers funds between user's wallet. User can specify the source and target wallet to transfer funds

### Request Parameters

#### Wallet Request

| Name           | Type          | Required | Description                                                                                                                                                                  |
| ---            | ---           | ---      | ---                                                                                                                                                                          |
| walletSrc      | string        | Yes      | Source wallet                                                                                                                                                                |
| walletSrcType  | string        | Yes      | Source type, valid values are:<br/>`SPOT@`: Spot Wallet<br/>`CROSS@`: Cross Wallet<br/>`ISOLATED@market`: Isolated wallet for the market where market the market symbol      |
| walletDest     | string        | Yes      | Destination wallet                                                                                                                                                           |
| walletDestType | string        | Yes      | Destination type, valid values are:<br/>`SPOT@`: Spot Wallet<br/>`CROSS@`: Cross Wallet<br/>`ISOLATED@market`: Isolated wallet for the market where market the market symbol |
| apiWallets     | Wallet Detail | Yes      | Transfer details                                                                                                                                                             |

#### Wallet Detail Request

| Name       | Type    | Required | Description                                          |
| ---        | ---     | ---      | ---                                                  |
| currency   | string  | Yes      | Wallet Currency                                      |
| allBalance | boolean | Yes      | Indicator if all wallet balance is to be transferred |



### Response Content

#### Wallet

| Name                 | Type         | Required | Description                          |
| ---                  | ---          | ---      | ---                                  |
| wallet               | string       | Yes      | Wallet name                          |
| activeWalletName     | string       | Yes      | Active wallet name                   |
| queryType            | integer      | Yes      | Query type                           |
| trackingID           | long         | Yes      | Internal tracking ID, not being used |
| walletTotalValue     | double       | Yes      | Wallet total value                   |
| totalValue           | double       | Yes      | Total value                          |
| marginBalance        | double       | Yes      | Margin balance                       |
| availableBalance     | double       | Yes      | Available Balance                    |
| unrealisedProfitLoss | double       | Yes      | Unrealised Profit / Loss             |
| maintenanceMargin    | double       | Yes      | Maintenance margin                   |
| leverage             | double       | Yes      | Leverage                             |
| openMargin           | double       | Yes      | Open margin                          |
| assets               | Asset object | Yes      | Assets available                     |
| assetsInUse          | Asset object | Yes      | Assets in use                        |

#### Assets / Asset in Use

| Name       | Type   | Required | Description |
| ---        | ---    | ---      | ---         |
| balance    | double | Yes      | Balance     |
| assetPrice | double | Yes      | Asset price |
| currency   | string | Yes      | Currency    |


# Websocket Streams

## Subscription

> Request

```json
{
  "op": "subscribe",
  "args": [
    "orderBookApi:BTCPFC_0"
  ]
}
```

> Response

```json
{
  "event": "subscribe",
  "channel": [
    "orderBookApi:BTCPFC_0"
  ]
}
```

To subscribe to a websocket feed

### Request Parameters

| Name | Type   | Required | Description                                                                                                            |
| ---  | ---    | ---      | ---                                                                                                                    |
| op   | string | Yes      | Operation. `subscribe` will subscribe to the topics provided in `args`. `unsubscribe` will unsubscribe from the topics |
| args | array  | Yes      | Topics to subscribe to.                                                                                                |

### Response Content

| Name    | Type   | Required | Description                                   |
| ---     | ---    | ---      | ---                                           |
| event   | string | Yes      | Respond with the event type                   |
| channel | array  | Yes      | Topics which have been sucessfully subscribed |


## Orderbook Snapshot (By grouping)

> Request

```json
{
  "op": "subscribe",
  "args": [
    "orderBookApi:BTCPFC_0"
  ]
}
```

> Response

```json
{
  "topic": "orderBookApi",
  "data": {
    "buyQuote":
    [
      {
        "price": 0,
        "size": 0
      }
    ],
    "sellQuote":
    [
      {
        "price": 0,
        "size": 0
      }
    ],
    "symbol":"BTCPFC",
    "timestamp":1565135165600
  }
}
```

Subscribe to the Orderbook in different groupings. The format to subscribe to will be `symbol_grouping`.

* `symbol` indicates the market symbol
* `grouping` indicates the grouping granularity. Valid values are 0-9.

### Response Content

#### Orderbook Object

| Name  | Type        | Required | Description                |
| ---   | ---         | ---      | ---                        |
| topic | string      | Yes      | Websocket topic            |
| data  | Data Object | Yes      | Refer to data object below |

#### Data Object

| Name      | Type         | Required | Description         |
| ---       | ---          | ---      | ---                 |
| buyQuote  | Quote Object | Yes      | Bid quotes          |
| sellQuote | Quote Object | Yes      | Asks quotes         |
| symbol    | string       | Yes      | Market symbol       |
| timestamp | long         | Yes      | Orderbook timestamp |

## Orderbook Snapshot (By depth)

> Request

```json
{
  "op": "subscribe",
  "args": [
    "orderBookL2Api:BTCPFC_0"
  ]
}
```

> Response

```json
{
  "topic": "orderBookL2Api",
  "data": {
    "buyQuote":
    [
      {
        "price": 0,
        "size": 0
      }
    ],
    "sellQuote":
    [
      {
        "price": 0,
        "size": 0
      }
    ],
    "symbol":"BTCPFC",
    "depth": 0,
    "timestamp":1565135165600
  }
}
```

Subscribe to the Level 2 Orderbook. The format to subscribe to will be `symbol_depth`.

* `symbol` indicates the market symbol
* `depth` indicates the levels of orderbook to retrieve. Value of 0 will retrieve the entire orderbook.

### Response Content

#### Orderbook Object

| Name  | Type        | Required | Description                |
| ---   | ---         | ---      | ---                        |
| topic | string      | Yes      | Websocket topic            |
| data  | Data Object | Yes      | Refer to data object below |

#### Data Object

| Name      | Type         | Required | Description         |
| ---       | ---          | ---      | ---                 |
| buyQuote  | Quote Object | Yes      | Bid quotes          |
| sellQuote | Quote Object | Yes      | Asks quotes         |
| symbol    | string       | Yes      | Market symbol       |
| depth     | int          | Yes      | Orderbook depth     |
| timestamp | long         | Yes      | Orderbook timestamp |

## Orderbook Incremental Updates

> Request

```json
{
  "op": "subscribe",
  "args": [
    "update:BTCPFC"
  ]
}
```

```json
{
  "op": "unsubscribe",
  "args": [
    "update:BTCPFC"
  ]
}
```

> Response

```json
{
  "topic": "update:BTCPFC",
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
    "symbol": "BTCPFC"
  }
}
```

```json
{
  "topic": "update:BTCPFC",
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
    "symbol": "BTCPFC"
  }
}
```

Subscribe to Orderbook incremental updates through the endpoint `wss://ws.btse.com/ws/oss/futures`. The topic to subscribe to will be `update` specifying the symbol (eg. `update:BTCPFC`). The first response received will be a snapshot of the current orderbook (this is indicated in the `type` field) and 50 levels will be returned. Incremental updates will be sent in subsequent packets with type `delta`.

Bids and asks will be sent in `price` and `size` tuples. The size sent will be the new updated size for the price. If a value of `0` is sent, the price should be removed from the local copy of the orderbook.

To ensure that the updates are received in sequence, `seqNum` indicates the current sequence and `prevSeqNum` refers to the packet before. `seqNum` will always be one after the `prevSeqNum`. If the sequence is out of order, you will need to unsubscribe and re-subscribe to the topic again.

Also if [crossed orderbook](https://en.wikipedia.org/wiki/Order_book#Crossed_book) ever occurs when the best bid higher or equal to the best ask, please unsubscribe and re-subscribe to the topic again.

### Response Content

#### Orderbook Object

| Name  | Type        | Required | Description                |
| ---   | ---         | ---      | ---                        |
| topic | string      | Yes      | Websocket topic            |
| data  | Data Object | Yes      | Refer to data object below |

#### Data Object

| Name       | Type         | Required | Description                                                                                                 |
| ---        | ---          | ---      | ---                                                                                                         |
| bids       | Quote Object | Yes      | Bid quotes                                                                                                  |
| asks       | Quote Object | Yes      | Asks quotes                                                                                                 |
| seqNum     | int          | Yes      | Current sequence number                                                                                     |
| prevSeqNum | int          | Yes      | Previous sequence number                                                                                    |
| type       | string       | Yes      | `snapshot` - Snapshot of the orderbook with a maximum of 50 levels<br/> `delta` -  Updates of the orderbook |
| timestamp  | long         | Yes      | Timestamp of the orderbook                                                                                  |
| symbol     | string       | Yes      | Orderbook symbol                                                                                            |


## Public Trade Fills

> Request

```json
{
  "op": "subscribe",
  "args": [
    "tradeHistoryApi:BTCPFC"
  ]
}
```

> Response

```json
{
  "topic": "tradeHistoryApi:BTCPFC",
  "data": [
  {
    "symbol": "BTCPFC",
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
| topic | string      | Yes      | Websocket topic            |
| data  | Data Object | Yes      | Refer to data object below |

#### Data Object

| Name      | Type   | Required | Description             |
| ---       | ---    | ---      | ---                     |
| symbol    | string | Yes      | Market symbol           |
| side      | string | Yes      | Trade Side, BUY or SELL |
| size      | double | Yes      | Transacted size         |
| price     | double | Yes      | Transacted price        |
| tradeId   | long   | Yes      | Trade sequence Id       |
| timestamp | long   | Yes      | Trade timestamp         |

## Authentication

> Request

```json
{
  "op":"authKeyExpires",
  "args":["APIKey", "nonce", "signature"]}
}
```

Authenticate the websocket session to subscribe to authenticated websocket topics. Assume we have values as follows:

* `btse-nonce`: 1624985375123
* `btse-api`: 4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x
* `secret`: 848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx

Our subscription request will be:

```
{
  "op":"authKeyExpires",
  "args":["4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x", "1624985375123", "c410d38c681579adb335885800cff24c66171b7cc8376cfe43da1408c581748156b89bcc5a115bb496413bda481139fb"]}
}
```

### Request Parameters

Below details the arguments needed to be sent in.

| Index | Type   | Required | Description                          |
| ---   | ---    | ---      | ---                                  |
| 0     | string | Yes      | First argument is the API key        |
| 1     | long   | Yes      | Nonce which is the current timestamp |
| 2     | string | Yes      | Generated signature                  |

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
    "notificationApiV2"
  ]
}
```

> Response

```json
{
  "topic": "notificationApiV1",
  "data": [
    {
      "symbol": "Market Symbol (eg. BTCPFC)",
      "orderID": "BTSE internal order ID",
      "side": "BUY",
      "type": "76",
      "price": "Order price or transacted price",
      "size": "Order size or transacted size",
      "originalSize": "Order size",
      "avgFillPrice": 35000,
      "fillSize": 0.001,
      "status": "<Refer to Status description on the left>",
      "clOrderID": "<Client order ID>",
      "maker": "<Maker flag, if true indicates that trade is a maker trade>",
      "stealth": 1,
      "timestamp": 1624985375123,
      "pegPriceDeviation": "Indicate the deviation percentage. Valid for only algo orders.",
      "remainingSize": "<Remaining size on the order>",
      "time_in_force": "<Time where this order is valid>",
      "txType": "STOP | TAKE_PROFIT",
      "triggerPrice": "Trade Trigger Price"
    }
  ]

}

```

Receive trade notifications by subscribing to the topic `notificationApiV2`. The websocket feed will push trade level notifications to the subscriber. If topic is subscribed without being authenticated, no messages will be sent.

### Response Content

| Name              | Type    | Required | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---               | ---     | ---      | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| symbol            | string  | Yes      | Market symbol                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| orderID           | string  | Yes      | Internal order ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| side              | string  | Yes      | Trade side. BUY or SELL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| type              | int     | Yes      | Order type. Valid values are:<br/>76: Limit Order<br/>77: Market Order<br/>80: Algo orders                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| price             | double  | Yes      | Order price or transcated price                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| size              | double  | Yes      | Order size or transacted size                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| originalSize      | double  | Yes      | Original order size                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| avgFilledPrice    | double  | Yes      | Average filled price                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| fillSize          | double  | Yes      | Filled size of order                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| status            | integer | Yes      | Status with values as follows:<br/>1: MARKET_UNAVAILABLE, Market is currently unavailable<br/>2: ORDER_INSERTED, Order is inserted successfully<br/>4: ORDER_FULLY_TRANSACTED, Order is fully transacted<br/>5: ORDER_PARTIALLY_TRANSACTED, Order is partially transacted<br/>6: ORDER_CANCELLED, Order is cancelled successfully<br/>8: INSUFFICIENT_BALANCE, Insufficient balance in account<br/>9: TRIGGER_INSERTED, Trigger Order is inserted successfully<br/>10: TRIGGER_ACTIVATED, Trigger Order is activated successfully<br/>12: ERROR_UPDATE_RISK_LIMIT, Error in updating risk limit<br/>28: TRANSFER_UNSUCCESSFUL, Transfer funds between spot and futures is unsuccessful<br/>27: TRANSFER_SUCCESSFUL, Transfer funds between futures and spot is successful<br/>41: ERROR_INVALID_RISK_LIMIT, Invalid risk limit was specified<br/>64: STATUS_LIQUIDATION, Account is undergoing liquidation<br/>101: FUTURES_ORDER_PRICE_OUTSIDE_LIQUIDATION_PRICE, Futures order is outside of liquidation price<br/>1003: ORDER_LIQUIDATION, Order is undergoing liquidation<br/>1004: ORDER_ADL, Order is undergoing ADL |
| clOrderID         | string  | Yes      | Custom order ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| maker             | boolean | Yes      | Indicator to indicate if trade is a maker trade                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| remainingSize     | double  | Yes      | Remaining size on the order                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| time_in_force     | string  | Yes      | Validity of the order                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| timestamp         | long    | Yes      | Order timestamp or transacted timestamp                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| txType            | string  | Yes      | Used by trigger or OCO orders. STOP indicates its a Stop order, TAKEPROFIT indicates its a take profit order, and LIMIT is when its not any of the above                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| stealth           | double  | Yes      | Percentage of orders to show on orderbook. Only for Algo orders                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| pegPriceDeviation | double  | Yes      | Deviation percentage. Only for Algo orders                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

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
    "orderId": "order id", //string
    "serialId": "serial ID after insertion into DB", //integer / long
    "clOrderId": "Client Order ID", //string
    "type": "order type", //string
    "symbol": "ex: BTC-USD", //string
    "side": "BUY|SELL" //string
    "price": "filled price", //double (need to make sure no scientific notation)
    "size": "filled size", //double (no scientific notation)
    "feeAmount": "Fees charged to user, value to be String on API", //double (no scientific notation)
    "feeCurrency": "Fee currency, eg. Buy would be BTC, Sell would be USD" //string
    "base": "Base currency, eg. BTC",  //string
    "quote": "Quote currency eg. USD", //string
    "maker": "maker or taker",  //boolean (if maker, return true, else return false)
    "timestamp": "Time trade was matched in the engine" //long, field taken from DB,
    "tradeId": "Trade Unique ID"
  }]
}


```

When a trade has been transacted, this topic will send the trade information back to the subscriber.

### Response Content

| Name        | Type    | Required | Description                                                                                |
| ---         | ---     | ---      | ---                                                                                        |
| symbol      | string  | Yes      | Market symbol                                                                              |
| orderID     | string  | Yes      | Internal order ID                                                                          |
| clOrderID   | string  | Yes      | Custom order ID                                                                            |
| serialId    | string  | Yes      | Trade sequence ID                                                                          |
| tradeId     | string  | Yes      | Trade unique identifier                                                                    |
| type        | int     | Yes      | Order type. Valid values are:<br/>76: Limit Order<br/>77: Market Order<br/>80: Algo orders |
| side        | string  | Yes      | Trade side. BUY or SELL                                                                    |
| price       | double  | Yes      | Transcated price                                                                           |
| size        | double  | Yes      | Transacted size                                                                            |
| feeAmount   | double  | Yes      | Fee amount charged                                                                         |
| feeCurrency | string  | Yes      | Fee currency                                                                               |
| base        | string  | Yes      | Base currency                                                                              |
| quote       | string  | Yes      | Quote currency                                                                             |
| maker       | boolean | Yes      | Indicator to indicate if trade is a maker trade                                            |
| timestamp   | long    | Yes      | Order timestamp or transacted timestamp                                                    |

</section>
