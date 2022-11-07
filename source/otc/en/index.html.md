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

## Version 1.1.3 (16th March 2022)

* Addition of request parameter [`side`](#quote-stream) to allow return one side quote.

## Version 1.1.2 (25th January 2022)

* Update [`accept`](#accept-quote) to allow partial accepting the OTC quote.

## Version 1.1.1 (24th November 2021)

* Addition of `unsubcribe-quote` and `unsubscribe-quote-all` op code to unsubscribe streaming OTC quote.

## Version 1.1.0 (17th September 2021)

* Addition of [`quote`](#quote-stream) websocket topic to subscribe to price streams on the OTC market.


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
     * `https://api.btse.com/otc`
     * `https://aws-api.btse.com/otc` (Optimised for connection via AWS, enabled by request)
  * Websocket
     * `wss://ws.btse.com/ws/otc`
     * `wss://aws-ws.btse.com/ws/otc` (Optimised for connection via AWS, enabled by request)
* Testnet
  * HTTP
     * `https://testapi.btse.io/otc`
  * Websocket
     * `wss://testws.btse.io/ws/otc`


## Authentication

* API Key (btse-api)
  * Parameter Name: `btse-api`, in: header. API key is obtained from BTSE platform as a string

* API Key (btse-nonce)
  * Parameter Name: `btse-nonce`, in: header. Representation of current timestamp in long format

* API Key (btse-sign)
  * Parameter Name: `btse-sign`, in: header. A composite signature produced based on the following algorithm: Signature=HMAC.Sha384 (secretkey, (urlpath + btse-nonce + bodyStr)) (note: bodyStr = '' when no data):

### Example 1: Query Quote

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v1/quote1624985375123{\"orderSizeInBaseCurrency\":1,\"orderAmountInOrderCurrency\":0,\"side\":\"buy\",\"baseCurrency\":\"BTC\",\"orderCurrency\":\"USD\"}" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 8ee43810606da581fb6ce03e10370f89125c2269a64de832a55cea219795e9ae0c3df86b51afbafdd28c03b16acd1427
```

* Endpoint to place an order is `https://api.btse.com/otc/api/v1/quote`
* Assume we have the values as follows:
  * btse-nonce: `1624985375123`
  * btse-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v1/quote`
  * Body: `{"orderSizeInBaseCurrency":1,"orderAmountInOrderCurrency":0,"side":"buy","baseCurrency":"BTC","orderCurrency":"USD"}`
  * Encrypted Text: `"/api/v1/quote1624985375123{"orderSizeInBaseCurrency":1,"orderAmountInOrderCurrency":0,"side":"buy","baseCurrency":"BTC","orderCurrency":"USD"}"`
* Generated signature will be:
  * btse-sign: `8ee43810606da581fb6ce03e10370f89125c2269a64de832a55cea219795e9ae0c3df86b51afbafdd28c03b16acd1427`


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

# Workflow

* Request for Quote to get an OTC quote from BTSE
* BTSE responds with a quote based on the request
* If users chooses to accept the quote, quote is sent to BTSE (Quote Accepted)
* If quote is accepted by BTSE, then transaction is completed (Transaction Completed)
* If quote rejected by BTSE, then BTSE will respond with an updated quote with reason of the rejection
* If quote is rejected by the user, then BTSE will respond if quote is rejected successfully (Quote Rejected)

# OTC Endpoints

## Market Summary

> Response

```json
{
  "assetName": "BTC",
  "maxOrderSizes": [
    5000,
    5000,
    5000
  ],
  "maxOrderValues": [
    100000,
    100000,
    100000
  ],
  "minOrderSizes": [
    0.05,
    0.05,
    0.05
  ],
  "minOrderValues": [
    0.0025,
    0.0025,
    0.0025
  ],
  "supportQuoteCurrencies": [
  ]
}
```

`GET /api/v1/getMarket`

Gets OTC market information

### Response Content
| Name                   | Type         | Required | Description                  |
| ---                    | ---          | ---      | ---                          |
| assetName              | string       | Yes      | Asset name                   |
| maxOrderSizes          | Double Array | Yes      | Maximum order size           |
| maxOrderValues         | Double Array | Yes      | Maximum order notional value |
| minOrderSizes          | Double Array | Yes      | Minimum order size           |
| minOrderValues         | Double Array | Yes      | Minimum order notional value |
| supportQuoteCurrencies | string Array | Yes      | Supported quote currencies   |

## Request for Quote

> Request

```json
{
  "baseCurrency": "BTC, USDT",
  "clientOrderId": "BTCUSD0304",
  "orderAmountInOrderCurrency": 2350,
  "orderCurrency": "USD, EUR",
  "orderSizeInBaseCurrency": 20.05,
  "side": "buy, sell"
}
```

> Response

```json
{
  "markets": [
    {
      "assetName": "string",
      "id": 0,
      "maxOrderSizes": [
        0
      ],
      "maxOrderValues": [
        0
      ],
      "minOrderSizes": [
        0
      ],
      "minOrderValues": [
        0
      ],
      "originTimestamp": 0,
      "packetID": 0,
      "packetTimestamp": 0,
      "parametersMap": {
        "property1": {},
        "property2": {}
      },
      "processingTimestamp": 0,
      "requestId": 0,
      "supportQuoteCurrencies": [
        "string"
      ],
      "trackingID": 0
    }
  ],
  "quoteAmountToDeduct": 21563.143,
  "quoteAmountToReceive": 0.311,
  "quoteCurrencyToDeductIn": "EUR",
  "quoteCurrencyToReceiveIn": "BTC",
  "quoteId": "1e5e9ec8-dfb1-****-****-99e20d476c21",
  "quotePriceInOrderCurrency": 6431,
  "quotePriceInUSD": 6431,
  "quoteTimestamp": 1586225934778,
  "quoteValidDurationMs": 10000,
  "status": 30001
}
```

`POST /api/v1/quote`

Request for a quote

### Request Parameters

| Name                       | Type         | Required | Description                    |
| ---                        | ---          | ---      | ---                            |
| baseCurrency               | string       | Yes      | Base currency (eg. BTC)        |
| orderCurrency              | string       | Yes      | Order currency                 |
| orderSizeInBaseCurrency    | Double Array | Yes      | Size of order in base currency |
| orderAmountInOrderCurrency | Double Array | Yes      | Order amount in order currency |
| clientOrderId              | Double Array | Yes      | Custom client order ID         |
| side                       | string       | Yes      | Order side, BUY or SELL        |


### Response Content
| Name                      | Type    | Required | Description                                                                                                                                                                                               |
| ---                       | ---     | ---      | ---                                                                                                                                                                                                       |
| markets                   | Asset   | Yes      | Asset information                                                                                                                                                                                         |
| quoteAmountToDeduct       | double  | Yes      | Quote amount to deduct                                                                                                                                                                                    |
| quoteAmountToReceive      | double  | Yes      | Quote amount to receive                                                                                                                                                                                   |
| quoteCurrencyToDeductIn   | string  | Yes      | Quote currency to deduct in                                                                                                                                                                               |
| quoteCurrencyToReceiveIn  | string  | Yes      | Quote currency to receive                                                                                                                                                                                 |
| quoteId                   | string  | Yes      | Quote ID                                                                                                                                                                                                  |
| quotePriceInOrderCurrency | double  | Yes      | Quote price in order currency                                                                                                                                                                             |
| quotePriceInUSD           | long    | Yes      | Quote price in USD                                                                                                                                                                                        |
| quoteTimestamp            | long    | Yes      | Quote timestamp                                                                                                                                                                                           |
| quoteValidDurationMs      | long    | Yes      | Quote validity                                                                                                                                                                                            |
| status                    | integer | Yes      | Order status with values: <br/>8: Insufficient Balance<br/>30001: Order Quote<br/>30008: OTC Order Requote<br/>30007: OTC Order completed successfully<br/>40001: Service Unavailable<br/>40003: Rejected |

## Accept Quote

> Request

```json
{
  "quoteId": "1e5e9ec8-dfb1-****-****-99e20d476c21",
  "baseAmount": 0,
  "quoteAmount": 300
}
```

> Response

```json
{
  "status": 30007,
  "quoteId": "1e5e9ec8-dfb1-****-****-99e20d476c21",
  "quoteValidDurationMs": 60000,
  "quoteAmountToReceive": 0.00823598,
  "quoteCurrencyToReceiveIn": "BTC",
  "quoteAmountToDeduct": 300.000102,
  "quoteCurrencyToDeductIn": "USD",
  "quoteTimestamp": 1643084422836,
  "quotePriceInOrderCurrency": 36290.47533,
  "quotePriceInUSD": 36290.4753,
  "side": "BUY"
}
```

`POST /api/v1/accept/{quoteId}`

Accepts a quote.
The quote is allowed to be **partially accepted** by taking `baseAmount` or `quoteAmount` in the request body,
which corresponds to `orderSizeInBaseCurrency` and `orderAmountInOrderCurrency` in [`quote`](#request-for-quote), respectively.
Note that if the amount is larger than the the number you quote, only the quoted number will be accepted.

### Request Parameter

| Name          | Type     | Required   | Description                                |
| ------------- | -------- | ---------- | ------------------------------------------ |
| quoteId       | string   | Yes        | Quote ID to supplied as a path parameter   |
| baseAmount    | double   | No         | The partial amount to accept the quote     |
| quoteAmount   | double   | No         | The partial amount to accept the quote     |

### Response Content

| Name                      | Type    | Required | Description                                                                                                                                                                                               |
| ---                       | ---     | ---      | ---                                                                                                                                                                                                       |
| status                    | integer | Yes      | Order status with values: <br/>8: Insufficient Balance<br/>30001: Order Quote<br/>30008: OTC Order Requote<br/>30007: OTC Order completed successfully<br/>40001: Service Unavailable<br/>40003: Rejected |
| quoteId                   | string  | Yes      | Quote ID                                                                                                                                                                                                  |
| quoteValidDurationMs      | long    | Yes      | Quote validity                                                                                                                                                                                            |
| quoteAmountToReceive      | double  | Yes      | Quote amount to receive                                                                                                                                                                                   |
| quoteCurrencyToReceiveIn  | string  | Yes      | Quote currency to receive                                                                                                                                                                                 |
| quoteAmountToDeduct       | double  | Yes      | Quote amount to deduct                                                                                                                                                                                    |
| quoteCurrencyToDeductIn   | string  | Yes      | Quote currency to deduct in                                                                                                                                                                               |
| quoteTimestamp            | long    | Yes      | Quote timestamp                                                                                                                                                                                           |
| quotePriceInOrderCurrency | double  | Yes      | Quote price in order currency                                                                                                                                                                             |
| quotePriceInUSD           | long    | Yes      | Quote price in USD                                                                                                                                                                                        |
| side                      | string  | Yes      | Buy or sell                                                                                                                                                                                               |



## Reject Quote

> Response

```json
{
  "errorCode": -1,
  "message": "string",
  "status": 0
}

```

`POST /otc/api/v1/reject/{quoteId}`

Reject current quote

### Request Parameter

| Name    | Type   | Required | Description                              |
| ---     | ---    | ---      | ---                                      |
| quoteId | string | Yes      | Quote ID to supplied as a path parameter |

## Query Order

> Response

```json
{
  "markets": [
    {
      "assetName": "string",
      "id": 0,
      "maxOrderSizes": [
        0
      ],
      "maxOrderValues": [
        0
      ],
      "minOrderSizes": [
        0
      ],
      "minOrderValues": [
        0
      ],
      "originTimestamp": 0,
      "packetID": 0,
      "packetTimestamp": 0,
      "parametersMap": {
        "property1": {},
        "property2": {}
      },
      "processingTimestamp": 0,
      "requestId": 0,
      "supportQuoteCurrencies": [
        "string"
      ],
      "trackingID": 0
    }
  ],
  "quoteAmountToDeduct": 21563.143,
  "quoteAmountToReceive": 0.311,
  "quoteCurrencyToDeductIn": "EUR",
  "quoteCurrencyToReceiveIn": "BTC",
  "quoteId": "1e5e9ec8-dfb1-****-****-99e20d476c21",
  "quotePriceInOrderCurrency": 6431,
  "quotePriceInUSD": 6431,
  "quoteTimestamp": 1586225934778,
  "quoteValidDurationMs": 10000,
  "status": 30001
}
```

`POST /api/v1/queryOrder/{quoteId}`

Query order information

### Request Parameter

| Name    | Type   | Required | Description                              |
| ---     | ---    | ---      | ---                                      |
| quoteId | string | Yes      | Quote ID to supplied as a path parameter |

### Response Content

| Name                      | Type    | Required | Description                                                                                                                                                                                               |
| ---                       | ---     | ---      | ---                                                                                                                                                                                                       |
| markets                   | Asset   | Yes      | Asset information                                                                                                                                                                                         |
| quoteAmountToDeduct       | double  | Yes      | Quote amount to deduct                                                                                                                                                                                    |
| quoteAmountToReceive      | double  | Yes      | Quote amount to receive                                                                                                                                                                                   |
| quoteCurrencyToDeductIn   | string  | Yes      | Quote currency to deduct in                                                                                                                                                                               |
| quoteCurrencyToReceiveIn  | string  | Yes      | Quote currency to receive                                                                                                                                                                                 |
| quoteId                   | string  | Yes      | Quote ID                                                                                                                                                                                                  |
| quotePriceInOrderCurrency | double  | Yes      | Quote price in order currency                                                                                                                                                                             |
| quotePriceInUSD           | long    | Yes      | Quote price in USD                                                                                                                                                                                        |
| quoteTimestamp            | long    | Yes      | Quote timestamp                                                                                                                                                                                           |
| quoteValidDurationMs      | long    | Yes      | Quote validity                                                                                                                                                                                            |
| status                    | integer | Yes      | Order status with values: <br/>8: Insufficient Balance<br/>30001: Order Quote<br/>30008: OTC Order Requote<br/>30007: OTC Order completed successfully<br/>40001: Service Unavailable<br/>40003: Rejected |

# Websocket Streams

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
echo -n "/ws/otc1624985375123"  | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= c410d38c681579adb335885800cff24c66171b7cc8376cfe43da1408c581748156b89bcc5a115bb496413bda481139fb
```


## Quote Stream

> Request

```json
{
  "op": "quote",
  "symbol": "BTC-USD",
  "side": "buy",
  "clOrderId": "ClientOrder1",
  "quantity": {
    "quantity": 1,
    "currency": "BTC"
  }
}
```

```json
{
  "op": "unsubscribe-quote",
  "symbol": "BTC-USD",
  "clOrderId": "ClientOrder1",
  "quantity": {
    "quantity": 1,
    "currency": "BTC"
  }
}
```

```json
{
  "op": "unsubscribe-quote-all"
}
```


> Response

```json
{
  "topic": "quote",
  "buyQuoteId": "015f05ba-1d55-46d7-94d9-214229414ae7",
  "sellQuoteId": "0683a41a-a2ad-467b-99b3-241f3ab0cec4",
  "clOrderId": null,
  "buyQuantity": 10,
  "buyUnitPrice": 47865.580838,
  "buyTotalAmount": 478655.80838,
  "sellQuantity": 10,
  "sellUnitPrice": 47649.40351972,
  "sellTotalAmount": 476494.0352,
  "status": null,
  "reason": null
}

```

Receive quote streams by subscribing to the `quote` websocket. The websocket topic will constantly push new prices to the subscriber. To accept the quote, indicate the buy or sell quote Id using the `/accept` API.

### Request Parameters

| Name      | Type   | Required | Description                                                                                                             |
| ---       | ---    | ---      | ---                                                                                                                     |
| op        | string | Yes      | Operation, in this case it is `quote`, `unsubscribe-quote`, or `unsubscribe-quote-all`                                  |
| symbol    | string | Yes      | Market symbol, refer to `getMarkets` API                                                                                |
| side      | string | No       | Quote side, `buy` or `sell`, case sensitive. Both sides will be returned when this field is empty/null                  |
| clOrderId | string | No       | Client custom order Id                                                                                                  |
| quantity  | double | Yes      | Order quantity                                                                                                          |
| currency  | string | Yes      | Can be either in the base or quote currency. If specified in the base currency, then the quote stream will respond with |

### Response Content

| Name            | Type   | Required | Description                                                                                                                                         |
| ---             | ---    | ---      | ---                                                                                                                                                 |
| topic           | string | Yes      | Websocket topic                                                                                                                                     |
| buyQuoteId      | string | No       | Quote Id for the buy side. If the value is empty / null, it means that you websocket stream is not authenticated or you doesn't subscribe this side |
| sellQuoteId     | string | No       | Quote Id for the sell side. If the value is empty / null, it means that you websocket stream is not authenticated or you doesn't subscribe this side|
| clOrderId       | string | Yes      | User customer Order Id                                                                                                                              |
| buyQuantity     | double | No       | Quantity to purchase based on the quote request. If the value is null, it means that you doesn't subscribe this side                                |
| buyUnitPrice    | double | No       | Unit price per unit of the base symbol. If the value is null, it means that you doesn't subscribe this side                                         |
| buyTotalAmount  | double | No       | Total price to pay in quote currency. If the value is null, it means that you doesn't subscribe this side                                           |
| sellQuantity    | double | No       | Quantity to sell based on the quote request. If the value is null, it means that you doesn't subscribe this side                                    |
| sellUnitPrice   | double | No       | Unit price per unit of the base symbol. If the value is null, it means that you doesn't subscribe this side                                         |
| sellTotalAmount | double | No       | Total price to pay in quote currency. If the value is null, it means that you doesn't subscribe this side                                           |
| status          | string | No       | Status of the response. If the value is null, it means that you doesn't subscribe this side                                                         |
| reason          | string | No       | If an error is returned, the reason field will contain the reasons for the error                                                                    |


</section>
