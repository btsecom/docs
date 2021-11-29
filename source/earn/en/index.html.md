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

## Version 1.0 (8th December 2021)

* Initial release of the earn(invest) api


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
     * `https://aws-api.btse.com/spot` (Optimised for connection via AWS)
* Testnet
  * HTTP
     * `https://testapi.btse.io/spot`

## Authentication

* API Key (btse-api)
  * Parameter Name: `btse-api`, in: header. API key is obtained from BTSE platform as a string

* API Key (btse-nonce)
  * Parameter Name: `btse-nonce`, in: header. Representation of current timestamp in long format

* API Key (btse-sign)
  * Parameter Name: `btse-sign`, in: header. A composite signature produced based on the following algorithm: Signature=HMAC.Sha384 (secretkey, (urlpath + btse-nonce + bodyStr)) (note: bodyStr = '' when no data):


# Investment Endpoints

## Query Investment Products

> Response

```json
[
  {
    "id": "OPENETH00001",
    "name": "ETH Flex Savings",
    "currency": "ETH",
    "type": "Flex",
    "startDate": 1610685918000,
    "interestStartDate": 1610719200000,
    "rates":
    [
      {
        "days": 1,
        "rate": 1.15
      }
    ],
    "compounding": true,
    "autoRenewSupported": false,
    "dailyLimit": 10.0,
    "minSize": 1.00000000,
    "incrementalSize": 1.00000000
  }
]
```

`GET /api/v3.2/invest/products`

Get all investment products

### Request Parameters

(None)

### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| id | string | Yes | Product id |
| name | string | Yes | Product name |
| currency | string | Yes | Currency |
| type | string | Yes | Product type |
| startDate | long | Yes | Inventment start date |
| interestStartDate | long | Yes | Interest start date |
| rates | RateObject[] | Yes | Interest rate information |
| compounding | double | Yes | is product compounding |
| autoRenewSupported | double | Yes | is product supported renew automatically |
| dailyLimit | double | Yes | Daily invent amount limit |
| minSize | double | Yes | Minimum invest size |
| incrementalSize | double | Yes | Invest step size |

### RateObject

|Name|Type|Required|Description|
|---|---|---|---|
| days | integer | Yes | Duration in days |
| rate | double | Yes | Interest rate |


## Deposit Investment

> Request

```json
{
    "productId": "OPENUSDT0001",
    "amount": 100.99,
    "renew": true,
    "rate": 6,
    "day": 7
}
```

`POST /api/v3.2/invest/deposit`

Deposit an investment

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| productId | string | Yes | Invest product id |
| amount | double | Yes | Invest amount |
| renew | boolean | Yes | renew automatically |
| rate | double | Yes | Interest rate |
| day | integer | Yes | Duration in days |


## Renew Investment

> Request

```json
{
    "orderId": 1,
    "autoRenew": false
}
```

> Response

```json
{
    "orderId": 1,
    "autoRenew": false
}
```

`POST /api/v3.2/invest/renew`

Renew an investment order

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| orderId | integer | Yes | Investment order id |
| autoRenew | boolean | Yes | renew automatically |

### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| orderId | integer | Yes | Investment order id |
| autoRenew | boolean | Yes | status of autoRenew flag |


## Redeem Investment

> Request

```json
{
    "orderId": 1,
    "amount": 12.34
}
```

`POST /api/v3.2/invest/redeem`

Redeem an investment order

### Request Parameters

|Name|Type|Required|Description|
|---|---|---|---|
| orderId | integer | Yes | Investment order id |
| amount | double | Yes | Redeem amount |


## Query Investment Orders

> Response

```json
[
  {
    "id": 456,
    "name": "ETH Flex Savings",
    "currency": "ETH",
    "type": "Flex",
    "rate": 1.15,
    "investAmt": 10.00000000,
    "interestEarned": 0.00031507,
    "nextInterestPayoutTime": 1610632800000,
    "startTime": 0,
    "endTime": 0,
    "duration": 86400000,
    "payoutLockTime": 300000,
    "autoRenew": false,
    "compounding": true,
    "autoRenewSupported": false,
    "dailyLimit": 0,
    "redemptionProcessing": false
  }
]
```

`GET /api/v3.2/invest/orders`

Query investment orders

### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| id | integer | Yes | Order id |
| name | string | Yes | Product name |
| currency | string | Yes | Currency |
| type | string | Yes | Product type |
| rate | boolean | Yes | Interest rate |
| investAmt | boolean | Yes | Amount |
| interestEarned | boolean | Yes | Intereset earned |
| nextInterestPayoutTime | boolean | Yes | Next interest payout time |
| startTime | boolean | Yes | Start time |
| endTime | boolean | Yes | End time |
| duration | boolean | Yes | Duration |
| payoutLockTime | boolean | Yes | Lock time of payout |
| autoRenew | boolean | Yes | renew automatically |
| compounding | boolean | Yes | is compounding |
| autoRenewSupported | boolean | Yes | is renew automatically supported |
| redemptionProcessing | boolean | Yes | is redemption processing |


## Query Investment History

> Response

```json
[
  {
    "txnTime": 1598918400000,
    "name": "USDT Flex Savings",
    "currency": "USDT",
    "rate": 0.5,
    "type": "Flex",
    "txnType": "INVEST_SERVICE_TYPE_DEPOSIT",
    "amount": 100,
    "totalAmount": 2000,
    "interestEarned": 1.22,
    "duration": 0
  }
]
```

`GET /api/v3.2/invest/history`

Query investment history

### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| txnTime | integer | Yes | Transaction time |
| name | string | Yes | Product name |
| currency | string | Yes | Currency |
| rate | string | Yes | Interest rate |
| type | boolean | Yes | Product type |
| txnType | boolean | Yes | Transaction type |
| amount | boolean | Yes | Transaction amount |
| totalAmount | boolean | Yes | Total amount of the investment |
| interestEarned | boolean | Yes | Interest earned |
| duration | boolean | Yes | Duration |
