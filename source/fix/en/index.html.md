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

FIX endpoint URL: **tcp+ssl://fix.btse.com:4363**

Clients should connect to the endpoint using SSL.

Sequence numbers are reset for each connection. Resend request and sequence reset messages are not supported.


# Change Log

## Version 0.0.1 (2nd September 2022)

* Publish [FIX API](#fix-api)


# Rate limit

Rate limit constraints are described below:

| Group    | Message Types included | Description |
| ---      | ---                    | ---         |
| Auth     | Logon (A), Logout (5)                              |  2 times in 1 second by group |
| General  | All message types except: Logon (A) and Logout (5) | 30 times in 1 second by group |

When rate limit rule is violated, client's request would be rejected and server returns a Business Message Reject (j).

| Tag | Name | Example | Description |
| --- | ---  | ---     | ---         |
| 8   | BeginString          | FIX.4.2                                                          | FIX version                                    |
| 9   | BodyLength           | 162                                                              | Length of the message body in bytes            |
| 10  | CheckSum             | 118                                                              | CheckSum of the message                        |
| 34  | MsgSeqNum            | 17                                                               | Sequence number of the message                 |
| 35  | MsgType              | j                                                                | Always set to "j": business message reject     |
| 45  | RefSeqNum            | 11                                                               | Sequence number of rejected message            |
| 49  | SenderCompID         | BTSE                                                             | Always set to: "BTSE"                          |
| 52  | SendingTime          | 20220914-10:27:55                                                | Sending time of the message                    |
| 56  | TargetCompID         | c123456c98765d306fae4f90b25c27a07cd8be12345678912d7ead46f0d9505a | Client's API Key                               |
| 57  | TargetSubID          | SPOT                                                             | "SPOT": spot market; "FUTURES": futures market |
| 58  | Text                 | exceeding rate limit                                             | Detail information                             |
| 372 | RefMsgType           | F                                                                | Message type of rejected message               |
| 380 | BusinessRejectReason | 4                                                                | Always set to "4": application not available   |


# Messages

```
8=FIX.4.2|9=162|35=A|49=zyfvB4QPg0A3kkVgqUE9V1fOA-Y6jhdG3seqIIZx|56=BTSE
```

All messages should include the following header:

This documentation uses | to represent the FIX field separator (byte 0x01). It should be replaced by 0x01 in actual messages.

| Tag |	Name | Example | Description |
| --- | ---  | ---     | ---         |
| 8  | BeginString  | FIX.4.2                                  | Must be set to "FIX.4.2"                             |
| 9  | BodyLength   | 162                                      | Length of the message body in bytes                  |
| 35 | MsgType      | 8                                        | Message type                                         |
| 49 | SenderCompID | zyfvB4QPg0A3kkVgqUE9V1fOA-Y6jhdG3seqIIZx | Client API key (for messages from the client)        |
| 56 | TargetCompID | BTSE                                     | Must be set to "BTSE" (for messages from the client) |

Messages should also include a sequence number MsgSeqNum (34) and a timestamp SendingTime (52). Sequence numbers start at 1 and must be incremented with every message. Messages with duplicate or out-of-order sequence numbers will be rejected. Sequence numbers are reset on new connections.

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
| 44	| Price       | 18000    | Limit price (required in Limit order and Market buy order)                           |
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

Only one of OrderID (37) and OrigClOrdID (41) should be provided.

If the order is successfully cancelled, an ExecutionReport (8) will be returned. Otherwise, an OrderCancelReject (9) will be returned.


## Order Cancel Reject (9)

Sent by the server to notify the client that an OrderCancelRequest (F) failed.


| Tag | Name | Value | Description |
| --- | ---  | ---   | ---         |
| 35  | MsgType          | 9        |                                                      |
| 37  | OrderID          | order123 | Copied from OrderCancelRequest, won't show up if not provided in OrderCancelRequest. |
| 41  | OrigClOrdID      | order123 | Copied from OrderCancelRequest, won't show up if not provided in OrderCancelRequest. |
| 39  | OrdStatus        | 0        | Currently only support: "0": new                     |
| 102 | CxlRejReason     | 1        | "1": unknown order, "99": others                     |
| 434 | CxlRejResponseTo | 1        | Always set to "1"                                    |
