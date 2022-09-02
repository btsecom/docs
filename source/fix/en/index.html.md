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


## Messages

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

### New Order Single (D)

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