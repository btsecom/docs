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

## Version 1.1.3 (10th July 2025)

* [**IMPORTANT**] BTSE will phase out support for two open API endpoints by **July 30, 2025**. The following endpoints will be deprecated:
  - [`Query available crypto network list for currency`](#query-available-crypto-network-list-for-currency-deprecated)
  - [`Query exchange rate between assets`](#query-exchange-rate-between-assets-deprecated)

  We encourage developers to transition away from these endpoints as they will no longer be supported after the end of July.</br>
  A new, improved endpoint to replace these can be accessed here:
  
  - [`Query crypto networks`](#query-crypto-networks)
  - [`Query asset exchange rate`](#query-asset-exchange-rate)


## Version 1.1.2 (10th April 2024)

* Update description of `status` and `type` in [`Query Wallet History`](#query-wallet-history)

## Version 1.1.1 (08th April 2024)

* Add API for querying [`Subaccount Transfer History`](#subaccount-transfer-history)

## Version 1.1.0 (16th November 2022)

* [IMPORTANT] BTSE will change futures market naming convention in **December 2022** to provide more clarity to retail users and here are the rules:
  - Change the suffix for perpetual markets from `PFC` to `PERP` (ex: BTCPFC -> BTC-PERP)
  - Change the suffix for time-based markets from `delivery month + year` to `settlement date (YYMMDD)` (ex: BTCZ22 -> BTC-221230)
  - Added a new optional query parameter `useNewSymbolNaming` in [`Query Wallet History`](#query-wallet-history) and [`Transfer Funds`](#transfer-funds) if user wants to use new market name

## Version 1.0.4 (25th, August 2022)

* Adjust param description of currency in APIs: [`Get Wallet Address`](#get-wallet-address), [`Create Wallet Address`](#create-wallet-address).

## Version 1.0.3 (13th, May 2022)

* Addition of a parameter `includeWithdrawFee` for [`withdraw funds`](#withdraw-funds) to set the fee will be inclusive/extra added.

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
  * HTTP (for [`Query crypto networks`](#query-crypto-networks) and [`Query asset exchange rate`](#query-asset-exchange-rate))
     * `https://api.btse.com/`
  * Websocket
     * `wss://ws.btse.com/ws/spot`
  * Websocket (for orderbook stream)
     * `wss://ws.btse.com/ws/oss/spot` (Used for Orderbook incremental update stream)
* Testnet
  * HTTP
     * `https://testapi.btse.io/spot`
  * HTTP (for [`Query crypto networks`](#query-crypto-networks) and [`Query asset exchange rate`](#query-asset-exchange-rate))
     * `https://testapi.btse.io/`
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

### Example 1: Get Wallet

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v3.2/user/wallet1624984297330" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 14b986706a4368221e0af14a6725377161805e7a57d568220478cb3590ce532d4fad4ac68e6c02a14afced6a0619bfd3
```

* Endpoint to get wallet is `https://api.btse.com/spot/api/v3.2/user/wallet`
* Assume we have the values as follows:
  * request-nonce: `1624984297330`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v3.2/user/wallet`
* Generated signature will be:
  * request-sign: `14b986706a4368221e0af14a6725377161805e7a57d568220478cb3590ce532d4fad4ac68e6c02a14afced6a0619bfd3`

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

# Public Endpoints

## Query available crypto network list for currency (Deprecated)

> Response

```json
[
  "Bitcoin",
  "Liquid"
]
```

`GET /api/v3.2/availableCurrencyNetworks`

Get available crypto network list for currency. This endpoint will be deprecated after **July 30, 2025**. Please replace this endpoint with [`Query crypto networks`](#query-crypto-networks).

### Request Parameters

| Name     | Type   | Required | Description |
| ---      | ---    | ---      | ---         |
| currency | String | Yes      | Ex: BTC     |

### Response Content

| Name     | Type   | Required | Description     |
| ---      | ---    | ---      | ---             |
| $network | String | Yes      | Name of network |

## Query exchange rate between assets (Deprecated)

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

Get the exchange rate between assets. This endpoint will be deprecated after **July 30, 2025**. Please replace this endpoint with [`Query asset exchange rate`](#query-asset-exchange-rate).

### Request Parameters

| Name             | Type     | Required   | Description   |
| ---------------- | -------- | ---------- | ------------- |
| srcCurrency      | String   | Yes        | Ex: BTC       |
| targetCurrency   | String   | Yes        | Ex: USD       |

### Response Content

| Name             | Type      | Required   | Description                    |
| ---------------- | --------- | ---------- | ------------------------------ |
| code             | Integer   | Yes        | Return code                    |
| msg              | String    | Yes        | Return message                 |
| time             | Long      | Yes        | Unix timestamp                 |
| data             | Float     | Yes        | Exchange rate between assets   |
| success          | Boolean   | Yes        | True or False                  |

## Query Crypto Networks

> Response

```json
{
  "success": true,
  "code": 1,
  "msg": "Success",
  "time": 1624989977940,
  "data": [
    {
      "network": "ERC20",
      "name": "Ethereum (ERC20)",
      "depositEnable": true,
      "withdrawEnable": true,
      "confirmationTime": 15,
      "depositAmtMin": "0",
      "depositFeeMin": "0",
      "depositFeeRate": "0",
      "depositExtFees": "0",
      "depositExtFeeRate": "0",
      "needAddressExtension": false,
      "withdrawAmtMin": "36.41",
      "withdrawFeeMin": "6.41",
      "withdrawFeeRate": "0",
      "withdrawExtFees": "0",
      "withdrawExtFeeRate": "0"
    },
    {
      "network": "RIPPLE",
      "name": "Ripple",
      "depositEnable": true,
      "withdrawEnable": true,
      "confirmationTime": 10,
      "depositAmtMin": "0",
      "depositFeeMin": "0",
      "depositFeeRate": "0",
      "depositExtFees": "0",
      "depositExtFeeRate": "0",
      "needAddressExtension": true,
      "addressExtensionTypeName": "tag",
      "withdrawAmtMin": "0.25",
      "withdrawFeeMin": "20",
      "withdrawFeeRate": "0",
      "withdrawExtFees": "0",
      "withdrawExtFeeRate": "0"
    }
  ]
}
```

`GET /public-api/wallet/v1/crypto/networks`

Get crypto network list with corresponding crypto.

This API can be publicly accessed without any security headers to get a default network list.

If you access with `Read` permission authentication, the result will be much more accurate by account setting.
The response of `depositEnable` and `withdrawEnable` is true by default under the publicly accessed environment.

* The total deposit fee is `max(depositFeeMin, (amount * depositFeeRate)) + (depositExtFees + depositExtFeeRate * amount)`.
* The total withdrawal fee is `max(withdrawFeeMin, (amount * withdrawFeeRate)) + (withdrawExtFees + withdrawExtFeeRate * amount)`.

### Request Parameters

| Name             | Type     | Required   | Description   |
| ---------------- | -------- | ---------- | ------------- |
| crypto           | String   | Yes        | Ex: BTC       |


### Response Content

| Name             | Type      | Required   | Description                                             |
| ---------------- | --------- | ---------- | ------------------------------------------------------- |
| data             | Object    | Yes        | Array of objects (CryptoNetworkItem)                    |
| success          | Boolean   | Yes        |Request validation is successful or not. It will be set to `true` when the HTTP status is `200.`                                                                        |
| code             | Integer   | Yes        | Request status code. It will be set to `1` when the request is processed successfully. When unsuccessful, there will be an error code.                               |
| msg              | String    | Yes        | Request status message. It will be set to `Success` when the request is processed successfully. When unsuccessful, there will be an error message.                 |
| time             | Long      | Yes        | Current unix timestamp.                                 |

### Data Object (CryptoNetworkItem)

| Name                     | Type     | Required | Description                          |
|--------------------------|----------|----------|--------------------------------------|
| network                  | String   | Yes      | Network                              |
| name                     | String   | Yes      | Network name                         |
| depositEnable            | Boolean  | Yes      | Allow to deposit                     |
| withdrawEnable           | Boolean  | Yes      | Allow to withdraw                    |
| confirmationTime         | Integer  | No       | Expected block confirmation time     |
| depositAmtMin            | String   | Yes      | Minimum amount of deposit            |
| depositFeeMin            | String   | Yes      | Minimum fees of deposit              |
| depositFeeRate           | String   | Yes      | Fee rate of deposit                  |
| depositExtFees           | String   | Yes      | Extra fees of deposit                |
| depositExtFeeRate        | String   | Yes      | Extra fee rate of deposit            |
| needAddressExtension     | Boolean  | Yes      | Supported address extension          |
| addressExtensionTypeName | String   | No       | Address extension type (e.g. tag)    |
| withdrawAmtMin           | String   | Yes      | Minimum amount of withdrawal         |
| withdrawFeeMin           | String   | Yes      | Minimum fees of withdraw             |
| withdrawFeeRate          | String   | Yes      | Fee rate of withdrawal               |
| withdrawExtFees          | String   | Yes      | Extra fees of withdraw               |
| withdrawExtFeeRate       | String   | Yes      | Extra fee rate of withdraw           |

## Query Asset Exchange Rate

> Response

```json
{
  "success": true,
  "code": 1,
  "msg": "Success",
  "time": 1624989977940,
  "data": {
    "rate": "19026.12846161"
  }
}
```

`GET /public-api/wallet/v1/assets/exchangeRate`

Retrieve exchange rate about a specific pair. For example, `baseCurrency` and `quoteCurrency`.

### Request Parameters

| Name             | Type     | Required   | Description                                                    |
| ---------------- | -------- | ---------- | -------------------------------------------------------------  |
| baseCurrency     | String   | Yes        | Example: baseCurrency=BTC</br>Base currency, such as BTC       |
| amount           | String   | Yes        | Example: amount=2</br>The quantity of `baseCurrency` .         |
| quoteCurrency    | String   | Yes        | Example: quoteCurrency=USDT</br>Quote currency, such as USDT.  |

### Response Content

### Response Content

| Name             | Type      | Required   | Description                                             |
| ---------------- | --------- | ---------- | ------------------------------------------------------- |
| data             | Object    | Yes        | Array of objects (CryptoNetworkItem)                    |
| success          | Boolean   | Yes        |Request validation is successful or not. It will be set to `true` when the HTTP status is `200.`                                                                        |
| code             | Integer   | Yes        | Request status code. It will be set to `1` when the request is processed successfully. When unsuccessful, there will be an error code.                               |
| msg              | String    | Yes        | Request status message. It will be set to `Success` when the request is processed successfully. When unsuccessful, there will be an error message.                 |
| time             | Long      | Yes        | Current unix timestamp.                                 |

### Data Object
| Name                     | Type     | Required | Description                                        |
|--------------------------|----------|----------|--------------------------------------------------- |
| rate                     | String   | No       | The rate of base-currency to quote-currency.       |

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
| currency  | String | Yes      | Currency          |
| total     | Double | Yes      | Total balance     |
| available | Double | Yes      | Available balance |

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
    "status": "COMPLETED",
    "timestamp": 1571630174639,
    "type": "Transfer_In",
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

| Name               | Type    | Required | Description                                                            |
| ---                | ---     | ---      | ---                                                                    |
| currency           | String  | No       | Currency, if not specified will return all currencies                  |
| startTime          | Long    | No       | Starting time in milliseconds (eg. 1624987283000)                      |
| endTime            | Long    | No       | Ending time in milliseconds (eg. 1624987283000)                        |
| count              | Integer | No       | Number of records to return                                            |
| useNewSymbolNaming | Boolean | No       | True to return futures market name in the new format, default to False |


### Response Content

| Name        | Type    | Required | Description                                |
| ---         | ---     | ---      | ---                                        |
| currency    | String  | Yes      | Currency                                   |
| amount      | Double  | Yes      | Amount in the record                       |
| fees        | Double  | Yes      | Fees charged if any                        |
| orderId     | String  | Yes      | Internal wallet order ID                   |
| wallet      | String  | Yes      | Wallet type. For spot will return `@SPOT`  |
| description | String  | Yes      | Description of the transaction             |
| status      | String  | Yes      | The status of the record is as follows<br/>`PROCESSING`<br/>`CANCELLED`<br/>`COMPLETED`<br/>`EXPIRED`<br/>`FAILURE`<br/>`PENDING` |
| type        | String  | Yes      | The type of the record is as follows<br/>`Deposit`<br/>`Withdraw`<br/>`Convert fiat`<br/>`Transfer_Out`<br/>`Transfer_In`<br/>`ReferralEarning`<br/>`Trading Fee Stake Freeze`<br/>`Trading Fee Stake Unfreeze`<br/>`Sub Account Transfer In`<br/>`Sub Account Transfer Out`<br/>`express buy`<br/>`Strategy Income`<br/>`Strategy Pay`<br/>`token voucher in`<br/>`spot trading fee rebate`<br/>`futures trading fee rebate`<br/>`trial fund`<br/>`general trading fee rebate`<br/>`token voucher out` |

## Create Wallet Address

> Request

```json
{
  "currency": "BTC",
  "network": "LIQUID"
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

`POST /api/v3.2/user/wallet/address` or `POST /api/v3.3/user/wallet/address`

Creates a wallet address. If the address created has not been used before, a 400 error will return with the existing unused address. To use this API, `Wallet` permission is required.

### Request Parameters

| Name     | Type   | Required | Description |
| ---      | ---    | ---      | ---         |
| currency | String | Yes      | Ex: BTC     |
| network  | String | Yes      | Ex: BITCOIN |

### Response Content

| Name    | Type   | Required | Description        |
| ---     | ---    | ---      | ---                |
| address | String | Yes      | Blockchain address |
| created | Long   | Yes      | Created timestamp  |

## Delete Wallet Address

> Request

```json
{
  "currency": "BTC",
  "network": "LIQUID",
  "address": "Blockchain address"
}
```

`DELETE /api/v3.2/user/wallet/address` or `DELETE /api/v3.3/user/wallet/address`

Delete  wallet address. If the address has been delete, a 400 error will return. To use this API, `Wallet` permission is required.

### Request Parameters

| Name     | Type   | Required | Description |
|----------| ---    | ---      | ---         |
| currency | String | Yes      | Ex: BTC     |
| network  | String | Yes      | Ex: BITCOIN |
| address  | String | Yes      | Ex: Blockchain address |

## Get Wallet Address

> Request

```json
{
  "currency": "BTC",
  "network": "LIQUID"
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

`GET /api/v3.2/user/wallet/address` or `GET /api/v3.3/user/wallet/address`

Gets a wallet address. To use this API, `Wallet` permission is required.

### Request Parameters

| Name     | Type   | Required | Description |
| ---      | ---    | ---      | ---         |
| currency | String | Yes      | Ex: BTC     |
| network  | String | Yes      | Ex: BITCOIN |

### Response Content

| Name    | Type   | Required | Description        |
| ---     | ---    | ---      | ---                |
| address | String | Yes      | Blockchain address |
| created | Long   | Yes      | Created timestamp  |

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

`POST /api/v3.2/user/wallet/withdraw` or `POST /api/v3.3/user/wallet/withdraw`

Performs a wallet withdrawal. To use this API, `Withdraw` permission is required.

### Request Parameters

| Name               | Type    | Required | Description                                                                                                                                                                                                                                                                            |
| ---                | ---     | ---      | ---                                                                                                                                                                                                                                                                                    |
| currency           | String  | Yes      | Currency-Network pair <br> Currency list can be retrieved from [Available currency list for action](#query-available-currency-list-for-wallet-action) <br> Network list can be retrieved from [Available network list for currency](#query-available-crypto-network-list-for-currency) |
| address            | String  | Yes      | Blockchain address                                                                                                                                                                                                                                                                     |
| tag                | String  | Yes      | Tag, used only by some blockchain (eg. XRP)                                                                                                                                                                                                                                            |
| amount             | String  | Yes      | Amount to withdraw (Max decimal supported is `8` for all currencies). Will return Invalid withdraw amount (code: 3506) if exceeds                                                                                                                                                      |
| includeWithdrawFee | Boolean | No       | If true or the field doesn't exist, the fee is included in amount. Otherwise, the fee is extra added and the deducted amount can be larger than the amount claimed                                                                                                                     |

### Response Content

| Name        | Type   | Required | Description                                                                                                                                                                                                     |
| ---         | ---    | ---      | ---                                                                                                                                                                                                             |
| withdraw_id | String | Yes      | Internal withdrawal ID. References the `orderID` field in `wallet_history` API. As withdrawal will not be processed immediately. User can query the wallet history API to check on the status of the withdrawal |


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
| $currencyName | String | Yes      | Name of currency |


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
| amount    | String | Yes      | amount of currency to convert   |
| fromAsset | String | Yes      | source currency to be converted |
| toAsset   | String | Yes      | destination currency            |

### Response Content

| Name               | Type   | Required | Description                               |
| ---                | ---    | ---      | ---                                       |
| amount             | Float  | Yes      | amount of source currency to be converted |
| settlementAmount   | Float  | Yes      | amount of converted destination currency  |
| amountCurrency     | String | Yes      | source currency                           |
| settlementCurrency | String | Yes      | destination currency                      |
| rate               | Float  | Yes      | exchange rate                             |

## Transfer Funds

> Request

```json
{
  "amount": "1.0",
  "asset": "BTC",
  "toUser": "jamesbond",
  "toUserMail": "james.bond@google.com"
}
```

> Response

```json
{
  "amount": "1",
  "asset": "BTC",
  "toUser": "jamesbond",
  "toUserMail": "james.bond@google.com"
}
```

`POST /api/v3.2/user/wallet/transfer` or `POST /api/v3.3/user/wallet/transfer`

Performs a internal currency transfer to other user from wallet. To use this API, `Transfer` permission is required. To get supported currency list please check [Available currency list for action](#query-available-currency-list-for-wallet-action)

### Request Parameters

| Name               | Type    | Required | Description                                                          |
| ---                | ---     | ---      | ---                                                                  |
| amount             | String  | Yes      | amount of currency to transfer                                       |
| asset              | String  | Yes      | currency to be transferred                                           |
| toUser             | String  | Yes      | receiver account                                                     |
| toUserMail         | String  | Yes      | receiver email                                                       |
| useNewSymbolNaming | Boolean | No       | True if use new futures market name in asset field, default to False |

### Response Content

| Name       | Type   | Required | Description                    |
| ---        | ---    | ---      | ---                            |
| amount     | String | Yes      | amount of currency to transfer |
| asset      | String | Yes      | currency to be transferred     |
| toUser     | String | Yes      | receiver account               |
| toUserMail | String | Yes      | receiver email                 |

## Subaccount transfer history

> Response

```json
{
  "code": 1,
  "msg": "Success",
  "time": 1653964265608,
  "success": true,
  "data": {
    "totalRows": 2,
    "pageSize": 10,
    "currentPage": 1,
    "totalPages": 1,
    "data": [
      {
        "timestamp": 1711707874850,
        "fromUser": "uuooxxsub00002",
        "receiver": "uuooxx",
        "currency": "USDT",
        "amount": 11
      }
    ]
  }
}
```

`GET /api/v3.2/subaccount/wallet/history`

Query transfer history for subaccounts

### Request Parameters

| Name               | Type    | Required | Description                                                          |
| ---                | ---     | ---     | ---                                                            |
| startTime          | Long    | No       | Starting time in milliseconds (eg. 1624987283000)                      |
| endTime            | Long    | No       | Ending time in milliseconds (eg. 1624987283000)                        |
| page             | String  | Yes     | Page number to query, default to 1 (1-based)           |
| pageSize         | String  | Yes     | Number of records in a page, default to 10, maximum 50 |

### Response Content

| Name       | Type   | Required | Description                    |
| ---        | ---    | ---     | ---                           |
| totalRows | Integer | Yes     |Total records               |
| pageSize | Integer | Yes     |Number of records in a page |
| currentPage | Integer | Yes     |current page number         |
| timestamp | Integer | Yes     | Unix timestamp                |
| fromUser | String | Yes     | sender account                |
| receiver | String | Yes     | receiver account                |
| currency | String | Yes     | currency of transferred      |
| amount | Integer | Yes     | amount of currency                |
