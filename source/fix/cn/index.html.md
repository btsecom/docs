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

FIX（金融信息交换）是一种标准的电子消息传输协议，可用于下订单、接收订单更新和执行，以及取消订单。我们的 FIX API 基于 FIX 4.2 规范，并模仿了其他热门加密货币交易所的 FIX 实现。

FIX 终端点：tcp+ssl://fix.btse.com:9876

| 环境       | SocketConnectHost      | SocketConnectPort |
| ---        | ---                    | ---               |
| 测试       | tcp+ssl://fix.btse.io  | 9876              |
| 生产       | tcp+ssl://fix.btse.com | 9876              |

Spot 和 Futures 的会话是分开的。

| SenderSubID |
| ---         |
| SPOT        |
| FUTURES     |


# 更新日志

## 版本 1.1.4（2023年11月15日）

添加新的订单生效时间（timeInForce）状态

## 版本 1.1.3（2023年7月10日）

添加 [心跳 (0)](#0) 推荐

## 版本 1.1.2（2023年7月10日）

* 在 Futures 市场中应用新的符号名称。在 [登录 (A)](#a) 消息中添加 ApplyNewSymbolName

## 版本 1.1.1（2023年2月7日）

* 修改常见请求属性

## 版本 1.1.0（2022年12月6日）

* 发布期货市场交易功能 [FIX API](#fix-api)

## 版本 1.0.0（2022年10月18日）

* 发布现货市场交易功能 [FIX API](#fix-api)


# 速率限制

速率限制约束如下：

| 组别    | 包括的消息类型 | 描述 |
| ---      | ---                    | ---         |
| Auth     | Logon (A), Logout (5)                              |  每组 1 秒 2 次 |
| General  | 除 Logon (A) 和 Logout (5) 之外的所有消息类型 |  每组 1 秒 30 次 |

当违反速率限制规则时，客户端的请求将被拒绝，服务器将返回业务消息拒绝 (j)。

| 标签 | 名称 | 示例 | 描述 |
| --- | ---  | ---     | ---         |
| 8   | BeginString          | FIX.4.2              | FIX 版本                                    |
| 9   | BodyLength           | 162                  | 消息正文的长度（以字节为单位）            |
| 10  | CheckSum             | 118                  | 消息的校验和                        |
| 34  | MsgSeqNum            | 17                   | 消息的序列号                  |
| 35  | MsgType              | j                    | 始终设置为 "j"：业务消息拒绝     |
| 45  | RefSeqNum            | 11                   | 被拒绝消息的序列号            |
| 49  | SenderCompID         | BTSE                 | 始终设置为 "BTSE"              |
| 52  | SendingTime          | 20220914-10:27:55    | 消息的发送时间                    |
| 56  | TargetCompID         | c123...05a           | 客户 API 密钥                   |
| 57  | TargetSubID          | SPOT                 | "SPOT"：现货市场；"FUTURES"：期货市场 |
| 58  | Text                 | exceeding rate limit | 详细信息                             |
| 372 | RefMsgType           | F                    | 被拒绝消息的消息类型           |
| 380 | BusinessRejectReason | 4                    | 始终设置为 "4"：应用程序不可用   |


# 消息

FIX 协议使用字段分隔符（字符：`0x01`）来分隔消息中的属性。

## 常见请求属性

以下属性在每个客户端的请求消息中都是必需的。

| 标签 | 名称 | 示例 | 描述 |
| --- | --- | --- | --- |
| 8  | BeginString  | FIX.4.2   | 必须设置为 "FIX.4.2"                             |
| 9  | BodyLength   | 162       | 消息体的长度，以字节为单位                  |
| 34 | MsgSeqNum    | 1         | 消息序列，从 1 开始，每个消息必须递增。具有重复或乱序序列号的消息将被拒绝。在新连接上会重置序列号。 |
| 35 | MsgType      | 8         | 消息类型                                         |
| 49 | SenderCompID | zyf...IZx | 客户端 API 密钥                                   |
| 50 | SenderSubID  | SPOT      | "SPOT"：现货市场；"FUTURES"：期货市场       |
| 52 | SendingTime  | 20220916-07:29:07 | 消息的发送时间                      |
| 56 | TargetCompID | BTSE      | 必须设置为 "BTSE"（用于来自客户端的消息） |
| 10 | CheckSum     | 145       | 消息的校验和                              |


## 登录 (A)

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

由客户端发送以初始化FIX会话。必须在建立连接后发送的第一条消息。每个连接只能建立一个会话；额外的登录消息将被拒绝。
客户端的API密钥和密钥可以在BTSE门户中的API页面生成。创建具有使用FIX API权限的密钥。

| 标签 | 名称 | 值 | 描述 |
| --- | --- | --- | --- |
|  35 | MsgType         | A                 |                           |
|  95 | RawDataLength   | 96                | RawData的长度         |
|  96 | RawData         | 8f7e...4783       | 出于安全原因，登录消息必须由客户端签名。要计算签名，使用API密钥，将以下字段连接在一起，用FIX字段分隔符（字节0x01）连接，并使用API密钥计算SHA384 HMAC：<br/><br/> * 发送时间 (52)<br/> * 消息类型 (35)<br/> * 消息序列号 (34)<br/> * 发送者组件标识 (49)<br/> * 目标组件标识 (56)<br/><br/>生成的哈希应以十六进制编码。 |
|  98 | EncryptMethod   | 0                 | 必须设置为 "0" (无) |
| 108 | HeartBInt       | 30                | 如果客户端将心跳间隔设置为N。我们建议您每隔N - 5秒左右发送一个心跳以保持连接活动。       |
| 141 | ResetSeqNumFlag | Y                 | 必须设置为 "Y"        |
| 5001 | ApplyNewSymbolName  | Y            | 此字段仅适用于期货。如果未提供此字段，FIX仅接受旧的符号名称。新符号模式：BTC-PERP，旧符号模式：BTCPFC |


## 心跳 (0)

如果客户端将心跳间隔设置为N。我们建议您每隔N - 5秒左右发送一个心跳以保持连接活动。

| 标签 | 名称 | 值 | 描述 |
| --- | --- | --- | --- |
|  35 | MsgType   |   0 |          |
| 112 | TestReqID | 123 | 如果此心跳是对TestRequest的响应，从TestRequest复制。 |

## 测试请求 (1)

| 标签 | 名称 | 值 | 描述 |
| --- | --- | --- | --- |
|  35 | MsgType   |   1 |          |
| 112 | TestReqID | 123 | 任意字符串，将由心跳消息回显。 |

## 注销 (5)

由任一方发送以终止会话。另一方应以另一个注销消息响应以确认会话终止。连接将在之后关闭。	
			
| 标签 | 名称    | 值 | 描述 |
| --- | ---     | --- | --- |
|  35 | MsgType | 5     |             |

## 新订单单（D）

由客户端发送以提交新订单。FIX API当前仅支持市价单和限价单。

| 标签 | 名称 | 值 | 描述                                                                                                 |
| --- | --- | --- |----------------------------------------------------------------------------------------------------|
| 35  | MsgType     | D        |                                                                                                    |
| 21  | HandlInst   | 1        | 必须设置为 "1" (AutomatedExecutionNoIntervention)                                                       |
| 11  | ClOrdID     | order123 | 任意选择的用于识别订单的客户端字符串；必须唯一                                                                            |
| 55  | Symbol      | BTC-USD  | 符号名称                                                                                               |
| 40  | OrdType     | 2        | "1": 市价; "2": 限价                                                                                   |
| 38  | OrderQty    | 1.1      | 基本单位的订单大小（在限价订单和市价卖单中必需）                                                                           |
| 44  | Price       | 18000    | 限价价格或市价买入价格（在限价订单和市价买入订单中必需）                                                                       |
| 54  | Side        | 1        | "1": 买入; "2": 卖出                                                                                   |
| 59  | TimeInForce | 1        | "1": 永久有效; "3": 立即成交或取消; "4": 填成或立刻取消; "a"=半分钟; "b"=五分钟; "c"=一小时; "d"=十二小时; "e"=一周; "f"=一个月; （限价单） |
| 18  | ExecInst    | 6        | 此参数是可选的。 "E": 仅减少， "6": 仅发布，未提供: 标准                                                                |

如果订单被接受，将返回执行报告（8），其中ExecType为：0（新建）、1（部分成交）、2（全部成交）、4（已取消）、7（已停止）、8（已拒绝）。


## 订单取消请求（F）

由客户端发送以请求取消订单。

| 标签 | 名称 | 值 | 描述 |
| --- | --- | --- | --- |
| 35  | MsgType     | F        |   |
| 37  | OrderID     | order123 | 订单的系统分配的订单ID |
| 41  | OrigClOrdID | order123 | 订单的客户分配的订单ID |
| 55  | Symbol      | BTC-USD  | 符号名称                           |

只应提供OrderID（37）或OrigClOrdID（41）中的一个。

如果订单成功取消，将返回执行报告（8）。否则，将返回订单取消拒绝（9）。


## 订单取消拒绝（9）

由服务器发送以通知客户端订单取消请求（F）失败。

| 标签 | 名称 | 值 | 描述                                                     |
| --- | --- | --- |--------------------------------------------------------|
| 35  | MsgType          | 9        |                                                        |
| 37  | OrderID          | order123 | 从OrderCancelRequest复制，如果未在OrderCancelRequest中提供，将不会显示。 |
| 41  | OrigClOrdID      | order123 | 从OrderCancelRequest复制，如果未在OrderCancelRequest中提供，将不会显示。 |
| 39  | OrdStatus        | 4        | 如果订单已取消，则为"4"（已取消）; 对订单所做的更改未成功 则为"8"（已拒绝）             |
| 102 | CxlRejReason     | 1        | "1": 未知订单, "99": 其他                                    |
| 434 | CxlRejResponseTo | 1        | 始终设置为 "1"                                              |

## 订单状态请求（H）

由服务器发送以通知客户端订单取消请求（F）失败。

| 标签 | 名称 | 值 | 描述 |
| --- | --- | --- | --- |
| 35 | MsgType     | H        |                                       |
| 37 | OrderID     | order123 | 要请求的订单的OrderID，或"*"以请求所有待处理订单 |
| 41 | OrigClOrdID | order123 | 订单的客户分配的订单ID |
| 54 | Side        | 1        | "1": 买入; "2": 卖出                   |
| 55 | Symbol      | BTC-USD  | 符号名称                           |

服务器将以所请求的订单或订单响应一个执行报告（8），ExecType=I（订单状态）。应仅提供OrderID（37）和OrigClOrdID（41）中的一个。如果同时提供OrderID（37）和OrigClOrdID（41），则仅应用OrderID（37）。当没有未完成订单时，服务器将包含Text（58）为"无未完成订单"。

## 执行报告（8）

由服务器在订单被成交，订单状态发生变化，或响应来自客户端的NewOrderSingle（D），OrderCancelRequest（F），或OrderStatusRequest（H）消息时发送。

| 标签 | 名称 | 值 | 描述 |
| --- | ---  | ---   | ---         |
| 11  | ClOrderId | order123 | 客户端选择的订单ID。 |
| 12  | Commission | 0.002 | 交易费。仅当此消息是成交的结果时才会出现 |
| 13  | CommType | 3 | 始终为3 |
| 14  | CumQty | 0.4 | 已成交的订单数量 |
| 17  | ExecID | d840c87b-ad98-47b1-95d3-4d41950fa776 | 订单ID |
| 31  | LastPx | 7999.25 | 成交价格。仅当此消息是成交的结果时才会出现 |
| 32  | LastQty | 0.4 | 成交数量。仅当此消息是成交的结果时才会出现 |
| 35  | MsgType | 8  |             |
| 37  | OrderID | d840c87b-ad98-47b1-95d3-4d41950fa776 | 订单ID |
| 38  | OrderQty | 1.2 | 原始订单数量 |
| 39  | OrdStatus | 0  | 订单状态（见下文） |
| 44  | Price | 8000 | 原始订单价格 |
| 54  | Side | 1  | "1": 买入; "2": 卖出 |
| 55  | Symbol | BTC-USD | 符号名称 |
| 58  | Text | 文本 | 拒绝订单的原因描述 |
| 60  | TransactTime | 20190525-08:26:38.989 | 订单更新的时间。仅在订单更新时出现 |
| 103  | OrdRejReason | 11 | "11": 请求失败时（UNSUPPORTED_ORDER_CHARACTERISTIC）。拒绝原因的详细信息将显示在Text（58）中 |
| 150  | ExecType | 1 | 此消息的原因（见下文） |
| 151  | LeavesQty | 0.8 | 仍然开放的订单数量 |
| 1057 | AggressorIndicator | Y | "Y": 主动成交; "N": 被动成交。仅当此消息是成交的结果时才会出现 |
| 5000 | Liquidation | Y | "Y": 消息对应于市场清算订单。 "N"或不出现：不是。 |


### ExecType值

ExecType（150）字段指示发送此ExecutionReport的原因。

| ExecType | 描述 |
| --- | ---|
| 0 | 新订单 |
| 1 | 部分成交的订单 |
| 3 | 完全成交的订单 |
| 4 | 订单已取消 |
| 5 | 订单已修改 |
| 7 | 订单退款（自成交） |
| 8 | 对拒绝的NewOrderSingle（D）请求的响应 |
| I | 对OrderStatusRequest（H）请求的响应 |

请注意，每个订单更改都会发送一个执行报告消息。

### OrdStatus值

| OrdStatus | 描述 |
| --- | --- |
| 0 | 新订单 |
| 1 | 部分成交的订单 |
| 3 | 完全成交的订单 |
| 4 | 已取消的订单 |
| 5 | 修改的订单 |
| 7 | 退款的订单 |
| 8 | 拒绝的订单 |


## 拒绝（3）

由服务器以响应无效消息发送。

| 标签 | 名称 | 值 | 描述 |
| --- | ---  | ---   | ---         |
| 35  | MsgType             | 3                |                                         |
| 45  | RefSeqNum           | 2                | 被拒绝消息的序列号 |
| 371 | RefTagID            | 38               | 被拒绝字段的标签编号        |
| 372 | RefMsgType          | D                | 被拒绝消息的消息类型    |
| 58  | Text                | 缺少数量 | 可读的原因描述 |
| 373 | SessionRejectReason | 1                | 用于识别拒绝原因的代码   |
