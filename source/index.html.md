---
title: BTSE Spot API
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

## Version 3.2.3 (2nd June 2021)

* Introduction of new notification topic. Refer to `notificationsApiV2` for details.


## Version 3.2.2 (29th January 2021)

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

## Version 3.2.1 (28th September 2020)

* New Amend Order API. Allows users to edit price, size and trigger prices for pending orders

## Version 3.2 (23rd June 2020)

* Deprecated v1 API
* Removed fees field for public API /api/v3.1/trades (not needed)
* Added new wallet APIs to create address, get wallet addresses and withdrawals
* Enhanced /user/wallet_historyAPI to return wallet details
* Introduction of API permissions. All current API keys will have Read, Trading and Transfer permissions. Refer to the tags beside the titles to see which category they are classified under
* Fixed incorrect messages returned on some APIs

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
     * `https://api.btse.com/spot`
     * `https://aws-api.btse.com/spot`
  * Websocket
     * `wss://ws.btse.com/ws/spot`
     * `wss://aws-ws.btse.com/ws/spot`
* Testnet
  * HTTP
     * `https://testapi.btse.io/spot`
  * Websocket
     * `wss://testws.btse.io/ws/spot`

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
$ echo -n "/api/v3.2/user/wallet1624984297330" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 14b986706a4368221e0af14a6725377161805e7a57d568220478cb3590ce532d4fad4ac68e6c02a14afced6a0619bfd3
```

* Endpoint to get wallet is `https://api.btse.com/spot/api/v3.2/user/wallet`
* Assume we have the values as follows: 
  * btse-nonce: `1624984297330`
  * btse-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v3.2/user/wallet`
* Generated signature will be: 
  * btse-sign: `14b986706a4368221e0af14a6725377161805e7a57d568220478cb3590ce532d4fad4ac68e6c02a14afced6a0619bfd3`

### Example 2: Place an order

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v3.2/order1624985375123{\"postOnly\":false,\"price\":8500.0,\"reduceOnly\":false,\"side\":\"BUY\",\"size\":0.002,\"stopPrice\":0.0,\"symbol\":\"BTC-USD\",\"time_in_force\":\"GTC\",\"trailValue\":0.0,\"triggerPrice\":0.0,\"txType\":\"LIMIT\",\"type\":\"LIMIT\"}" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 134c4a41c5451b88fb2955ec2b35814e4a5d432b85723edc90d6c1161118eb3bb6ffa730f2ac415c00a9f072c770a85f
```

