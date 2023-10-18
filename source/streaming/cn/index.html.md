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

# 更新日志

## 版本 1.2（2023年5月17日）

* 添加 [`Ping/Pong`](#ping-pong) 用于 WebSocket 数据流

## 版本 1.1（2022年3月16日）

* 添加请求参数 [`quote`](#42034b88ca) 以允许返回一个方向的报价。

## 版本 1.0（2021年11月19日）

* 添加 [`报价数据流`](#42034b88ca) WebSocket 主题以订阅 OTC 市场上的价格数据流


# 概述

## 生成 API 密钥

在使用经过身份验证的 API 之前，您需要在 BTSE 平台上创建一个 API 密钥。要创建 API 密钥，您可以按照以下步骤操作：

* 使用用户名/电子邮件和密码登录 BTSE 网站
* 单击右上角的“账户”
* 选择 API 选项卡
* 单击“新建 API”按钮以创建 API 密钥和密码。 (注意：密码将只出现一次)
* 使用您的 API 密钥和密码构建签名。

## 终端节点

### 流式 OTC 报价

* 生产
  * WebSocket
     * `wss://ws.btse.com/ws/otc`
* 测试网
  * WebSocket
     * `wss://testws.btse.io/ws/otc`

## 身份验证

* API 密钥（request-api）
  * 参数名称：`request-api`，位置：头部。API 密钥是从 BTSE 平台获取的string

* API 密钥（request-nonce）
  * 参数名称：`request-nonce`，位置：头部。以长格式表示的当前时间戳

* API 密钥（request-sign）
  * 参数名称：`request-sign`，位置：头部。基于以下算法生成的复合签名：Signature=HMAC.Sha384 (secretkey, (urlpath + request-nonce + bodyStr)) (注意：当没有数据时，bodyStr = ''）：

# 工作流程

## 流式 OTC

* 如果需要，通过 `市场概要` OTC API 获取市场信息。
* 订阅 `报价数据流` 以定期获取流式的 OTC 报价和报价 ID。
* 请参考 `OTC` 部分以了解接受报价的 API
  - 如果用户选择接受报价，报价将被发送到 BTSE（报价已接受）
  - 如果 BTSE 接受报价，则交易已完成（交易已完成）
  - 如果 BTSE 拒绝报价，则 BTSE 将以拒绝原因更新的报价回应


# WebSocket 数据流

## Ping/Pong
对于我们的所有 WebSocket 服务器，只需发送“ping”消息，WebSocket 服务器将在 WebSocket 连接已建立且处于活动状态时回应“pong”消息。
> 请求

```
ping
```

> 响应

```
pong
```

## 身份验证

> 请求

```json
{
  "op":"authKeyExpires",
  "args":["APIKey", "nonce", "signature"]
}
```

身份验证 WebSocket 会话以订阅经过身份验证的 WebSocket 主题。假设我们有以下值：

* `request-nonce`: 1624985375123
* `request-api`: 4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x
* `secret`: 848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx

我们的订阅请求将是：

```
{
  "op":"authKeyExpires",
  "args":["4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x", "1624985375123", "c410d38c681579adb335885800cff24c66171b7cc8376cfe43da1408c581748156b89bcc5a115bb496413bda481139fb"]
}
```

### 请求参数

下面详细说明了需要发送的参数。

| 索引 | 类型   | 是否必须     | 描述                          |
| ---  | ---    | ---      | ---                          |
| 0    | string | Yes       | 第一个参数是 API 密钥        |
| 1    | long | Yes       | Nonce，即当前时间戳           |
| 2    | string | Yes       | 生成的签名                    |

> 生成签名

```shell
echo -n "/ws/otc1624985375123"  | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= c410d38c681579adb335885800cff24c66171b7cc8376cfe43da1408c581748156b89bcc5a115bb496413bda481139fb
```

## 报价数据流

> 请求

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


> 响应

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

通过订阅 `quote` WebSocket，接收报价数据流。WebSocket 主题将不断向订阅者推送新价格。要接受报价，请使用 `/accept` API 指示买入或卖出报价 ID。

### 请求参数

| 名称      | 类型   | 是否必须     | 描述                                                                                   |
| ---       | ---    | ---      | ---                                                                                   |
| op        | string | Yes       | 操作，此处为 `quote`、`unsubscribe-quote` 或 `unsubscribe-quote-all`                  |
| symbol    | string | Yes       | 市场标志，参考 `getMarkets` API                                                        |
| side      | string | No       | 报价方向，`buy` 或 `sell`，区分大小写。如果此字段为空/为null，则将返回两个方向的报价  |
| clOrderId | string | No       | 客户自定义订单 ID                                                                     |
| quantity  | double | Yes       | 订单数量                                                                             |
| currency  | string | Yes       | 可以是基础货币或报价货币。如果指定基础货币，那么报价流将以响应形式返回 |

### 响应内容

| 名称            | 类型   | 是否必须     | 描述                                                                                             |
| ---             | ---    | ---      | ---                                                                                             |
| topic           | string | Yes       | WebSocket 主题                                                                                  |
| buyQuoteId      | string | No       | 买方的报价 ID。如果该值为空/为null，则表示您的 WebSocket 流未经身份验证或您未订阅此方向  |
| sellQuoteId     | string | No       | 卖方的报价 ID。如果该值为空/为null，则表示您的 WebSocket 流未经身份验证或您未订阅此方向 |
| clOrderId       | string | Yes       | 用户自定义订单 ID                                                                               |
| buyQuantity     | double | No       | 基于报价请求的购买数量。如果该值为null，则表示您未订阅此方向                          |
| buyUnitPrice    | double | No       | 基础符号每单位的单价。如果该值为null，则表示您未订阅此方向                         |
| buyTotalAmount  | double | No       | 以报价货币支付的总价格。如果该值为null，则表示您未订阅此方向                      |
| sellQuantity    | double | No       | 基于报价请求的销售数量。如果该值为null，则表示您未订阅此方向                      |
| sellUnitPrice   | double | No       | 基础符号每单位的单价。如果该值为null，则表示您未订阅此方向                     |
| sellTotalAmount | double | No       | 以报价货币支付的总价格。如果该值为null，则表示您未订阅此方向                   |
| status          | string | No       | 响应状态。如果该值为null，则表示您未订阅此方向                                  |
| reason          | string | No       | 如果返回错误，reason 字段将包含错误的原因                                      |


</section>
