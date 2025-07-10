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

## 版本 1.1.4 (2024年9月16日)

* 在所有API描述中更新权限相关内容

## 版本 1.1.3 (2022年3月16日)

* 增加了请求参数 [`side`](#42034b88ca)，以允许返回单边报价。

## 版本 1.1.2 (2022年1月25日)

* 更新 [`接受报价`](#a61744ae67) 以允许部分接受场外交易报价。

## 版本 1.1.1 (2021年11月24日)

* 添加了 `unsubcribe-quote` 和 `unsubscribe-quote-all` 操作代码以取消订阅场外交易报价的流。

## 版本 1.1.0 (2021年9月17日)

* 添加了 [`报价数据流`](#42034b88ca) WebSocket 主题，用于订阅场外市场的价格流。


# 概览

## 生成API密钥

在使用经过身份验证的API之前，您需要在BTSE平台上创建API密钥。要创建API密钥，您可以按照以下步骤操作：

* 使用用户名/电子邮件和密码登录到BTSE网站
* 单击右上角的“帐户”
* 选择API选项卡
* 单击“新API”按钮以创建API密钥和口令。（注意：口令只会显示一次）
* 使用您的API密钥和口令构建签名。

## 终端点

* 生产环境
  * HTTP
     * `https://api.btse.com/otc`
  * WebSocket
     * `wss://ws.btse.com/ws/otc`
* 测试环境
  * HTTP
     * `https://testapi.btse.io/otc`
  * WebSocket
     * `wss://testws.btse.io/ws/otc`

## 认证

* API密钥（request-api）
  * 参数名称：`request-api`，位置：头部。API密钥以string形式从BTSE平台获取

* API密钥（request-nonce）
  * 参数名称：`request-nonce`，位置：头部。当前时间戳的long表示

* API密钥（request-sign）
  * 参数名称：`request-sign`，位置：头部。基于以下算法生成的综合签名：Signature=HMAC.Sha384（secretkey，（urlpath + request-nonce + bodyStr））（注意：当没有数据时，bodyStr = ''）：

### 示例 1：查询行情

> **HMAC SHA384签名**

```shell
$ echo -n "/api/v1/quote1624985375123{\"orderSizeInBaseCurrency\":1,\"orderAmountInOrderCurrency\":0,\"side\":\"buy\",\"baseCurrency\":\"BTC\",\"orderCurrency\":\"USD\"}" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 8ee43810606da581fb6ce03e10370f89125c2269a64de832a55cea219795e9ae0c3df86b51afbafdd28c03b16acd1427
```


* 下单的终端点是 `https://api.btse.com/otc/api/v1/quote`
* 假设我们有以下数值：
  * request-nonce: `1624985375123`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path：`/api/v1/quote`
  * Body：`{"orderSizeInBaseCurrency":1,"orderAmountInOrderCurrency":0,"side":"buy","baseCurrency":"BTC","orderCurrency":"USD"}`
  * Encrypted Text：`"/api/v1/quote1624985375123{"orderSizeInBaseCurrency":1,"orderAmountInOrderCurrency":0,"side":"buy","baseCurrency":"BTC","orderCurrency":"USD"}"`
* 生成的签名将是：
  * request-sign: `8ee43810606da581fb6ce03e10370f89125c2269a64de832a55cea219795e9ae0c3df86b51afbafdd28c03b16acd1427`


## 速率限制

* 实施以下速率限制：

BTSE的速率限制如下：

* 每个API：`每秒15个请求`
* 每个用户：`每秒30个请求`

## API状态代码

每个API将返回以下HTTP状态之一：

* 200 - API请求成功，有关预期的有效载荷，请参考特定的API响应
* 400 - 错误请求。服务器将不会处理此请求。通常是由于请求中发送了无效参数
* 401 - 未经授权的请求。服务器不会处理此请求，因为它没有有效的身份验证凭据
* 403 - 禁止请求。提供了凭据，但不足以执行请求
* 404 - 未找到。表示服务器理解请求，但无法找到目标资源的正确表示
* 405 - 不允许的方法。表示请求方法对请求的服务器不知道
* 408 - 请求超时。表示服务器未完成请求。BTSE API的超时设置为30秒
* 429 - 请求太多。表示客户端已超过服务器设置的速率限制。有关更多详细信息，请参考速率限制
* 500 - 内部服务器错误。表示服务器遇到意外条件，导致无法完成请求

## API ENUM

连接到BTSE API时，您将遇到代表BTSE中不同状态或状态类型的数字代码。以下部分提供了您可能看到的代码列表。

* 30000: OTC订单查询
* 30001: OTC订单报价
* 30007: OTC订单完成成功
* 30008: OTC订单重新报价

# 工作流程

* 请求报价以从BTSE获取OTC报价
* BTSE根据请求响应报价
* 如果用户选择接受报价，则将报价发送给BTSE（已接受的报价）
* 如果BTSE接受了报价，则交易完成（交易已完成）
* 如果BTSE拒绝了报价，则BTSE将以拒绝原因响应的更新报价
* 如果用户拒绝了报价，BTSE将响应报价是否成功被拒绝（已拒绝的报价）

# OTC终端点

## 市场摘要

> 响应

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

获取OTC市场信息

### 响应内容
| 名称                   | 类型          | 是否必须      | 描述                        |
| ---                    | ---           | ---      | ---                        |
| assetName              | String        | Yes       | 资产名称                    |
| maxOrderSizes          | Double    | Yes       | 最大订单大小                |
| maxOrderValues         | Double    | Yes       | 最大订单名义价值            |
| minOrderSizes          | Double    | Yes       | 最小订单大小                |
| minOrderValues         | Double    | Yes       | 最小订单名义价值            |
| supportQuoteCurrencies | String Array    | Yes       | 支持的报价货币              |

## 请求报价

> 请求

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

> 响应

```json
{
  "markets": [
    {
      "assetName": "String",
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
        "String"
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

请求报价。需要`交易`权限。

### 请求参数

| 名称                       | 类型          | 是否必须      | 描述                        |
| ---                        | ---           | ---      | ---                        |
| baseCurrency               | String        | Yes       | 基础货币 (例如 BTC)         |
| orderCurrency              | String        | Yes       | 订单货币                   |
| orderSizeInBaseCurrency    | Double    | Yes       | 基础货币中的订单大小        |
| orderAmountInOrderCurrency | Double    | Yes       | 订单货币中的订单金额        |
| clientOrderId              | Double    | Yes       | 自定义客户订单ID            |
| side                       | String        | Yes       | 订单方向，BUY或SELL         |


### 响应内容
| 名称                      | 类型    | 是否必须      | 描述                                                                                                                                                                                               |
| ---                       | ---     | ---      | ---                                                                                                                                                                                               |
| markets                   | 资产   | Yes       | 资产信息                                                                                                                                                                                          |
| quoteAmountToDeduct       | Double  | Yes       | 需要扣除的报价金额                                                                                                                                                                                |
| quoteAmountToReceive      | Double  | Yes       | 需要接收的报价金额                                                                                                                                                                                |
| quoteCurrencyToDeductIn   | String  | Yes       | 扣除的报价货币                                                                                                                                                                                    |
| quoteCurrencyToReceiveIn  | String  | Yes       | 接收的报价货币                                                                                                                                                                                    |
| quoteId                   | String  | Yes       | 报价ID                                                                                                                                                                                            |
| quotePriceInOrderCurrency | Double  | Yes       | 订单货币中的报价价格                                                                                                                                                                              |
| quotePriceInUSD           | Long  | Yes       | 报价价格 (USD)                                                                                                                                                                                   |
| quoteTimestamp            | Long  | Yes       | 报价时间戳                                                                                                                                                                                       |
| quoteValidDurationMs      | Long  | Yes       | 报价有效期                                                                                                                                                                                        |
| status                    | Integer    | Yes       | 订单状态，具有以下值：<br/>8: 余额不足<br/>30001: 订单报价<br/>30008: OTC订单重新报价<br/>30007: OTC订单已成功完成<br/>40001: 服务不可用<br/>40003: 拒绝 |

## 接受报价

> 请求

```json
{
  "quoteId": "1e5e9ec8-dfb1-****-****-99e20d476c21",
  "baseAmount": 0,
  "quoteAmount": 300
}
```

> 响应

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

接受报价。
该报价允许通过在请求体中获取 `baseAmount` 或 `quoteAmount` 来**部分接受**，
这分别对应 [`报价`](#db8afb45d1)中的 `orderSizeInBaseCurrency` 和 `orderAmountInOrderCurrency`。
请注意，如果金额大于您报价的数字，只会接受报价的数字。需要`交易`权限。

### 请求参数

| 名称          | 类型     | 是否必须     | 描述                                     |
| ------------- | -------- | -------- | ---------------------------------------- |
| quoteId       | String   | Yes       | 作为路径参数提供的报价ID                |
| baseAmount    | Double   | No       | 接受报价的部分金额                      |
| quoteAmount   | Double   | No       | 接受报价的部分金额                      |

### 响应内容


| 名称                      | 类型    | 是否必须  | 描述                                                                                                                                                                                               |
| ------------------------ | ------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| status                   | Integer | Yes       | 订单状态，其值为：<br/>8: 余额不足<br/>30001: 订单报价<br/>30008: OTC订单重新报价<br/>30007: OTC订单成功完成<br/>40001: 服务不可用<br/>40003: 被拒绝                                                   |
| quoteId                  | String  | Yes       | 报价ID                                                                                                                                                                                              |
| quoteValidDurationMs     | Long    | Yes       | 报价有效期                                                                                                                                                                                          |
| quoteAmountToReceive     | Double  | Yes       | 应收报价金额                                                                                                                                                                                        |
| quoteCurrencyToReceiveIn | String  | Yes       | 应收报价货币                                                                                                                                                                                        |
| quoteAmountToDeduct      | Double  | Yes       | 扣除的报价金额                                                                                                                                                                                      |
| quoteCurrencyToDeductIn  | String  | Yes       | 扣除的报价货币                                                                                                                                                                                      |
| quoteTimestamp           | Long    | Yes       | 报价时间戳                                                                                                                                                                                          |
| quotePriceInOrderCurrency| Double  | Yes       | 订单货币中的报价价格                                                                                                                                                                                |
| quotePriceInUSD          | Long    | Yes       | USD中的报价价格                                                                                                                                                                                     |
| side                     | String  | Yes       | BUY或SELL                                                                                                                                                                                              |


## 拒绝报价

> 响应

```json
{
  "errorCode": -1,
  "message": "String",
  "status": 0
}

```

`POST /otc/api/v1/reject/{quoteId}`

拒绝当前报价。需要`交易`权限。

### 请求参数

| 名称     | 类型   | 是否必须     | 描述                              |
| ---      | ---    | ---      | ---                             |
| quoteId  | String | Yes       | 路径参数中提供的报价 ID             |

## 查询订单

> 响应

```json
{
  "markets": [
    {
      "assetName": "String",
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
        "String"
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

查询订单信息。需要`读取`权限。

### 请求参数

| 名称     | 类型   | 是否必须     | 描述                              |
| ---      | ---    | ---      | ---                             |
| quoteId  | String | Yes       | 路径参数中提供的报价 ID             |

### 响应内容

| 名称                      | 类型    | 是否必须     | 描述                                                                                                                                                                 |
| ---                       | ---     | ---      | ---                                                                                                                                                                 |
| markets                   | 资产   | Yes       | 资产信息                                                                                                                                                             |
| quoteAmountToDeduct       | Double | Yes       | 需要扣除的报价金额                                                                                                                                                     |
| quoteAmountToReceive      | Double | Yes       | 需要接收的报价金额                                                                                                                                                     |
| quoteCurrencyToDeductIn   | String  | Yes       | 扣除的报价货币                                                                                                                                                         |
| quoteCurrencyToReceiveIn  | String  | Yes       | 接收的报价货币                                                                                                                                                         |
| quoteId                   | String  | Yes       | 报价 ID                                                                                                                                                              |
| quotePriceInOrderCurrency | Double | Yes       | 订单货币中的报价价格                                                                                                                                                     |
| quotePriceInUSD           | Long  | Yes       | 报价价格（美元）                                                                                                                                                       |
| quoteTimestamp            | Long  | Yes       | 报价时间戳                                                                                                                                                           |
| quoteValidDurationMs      | Long  | Yes       | 报价有效期                                                                                                                                                           |
| status                    | Integer   | Yes       | 具有以下值的订单状态：<br/>8: 余额不足<br/>30001: 订单报价<br/>30008: OTC 订单重新报价<br/>30007: OTC 订单成功完成<br/>40001: 服务不可用<br/>40003: 已拒绝 |

# WebSocket 数据流

## 认证

> 请求

```json
{
  "op":"authKeyExpires",
  "args":["APIKey", "nonce", "signature"]
}
```

认证 WebSocket 会话以订阅经过身份验证的 WebSocket 主题。假设我们有以下值：

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
| 0    | String | Yes       | 第一个参数是 API 密钥        |
| 1    | Long | Yes       | Nonce，即当前时间戳           |
| 2    | String | Yes       | 生成的签名                    |

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
| op        | String | Yes       | 操作，此处为 `quote`、`unsubscribe-quote` 或 `unsubscribe-quote-all`                  |
| symbol    | String | Yes       | 市场标志，参考 `getMarkets` API                                                        |
| side      | String | No       | 报价方向，`buy` 或 `sell`，区分大小写。如果此字段为空/为null，则将返回两个方向的报价  |
| clOrderId | String | No       | 客户自定义订单 ID                                                                     |
| quantity  | Double | Yes       | 订单数量                                                                             |
| currency  | String | Yes       | 可以是基础货币或报价货币。如果指定基础货币，那么报价流将以响应形式返回 |

### 响应内容

| 名称            | 类型   | 是否必须     | 描述                                                                                             |
| ---             | ---    | ---      | ---                                                                                             |
| topic           | String | Yes       | WebSocket 主题                                                                                  |
| buyQuoteId      | String | No       | 买方的报价 ID。如果该值为空/为null，则表示您的 WebSocket 流未经身份验证或您未订阅此方向  |
| sellQuoteId     | String | No       | 卖方的报价 ID。如果该值为空/为null，则表示您的 WebSocket 流未经身份验证或您未订阅此方向 |
| clOrderId       | String | Yes       | 用户自定义订单 ID                                                                               |
| buyQuantity     | Double | No       | 基于报价请求的购买数量。如果该值为null，则表示您未订阅此方向                          |
| buyUnitPrice    | Double | No       | 基础符号每单位的单价。如果该值为null，则表示您未订阅此方向                         |
| buyTotalAmount  | Double | No       | 以报价货币支付的总价格。如果该值为null，则表示您未订阅此方向                      |
| sellQuantity    | Double | No       | 基于报价请求的销售数量。如果该值为null，则表示您未订阅此方向                      |
| sellUnitPrice   | Double | No       | 基础符号每单位的单价。如果该值为null，则表示您未订阅此方向                     |
| sellTotalAmount | Double | No       | 以报价货币支付的总价格。如果该值为null，则表示您未订阅此方向                   |
| status          | String | No       | 响应状态。如果该值为null，则表示您未订阅此方向                                  |
| reason          | String | No       | 如果返回错误，reason 字段将包含错误的原因                                      |



</section>