* Endpoint to place an order is `https://api.btse.com/spot/api/v3.2/order`
* Assume we have the values as follows: 
  * btse-nonce: `1624985375123`
  * btse-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v3.2/order`
  * Body: `{"postOnly":false,"price":8500.0,"reduceOnly":false,"side":"BUY","size":0.002,"stopPrice":0.0,"symbol":"BTC-USD","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
  * Encrypted Text: `/api/v3.2/order1624985375123{"postOnly":false,"price":8500.0,"reduceOnly":false,"side":"BUY","size":0.002,"stopPrice":0.0,"symbol":"BTC-USD","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
* Generated signature will be:
  * btse-sign: `134c4a41c5451b88fb2955ec2b35814e4a5d432b85723edc90d6c1161118eb3bb6ffa730f2ac415c00a9f072c770a85f`


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
* 101: FUTURES_ORDER_PRICE_OUTSIDE_LIQUIDATION_PRICE = Futures order is outside of liquidation price
* 1003: ORDER_LIQUIDATION = Order is undergoing liquidation
* 1004: ORDER_ADL = Order is undergoing ADL





# Public Endpoints

## Market Summary

> Response

```json
[
  {
    "symbol": "BTC-USD",
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

`GET /api/v3.2/market_summary`

Gets market summary information. If no symbol parameter is sent, then all markets will be retrieved. 

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | No | Market symbol | 

### Response Content
|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol |
| last | double | Yes | Last price | 
| lowestAsk | double | Yes | Lowest ask price in the orderbook | 
| highestBid | double | Yes | Highest bid price in the orderbook |
| percentageChange | double | Yes | Percentage change against the price within the last 24hours | 
| volume | double | Yes | Transacted volume | 
| high24Hr | double | Yes | Highest price over the last 24hours | 
| low24Hr | double | Yes | Lowest price over the last 24hours | 
| base | string | Yes | Base currency | 
| quote | string | Yes | Quote currency | 
| active | boolean | Yes | Indicator if market is active | 
| size | double | Yes | Transacted size | 
| minValidPrice | double | Yes | Minimum valid price | 
| minPriceIncrement | double | Yes | Price increment | 
| minOrderSize | double | Yes | Minimum tick size | 
| minSizeIncrement | double | Yes | Tick size | 
| maxOrderSize | double | Yes | Maximum order size |
| openInterest | double | No | Not valid for spot | 
| openInterestUSD | double | No | Not valid for spot | 
| contractStart | date | No | Not valid for spot | 
| contractEnd | date | No | Not valid for spot | 
| timeBasedContract | boolean | No | Not valid for spot | 
| openTime | date | Yes | Market opening time | 
| closeTime | date | Yes | Market closing time | 
| startMatching | date | Yes | Matching start time | 
| inactiveTime | date | Yes | Time where market is inactive | 
| fundingRate | double | No | Not valid for spot | 
| contractSize | double | No | Not valid for spot | 
| maxPosition | double | No | Not valid for spot | 
| minRiskLimit | double | No | Not valid for spot | 
| maxRiskLimit | double | No | Not valid for spot | 
| availableSettlement | array | No | Not valid for spot | 
| futures | boolean | Yes | Indicator if symbol is a futures contract | 

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

`GET /api/v3.2/ohlcv`

Gets candle stick charting data. Default of 300 data points will be returned at any one time. 

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| start | long | No | Starting time (eg. 1624987283000) | 
| end | long | No | Ending time (eg. 1624987283000) | 
| resolution | string | Yes | Supported resolutions are: <br/> 1: 1min<br/> 5: 5mins<br/> 15: 15mins<br/>30: 30mins<br/>60: 60mins<br/>360: 6hours<br/>1440: 1day| 


### Response Content

Returns a 2D array with the indexes described in the table below

|Index|Type|Required|Description|
|---|---|---|---|
| 0 | long | Yes | Unix time |
| 1 | double | Yes | Open price | 
| 2 | double | Yes | High Price | 
| 3 | double | Yes | Low price |
| 4 | double | Yes | Closing price |
| 5 | double | Yes | Volume |


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

`GET /api/v3.2/price`

Retrieve current prices on the platform. If no symbol specified, all symbols will be returned.

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | double | Yes | Market symbol |
| indexPrice | double | Yes | Index price |
| lastPrice | double | Yes | Last transacted price | 
| markPrice | double | Yes | Not valid for spot | 

## Orderbook (Level 1)

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

`GET /api/v3.2/orderbook`

Retrieves a Level 1 snapshot of the orderbook

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| group | integer | No | Orderbook grouping. Valid values are: <br/>0-9 where 0 indicates level 0 grouping (eg. for BTC, it will be 0.5)<br/>Level 1 grouping for BTC would be 1<br/> | 
| limit_bids | integer | No | Orderbook depth on the bid side | 
| limit_asks | integer | No | Orderbook depth on the ask side | 


### Response Content

#### Orderbook

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol |
| buyQuote | Quote | Yes | Array of Buy quotes |
| sellQuote | Quote | Yes | Array of Sell quotes | 
| timestamp | double | Yes | Timestamp of orderbook | 

#### Quote

|Name|Type|Required|Description|
|---|---|---|---|
| price | double | Yes | order price |
| size | double | Yes | order size |



## Orderbook (Level 2)

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

`GET /api/v3.2/orderbook/L2`

Retrieves a Level 2 snapshot of the orderbook

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| depth | integer | No | Orderbook depth | 

### Response Content

#### Orderbook

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol |
| buyQuote | Quote | Yes | Array of Buy quotes |
| sellQuote | Quote | Yes | Array of Sell quotes | 
| timestamp | double | Yes | Timestamp of orderbook | 

#### Quote

|Name|Type|Required|Description|
|---|---|---|---|
| price | double | Yes | order price |
| size | double | Yes | order size |


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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

## Query Server Time

> Response

```json
{
  "iso": "2021-06-29T18:14:30.886Z",
  "epoch": 1624990470
}
```

`GET /api/v3.2/time`

Gets server time

### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| iso | long | Yes | Time in YYYY-MM-DDTHH24:MI:SS.Z format |
| epoch | long | Yes | Returns epoch timestamp | 


# Trade Endpoints

## Create new order

> Request

```json
{
  "clOrderID": "string",
  "deviation": 0,
  "postOnly": false,
  "price": 7010,
  "side": "BUY",
  "size": 1,
  "stealth": 0,
  "stopPrice": 0,
  "symbol": "BTC-USD",
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
  "symbol": "BTC-USD",
  "timestamp": 1576812000872,
  "trigger": true,
  "triggerPrice": 8300
}
```

`POST /api/v3.2/order`

Creates a new order. Requires `Trading` permission

### Request Parameters

|Name|Type|Required|Description| 
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| price | double | Yes | Order price | 
| size | double | Yes | Order size | 
| time_in_force | string | No | Time validity of the order<br/>GTC: Good till Cancel<br/>IOC: Immediate or Cancel<br/>FOK: Fill or Kill<br/>FIVEMIN: Order valid for 5 mins<br/> HOUR: Order valid for an hour<br/>TWELVEHOUR: Order valid for 12 hours<br/>DAY: Order valid for a day<br/>WEEK: Order valid for a week<br/>MONTH: Order valid for a month | 
| type | string | Yes | Order type<br/>LIMIT: Limit Orders<br/>MARKET: Market Orders<br/>OCO: One cancel the other| 
| txType | string | Yes | Used for Stop orders or trigger orders<br/>STOP: Stop Order, `stopPrice` is mandatory<br/>TRIGGER: Trigger order, `triggerPrice` is mandatory<br/>LIMIT: Default, used when its not a Stop order nor Trigger order | 
| stopPrice | double | No | Mandatory when creating a Stop or OCO order. Indicates the stop price | 
| triggerPrice | double | Yes | Mandatory when creating a Trigger or OCO order. Indicates the trigger price | 
| trailValue | double | Yes | Trail value | 
| postOnly | boolean | Yes | Boolean to indicate if this is a post only order. For post only orders, traders are charged maker fees | 
| clOrderID | string | Yes | Custom order Id | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol |
| clOrderID | string | Yes | Customer tag sent in by trader |
| fillSize | string | Yes | Trade filled size |
| orderID | string | Yes | Order ID |
| orderType | string | Yes | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order |
| postOnly | boolean | Yes | Indicates if order is a post only order |
| price | double | Yes | Order price |
| side | string | Yes | Order side<br/>BUY or SELL |
| size | double | Yes | Order size |
| status | integer | Yes | Order status<br/>	2: Order Inserted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found |
| stopPrice | string | Yes | Stop price |
| time_in_force | string | Yes | Order validity |
| timestamp | string | Yes | Order timestamp |
| trigger | string | Yes | Indicator if order is a trigger order |
| triggerPrice | string | Yes | Order trigger price, returns 0 if order is not a trigger order |
| averageFillPrice | string | Yes | Average filled price. Returns the average filled price for partially transacted orders |
| message | string | Yes | Trade messages |
| stealth | string | Yes | Only valid for Algo orders |
| deviation | string | Yes | Only valid for Algo orders |

## Create new algo order

> Request

```json
{
  "clOrderID": "string",
  "deviation": 0,
  "postOnly": false,
  "price": 7010,
  "side": "BUY",
  "size": 1,
  "stealth": 0,
  "stopPrice": 0,
  "symbol": "BTC-USD",
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
  "symbol": "BTC-USD",
  "timestamp": 1576812000872,
  "trigger": true,
  "triggerPrice": 8300
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

|Name|Type|Required|Description| 
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| price | double | Yes | Minimum price for a sell order, this is the lowest price that a user is willing to sell at. Maximum price for a buy order, this is the maximum price a user is willing to buy at.  | 
| size | double | Yes | Order size | 
| time_in_force | string | No | Time validity of the order<br/>GTC: Good till Cancel<br/>IOC: Immediate or Cancel<br/>FOK: Fill or Kill<br/>FIVEMIN: Order valid for 5 mins<br/> HOUR: Order valid for an hour<br/>TWELVEHOUR: Order valid for 12 hours<br/>DAY: Order valid for a day<br/>WEEK: Order valid for a week<br/>MONTH: Order valid for a month | 
| type | string | Yes | Order type<br/>LIMIT: Limit Orders<br/>MARKET: Market Orders<br/>OCO: One cancel the other| 
| txType | string | Yes | Used for Stop orders or trigger orders<br/>STOP: Stop Order, `stopPrice` is mandatory<br/>TRIGGER: Trigger order, `triggerPrice` is mandatory<br/>LIMIT: Default, used when its not a Stop order nor Trigger order | 
| stopPrice | double | No | Mandatory when creating a Stop or OCO order. Indicates the stop price | 
| triggerPrice | double | Yes | Mandatory when creating a Trigger or OCO order. Indicates the trigger price | 
| trailValue | double | Yes | Trail value | 
| postOnly | boolean | Yes | Boolean to indicate if this is a post only order. For post only orders, traders are charged maker fees | 
| clOrderID | string | Yes | Custom order Id | 
| deviation | double | Yes | How many percent of the order is to be displayed on the orderbook.  | 
| stealth | double | Yes | How much should the order price deviate from index price. Value is in percentage and can range from `-10` to `10` | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol |
| clOrderID | string | Yes | Customer tag sent in by trader |
| fillSize | string | Yes | Trade filled size |
| orderID | string | Yes | Order ID |
| orderType | string | Yes | Order type <br/>76: Limit Order<br/>77: Market order<br/>80: Algo order |
| postOnly | boolean | Yes | Indicates if order is a post only order |
| price | double | Yes | Order price |
| side | string | Yes | Order side<br/>BUY or SELL |
| size | double | Yes | Order size |
| status | integer | Yes | Order status<br/>	2: Order Inserted<br/>4: Order Fully Transacted<br/>5: Order Partially Transacted<br/>6: Order Cancelled<br/>9: Trigger Inserted<br>10: Trigger Activated<br/>15: Order Rejected<br/>16: Order Not Found |
| stopPrice | string | Yes | Stop price |
| time_in_force | string | Yes | Order validity |
| timestamp | string | Yes | Order timestamp |
| trigger | string | Yes | Indicator if order is a trigger order |
| triggerPrice | string | Yes | Order trigger price, returns 0 if order is not a trigger order |
| averageFillPrice | string | Yes | Average filled price. Returns the average filled price for partially transacted orders |
| message | string | Yes | Trade messages |
| stealth | string | Yes | Stealth value of order |
| deviation | string | Yes | Deviation value of order |

## Amend Order

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |


## Cancel Order

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

## Dead man's switch (Cancel all after)

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

## Query Open Orders

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

## Query Account Fees

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

# Wallet Endpoints

## Query Wallet Balance

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

## Query Wallet History

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

## Create Wallet Address

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

## Get Wallet Address

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

## Withdraw Funds

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

`GET /api/v3.2/trades`

Get trade fills for the market specified by `symbol`

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | string | Yes | Market symbol | 
| startTime | long | No | Starting time (eg. 1624987283000) | 
| endTime | long | No | Ending time (eg. 1624987283000) | 
| beforeSerialId | string | Yes | Condition to retrieve records before the specified serial Id. Used for pagination| 
| afterSerialId | string | Yes | Condition to retrieve records after the specified serial Id. Used for pagination| 
| count | integer | Yes | Number of records to return | 
| includeOld | boolean | Yes | Retrieve trade  history records past 7 days | 


### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| symbol | long | Yes | Market symbol |
| side | string | Yes | Trade side. Values are: [`Buy`, `SELL`] | 
| price | double | Yes | Transacted price | 
| size | double | Yes | Transacted size |
| serialId | double | Yes | Serial Id, running sequence number |
| timestamp | double | Yes | Transacted timestamp |

# Websocket Streams

## Subscription 

## L1 Orderbook Snapshot

## L2 Orderbook Snapshot

## Public Trade Fills

## Authentication

## Notifications

## User Trade Fills

</section>
