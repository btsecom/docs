---
title: BTSE FIX Documentation
language_tabs:
- json
  toc_footers: []
  includes: []
  search: true
  highlight_theme: darkula
  code_clipboard: true
  headingLevel: 2

---

# FIX API

FIX (Financial Information eXchange) is a standard electronic messaging protocol which can be used to place orders, receive order updates and executions, and cancel orders. Our FIX api is based on the FIX 4.2 specification and modeled after FIX implementations of other popular cryptocurrency exchanges.

<aside class="notice">
This service is restricted. Please drop an email to bd@btse.com for further information
</aside>

FIX endpoints: tcp+ssl://fix.btse.com:9876

| Environment | SocketConnectHost      | SocketConnectPort |
| ---         | ---                    | ---               |
| test        | tcp+ssl://fix.btse.io  | 9876              |
| production  | tcp+ssl://fix.btse.com | 9876              |

Sessions for Spot and Futures are separated.

| SenderSubID |
| ---         |
| SPOT        |
| FUTURES     |


# Change Log

## Version 1.1.1 (7th February 2023)

* Revise Common request attributes

## Version 1.1.0 (6th December 2022)

* Release Futures market trading functions [FIX API](#fix-api)

## Version 1.0.0 (18th October 2022)

* Release Spot market trading functions [FIX API](#fix-api)


# Rate limit

Rate limit constraints are described below:

| Group    | Message Types included | Description |
| ---      | ---                    | ---         |
| Auth     | Logon (A), Logout (5)                              |  2 times in 1 second by group |
| General  | All message types except: Logon (A) and Logout (5) | 30 times in 1 second by group |

When rate limit rule is violated, client's request would be rejected and server returns a Business Message Reject (j).

| Tag | Name | Example | Description |
| --- | ---  | ---     | ---         |
| 8   | BeginString          | FIX.4.2              | FIX version                                    |
| 9   | BodyLength           | 162                  | Length of the message body in bytes            |
| 10  | CheckSum             | 118                  | CheckSum of the message                        |
| 34  | MsgSeqNum            | 17                   | Sequence number of the message                 |
| 35  | MsgType              | j                    | Always set to "j": business message reject     |
| 45  | RefSeqNum            | 11                   | Sequence number of rejected message            |
| 49  | SenderCompID         | BTSE                 | Always set to: "BTSE"                          |
| 52  | SendingTime          | 20220914-10:27:55    | Sending time of the message                    |
| 56  | TargetCompID         | c123...05a           | Client's API Key                               |
| 57  | TargetSubID          | SPOT                 | "SPOT": spot market; "FUTURES": futures market |
| 58  | Text                 | exceeding rate limit | Detail information                             |
| 372 | RefMsgType           | F                    | Message type of rejected message               |
| 380 | BusinessRejectReason | 4                    | Always set to "4": application not available   |


# Messages

FIX protocol uses field separator (character: `0x01`) to separate attributes in messages.

## Common request attributes

Below attributes are required in every client's request message.

| Tag |	Name | Example | Description |
| --- | ---  | ---     | ---         |
| 8  | BeginString  | FIX.4.2   | Must be set to "FIX.4.2"                             |
| 9  | BodyLength   | 162       | Length of the message body in bytes                  |
| 34 | MsgSeqNum    | 1         | Sequence of message, starts from 1 and must be incremented with every message. Messages with duplicate or out-of-order sequence numbers will be rejected. Sequence numbers are reset on new connections. |
| 35 | MsgType      | 8         | Message type                                         |
| 49 | SenderCompID | zyf...IZx | Client API key                                       |
| 50 | SenderSubID  | SPOT      | "SPOT": spot market; "FUTURES": futures market       |
| 52 | SendingTime  | 20220916-07:29:07 | Sending time of message                      |
| 56 | TargetCompID | BTSE      | Must be set to "BTSE" (for messages from the client) |
| 10 | CheckSum     | 145       | CheckSum of the message                              |


## Logon (A)

``` java
import org.apache.commons.codec.binary.Hex;
import org.apache.commons.codec.digest.HmacAlgorithms;
import org.apache.commons.codec.digest.HmacUtils;

// initialize String parameters: apiSecret, sendingTime, messageType, messageSeqNum, senderCompID, targetCompID


// compute the SHA384 HMAC using the API secret
final char SOH = 1;
final CharSequence SEPARATOR = Character.toString(SOH);

final String DATARAW = String.join(SEPARATOR, sendingTime, messageType, messageSeqNum, senderCompID, targetCompID);
final String SIGNATURE = Hex.encodeHexString(HmacUtils.getInitializedMac(HmacAlgorithms.HMAC_SHA_384, apiSecret.getBytes()).doFinal(dataRaw.getBytes()));
```

Sent by the client to initiate a FIX session. Must be the first message sent after a connection is established. Only one session can be established per connection; additional Logon messages are rejected.
Client's API Key and secret can be generated from API page in BTSE portal. Create key with permissions to use FIX APIs.

| Tag | Name | Value | Description |
| --- | ---  | ---   | ---         |
|  35 | MsgType         | A                 |                           |
|  95 | RawDataLength   | 96                | Length of RawData         |
|  96 | RawData         | 8f7e...4783       | For security, the Logon message must be signed by the client. To compute the signature, concatenate the following fields, joined by the FIX field separator (byte 0x01), and compute the SHA384 HMAC using the API secret:<br/><br/> * SendingTime (52)<br/> * MsgType (35)<br/> * MsgSeqNum (34)<br/> * SenderCompID (49)<br/> * TargetCompID (56)<br/><br/>The resulting hash should be hex-encoded. |
|  98 | EncryptMethod   | 0                 | Must be set to "0" (None) |
| 108 | HeartBInt       | 30                | Must be set to "30"       |
| 141 | ResetSeqNumFlag | Y                 | Must be set to "Y"        |


## Heartbeat (0)

| Tag | Name | Value | Description |
| --- | ---  | ---   | ---         |
|  35 | MsgType   |   0 |          |
| 112 | TestReqID | 123 | If this heartbeat is in response to a TestRequest, copied from the TestRequest. |

## Test Request (1)

| Tag | Name | Value | Description |
| --- | ---  | ---   | ---         |
|  35 | MsgType   |   1 |          |
| 112 | TestReqID | 123 | Arbitrary string, to be echoed back by a Heartbeat. |

## Logout (5)

Sent by either side to terminate the session. The other side should respond with another Logout message to acknowledge session termination. The connection will be closed afterwards.			

| Tag | Name    | Value | Description |
| --- | ---     | ---   | ---         |
|  35 | MsgType | 5     |             |

## New Order Single (D)

Sent by the client to submit a new order. Only Market, Limit orders are currently supported by the FIX API.

| Tag |	Name | Value | Description |
| --- | ---  | ---   | ---         |
| 35	| MsgType     | D        |   |
| 21	| HandlInst   | 1        | Must be set to "1" (AutomatedExecutionNoIntervention)                                |
| 11	| ClOrdID     | order123 | Arbitrary client-selected string to identify the order; must be unique               |
| 55	| Symbol      | BTC-USD  | Symbol name                                                                          |
| 40	| OrdType     | 2        | "1": Market; "2": Limit                                                              |
| 38	| OrderQty    | 1.1      | Order size in base units (required in Limit order and Market sell order)             |
| 44	| Price       | 18000    | Limit price or Market buy price (required in Limit order and Market buy order)       |
| 54	| Side        | 1        | "1": buy; "2": sell                                                                  |
| 59	| TimeInForce | 1        | "1": Good Till Cancel; "3": Immediate or Cancel; "4": Fill or Kill (for Limit order) |
| 18	| ExecInst    | 6        | This parameter is optional. "E": reduce only, "6": post only, not supplied: standard |

If the order is accepted, an ExecutionReport (8) will be returned with ExecType: 0 (New), 1 (Partial fill), 2 (Fill), 4 (Canceled), 7 (Stopped), 8 (Rejected).


## Order Cancel Request (F)

Sent by the client to request to cancel an order.

| Tag | Name | Value | Description |
| --- | ---  | ---   | ---         |
| 35  | MsgType     | F        |   |
| 37  | OrderID     | order123 | System-assigned order ID of the order |
| 41  | OrigClOrdID | order123 | Client-assigned order ID of the order |
| 55  | Symbol      | BTC-USD  | Symbol name                           |

Only one of OrderID (37) and OrigClOrdID (41) should be provided.

If the order is successfully cancelled, an ExecutionReport (8) will be returned. Otherwise, an OrderCancelReject (9) will be returned.


## Order Cancel Reject (9)

Sent by the server to notify the client that an OrderCancelRequest (F) failed.

| Tag | Name | Value | Description |
| --- | ---  | ---   | ---         |
| 35  | MsgType          | 9        |                                                      |
| 37  | OrderID          | order123 | Copied from OrderCancelRequest, won't show up if not provided in OrderCancelRequest. |
| 41  | OrigClOrdID      | order123 | Copied from OrderCancelRequest, won't show up if not provided in OrderCancelRequest. |
| 39  | OrdStatus        | 4        | "4" (Canceled) if the order was already cancelled                     |
| 102 | CxlRejReason     | 1        | "1": unknown order, "99": others                     |
| 434 | CxlRejResponseTo | 1        | Always set to "1"                                    |

## Order Status Request (H)

Sent by the server to notify the client that an OrderCancelRequest (F) failed.

| Tag | Name | Value | Description |
| --- | ---  | ---   | ---         |
| 35 | MsgType     | H        |                                       |
| 37 | OrderID     | order123 | OrderID of the order to request, or "*" to request all pending orders |
| 41 | OrigClOrdID | order123 | Client-assigned order ID of the order |
| 54 | Side        | 1        | "1": buy; "2": sell                   |
| 55 | Symbol      | BTC-USD  | Symbol name                           |

The server will respond with an ExecutionReport (8) with ExecType=I (OrderStatus) with the requested order or orders. Only one of OrderID (37) and OrigClOrdID (41) should be provided. If both OrderId (37) and OrigClOrdID (41) are provided, only OrderId (37) would be applied. When there are no open orders, the server will include Text (58) of "No open orders".

## Execution Report (8)

Sent by the server whenever an order receives a fill, whenever the status of an order changes, or in response to a NewOrderSingle (D), OrderCancelRequest (F), or OrderStatusRequest (H) message from the client.			

| Tag | Name | Value | Description |
| --- | ---  | ---   | ---         |
| 11  | ClOrderId | order123 | Client-selected order ID. |
| 12  | Commission | 0.002 | Fee for trade. Only present if this message was the result of a fill |
| 13  | CommType | 3 | Always 3 |
| 14  | CumQty | 0.4 | Quantity of order that has already been filled |
| 17  | ExecID | d840c87b-ad98-47b1-95d3-4d41950fa776 | Order ID |
| 31  | LastPx | 7999.25 | Fill price. Only present if this message was the result of a fill |
| 32  | LastQty | 0.4 | Fill quantity. Only present if this message was the result of a fill |
| 35  | MsgType | 8  |             |
| 37  | OrderID | d840c87b-ad98-47b1-95d3-4d41950fa776 | Order ID |
| 38  | OrderQty | 1.2 | Original order quantity |
| 39  | OrdStatus | 0  | Order status (see below) |
| 44  | Price | 8000 | Original order price |
| 54  | Side | 1  | "1": buy; "2": sell |
| 55  | Symbol | BTC-USD | Symbol name |
| 58  | Text | text | Description of the reason the order was rejected |
| 60  | TransactTime | 20190525-08:26:38.989 | Time of the order update. Only present on order updates |
| 103  | OrdRejReason | 11 | "11": when request is failed (UNSUPPORTED_ORDER_CHARACTERISTIC). The rejected reason detail will be shown in Text(58) |
| 150  | ExecType | 1 | Reason for this message (see below) |
| 151  | LeavesQty | 0.8 | Quantity of order that is still open |
| 1057 | AggressorIndicator | Y | "Y": taker fill; "N": maker fill. Only present if this message was the result of a fill |
| 5000 | Liquidation | Y | "Y": messages corresponds to an on-market liquidation order. "N" or absent: it does not. |


### ExecType values 

The ExecType (150) field indicates the reason why this ExecutionReport was sent.

| ExecType | Description |
| --- | ---|
| 0 | New order |
| 1 | Partially filled order |
| 3 | Fully filled order |
| 4 | Order cancelled |
| 5 | Order amended |
| 7 | Order refund (self-trade) |
| 8 | Response to a rejected NewOrderSingle (D) request |
| I | Response to a OrderStatusRequest (H) request |

Note that every order changed will send a execution report message.

### OrdStatus values

| OrdStatus | Description |
| --- | --- |
| 0 | New Order |
| 1 | Partially filled order |
| 3 | Fully filled order |
| 4 | Cancelled order |
| 5 | Amended order |
| 7 | Refunded order |
| 8 | Rejected order |


## Reject (3)

Sent by the server in response to an invalid message.

| Tag | Name | Value | Description |
| --- | ---  | ---   | ---         |
| 35  | MsgType             | 3                |                                         |
| 45  | RefSeqNum           | 2                | Sequence number of the rejected message |
| 371 | RefTagID            | 38               | Tag number of the rejected field        |
| 372 | RefMsgType          | D                | Message type of the rejected message    |
| 58  | Text                | Missing quantity | Human-readable description of the reason for the rejection |
| 373 | SessionRejectReason | 1                | Code to identify the rejection reason   |