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

## Version 1.0 (19th November 2021)

* Addition of [`quote`](#quote-stream) websocket topic to subscribe to price streams on the OTC market


# Overview

## Generating API Key

You will need to create an API key on the BTSE platform before you can use authenticated APIs. To create API keys, you can follow the steps below:

* Login with your username / email and password into the BTSE website
* Click on “Account” on the top right hand corner
* Select the API tab
* Click on “New API” button to create an API key and passphrase. (Note: the passphrase will only appear once)
* Use your API key and passphrase to construct a signature.

## Endpoints

### Streaming OTC quote

* Production
  * Websocket
     * `wss://ws.btse.com/ws/otc`
     * `wss://aws-ws.btse.com/ws/otc` (Optimised for connection via AWS)
* Testnet
  * Websocket
     * `wss://testws.btse.io/ws/otc`


## Authentication

* API Key (btse-api)
  * Parameter Name: `btse-api`, in: header. API key is obtained from BTSE platform as a string

* API Key (btse-nonce)
  * Parameter Name: `btse-nonce`, in: header. Representation of current timestamp in long format

* API Key (btse-sign)
  * Parameter Name: `btse-sign`, in: header. A composite signature produced based on the following algorithm: Signature=HMAC.Sha384 (secretkey, (urlpath + btse-nonce + bodyStr)) (note: bodyStr = '' when no data):

# Workflow

## Streaming OTC

* Fetch market info via `Market Summary` OTC api if needed.
* Subscribe to `Quote Stream` to get streaming otc quote along with quote ids periodically.
* Please refer to `OTC` section for API to accept the quote
  - If users chooses to accept the quote, quote is sent to BTSE (Quote Accepted)
  - If quote is accepted by BTSE, then transaction is completed (Transaction Completed)
  - If quote rejected by BTSE, then BTSE will respond with an updated quote with reason of the rejection

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

|Index|Type|Required|Description|
|---|---|---|---|
| 0 | string | Yes | First argument is the API key |
| 1 | long | Yes | Nonce which is the current timestamp |
| 2 | string | Yes | Generated signature |

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
  "clOrderId": "ClientOrder1",
  "quantity": {
    "quantity": 1,
    "currency": "BTC"
  }
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

|Name|Type|Required|Description|
|---|---|---|---|
| op | string | Yes | Operation, in this case its `quote` |
| symbol | string | Yes | Market symbol, refer to `getMarkets` API |
| clOrderId | string | No | Client custom order Id |
| quantity | double | Yes | Order quantity |
| currency | string | Yes | Can be either in the base or quote currency. If specified in the base currency, then the quote stream will respond with  |

### Response Content

|Name|Type|Required|Description|
|---|---|---|---|
| topic | string | Yes | Websocket topic |
| buyQuoteId | string | Yes | Quote Id for the buy side. If the value is empty / null, it means that you websocket stream is not authenticated |
| sellQuoteId | string | Yes | Quote Id for the sell side. If the value is empty / null, it means that you websocket stream is not authenticated |
| clOrderId | string | Yes | User customer Order Id |
| buyQuantity | double | Yes | Quantity to purchase based on the quote request |
| buyUnitPrice | double | Yes | Unit price per unit of the base symbol |
| buyTotalAmount | double | Yes | Total price to pay in quote currency |
| sellQuantity | double | Yes | Quantity to sell based on the quote request |
| sellUnitPrice | double | Yes | Unit price per unit of the base symbol |
| sellTotalAmount | double | Yes | Total price to pay in quote currency |
| status | string | No | Status of the response |
| reason | string | No | If an error is returned, the reason field will contain the reasons for the error |


</section>
