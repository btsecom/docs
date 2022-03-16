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

## Version 1.0.2 (16th March 2022)

* Max decimal supported for [`withdraw funds`](#withdraw-funds) is 8, will return `CRYPTO_WITHDRAW_INVALID_AMOUNT (error code: 3506)` if exceeds

## Version 1.0.1 (25th January 2022)

* Addition of [`exchangeRate`](#query-exchange-rate-between-assets) api to get current exchange rate between assets

## Version 1.0.0 (13th January 2022)

* Migrate wallet related endpoints to this section

# Overview

## Generating API Key

You will need to create an API key on the BTSE platform before you can use authenticated APIs. To create API keys, you can follow the steps below:

* Login with your username / email and password into the BTSE website
* Click on “Account” on the top right hand corner
* Select the API tab
* Click on `New API` button to create an API key and passphrase. (Note: the passphrase will only appear once)
* Use your API key and passphrase to construct a signature.

## Endpoints

* Production
  * HTTP
     * `https://api.btse.com/spot`
     * `https://aws-api.btse.com/spot` (Optimised for connection via AWS)
  * Websocket
     * `wss://ws.btse.com/ws/spot`
     * `wss://aws-ws.btse.com/ws/spot` (Optimised for connection via AWS)
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

## Rate Limits

* The following rate limits are enforced:

Rate limits for BTSE is as follows:

**Wallet operation**

* Per User: `5 requests/second`

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
* 3505: Invalid protocol
* 3506: Invalid withdraw amount
* 3507: Invalid withdraw address
* 3508: Withdraw failed


# Public Endpoints

## Query available crypto network list for currency

> Response

```json
[
  "Bitcoin",
  "Liquid"
]
```

`GET /api/v3.2/availableCurrencyNetworks`

Get available crypto network list for currency.

### Request Parameters

| Name     | Type   | Required | Description |
| ---      | ---    | ---      | ---         |
| currency | string | Yes      | Ex: BTC     |

### Response Content

| Name     | Type   | Required | Description     |
| ---      | ---    | ---      | ---             |
| $network | string | Yes      | Name of network |

## Query exchange rate between assets

> Response

```json
{
  "code": 1,
  "msg": "Success",
  "time": 1643085970137,
  "data": 36051.55950285,
  "success": true
}
```

`GET /api/v3.2/exchangeRate`

Get the exchange rate between assets.

### Request Parameters

| Name             | Type     | Required   | Description   |
| ---------------- | -------- | ---------- | ------------- |
| srcCurrency      | string   | Yes        | Ex: BTC       |
| targetCurrency   | string   | Yes        | Ex: USD       |

### Response Content

| Name             | Type      | Required   | Description                    |
| ---------------- | --------- | ---------- | ------------------------------ |
| code             | integer   | Yes        | Return code                    |
| msg              | string    | Yes        | Return message                 |
| time             | long      | Yes        | Unix timestamp                 |
| data             | float     | Yes        | Exchange rate between assets   |
| success          | boolean   | Yes        | True or False                  |

# Wallet Endpoints

## Query Wallet Balance

> Response

```json
[
  {
    "available": 520.52,
    "currency": "USD",
    "total": 5566.5566
  }
]
```

`GET /api/v3.2/user/wallet`

Query user's wallet balance. Requires `Read` permissions on the API key.
### Response Content

| Name      | Type   | Required | Description       |
| ---       | ---    | ---      | ---               |
| currency  | string | Yes      | Currency          |
| total     | double | Yes      | Total balance     |
| available | double | Yes      | Available balance |
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

`GET /api/v3.2/user/wallet_history`

Get user's wallet history records on the spot wallet

### Request Parameters

| Name      | Type    | Required | Description                                           |
| ---       | ---     | ---      | ---                                                   |
| currency  | string  | No       | Currency, if not specified will return all currencies |
| startTime | long    | No       | Starting time (eg. 1624987283000)                     |
| endTime   | long    | No       | Ending time (eg. 1624987283000)                       |
| count     | integer | No       | Number of records to return                           |


### Response Content

| Name        | Type    | Required | Description                                                                                                                                                                                                                                                            |
| ---         | ---     | ---      | ---                                                                                                                                                                                                                                                                    |
| currency    | string  | Yes      | Currency                                                                                                                                                                                                                                                               |
| amount      | double  | Yes      | Amount in the record                                                                                                                                                                                                                                                   |
| fees        | double  | Yes      | Fees charged if any                                                                                                                                                                                                                                                    |
| orderId     | string  | Yes      | Internal wallet order ID                                                                                                                                                                                                                                               |
| wallet      | string  | Yes      | Wallet type. For spot will return `@SPOT`                                                                                                                                                                                                                              |
| description | string  | Yes      | Description of the transaction                                                                                                                                                                                                                                         |
| status      | integer | Yes      | 1: PENDING<br/>2: PROCESSING<br/>10: COMPLETED<br/>16: CANCELLED                                                                                                                                                                                                       |
| type        | integer | Yes      | `Deposit`: Deposits into account<br/>`Withdraw`: Withdrawals from account<br/>`Transfer_In`: BTSE internal transfer where funds are transferred in<br/>`Transfer_Out`: BTSE internal transfer where funds are transferred out<br/>`ReferralEarning`: Referral Earnings |

## Create Wallet Address

> Request

```json
{
  "currency": "BTC"
}
```

> Response

```json
[
  {
    "address": "Blockchain address",
    "created": 1592627542
  }
]
```

`POST /api/v3.2/user/wallet/address`

Creates a wallet address. If the address created has not been used before, a 400 error will return with the existing unused address. To use this API, `Wallet` permission is required.

### Request Parameters

| Name     | Type   | Required | Description             |
| ---      | ---    | ---      | ---                     |
| currency | string | Yes      | Currency to get address |

### Response Content

| Name    | Type   | Required | Description        |
| ---     | ---    | ---      | ---                |
| address | string | Yes      | Blockchain address |
| created | long   | Yes      | Created timestamp  |

## Get Wallet Address

> Request

```json
{
  "currency": "BTC"
}
```

> Response

```json
[
  {
    "address": "Blockchain address",
    "created": 1592627542
  }
]
```

`GET /api/v3.2/user/wallet/address`

Gets a wallet address. To use this API, `Wallet` permission is required.

### Request Parameters

| Name     | Type   | Required | Description                |
| ---      | ---    | ---      | ---                        |
| currency | string | Yes      | Currency to create address |

### Response Content

| Name    | Type   | Required | Description        |
| ---     | ---    | ---      | ---                |
| address | string | Yes      | Blockchain address |
| created | long   | Yes      | Created timestamp  |

## Withdraw Funds

> Request

```json
{
  "currency": "BTC-Bitcoin",
  "address": "BTCAddress",
  "tag": "Tag",
  "amount": "0.001"
}
```

> Response

```json
{
  "withdraw_id": "<withdrawal ID>"
}
```

`POST /api/v3.2/user/wallet/withdraw`

Performs a wallet withdrawal. To use this API, `Withdraw` permission is required.

### Request Parameters

| Name     | Type   | Required | Description                                                                                                                                                                                                                                                                            |
| ---      | ---    | ---      | ---                                                                                                                                                                                                                                                                                    |
| currency | string | Yes      | Currency-Network pair <br> Currency list can be retrieved from [Available currency list for action](#query-available-currency-list-for-wallet-action) <br> Network list can be retrieved from [Available network list for currency](#query-available-crypto-network-list-for-currency) |
| address  | string | Yes      | Blockchain address                                                                                                                                                                                                                                                                     |
| tag      | string | Yes      | Tag, used only by some blockchain (eg. XRP)                                                                                                                                                                                                                                            |
| amount   | string | Yes      | Amount to withdraw (Max decimal supported is `8` for all currencies). Will return Invalid withdraw amount (code: 3506) if exceeds                                                                                                                                                      |

### Response Content

| Name        | Type   | Required | Description                                                                                                                                                                                                     |
| ---         | ---    | ---      | ---                                                                                                                                                                                                             |
| withdraw_id | string | Yes      | Internal withdrawal ID. References the `orderID` field in `wallet_history` API. As withdrawal will not be processed immediately. User can query the wallet history API to check on the status of the withdrawal |


## Query available currency list for wallet action

> Response

```json
[
  "USD",
  "JPY",
  "GBP",
  "HKD",
  "SGD"
]
```

`GET /api/v3.2/availableCurrencies`

Get available currency list for wallet action.

### Request Parameters

| Name   | Type | Required | Description                        |
| ---    | ---  | ---      | ---                                |
| action | enum | Yes      | CONVERT, WITHDRAW, SEND (transfer) |

### Response Content

| Name          | Type   | Required | Description      |
| ---           | ---    | ---      | ---              |
| $currencyName | string | Yes      | Name of currency |


## Convert funds

> Request

```json
{
  "amount": "1",
  "fromAsset": "BTC",
  "toAsset": "USD"
}
```

> Response

```json
{
    "amount": 1.0,
    "settlementAmount": 66680.43282,
    "amountCurrency": "BTC",
    "settlementCurrency": "USD",
    "rate": 66680.43282
}
```

`POST /api/v3.2/user/wallet/convert`

Performs a currency conversion from wallet. To use this API, `Wallet` permission is required. To get supported currency list please check [Available currency list for action](#query-available-currency-list-for-wallet-action)

### Request Parameters

| Name      | Type   | Required | Description                     |
| ---       | ---    | ---      | ---                             |
| amount    | string | Yes      | amount of currency to convert   |
| fromAsset | string | Yes      | source currency to be converted |
| toAsset   | string | Yes      | destination currency            |

### Response Content

| Name               | Type   | Required | Description                               |
| ---                | ---    | ---      | ---                                       |
| amount             | float  | Yes      | amount of source currency to be converted |
| settlementAmount   | float  | Yes      | amount of converted destination currency  |
| amountCurrency     | string | Yes      | source currency                           |
| settlementCurrency | string | Yes      | destination currency                      |
| rate               | float  | Yes      | exchange rate                             |

## Transfer funds

> Request

```json
{
  "amount": "1.0",
  "asset": "BTC",
  "toUser": "jamesbond",
  "toUserMail": "james.bond@nogle.com"
}
```

> Response

```json
{
  "amount": "1",
  "asset": "BTC",
  "toUser": "jamesbond",
  "toUserMail": "james.bond@nogle.com"
}
```

`POST /api/v3.2/user/wallet/transfer`

Performs a internal currency transfer to other user from wallet. To use this API, `Wallet` permission is required. To get supported currency list please check [Available currency list for action](#query-available-currency-list-for-wallet-action)

### Request Parameters

| Name       | Type   | Required | Description                    |
| ---        | ---    | ---      | ---                            |
| amount     | string | Yes      | amount of currency to transfer |
| asset      | string | Yes      | currency to be transferred     |
| toUser     | string | Yes      | receiver account               |
| toUserMail | string | Yes      | receiver email                 |

### Response Content

| Name       | Type   | Required | Description                    |
| ---        | ---    | ---      | ---                            |
| amount     | string | Yes      | amount of currency to transfer |
| asset      | string | Yes      | currency to be transferred     |
| toUser     | string | Yes      | receiver account               |
| toUserMail | string | Yes      | receiver email                 |
