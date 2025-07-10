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

# 更改日志

## 版本 1.0.0（2025年7月10日）

* 释出 v3.3 API。此更改将于2025年7月16日生效。

# 概述

# 从 v3.2 到 v3.3 的迁移

我们正在更新多个与订单相关的 API 接口，以提升字段的一致性与清晰度。请仔细查阅以下变更内容，部分现有字段将被弃用并由新字段取代。

### 查询订单接口字段更新 

对于以下接口，字段  `size`、`fillSize`、`originalSize` 和 `remainingSize` 将被弃用，并替换为以下字段：
  * `originalOrderBaseSize`
  * `originalOrderQuoteSize`
  * `currentOrderBaseSize`
  * `currentOrderQuoteSize`
  * `remainingOrderBaseSize`
  * `remainingOrderQuoteSize`
  * `filledBaseSize`
  * `totalFilledBaseSize`
  * `orderCurrency` (取值为 "base" 或 "quote")

**影响接口**
  * [`创建新订单`](#8be954be0d)
    * Both `POST /api/v3.3/order` and `POST /api/v3.3/order/peg`
  * [`修正订单`](#d347e421a4)
  * [`取消订单`](#3eedd32d80)

### 订单查询相关接口字段更新

为提升数据结构的清晰度与一致性，以下旧字段将被弃用：
  * `size`
  * `filledSize`
  * `remainingSize` 
  * `fillSize` （在某些接口中）

将替换为以下优化后的字段：
  * `originalOrderBaseSize`
  * `originalOrderQuoteSize`
  * `currentOrderBaseSize`
  * `currentOrderQuoteSize`
  * `remainingOrderBaseSize`
  * `remainingOrderQuoteSize`
  * `totalFilledBaseSize`
  * `orderCurrency` ("base" or "quote")

**影响接口**
  * [`查询订单`](#90376e83a0) - 替换字段： `size`、`filledSize`、`remainingSize` 
  * [`查询未完成订单`](#72485acdf4) - 替换字段： `size`、`fillSize`、`filledSize`、`remainingSize` 

## 生成API密钥

在您可以使用经过身份验证的API之前，您需要在BTSE平台上创建一个API密钥。要创建API密钥，您可以按照以下步骤操作：

* 使用您的用户名/电子邮件和密码登录到BTSE网站
* 单击右上角的账户
* 选择API选项卡
* 单击新API按钮以创建API密钥和口令。（注意：口令只会出现一次）
* 使用您的API密钥和口令来构建一个签名。

## 终端点

* 生产环境
  * HTTP
     * `https://api.btse.com/spot`
  * WebSocket
     * `wss://ws.btse.com/ws/spot`
  * WebSocket（用于订单簿数据流）
     * `wss://ws.btse.com/ws/oss/spot`（用于订单簿增量更新数据流）
* 测试网
  * HTTP
     * `https://testapi.btse.io/spot`
  * WebSocket
     * `wss://testws.btse.io/ws/spot`
  * WebSocket（用于订单簿数据流）
     * `wss://testws.btse.io/ws/oss/spot`（用于订单簿增量更新数据流）

## 身份验证

* API密钥（request-api）
  * 参数名称：`request-api`，位置：标头。API密钥以String形式从BTSE平台获取

* API密钥（request-nonce）
  * 参数名称：`request-nonce`，位置：标头。以长格式表示的当前时间戳

* API密钥（request-sign）
  * 参数名称：`request-sign`，位置：标头。基于以下算法生成的复合签名：Signature=HMAC.SHA384（secretkey，（urlpath + request-nonce + bodyStr））（注：当没有数据时，bodyStr = ''）。

### 示例1：下订单

> **HMAC SHA384签名**

```shell
$ echo -n "/api/v3.3/order1624985375123{\"postOnly\":false,\"price\":8500.0,\"side\":\"BUY\",\"size\":0.002,\"stopPrice\":0.0,\"symbol\":\"BTC-USD\",\"time_in_force\":\"GTC\",\"trailValue\":0.0,\"triggerPrice\":0.0,\"txType\":\"LIMIT\",\"type\":\"LIMIT\"}" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)=e9cd0babdf497b536d1e48bc9cf1fadad3426b36406b5747d77ae4e3cdc9ab556863f2d0cf78e0228c39a064ad43afb7
```

* 下单的终端点是 `https://api.btse.com/spot/api/v3.3/order`
* 假设我们有以下数值:
  * request-nonce: `1624985375123`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v3.3/order`
  * Body: `{"postOnly":false,"price":8500.0,"side":"BUY","size":0.002,"stopPrice":0.0,"symbol":"BTC-USD","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
  * Encrypted Text: `/api/v3.3/order1624985375123{"postOnly":false,"price":8500.0,"side":"BUY","size":0.002,"stopPrice":0.0,"symbol":"BTC-USD","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
* 生成的签名如下:
  * request-sign: `e9cd0babdf497b536d1e48bc9cf1fadad3426b36406b5747d77ae4e3cdc9ab556863f2d0cf78e0228c39a064ad43afb7`

## 速率限制

* 下列速率限制适用:

BTSE的速率限制如下:

**查询**

* 每API: `每秒15次请求`
* 每用户: `每秒30次请求`

**订单**

* 每API: `每秒75次请求`
* 每用户: `每秒75次请求`

## API状态代码

每个API将返回以下HTTP状态之一:

* 200 - API请求成功，请参考具体API响应以获取预期有效载荷
* 400 - 错误请求。服务器将不会处理此请求。通常是由于请求中发送了无效参数造成的
* 401 - 未授权请求。服务器将不会处理此请求，因为它没有有效的身份验证凭据
* 403 - 禁止请求。凭据已提供，但它们不足以执行请求
* 404 - 未找到。表示服务器理解了请求，但找不到正确的目标资源的表示
* 405 - 不允许的方法。表示请求方法对请求的服务器是未知的
* 408 - 请求超时。表示服务器未完成请求。BTSE API的超时设置为30秒
* 429 - 请求过多。表示客户端已超过服务器设置的速率限制。详细信息请参考速率限制
* 500 - 服务器内部错误。表示服务器遇到意外情况，导致无法完成请求

## API Enum

在连接BTSE API时，您将遇到代表BTSE中不同状态或状态类型的数字代码。以下部分提供了您可能会看到的代码列表。

* -1: TIMEOUT = 请求逾时，请检查订单状态
* 1: MARKET_UNAVAILABLE = 期货市场不可用
* 2: ORDER_INSERTED = 订单成功插入
* 4: ORDER_FULLY_TRANSACTED = 订单完全成交
* 5: ORDER_PARTIALLY_TRANSACTED = 订单部分成交
* 6: ORDER_CANCELLED = 订单成功取消
* 7: ORDER_REFUNDED = 订单已退款
* 8: INSUFFICIENT_BALANCE = 账户余额不足
* 9: TRIGGER_INSERTED = 触发订单成功插入
* 10: TRIGGER_ACTIVATED = 触发订单成功激活
* 11: ERROR_INVALID_CURRENCY = 无效的货币错误
* 12: ERROR_UPDATE_RISK_LIMIT = 更新风险限制出错
* 13: ERROR_INVALID_LEVERAGE = 无效的杠杆错误
* 15: ORDER_REJECTED = 订单被拒绝
* 16: ORDER_NOTFOUND = 找不到具有提供的订单ID或clOrderID的订单
* 17: REQUEST_FAILED = 无法完成请求，请检查订单状态
* 20: SUCCESS = 操作成功
* 21: FREEZE_SUCCESSFUL = 冻结成功
* 27: TRANSFER_SUCCESSFUL = 在期货和现货之间转移资金成功
* 28: TRANSFER_UNSUCCESSFUL = 在现货和期货之间转移资金失败
* 29: QUERY_GET_ORDERS = 获取订单查询
* 31: QUERY_GET_POSITIONS = 获取仓位查询
* 33: QUERY_GET_ALL_POSITIONS_ORDERS = 获取所有仓位订单查询
* 34: QUERY_WALLET = 钱包查询
* 36: QUERY_FUTURES_MARGIN = 期货保证金查询
* 41: ERROR_INVALID_RISK_LIMIT = 指定了无效的风险限制
* 51: QUERY_GET_ORDERS_WITH_LIMIT = 获取带限制的订单查询
* 64: STATUS_LIQUIDATION = 账户正在清算
* 65: STATUS_ACTIVE = 订单处于活动状态
* 66: MODE_BUY = 购买模式
* 76: ORDER_TYPE_LIMIT = 限价订单
* 77: ORDER_TYPE_MARKET = 市价订单
* 80: ORDER_TYPE_PEG = 挂单/算法订单
* 81: ORDER_TYPE_OTC = 场外交易订单
* 83: MODE_SELL = 卖出模式
* 85: STATUS_PROCESSING = 订单处于非活动状态
* 88: STATUS_INACTIVE = 订单处于非活动状态
* 101: FUTURES_ORDER_PRICE_OUTSIDE_LIQUIDATION_PRICE = 期货订单超出了清算价格
* 110: FUTURES_FUNDING = 期货资金
* 123: AMEND_ORDER = 修改订单
* 124: UNFREEZE_SUCCESSFUL = 解冻成功
* 300: ERROR_MAX_ORDER_SIZE_EXCEEDED = 超出最大订单大小错误
* 301: ERROR_INVALID_ORDER_SIZE = 无效的订单大小错误
* 302: ERROR_INVALID_ORDER_PRICE = 无效的订单价格错误
* 303: ERROR_RATE_LIMITS_EXCEEDED = 超出速率限制错误
* 304: ERROR_MAX_OPEN_ORDER_EXCEEDED = 超出最大开放订单限制
* 1003: ORDER_LIQUIDATION = 订单正在清算
* 1004: ORDER_ADL = 订单正在经历ADL
* 30410: BLOCK_TRADE_COMPLETE_SUCCESS = 区块交易完成成功


# 公共终端点

## 市场摘要

> 响应

```json
[
  {
    "symbol": "BTC-USD",
    "last": 36976,
    "lowestAsk": 37012,
    "highestBid": 36972,
    "percentageChange": -4.633438649,
    "volume": 81456627.51106991,
    "high24Hr": 39478.5,
    "low24Hr": 36821.5,
    "base": "BTC",
    "quote": "USD",
    "active": true,
    "size": 2117.88522,
    "minValidPrice": 0.01,
    "minPriceIncrement": 0.5,
    "minOrderSize": 0.00001,
    "maxOrderSize": 2000,
    "minSizeIncrement": 0.00001,
    "openInterest": 0,
    "openInterestUSD": 0,
    "contractStart": 0,
    "contractEnd": 0,
    "timeBasedContract": false,
    "openTime": 0,
    "closeTime": 0,
    "startMatching": 0,
    "inactiveTime": 0,
    "fundingRate": 0,
    "contractSize": 0,
    "maxPosition": 0,
    "minRiskLimit": 0,
    "maxRiskLimit": 0,
    "availableSettlement": null,
    "futures": false,
    "isMarketOpenToOtc": false,
    "isMarketOpenToSpot": true
  }
]
```

`GET /api/v3.3/market_summary`

获取市场摘要信息。如果没有发送symbol参数，则将检索所有市场。

### 请求参数

| 名称     | 类型     | 是否必须   | 描述     |
| -------- | -------- | ---------- | --------------- |
| symbol   | String   | No      | 市场符号   |

### 回复内容

| 名称                | 类型     | 是否必须   | 描述                                                 |
| ------------------  | -------- | ---------- | -------------                                               |
| symbol              | String   | Yes      | 市场符号                                               |
| last                | Double   | Yes      | 最后价格                                                |
| lowestAsk           | Double   | Yes      | 订单簿中的最低卖出价                            |
| highestBid          | Double   | Yes      | 订单簿中的最高买入价                            |
| percentageChange    | Double   | Yes      | 在过去24小时内与价格的百分比变化        |
| volume              | Double   | Yes      | 成交量                                                 |
| high24Hr            | Double   | Yes      | 过去24小时内的最高价格                           |
| low24Hr             | Double   | Yes      | 过去24小时内的最低价格                           |
| base                | String   | Yes      | 基础货币                                               |
| quote               | String   | Yes      | 报价货币                                               |
| active              | Boolean  | Yes      | 市场yes否活跃的指示                                 |
| size                | Double   | Yes      | 成交大小                                               |
| minValidPrice       | Double   | Yes      | 最小有效价格                                         |
| minPriceIncrement   | Double   | Yes      | 价格递增                                               |
| minOrderSize        | Double   | Yes      | 最小交易量                                             |
| minSizeIncrement    | Double   | Yes      | 交易量递增                                           |
| maxOrderSize        | Double   | Yes      | 最大订单大小                                         |
| openInterest        | Double   | No      | 不适用于现货市场                                    |
| openInterestUSD     | Double   | No      | 不适用于现货市场                                    |
| contractStart       | date     | No      | 不适用于现货市场                                    |
| contractEnd         | date     | No      | 不适用于现货市场                                    |
| timeBasedContract   | Boolean   | No      | 不适用于现货市场                                    |
| openTime            | date     | Yes      | 市场开盘时间                                         |
| closeTime           | date     | Yes      | 市场收盘时间                                         |
| startMatching       | date     | Yes      | 匹配开始时间                                         |
| inactiveTime        | date     | Yes      | 市场不活跃时间                                     |
| fundingRate         | Double   | No      | 不适用于现货市场                                    |
| contractSize        | Double   | No      | 不适用于现货市场                                    |
| maxPosition         | Double   | No      | 不适用于现货市场                                    |
| minRiskLimit        | Double   | No      | 不适用于现货市场                                    |
| maxRiskLimit        | Double   | No      | 不适用于现货市场                                    |
| availableSettlement | Array    | No      | 不适用于现货市场                                    |
| futures             | Boolean  | Yes      | 符号是否为期货合同的指示                         |
| isMarketOpenToOtc   | Boolean  | Yes        | 表示该市场是否对OTC（场外交易）开放                           |
| isMarketOpenToSpot  | Boolean  | Yes        | 表示该市场是否对现货交易开放                                  |

## 图表数据

> 响应

```json
[
  [
    1624987380,
    36477,
    36477,
    36473.5,
    36473.5,
    693.049
  ],
  [
    1624987320,
    36476.5,
    36481.5,
    36466,
    36466,
    2370.8095
  ]
]
```

`GET /api/v3.3/ohlcv`

获取蜡烛图数据。默认情况下，每次将返回300个数据点。

### 请求参数

| 名称        | 类型   | 是否必须   | 描述                                                                                                       |
| ---         | ---    | ---      | ---                                                                                                       |
| symbol      | String | Yes      | 市场符号                                                                                                 |
| start       | Long   | No      | 开始时间（毫秒）（例如：1624987283000）                                                                     |
| end         | Long   | No      | 结束时间（毫秒）（例如：1624987283000）                                                                     |
| resolution  | String | Yes      | 支持的分辨率如下：<br/> 1: 1分钟<br/> 5: 5分钟<br/> 15: 15分钟<br/>30: 30分钟<br/>60: 60分钟<br/>240: 4小时<br/>360: 6小时<br/>1440: 1天<br/>10080: 1周<br/>43200: 1月 |


### 响应内容

返回一个包含在下表中描述的索引的二维数组。

| 索引 | 类型   | 是否必须   | 描述             |
| ---  | ---    | ---      | ---             |
| 0    | Long   | Yes      | Unix 时间        |
| 1    | Double | Yes      | 开盘价           |
| 2    | Double | Yes      | 最高价           |
| 3    | Double | Yes      | 最低价           |
| 4    | Double | Yes      | 收盘价           |
| 5    | Double | Yes      | 成交量           |


## 查询市场价格

> 响应

```json
[
  {
    "symbol": "BTC-USD",
    "indexPrice": 36288.949684967,
    "lastPrice": 36286.5,
    "markPrice": 0
  }
]
```

`GET /api/v3.3/price`

获取平台上的当前价格。如果未指定市场符号，则将返回所有符号。

### 请求参数

| 名称   | 类型   | 是否必须   | 描述          |
| ---    | ---    | ---      | ---          |
| symbol | String | Yes      | 市场符号    |


### 响应内容

| Name       | 类型   | 是否必须 | Description           |
| ---        | ---    | ---      | ---                   |
| symbol     | Double | Yes      | 市场符号            |
| indexPrice | Double | Yes      | 指数价格            |
| lastPrice  | Double | Yes      | 最后成交价格      |
| markPrice  | Double | Yes      | 现货市场不适用    |

## 订单簿（按分组）

> 响应

```json
{
  "buyQuote": [
    {
      "price": "36371.0",
      "size": "0.01485"
    }
  ],
  "sellQuote": [
    {
      "price": "36380.5",
      "size": "0.01782"
    }
  ],
  "timestamp": 1624989459489,
  "symbol": "BTC-USD"
}
```

`GET /api/v3.3/orderbook`

检索订单簿的二级快照，允许您指定分组以及竞标/询价深度

### 请求参数

| 名称       | 类型    | 是否必须   | 描述                                                                                                                                                                                                                                                                 |
| ---        | ---     | ---      |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol     | String  | Yes      | 市场符号                                                                                                                                                                                                                                                          |
| group      | Integer    | No      | 订单簿分组。有效值为：<br/>0-8，其中0表示0级分组（例如，对于BTC，它将是0.1）<br/>BTC的一级分组为0.5<br/>BTC的一级分组为1<br/>  |
| limit_bids | Integer    | No      | 竞标方的订单簿深度                                                                                                                                                                                                                                                   |
| limit_asks | Integer    | No      | 询价方的订单簿深度                                                                                                                                                                                                                                                   |

### 响应内容

#### 订单簿

| 名称      | 类型   | 是否必须   | 描述            |
| ---       | ---    | ---      | ---            |
| symbol    | String | Yes      | 市场符号      |
| buyQuote  | Quote  | Yes      | 竞买报价array  |
| sellQuote | Quote  | Yes      | 竞卖报价array  |
| timestamp | Double | Yes      | 订单簿时间戳 |

#### 报价

| 名称  | 类型   | 是否必须   | 描述         |
| ---   | ---    | ---      | ---         |
| price | Double | Yes      | 订单价格   |
| size  | Double | Yes      | 订单大小   |


## 订单簿

> 响应

```json
{
  "buyQuote": [
    {
      "price": "36235.0",
      "size": "7.67500"
    }
  ],
  "sellQuote": [
    {
      "price": "36241.5",
      "size": "0.60200"
    }
  ],
  "timestamp": 1624989977940,
  "symbol": "BTC-USD"
}
```

`GET /api/v3.3/orderbook/L2`

检索订单簿的二级快照

### 请求参数

| 名称   | 类型    | 是否必须   | 描述             |
| ---    | ---     | ---      | ---             |
| symbol | String  | Yes      | 市场符号       |
| depth  | Integer    | No      | 订单簿深度   |

### 响应内容

#### 订单簿

| 名称      | 类型   | 是否必须   | 描述            |
| ---       | ---    | ---      | ---            |
| symbol    | String | Yes      | 市场符号      |
| buyQuote  | Quote  | Yes      | 竞买报价array  |
| sellQuote | Quote  | Yes      | 竞卖报价array  |
| timestamp | Double | Yes      | 订单簿时间戳 |

#### 报价

| 名称  | 类型   | 是否必须   | 描述         |
| ---   | ---    | ---      | ---         |
| price | Double | Yes      | 订单价格   |
| size  | Double | Yes      | 订单大小   |


## 查询交易成交

> 响应

```json
[
  {
    "price": 36164,
    "size": 0.035,
    "side": "SELL",
    "symbol": "BTC-USD",
    "serialId": 85997835,
    "timestamp": 1624990097000
  }
]
```

`GET /api/v3.3/trades`

获取指定`symbol`市场的交易成交。

### 请求参数

| 名称       | 类型     | 是否必须  | 描述                               |
| ---       | ---     | ---      | ---                                |
| symbol    | String  | Yes      | 市场符号                            |
| startTime | Long    | No       | 开始时间（毫秒）（例如，1624987283000）|
| endTime   | Long    | No       | 结束时间（毫秒）（例如，1624987283000）|
| count     | Integer | No       | 要返回的记录数                       |

* 成交紀錄最大天数

| 时间区间             | 最大天数     | 说明                                                  |
| :---:               | ---:        | :---:                                                |
| startTime / endTime | 30          | 在指定区间中最多**30**天记录                            |
| startTime /    -    | 3           | 未指定**结束时间**, 则从**开始时间**往后**3**天           |
|      -    / endTime | 3           | 未指定**开始时间**, 则从**结束时间**往前**3**天           |
|      -    /    -    | 3           | 都未指定时间, 则使用**当前时间**作为**结束时间**往前**3**天 |

### 响应内容

| 名称       | 类型    | 是否必须   | 描述                              |
| ---       | ---     | ---      | ---                               |
| symbol    | String  | Yes      | 市场符号                           |
| side      | String  | Yes      | 交易方向。可选值为：[`BUY`, `SELL`]  |
| price     | Double  | Yes      | 成交价格                           |
| size      | Double  | Yes      | 成交大小                           |
| serialId  | Double  | Yes      | 流水号，递增的序列号                 |
| timestamp | Double  | Yes      | 成交时间戳                         |


## 查询服务器时间

> 响应

```json
{
  "iso": "2021-06-29T18:14:30.886Z",
  "epoch": 1624990470
}
```

`GET /api/v3.3/time`

获取服务器时间

### 响应内容

| 名称  | 类型 | 是否必须   | 描述                              |
| ---   | ---  | ---      | ---                              |
| iso   | Long | Yes      | 以YYYY-MM-DDTHH24:MI:SS.Z格式的时间 |
| epoch | Long | Yes      | 返回的纪元时间戳


# 交易端点

## 创建新订单

> 请求（创建`MARKET`订单）

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "side": "BUY",
  "type": "MARKET"
}
```

> 请求（创建`MARKET STOP`订单）

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "side": "BUY",
  "type": "MARKET",
  "txType": "Stop",
  "triggerPrice": 32000
}
```

> 请求（创建`LIMIT`订单）

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "price": 34000,
  "side": "BUY",
  "type": "LIMIT"
}
```

> 请求（创建`LIMIT STOP`订单）

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "price": 34000,
  "side": "BUY",
  "type": "LIMIT",
  "txType": "Stop",
  "triggerPrice": 32000
}
```

> 请求（创建`OCO`订单）

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "price": 24000,
  "side": "BUY",
  "type": "OCO",
  "txType": "LIMIT",
  "stopPrice": 40010,
  "triggerPrice": 40000
}
```

> 请求（创建`PEG`订单）

```json
{
  "symbol": "BTC-USD",
  "size": 10,
  "price": 25000,
  "side": "BUY",
  "type": "PEG",
  "deviation": -10,
  "stealth": 10
}
```

> 响应（通用）

```json
[
  {
    "status": 2,
    "symbol": "BTC-USD",
    "orderType": 80,
    "price": 22062.5,
    "side": "BUY",
    "orderID": "990db9b6-2ed4-4c68-b46e-827c88cc3884",
    "timestamp": 1660208800123,
    "triggerPrice": 0.0,
    "stopPrice": null,
    "trigger": false,
    "message": "",
    "avgFilledPrice": 0.0,
    "clOrderID": null,
    "stealth": 0.1,
    "deviation": -0.1,
    "postOnly": false,
    "time_in_force": "GTC",
    "originalOrderBaseSize":10,
    "originalOrderQuoteSize":null,
    "currentOrderBaseSize":10,
    "currentOrderQuoteSize":null,
    "filledBaseSize":0,
    "totalFilledBaseSize":0,
    "remainingBaseSize":10,
    "remainingQuoteSize":null,
    "orderCurrency":"base"
  }
]
```

> 响应（用于`OCO`订单）

```json
[
    {
        "status": 2,
        "symbol": "BTC-USD",
        "orderType": 76,
        "price": 24000.0,
        "side": "BUY",
        "orderID": "2b672b4b-77c1-4abf-ba30-df3e82a147b0",
        "timestamp": 1660211562864,
        "triggerPrice": 0.0,
        "stopPrice": null,
        "trigger": false,
        "message": "",
        "avgFilledPrice": 0.0,
        "clOrderID": null,
        "stealth": 1.0,
        "deviation": 1.0,
        "postOnly": false,
        "time_in_force": "GTC",
        "originalOrderBaseSize":10,
        "originalOrderQuoteSize":null,
        "currentOrderBaseSize":10,
        "currentOrderQuoteSize":null,
        "filledBaseSize":0,
        "totalFilledBaseSize":0,
        "remainingBaseSize":10,
        "remainingQuoteSize":null,
        "orderCurrency":"base"
    },
    {
        "status": 9,
        "symbol": "BTC-USD",
        "orderType": 76,
        "price": 40010.0,
        "side": "BUY",
        "orderID": "7ccf5398-fddd-4d07-a89c-a4f2e72b64ce",
        "timestamp": 1660211562864,
        "triggerPrice": 40000.0,
        "stopPrice": null,
        "trigger": true,
        "message": "",
        "avgFilledPrice": 0.0,
        "clOrderID": null,
        "stealth": 1.0,
        "deviation": 1.0,
        "postOnly": false,
        "time_in_force": "GTC",
        "originalOrderBaseSize":10,
        "originalOrderQuoteSize":null,
        "currentOrderBaseSize":10,
        "currentOrderQuoteSize":null,
        "filledBaseSize":0,
        "totalFilledBaseSize":0,
        "remainingBaseSize":10,
        "remainingQuoteSize":null,
        "orderCurrency":"base"
    }
]
```

`POST /api/v3.3/order` or `POST /api/v3.3/order/peg` （这两个端点的工作方式相同）

创建新订单。需要具有`交易`权限。请注意，指数订单仅支持 USD 报价。

### 请求参数

| 名称          | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                                                                        |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                                                                        |
| symbol        | String  | Yes      | 市场标志                                                                                                                                                                                                                                                                                                                                                 |
| price         | Double  | No      | 创建 MARKET 订单时除外。卖单的最低价格，这是用户愿意卖出的最低价格。买单的最高价格，这是用户愿意买入的最高价格。                                                                                                                                                                                                                    |
| size          | Double  | Yes      | 订单大小                                                                                                                                                                                                                                                                                                                                                  |
| side          | String  | Yes      | 'BUY' 或 'SELL'                                                                                                                                                                                                                                                                                                                                         |
| time_in_force | String  | No      | 订单的时间有效性<br/>GTC：有效直到取消<br/>IOC：立即取消<br/>FOK：全部成交或取消<br/>HALFMIN：订单有效时间为30秒<br/>FIVEMIN：订单有效时间为5分钟<br/>HOUR：订单有效时间为1小时<br/>TWELVEHOUR：订单有效时间为12小时<br/>DAY：订单有效时间为1天<br/>WEEK：订单有效时间为1周<br/>MONTH：订单有效时间为1个月 |
| type          | String  | Yes      | 订单类型<br/>LIMIT：限价订单<br/>MARKET：市价订单<br/>OCO：一边成交后取消另一边<br/>PEG：价格根据指数价格偏差而定                                                                                                                                                                                        |
| txType        | String  | No      | 用于止损单或触发单<br/>STOP：止损单，'triggerPrice' 为必须项<br/>TRIGGER：触发单，'triggerPrice' 为必须项<br/>LIMIT：默认，当不是止损单或触发单时使用                                                                                                                                                  |
| stopPrice     | Double  | No      | 创建OCO订单时为必须项。表示触发价格                                                                                                                                                                                                                                                                                                    |
| triggerPrice  | Double  | No      | 创建止损单、触发单或OCO订单时为必须项。表示触发价格                                                                                                                                                                                                                                                                                                  |
| trailValue    | Double  | No      | 跟踪值                                                                                                                                                                                                                                                                                                                                                  |
| postOnly      | Boolean    | No      | Boolean，指示是否为仅限挂单。对于仅限挂单，交易员将支付挂单方的费用                                                                                                                                                                                                                                                                     |
| clOrderID     | String  | No      | 自定义订单ID                                                                                                                                                                                                                                                                                                                                            |
| stealth       | Double  | No      | 创建 PEG 订单时为是否必须项。要在订单簿上显示多少百分比的订单。                                                                                                                                                                                                                                                                                               |
| deviation     | Double  | No      | 适用于 PEG 订单。订单价格应与指数价格相差多少。该值以百分比表示，范围从 -10 到 10                                                                                                                                                                                                                                                                      |


### 响应内容

| 名称             | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                         |
| ---              | ---     | ---      | ---                                                                                                                                                                                                                                                                                         |
| symbol           | String  | Yes      | 市场标志                                                                                                                                                                                                                                                                                   |
| clOrderID        | String  | Yes      | 由交易员发送的客户标签                                                                                                                                                                                                                                                                      |
| orderID          | String  | Yes      | 订单ID                                                                                                                                                                                                                                                                                      |
| orderType        | Integer    | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: 挂单/算法订单                                                                                                                                                                                                                      |
| postOnly         | Boolean    | Yes      | 指示是否为仅限挂单的标志                                                                                                                                                                                                                                                              |
| price            | Double  | Yes      | 订单价格                                                                                                                                                                                                                                                                                   |
| side             | String  | Yes      | 订单方向<br/>BUY 或 SELL                                                                                                                                                                                                                                                                   |
| status           | Integer    | Yes      | 订单状态<br/>2: 订单已插入<br/>4: 订单已完全成交<br/>5: 订单部分成交<br/>6: 订单已取消<br/>7: 订单已退款<br/>8: 余额不足<br/>9: 触发已插入<br>10: 触发已激活<br>15: 订单已拒绝<br>16: 订单未找到<br>17: 请求失败 |
| stopPrice        | Double  | Yes      | 止损价格                                                                                                                                                                                                                                                                                   |
| time_in_force    | String  | Yes      | 订单有效性                                                                                                                                                                                                                                                                                 |
| timestamp        | Long  | Yes      | 订单时间戳                                                                                                                                                                                                                                                                                |
| trigger          | Boolean    | Yes      | 指示订单是否为触发订单的标志                                                                                                                                                                                                                                                         |
| triggerPrice     | Double  | Yes      | 订单触发价格，如果订单不是触发订单，则返回0                                                                                                                                                                                                                                      |
| avgFilledPrice | Double  | Yes      | 部分成交订单的平均成交价格。返回部分成交订单的平均成交价格                                                                                                                                                                                                                                  |
| message          | String  | Yes      | 交易信息                                                                                                                                                                                                                                                                                   |
| stealth          | Double  | Yes      | 订单的隐身值                                                                                                                                                                                                                                                                             |
| deviation        | Double  | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                             |
| originalOrderBaseSize         | Double | Yes | 以基础货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| originalOrderQuoteSize        | Double | Yes | 以报价货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| currentOrderBaseSize          | Double | Yes | 以基础货币计算的当前订单数量。表示已成交数量与剩余未成交数量的总和 |
| currentOrderQuoteSize         | Double | Yes | 以报价货币计算的当前订单数量，表示已成交数量与剩余未成交数量的总和 |
| remainingOrderBaseSize        | Double | Yes | 以基础货币计算的剩余订单数量 = 当前订单基础货币数量 - 已成交的基础货币数量 |
| remainingOrderQuoteSize       | Double | Yes | 以报价货币计算的剩余订单数量 = 当前订单报价货币数量 - 已成交的报价货币数量 |
| filledBaseSize                | Double | Yes | 订单中已成交的基础货币数量 |
| totalFilledBaseSize           | Double | Yes | 此订单以基础货币计算的累计成交数量 |
| orderCurrency                 | Double | Yes | "base" 或 "quote" |

## 查询订单

`GET /api/v3.3/order`

查询指定 orderID/clOrderID 的订单详情，仅适用于未结订单及取消时间在30分钟内的已取消订单。
请注意，该 API 需要具备`交易`权限。

> 响应

```json
{
  "orderID": "<Order UUID>",
  "symbol": "BTC-USDT",
  "quote": "USDT",
  "status": 6,
  "orderType": 76,
  "price": 30000,
  "side": "SELL",
  "orderValue": 0.300102,
  "trailValue": 0,
  "avgFilledPrice": 0,
  "clOrderID": "<Client OrderID>",
  "timeInForce": "GTC",
  "timestamp": 1697766317422,
  "pegPriceMin": 0,
  "pegPriceMax": 0,
  "pegPriceDeviation": 0,
  "triggerOrder": false,
  "triggerPrice": 0,
  "triggerOriginalPrice": 0,
  "triggerOrderType": 0,
  "triggerTrailingStopDeviation": 0,
  "triggerStopPrice": 0,
  "triggered": false,
  "originalOrderBaseSize":10,
  "originalOrderQuoteSize":null,
  "currentOrderBaseSize":10,
  "currentOrderQuoteSize":null,
  "totalFilledBaseSize":0,
  "remainingBaseSize":10,
  "remainingQuoteSize":null,
  "orderCurrency":"base"
}
```

### 请求参数

| 名称       | 类型    | 是否必须     | 描述                                                                         |
| ---       | ---    | ---      | ---                                                                             |
| orderID   | String	 | No       | 订单的唯一标识符。当未提供clOrderID时，此项为必填。如果提供了orderID，则将忽略clOrderID。 |
| clOrderID | String	 | No       | 客户自定义订单ID。当未提供orderID时，此项为必填。                                     |


### 响应内容

| 名称       | 类型    | 是否必须     | 描述                                                             |
| ---                           | ---     | ---      | ---                                            |
| orderID                       | String  | Yes      | 内部订单ID                                      |
| symbol                        | String  | Yes      | 市场交易对标识符                                   |
| quote                         | String  | Yes      | 报价货币的符号                                   |
| orderType                     | Integer | Yes      | 订单类型                                      |
| side                          | String  | Yes      | 订单方向                                      |
| price                         | Double  | Yes      | 订单价格                                      |
| orderValue                    | Double  | Yes      | 此订单的总价值                                 |
| pegPriceMin                   | Double  | Yes      | 最小可能的挂单价格，优先于挂单价格偏差             |
| pegPriceMax                   | Double  | Yes      | 最大可能的挂单价格，优先于挂单价格偏差             |
| pegPriceDeviation             | Double  | Yes      | 与指数价格的百分比偏差                          |
| timestamp                     | Long    | Yes      | 订单时间戳                                    |
| triggerOrder                  | Boolean | Yes      | 指示订单是否为触发订单                          |
| triggerPrice                  | Double  | Yes      | 订单触发价格，如果订单不是触发订单则返回0          |
| triggerOriginalPrice          | Double  | Yes      | 原始订单的价格。仅对触发订单有效                 |
| triggerOrderType              | Integer | Yes      | 订单类型                                      |
| triggerTrailingStopDeviation  | Double  | Yes      | 止损价格的百分比偏差                           |
| triggerStopPrice              | Double  | Yes      | 止损价格，仅适用于算法订单                       |
| triggered                     | Boolean | Yes      | 指示订单是否已触发                         |
| trailValue                    | Double  | Yes      | 跟踪价值                                       |
| clOrderID                     | String  | Yes      | 由交易员发送的客户标签                          |
| avgFilledPrice                | Double  | Yes      | 平均成交价格。对于部分交易的订单，返回平均成交价格 |
| originalOrderBaseSize         | Double | Yes | 以基础货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| originalOrderQuoteSize        | Double | Yes | 以报价货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| currentOrderBaseSize          | Double | Yes | 以基础货币计算的当前订单数量。表示已成交数量与剩余未成交数量的总和 |
| currentOrderQuoteSize         | Double | Yes | 以报价货币计算的当前订单数量，表示已成交数量与剩余未成交数量的总和 |
| remainingOrderBaseSize        | Double | Yes | 以基础货币计算的剩余订单数量 = 当前订单基础货币数量 - 已成交的基础货币数量 |
| remainingOrderQuoteSize       | Double | Yes | 以报价货币计算的剩余订单数量 = 当前订单报价货币数量 - 已成交的报价货币数量 |
| totalFilledBaseSize           | Double | Yes | 此订单以基础货币计算的累计成交数量 |
| orderCurrency                 | Double | Yes | "base" 或 "quote" |
| status                        | Integer | Yes      | 订单状态。请参照[`API Enum`](#api-enum)      |
| timeInForce                   | String  | Yes      | 订单有效期                                    |

## 修正订单

> 请求 (修正价格)

```json
{
  "symbol": "BTC-USD",
  "orderID": "25248336-66d8-41ff-99fd-83489c4e6029",
  "type": "PRICE",
  "value": 35000
}

```
> 请求 (修正数量)

```json
{
  "orderID": "689bf733-4879-4e32-8d1f-cb81f63d24d4",
  "type": "SIZE",
  "value": 10.05,
  "symbol": "BTC-USD"
}
```

> 请求 (修正触发价格)

```json
{
  "orderID": "cb2785b0-558e-4b30-bf1f-8a8c56174d0c",
  "type": "TRIGGERPRICE",
  "value": 40020,
  "symbol": "BTC-USD"
}
```

> 请求 (修正多个属性)

```json
{
  "symbol": "BTC-USD",
  "orderID": "cb2785b0-558e-4b30-bf1f-8a8c56174d0c",
  "type": "ALL",
  "orderPrice": 40010,
  "orderSize": 10.05,
  "triggerPrice": 40000
}
```

> 响应

```json
[
  {
    "status": 15,
    "symbol": "BTC-null",
    "orderType": 0,
    "price": 0.0,
    "side": "BUY",
    "orderID": "25248336-66d8-41ff-99fd-83489c4e6029",
    "timestamp": 1660277763249,
    "triggerPrice": 0.0,
    "stopPrice": null,
    "trigger": false,
    "message": "",
    "avgFilledPrice": 0.0,
    "clOrderID": "",
    "stealth": 0.0,
    "deviation": 0.0,
    "postOnly": false,
    "time_in_force": "GTC",
    "originalOrderBaseSize":10,
    "originalOrderQuoteSize":null,
    "currentOrderBaseSize":10,
    "currentOrderQuoteSize":null,
    "filledBaseSize":0,
    "totalFilledBaseSize":0,
    "remainingBaseSize":10,
    "remainingQuoteSize":null,
    "orderCurrency":"base"
  }
]
```

`PUT /api/v3.3/order`

修改订单的价格、大小或触发价格。对于触发订单，如果订单已经被触发，触发价格将无法进一步修改。修改订单_不适用于_算法订单。需要`交易`权限。

### 请求参数

| 名称          | 类型    | 是否必须     | 描述                        |
| ---           | ---     | ---      | ---                        |
| symbol        | String  | Yes      | 市场标识符                |
| orderID       | String  | No      | 内部订单ID。当未提供`clOrderID`时必须提供。如果提供了`orderID`，则将忽略`clOrderID`。 |
| clOrderID     | String  | No      | 自定义订单ID。当未提供`orderID`时必须提供。 |
| type          | String  | Yes      | 修改类型<br/>`PRICE`: 修改订单价格<br/>`SIZE`: 修改订单大小<br/>`TRIGGERPRICE`: 修改触发价格，仅适用于触发单。<br/>`ALL`: 修改多个字段。注意：`TRIGGERPRICE` 仅可在订单为触发单时修改，意味着如果不是触发单，请不要传入`TRIGGERPRICE`。 |
| value         | Double  | No      | 对于类型：`PRICE`、`SIZE`、`TRIGGERPRICE`，是否必须项。要修改的值。值取决于设置的类型。 |
| orderPrice    | Double  | No      | 对于类型：`ALL`，要修改的订单价格。 |
| orderSize     | Double  | No      | 对于类型：`ALL`，要修改的订单大小。 |
| triggerPrice  | Double  | No      | 对于类型：`ALL`，要修改的触发价格。 |

### 响应内容

| 名称             | 类型    | 是否必须 | 说明                                                                                                                                                                                                                                                                                         |
| ---              | ---     | ---      | ---                                                                                                                                                                                                                                                                                         |
| symbol           | String  | Yes      | 市场符号                                                                                                                                                                                                                                                                                       |
| clOrderID        | String  | Yes      | 由交易员发送的客户标签                                                                                                                                                                                                                                                                         |
| orderID          | String  | Yes      | 订单ID                                                                                                                                                                                                                                                                                        |
| orderType        | Integer | Yes      | 订单类型<br/>76: 限价单<br/>77: 市价单<br/>80: Peg/Algo订单                                                                                                                                                                                                                                 |
| postOnly         | Boolean | Yes      | 表示订单是否仅为发布订单                                                                                                                                                                                                                                                                       |
| price            | Double  | Yes      | 订单价格                                                                                                                                                                                                                                                                                     |
| side             | String  | Yes      | 订单方向<br/>BUY或SELL                                                                                                                                                                                                                                                                       |
| status           | Integer | Yes      | 订单状态<br/>2: 已插入订单<br/>4: 订单已完全成交<br/>5: 订单部分成交<br/>6: 订单已取消<br/>7: 订单已退款<br/>8: 余额不足<br/>9: 触发器已插入<br/>10: 触发器已激活<br/>15: 订单被拒绝<br/>16: 未找到订单<br/>17: 请求失败                                                                 |
| stopPrice        | Double  | Yes      | 停止价格                                                                                                                                                                                                                                                                                     |
| time_in_force    | String  | Yes      | 订单有效期                                                                                                                                                                                                                                                                                   |
| timestamp        | Long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                                   |
| trigger          | Boolean | Yes      | 指示订单是否为触发订单                                                                                                                                                                                                                                                                       |
| triggerPrice     | Double  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                                     |
| avgFilledPrice | Double  | Yes      | 平均成交价格。对于部分交易的订单，返回平均成交价格                                                                                                                                                                                                                                           |
| message          | String  | Yes      | 交易消息                                                                                                                                                                                                                                                                                      |
| stealth          | Double  | Yes      | 订单的隐身值                                                                                                                                                                                                                                                                                 |
| deviation        | Double  | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                                 |
| originalOrderBaseSize         | Double | Yes | 以基础货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| originalOrderQuoteSize        | Double | Yes | 以报价货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| currentOrderBaseSize          | Double | Yes | 以基础货币计算的当前订单数量。表示已成交数量与剩余未成交数量的总和 |
| currentOrderQuoteSize         | Double | Yes | 以报价货币计算的当前订单数量，表示已成交数量与剩余未成交数量的总和 |
| remainingOrderBaseSize        | Double | Yes | 以基础货币计算的剩余订单数量 = 当前订单基础货币数量 - 已成交的基础货币数量 |
| remainingOrderQuoteSize       | Double | Yes | 以报价货币计算的剩余订单数量 = 当前订单报价货币数量 - 已成交的报价货币数量 |
| filledBaseSize                | Double | Yes | 订单中已成交的基础货币数量 |
| totalFilledBaseSize           | Double | Yes | 此订单以基础货币计算的累计成交数量 |
| orderCurrency                 | Double | Yes | "base" 或 "quote" |


## 取消订单

> 请求

```
/api/v3.3/order?symbol=BTC-USD&clOrderID=my-order-id
```

> 响应（通用）

```json
[
  {
    "status": 6,
    "symbol": "BTC-USD",
    "orderType": 76,
    "price": 24000.0,
    "side": "BUY",
    "orderID": "9be4a6bb-bf56-4a81-a105-2a22c9629a48",
    "timestamp": 1660278598333,
    "triggerPrice": 0.0,
    "stopPrice": null,
    "trigger": false,
    "message": "",
    "avgFilledPrice": 0.0,
    "clOrderID": "jack-test-1",
    "stealth": 1.0,
    "deviation": 1.0,
    "postOnly": false,
    "time_in_force": "GTC",
    "originalOrderBaseSize":10,
    "originalOrderQuoteSize":null,
    "currentOrderBaseSize":10,
    "currentOrderQuoteSize":null,
    "filledBaseSize":0,
    "totalFilledBaseSize":0,
    "remainingBaseSize":10,
    "remainingQuoteSize":null,
    "orderCurrency":"base"
  }
]
```
> 响应（对于`OCO`订单）

```json
[
  {
    "status": 6,
    "symbol": "BTC-USD",
    "orderType": 76,
    "price": 23000.0,
    "side": "BUY",
    "orderID": "e3806536-776c-4d8f-8436-bde12a79620b",
    "timestamp": 1660286055127,
    "triggerPrice": 0.0,
    "stopPrice": null,
    "trigger": false,
    "message": "",
    "avgFilledPrice": 0.0,
    "clOrderID": "",
    "stealth": 1.0,
    "deviation": 1.0,
    "postOnly": false,
    "time_in_force": "GTC",
    "originalOrderBaseSize":10,
    "originalOrderQuoteSize":null,
    "currentOrderBaseSize":10,
    "currentOrderQuoteSize":null,
    "filledBaseSize":0,
    "totalFilledBaseSize":0,
    "remainingBaseSize":10,
    "remainingQuoteSize":null,
    "orderCurrency":"base"

  },
  {
    "status": 6,
    "symbol": "BTC-USD",
    "orderType": 76,
    "price": 0.0,
    "side": "BUY",
    "orderID": "ad4d0eeb-81a1-48f4-86c3-90436bb53718",
    "timestamp": 1660286055128,
    "triggerPrice": 40010.0,
    "stopPrice": null,
    "trigger": true,
    "message": "",
    "avgFilledPrice": 0.0,
    "clOrderID": "",
    "stealth": 1.0,
    "deviation": 1.0,
    "postOnly": false,
    "time_in_force": "GTC",
    "originalOrderBaseSize":10,
    "originalOrderQuoteSize":null,
    "currentOrderBaseSize":10,
    "currentOrderQuoteSize":null,
    "filledBaseSize":0,
    "totalFilledBaseSize":0,
    "remainingBaseSize":10,
    "remainingQuoteSize":null,
    "orderCurrency":"base"
  }
]
```

`DELETE /api/v3.3/order`

取消尚未成交的挂单。`orderID` 是用于取消特定订单的唯一标识符。`clOrderID` 是交易员发送的自定义标识。通过 `clOrderID` 进行取消时，所有具有相同ID的订单将被取消。如果没有发送 `orderID` 和 `clOrderID`，则将取消当前市场上的所有订单。需要`交易`权限。

### 请求参数

| 名称      | 类型   | 是否必须    | 描述                                                                                                                      |
| ---       | ---    | ---      | ---                                                                                                                        |
| symbol    | String | Yes      | 市场交易对的标识符                                                                                                        |
| orderID   | String | No      | 订单的唯一标识符。当未提供 `clOrderID` 时为是否必须项。如果提供了 `orderID`，`clOrderID` 将被忽略。         |
| clOrderID | String | No      | 客户自定义订单标识。当未提供 `orderID` 时为是否必须项。                                                               |

### 响应内容

| 名称               | 类型     | 是否必须    | 描述                                                                                                                                                                                                                                                                                      |
| ---                | ---      | ---      | ---                                                                                                                                                                                                                                                                                      |
| symbol             | String   | Yes      | 市场交易对的标识符                                                                                                                                                                                                                                                                       |
| clOrderID          | String   | Yes      | 交易员发送的客户标签                                                                                                                                                                                                                                                                      |
| orderID            | String   | Yes      | 订单 ID                                                                                                                                                                                                                                                                                   |
| orderType          | Integer     | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: 挂单/算法订单                                                                                                                                                                                                                     |
| postOnly           | Boolean   | Yes      | 表示订单是否为只允许挂单                                                                                                                                                                                                                                                               |
| price              | Double   | Yes      | 订单价格                                                                                                                                                                                                                                                                                 |
| side               | String   | Yes      | 订单方向<br/>BUY或SELL                                                                                                                                                                                                                                                                  |
| status             | Integer     | Yes      | 订单状态<br/>2: 订单已插入<br/>3: 订单已成交<br/>4: 订单已完全成交<br/>5: 订单已部分成交<br/>6: 订单已取消<br/>7: 订单已退款<br/>9: 触发已插入<br>10: 触发已激活<br>15: 订单已拒绝<br>16: 未找到订单<br>17: 请求失败 |
| stopPrice          | Double   | Yes      | 止损价格                                                                                                                                                                                                                                                                                  |
| time_in_force      | String   | Yes      | 订单有效期                                                                                                                                                                                                                                                                               |
| timestamp          | Long   | Yes      | 订单时间戳                                                                                                                                                                                                                                                                               |
| trigger            | Boolean   | Yes      | 表示订单是否为触发订单                                                                                                                                                                                                                                                                   |
| triggerPrice       | Double   | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                               |
| avgFilledPrice   | Double   | Yes      | 部分成交订单的平均成交价格。返回部分成交订单的平均成交价格                                                                                                                                                                                                                                   |
| message            | String   | Yes      | 交易消息                                                                                                                                                                                                                                                                                 |
| stealth            | Double   | Yes      | 订单的隐匿值                                                                                                                                                                                                                                                                             |
| deviation          | Double   | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                             |
| originalOrderBaseSize         | Double | Yes | 以基础货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| originalOrderQuoteSize        | Double | Yes | 以报价货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| currentOrderBaseSize          | Double | Yes | 以基础货币计算的当前订单数量。表示已成交数量与剩余未成交数量的总和 |
| currentOrderQuoteSize         | Double | Yes | 以报价货币计算的当前订单数量，表示已成交数量与剩余未成交数量的总和 |
| remainingOrderBaseSize        | Double | Yes | 以基础货币计算的剩余订单数量 = 当前订单基础货币数量 - 已成交的基础货币数量 |
| remainingOrderQuoteSize       | Double | Yes | 以报价货币计算的剩余订单数量 = 当前订单报价货币数量 - 已成交的报价货币数量 |
| filledBaseSize                | Double | Yes | 订单中已成交的基础货币数量 |
| totalFilledBaseSize           | Double | Yes | 此订单以基础货币计算的累计成交数量 |
| orderCurrency                 | Double | Yes | "base" 或 "quote" |

## 延时自动取消所有

> 请求

```json
{
  "timeout": 60000
}
```

`POST /api/v3.3/order/cancelAllAfter`

允许交易员发送一个超时值，这是一个订单的生存时间 (TTL) 值。通过发送另一个 `cancelAllAfter` 请求来延长超时时间。如果服务器在超时时间到达之前没有收到另一个请求，所有订单将被取消。需要`交易`权限。

### 请求参数

| 名称    | 类型  | 是否必须    | 描述                   |
| ---     | ---   | ---      | ---                   |
| timeout | Long | Yes      | 超时值（以毫秒为单位） |


### 响应内容

* 如果设置正确，将返回 HTTP 200 响应代码

## 查询未完成订单

> 响应

```json
[
  {
    "orderType": 76,
    "price": 35000.0,
    "size": 0.01,
    "side": "BUY",
    "orderValue": 350.0,
    "filledSize": 0.0,
    "pegPriceMin": 0.0,
    "pegPriceMax": 0.0,
    "pegPriceDeviation": 0.0,
    "cancelDuration": 0,
    "timestamp": 1660291619263,
    "orderID": "3c9c9c1f-8fef-43d0-82c7-ccef67435b14",
    "triggerOrder": false,
    "triggerPrice": 0.0,
    "triggerOriginalPrice": 0.0,
    "triggerOrderType": 0,
    "triggerTrailingStopDeviation": 0.0,
    "triggerStopPrice": 0.0,
    "symbol": "BTC-USD",
    "trailValue": 0.0,
    "avgFilledPrice": 0.0,
    "fillSize": 0.0,
    "clOrderID": "_yndef1660291619198",
    "orderState": "STATUS_ACTIVE",
    "timeInForce": "GTC",
    "triggered": false
  }
]
```

`GET /api/v3.3/user/open_orders`

检索尚未匹配或最近匹配的未完成订单。需要`交易`权限。

### 请求参数

| 名称      | 类型   | 是否必须    | 描述                                                                         |
| ---       | ---    | ---      | ---                                                                         |
| symbol    | String | No      | 市场交易对标识符                                                           |
| orderID   | String | No      | 使用内部订单ID进行查询                                                     |
| clOrderID | String | No      | 使用自定义订单ID进行查询。如果提供了`orderID`，将忽略`clOrderID`。       |


### 响应内容

| 名称                       | 类型   | 是否必须    | 描述                                                                                   |
| ---                          | ---    | ---      | ---                                                                                     |
| orderType                  | Integer   | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: 挂单/算法订单                  |
| price                      | Double | Yes      | 订单价格                                                                               |
| side                       | String | Yes      | 订单方向<br/>`BUY` 或 `SELL`                                                        |
| orderValue                 | Double | Yes      | 该订单的总价值                                                                         |
| pegPriceMin                | Double | Yes      | 最小可能的挂单价格，优先于挂单价格偏差                                               |
| pegPriceMax                | Double | Yes      | 最大可能的挂单价格，优先于挂单价格偏差                                               |
| pegPriceDeviation          | Double | Yes      | 与指数价格的百分比偏差                                                              |
| cancelDuration             | Double | Yes      | 如果不为0，则为订单过期时间                                                           |
| timestamp                  | Long | Yes      | 下单时间                                                                              |
| orderID                    | String | Yes      | 订单ID                                                                               |
| triggerOrder               | Boolean | Yes      | 指示订单是否为触发订单                                                               |
| triggerPrice               | Double | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                          |
| triggerOriginalPrice       | Double | Yes      | 原始订单的价格。仅对触发订单有效                                                     |
| triggerOrderType           | Double | Yes      | 订单类型 <br/>`76: 限价订单`<br/>`77: 市价订单`<br/>`80: 挂单/算法订单`            |
| triggerTrailingStopDeviation | Double | Yes      | 止损价格的百分比偏差                                                               |
| triggerStopPrice           | Double | Yes      | 止损价格，仅适用于算法订单                                                          |
| symbol                     | String | Yes      | 市场名称（例如，BTC-USD）                                                           |
| trailValue                 | Double | Yes      | 跟踪价值                                                                               |
| avgFilledPrice           | Double | Yes      | 平均成交价格。仅适用于部分成交订单                                                   |
| clOrderID                  | String | Yes      | 客户订单ID                                                                           |
| orderState                 | String | Yes      | `STATUS_ACTIVE`、`STATUS_INACTIVE`                                                      |
| timeInForce                | String | Yes      | 订单有效期                                                                           |
| triggered                  | Boolean | Yes      | 指示订单是否已触发                                                                   |
| originalOrderBaseSize         | Double | Yes | 以基础货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| originalOrderQuoteSize        | Double | Yes | 以报价货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| currentOrderBaseSize          | Double | Yes | 以基础货币计算的当前订单数量。表示已成交数量与剩余未成交数量的总和 |
| currentOrderQuoteSize         | Double | Yes | 以报价货币计算的当前订单数量，表示已成交数量与剩余未成交数量的总和 |
| remainingOrderBaseSize        | Double | Yes | 以基础货币计算的剩余订单数量 = 当前订单基础货币数量 - 已成交的基础货币数量 |
| remainingOrderQuoteSize       | Double | Yes | 以报价货币计算的剩余订单数量 = 当前订单报价货币数量 - 已成交的报价货币数量 |
| totalFilledBaseSize           | Double | Yes | 此订单以基础货币计算的累计成交数量 |
| orderCurrency                 | Double | Yes | "base" 或 "quote" |

## 查询用户交易成交

> 响应

```json
[
  {
    "tradeId": "9c6d016f-fbe3-4f82-aecc-8163e9220397",
    "orderId": "ba0b69ae-991e-494a-afcb-bfbaeb1adc55",
    "clOrderID": "_W_dmoryhbw1698118893191",
    "username": "btse",
    "side": "BUY",
    "orderType": 77,
    "triggerType": 0,
    "price": 34799.000000025,
    "size": 0.4,
    "filledPrice": 34799.000000025,
    "filledSize": 0.00001,
    "triggerPrice": 0,
    "base": "BTC",
    "quote": "USDT",
    "symbol": "BTC-USDT",
    "feeCurrency": "BTC",
    "feeAmount": 0.000000006,
    "wallet": "SPOT@",
    "realizedPnl": 0,
    "total": 0,
    "serialId": 94711228,
    "timestamp": 1698118893000,
    "avgFilledPrice": 34799.000000025
  }
]
```

`GET /api/v3.3/user/trade_history`

检索用户的交易历史，包括资金费用数据。需要`读取`权限。

### 请求参数

| 名称          | 类型    | 是否必须    | 描述                                                                                       |
| ---           | ---     | ---      | ---                                                                                       |
| symbol        | String  | Yes      | 市场交易对标识符                                                                         |
| startTime     | Long  | No      | 开始时间（以毫秒为单位，例如：1624987283000）                                             |
| endTime       | Long  | No      | 结束时间（以毫秒为单位，例如：1624987283000）                                             |
| count         | Integer    | No      | 要返回的记录数                                                                           |
| clOrderID     | String  | No      | 使用自定义订单ID查询交易历史                                                           |
| orderID       | String  | No      | 使用订单ID查询交易历史                                                                 |
| isMatchSymbol | Boolean  | No      | 精确匹配 `symbol`。如果设置为True，只匹配该标的物的记录                                |

* 交易历史纪录最大天数

| 时间区间             | 最大天数     | 说明                                                  |
| :---:               | ---:        | :---:                                                |
| startTime / endTime | 7          | 在指定区间中最多**7**天记录，若指定区间超过**7**天，则**开始时间**将设为**结束时间**的前**7**天                            |
| startTime /    -    | 7           | 未指定**结束时间**, 则从**开始时间**往后**7**天           |
|      -    / endTime | 7           | 未指定**开始时间**, 则从**结束时间**往前**7**天           |
|      -    /    -    | 7           | 都未指定时间, 则使用**当前时间**作为**结束时间**往前**7**天 |

### 响应内容

| 名称        | 类型    | 是否必须    | 描述                       |
| ---         | ---     | ---      | ---                       |
| symbol      | String  | Yes      | 市场交易对标识符         |
| side        | String  | Yes      | 交易方向。可选值：[`BUY`, `SELL`] |
| price       | Double  | Yes      | 成交价格                   |
| size        | Double  | Yes      | 原始订单数量                   |
| serialId    | Long  | Yes      | 序列ID，运行的序列号        |
| tradeId     | String  | Yes      | 交易标识符                 |
| timestamp   | Long  | Yes      | 成交时间戳                 |
| base        | Long  | Yes      | 基础货币                   |
| quote       | Long  | Yes      | 报价货币                   |
| clOrderID   | Long  | Yes      | 自定义订单ID               |
| orderId     | Long  | Yes      | 订单ID                     |
| feeAmount   | Long  | Yes      | 手续费金额                 |
| feeCurrency | Long  | Yes      | 手续费货币                 |
| filledPrice | Long  | Yes      | 成交价格                   |
| filledSize  | Long  | Yes      | 成交数量                   |
| orderType   | Integer    | Yes      | 订单类型                   |
| realizedPnl | Long  | Yes      | 在现货交易中不使用         |
| total       | Long  | Yes      | 在现货交易中不使用         |
| triggerType     | Integer| yes      | 1001: 止损 1002: 止盈       |
| triggerPrice    | Double | yes      | 触发价格                           |
| wallet          | String | yes      | SPOT@ 用于现货交易            |
| avgFilledPrice  | String | yes      | 平均成交价                     |
| username        | String | yes      | 用户名                                |

## 查询账户费用

> 响应

```json
{
  "makerfee": 0,
  "symbol": "btc-usd",
  "takerfee": 0
}
```

`GET /api/v3.3/user/fees`

检索用户的交易费用。需要`读取`权限。

### 请求参数

| 名称     | 类型     | 是否必须    | 描述                                   |
| -------- | -------- | -------- | --------------------------------------- |
| symbol   | String   | No      | 用于筛选特定市场的市场标识符         |

### 响应内容

| 名称     | 类型     | 是否必须    | 描述             |
| ---      | ---      | ---      | ---             |
| symbol   | String   | Yes      | 市场标识符     |
| makerfee | Double   | Yes      | 创造者费用     |
| takerfee | Double   | Yes      | 接收者费用     |



# 投资终端点

## 查询投资产品

> 响应

```json
[
  {
    "id": "openeth00001",
    "name": "eth flex savings",
    "currency": "eth",
    "type": "flex",
    "startdate": 1610685918000,
    "intereststartdate": 1610719200000,
    "rates":
    [
      {
        "days": 1,
        "rate": 1.15
      }
    ],
    "compounding": true,
    "autorenewsupported": false,
    "dailylimit": 10.0,
    "minsize": 1.00000000,
    "incrementalsize": 1.00000000
  }
]
```

`GET /api/v3.3/invest/products`

获取所有投资产品。需要`钱包`权限。

### 请求参数

(无)

### 响应内容

| 名称               | 类型         | 是否必须    | 描述                                      |
| ---                | ---          | ---      | ---                                      |
| id                 | String       | Yes      | 产品ID                                   |
| name               | String       | Yes      | 产品名称                                 |
| currency           | String       | Yes      | 货币类型                                 |
| type               | String       | Yes      | 产品类型                                 |
| startdate          | Long       | Yes      | 投资开始日期                             |
| intereststartdate  | Long       | Yes      | 利息开始日期                             |
| rates              | rateobject[]  | Yes      | 利率信息                                 |
| compounding        | Double       | Yes      | 是否复利                                 |
| autorenewsupported | Double       | Yes      | 是否支持自动续约                         |
| dailylimit         | Double       | Yes      | 每日投资金额限制                         |
| minsize            | Double       | Yes      | 最小投资额                               |
| incrementalsize    | Double       | Yes      | 投资递增步长                             |

### 利率对象

| 名称 | 类型    | 是否必须    | 描述              |
| ---  | ---     | ---      | ---              |
| days | Integer    | Yes      | 天数              |
| rate | Double | Yes      | 利率              |


## 存入投资

> 请求

```json
{
    "productId": "openusdt0001",
    "amount": 100.99
}
```

`POST /api/v3.3/invest/deposit`

存入一项投资。需要`钱包`权限。

### 请求参数

| 名称      | 类型    | 是否必须    | 描述                  |
| ---       | ---     | ---      | ---                  |
| productId | String  | Yes      | 投资产品ID           |
| amount    | Double  | Yes      | 投资金额             |


## 续投资

> 请求

```json
{
    "orderId": 1,
    "autoRenew": false
}
```

> 响应

```json
{
    "orderId": 1,
    "autoRenew": false
}
```

`POST /api/v3.3/invest/renew`

续投资订单。需要`钱包`权限。

### 请求参数

| 名称      | 类型    | 是否必须    | 描述                  |
| ---       | ---     | ---      | ---                  |
| orderId   | Integer    | Yes      | 投资订单ID           |
| autoRenew | Boolean  | Yes      | 自动续投标志         |

### 响应内容

| 名称      | 类型    | 是否必须    | 描述                      |
| ---       | ---     | ---      | ---                      |
| orderId   | Integer    | Yes      | 投资订单ID              |
| autoRenew | Boolean  | Yes      | 自动续投标志的状态     |


## 赎回投资

> 请求

```json
{
    "orderId": 1,
    "amount": 12.34
}
```

`POST /api/v3.3/invest/redeem`

赎回投资订单。需要`钱包`权限。

### 请求参数

| 名称    | 类型    | 是否必须    | 描述                  |
| ---     | ---     | ---      | ---                  |
| orderId | Integer    | Yes      | 投资订单ID           |
| amount  | Double  | Yes      | 赎回金额             |


## 查询投资订单

> 响应

```json
[
  {
    "id": 456,
    "name": "eth flex savings",
    "currency": "eth",
    "type": "flex",
    "rate": 1.15,
    "investamt": 10.00000000,
    "interestearned": 0.00031507,
    "nextinterestpayouttime": 1610632800000,
    "starttime": 0,
    "endtime": 0,
    "duration": 86400000,
    "payoutlocktime": 300000,
    "autorenew": false,
    "compounding": true,
    "autorenewsupported": false,
    "dailylimit": 0,
    "redemptionprocessing": false
  }
]
```

`GET /api/v3.3/invest/orders`

查询投资订单。需要`钱包`权限。

### 响应内容

| 名称                   | 类型    | 是否必须    | 描述                               |
| ---                    | ---     | ---      | ---                               |
| id                     | Integer    | Yes      | 订单ID                            |
| name                   | String  | Yes      | 产品名称                           |
| currency               | String  | Yes      | 货币类型                           |
| type                   | String  | Yes      | 产品类型                           |
| rate                   | Double  | Yes      | 利率                               |
| investment             | Double  | Yes      | 投资金额                           |
| interestearned         | Double  | Yes      | 已获得利息                         |
| nextinterestpayouttime | Integer    | Yes      | 下次利息支付时间                   |
| starttime              | Integer    | Yes      | 开始时间                           |
| endtime                | Integer    | Yes      | 结束时间                           |
| duration               | Integer    | Yes      | 期限                               |
| payoutlocktime         | Integer    | Yes      | 支付锁定时间                       |
| autorenew              | Boolean  | Yes      | 自动续投                           |
| compounding            | Boolean  | Yes      | 复利                               |
| autorenewsupported     | Boolean  | Yes      | 支持自动续投                       |
| redemptionprocessing   | Boolean  | Yes      | 赎回处理中                         |


## 查询投资历史

> 响应

```json
[
  {
    "txntime": 1598918400000,
    "name": "usdt flex savings",
    "currency": "usdt",
    "rate": 0.5,
    "type": "flex",
    "txntype": "invest_service_type_deposit",
    "amount": 100,
    "totalamount": 2000,
    "interestearned": 1.22,
    "duration": 0
  }
]
```

`GET /api/v3.3/invest/history`

查询投资历史。需要`钱包`权限。

### 响应内容

| 名称           | 类型    | 是否必须    | 描述                             |
| ---            | ---     | ---      | ---                             |
| txntime        | Integer    | Yes      | 交易时间                        |
| name           | String  | Yes      | 产品名称                        |
| currency       | String  | Yes      | 货币类型                        |
| rate           | String  | Yes      | 利率                            |
| type           | Boolean  | Yes      | 产品类型                        |
| txntype        | String  | Yes      | 交易类型                        |
| amount         | Double  | Yes      | 交易金额                        |
| totalamount    | Double  | Yes      | 投资总金额                      |
| interestearned | Double  | Yes      | 已赚得的利息                    |
| duration       | Boolean  | Yes      | 期限                            |


# 订单簿 WebSocket 流

## 终端点
  * 生产环境
     * `wss://ws.btse.com/ws/oss/spot`
  * 测试网络
     * `wss://testws.btse.io/ws/oss/spot`

## OSS L1 快照

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "snapshotL1:BTC-USD"
  ]
}

{
  "op": "unsubscribe",
  "args": [
    "snapshotL1:BTC-USD"
  ]
}
```

> 响应

```json
{
  "topic": "snapshotL1:BTC-USD",
  "data": {
    "bids": [
      [
          "28016.7",
          "1.48063"
      ]
    ],
    "asks": [
      [
          "28033.6",
          "1.34133"
      ]
    ],
    "type": "snapshotL1",
    "symbol": "BTC-USD",
    "timestamp": 1680750154232
  }
}
```

通过端点 `wss://ws.btse.com/ws/oss/spot` 订阅Level 1订单簿。订阅的格式将为 `symbol`。

* `symbol` 表示市场符号

### 响应内容

#### 订单簿对象

| 名称  | 类型        | 是否必须    | 描述                 |
| ---   | ---         | ---      | ---                 |
| topic | String      | Yes      | WebSocket 主题       |
| data  | Data Object    | Yes      | 详细数据，请参考下方数据对象 |

#### 数据对象

| 名称      | 类型         | 是否必须    | 描述            |
| ---       | ---          | ---      | ---            |
| bids      | Quote Object    | Yes      | 买盘报价        |
| asks      | Quote Object    | Yes      | 卖盘报价        |
| symbol    | String      | Yes      | 市场标识符      |
| type      | String      | Yes      | `snapshotL1` - L1 数据指的是交易对订单簿的最佳买盘/最佳卖盘。 |
| timestamp | Long      | Yes      | 订单簿时间戳    |

## 订单簿增量更新

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "update:BTC-USD_0"
  ]
}
```

```json
{
  "op": "unsubscribe",
  "args": [
    "update:BTC-USD_0"
  ]
}
```

> 响应

```json
{
  "topic": "update:BTC-USD_0",
  "data": {
    "bids": [
      [
        "59252.5",
        "0.06865"
      ],
      [
        "59249.0",
        "0.24000"
      ],
      [
        "59235.5",
        "0.16073"
      ],
      [
        "59235.0",
        "0.26626"
      ],
      [
        "59233.0",
        "0.50000"
      ]
    ],
    "asks": [
      [
        "59292.0",
        "0.50000"
      ],
      [
        "59285.5",
        "0.24000"
      ],
      [
        "59285.0",
        "0.15598"
      ],
      [
        "59282.5",
        "0.06829"
      ],
      [
        "59278.5",
        "0.01472"
      ]
    ],
    "seqNum": 628282,
    "prevSeqNum": 628281,
    "type": "snapshot",
    "timestamp": 1565135165600,
    "symbol": "BTC-USD"
  }
}
```

```json
{
  "topic": "update:BTC-USD",
  "data": {
    "bids": [],
    "asks": [
      [
        "59367.5",
        "2.15622"
      ],
      [
        "59325.5",
        "0"
      ]
    ],
    "seqNum": 628283,
    "prevSeqNum": 628282,
    "type": "delta",
    "timestamp": 1565135165600,
    "symbol": "BTC-USD"
  }
}
```

通过端点 `wss://ws.btse.com/ws/oss/spot` 订阅订单簿的增量更新。主题的格式将为 `update:symbol_grouping`（例如 `update:BTC-USD_0`）。收到的第一个响应将是当前订单簿的快照（在 `type` 字段中指示），并返回50个级别。随后的数据包将发送增量更新，其类型为 `delta`。

买单和卖单将在 `price` 和 `size` 元组中发送。发送的大小将是价格的新更新大小。如果发送了 `0` 的值，则应从订单簿的本地副本中删除该价格。

为确保按顺序接收更新，`seqNum` 表示当前序列，`prevSeqNum` 指的是之前的数据包。`seqNum` 将始终在 `prevSeqNum` 之后一个。如果序列是乱序的，您将需要取消订阅并再次重新订阅该主题。

此外，如果当最佳出价高于或等于最佳要价时发生[交叉订单簿](https://en.wikipedia.org/wiki/Order_book#Crossed_book)，请取消订阅并重新订阅该主题。

### 响应内容

#### 订单簿对象

| 名称  | 类型        | 是否必须    | 描述                 |
| ---   | ---         | ---      | ---                 |
| topic | String      | Yes      | WebSocket 主题       |
| data  | Data Object    | Yes      | 详细数据，请参考下方数据对象 |

#### 数据对象

| 名称       | 类型         | 是否必须    | 描述                                                                                                 |
| ---        | ---          | ---      | ---                                                                                                 |
| bids       | Quote Object     | Yes      | 买盘报价                                                                                            |
| asks       | Quote Object     | Yes      | 卖盘报价                                                                                            |
| seqNum     | Integer         | Yes      | 当前序列号                                                                                          |
| prevSeqNum | Integer         | Yes      | 前一个序列号                                                                                        |
| type       | String       | Yes      | `snapshot` - 最多 50 层的订单簿快照<br/> `delta` -  订单簿的更新                           |
| timestamp  | Long       | Yes      | 订单簿时间戳                                                                                        |
| symbol     | String       | Yes      | 订单簿标识符                                                                                      |

#### 订单簿错误响应

| 错误代码 | 消息                                                                                |
| ---      | ---                                                                                 |
| 1000     | 当前不支持提供的市场交易对。                                                   |
| 1001     | 当前不支持提供的操作。                                                         |
| 1002     | 无效请求。请仔细检查您的请求并提供所需的所有信息。                           |
| 1005     | 提供的主题不存在。                                                             |
| 1007     | 用户消息缓冲区已满。                                                           |
| 1008     | 达到最大失败尝试次数，正在关闭会话。                                           |

# Websocket 流

## 终端点
  * 生产环境
    * `wss://ws.btse.com/ws/spot`
  * 测试环境
    * `wss://testws.btse.io/ws/spot`

## Ping/Pong
对于我们所有的WebSocket服务器，只需发送一个'ping'消息，如果WebSocket连接已建立并处于活动状态，WebSocket服务器将回复一个'pong'消息。
> 请求

```
ping
```

> 响应

```
pong
```

## 订阅

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "tradeHistoryApi:BTC-USD"
  ]
}
```

> 响应

```json
{
  "event": "subscribe",
  "channel": [
    "tradeHistoryApi:BTC-USD"
  ]
}
```

订阅公开交易成交的Websocket

### 请求参数

| 名称   | 类型   | 是否必须     | 描述                                     |
| ---    | ---    | ---      | ---                                     |
| op     | String | Yes      | 操作。`subscribe` 将订阅提供的主题。`unsubscribe` 将取消订阅主题。 |
| args   | Array   | Yes      | 要订阅的主题。                         |

### 响应内容

| 名称    | 类型   | 是否必须     | 描述                                      |
| ---     | ---    | ---      | ---                                      |
| event   | String | Yes      | 事件类型响应。                           |
| channel | Array   | Yes      | 已成功订阅的主题。                       |




## 公共交易成交

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "tradeHistoryApi:BTC-USD"
  ]
}
```

> 响应

```json
{
  "topic": "tradeHistoryApi:BTC-USD",
  "data": [
  {
    "symbol": "BTC-USD",
    "side": "SELL",
    "size": 0.007,
    "price": 5302.8,
    "tradeId": 118974855,
    "timestamp": 1584446020295
  }
  ]
}
```

订阅市场的最近交易记录。主题将为 `tradeHistoryApi:<market>`，其中 `<market>` 是市场符号。

### 响应内容

#### 交易历史对象

| 名称  | 类型        | 是否必须     | 描述                      |
| ---   | ---         | ---      | ---                      |
| topic | String      | Yes      | WebSocket 主题            |
| data  | Data Object    | Yes      | 请参考下面的数据对象说明   |

#### 数据对象

| 名称      | 类型   | 是否必须     | 描述                   |
| ---       | ---    | ---      | ---                   |
| symbol    | String | Yes      | 市场符号               |
| side      | String | Yes      | 交易方向，BUY或SELL   |
| size      | Double | Yes      | 交易的数量             |
| price     | Double | Yes      | 交易价格               |
| tradeId   | Long | Yes      | 交易序列号             |
| timestamp | Long | Yes      | 交易时间戳             |

## 认证

> 请求

```json
{
  "op":"authKeyExpires",
  "args":["APIKey", "nonce", "signature"]
}
```

对WebSocket会话进行身份验证，以订阅经过身份验证的WebSocket主题。假设我们具有以下数值：

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

下面详细介绍了需要发送的参数。

| 索引 | 类型   | 是否必须     | 描述                                 |
| ---  | ---    | ---      | ---                                 |
| 0    | String | Yes      | 第一个参数是 API 密钥              |
| 1    | Long | Yes      | 随机数，即当前时间戳                |
| 2    | String | Yes      | 生成的签名                         |

> 生成签名

```shell
echo -n "/ws/spot1624985375123"  | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= c410d38c681579adb335885800cff24c66171b7cc8376cfe43da1408c581748156b89bcc5a115bb496413bda481139fb
```


## 通知

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "notificationApiV3"
  ]
}
```

> 响应

```json
{
  "topic": "notificationApiV3",
  "data": {
      "symbol": "Market Symbol (eg. BTC-USD)",
      "orderID": "BTSE internal order ID",
      "side": "BUY",
      "orderType": "76",
      "price": "Order price or transacted price",
      "avgFilledPrice": 35000,
      "status": "<Refer to Status description on the left>",
      "clOrderID": "<Client order ID>",
      "maker": "<Maker flag, if true indicates that trade is a maker trade>",
      "stealth": 1,
      "timestamp": 1624985375123,
      "pegPriceDeviation": "Indicate the deviation percentage. Valid for only algo orders.",
      "time_in_force": "<Time where this order is valid>",
      "txType": 0,
      "triggerPrice": "Trade Trigger Price",
      "originalOrderBaseSize":10,
      "originalOrderQuoteSize":null,
      "currentOrderBaseSize":10,
      "currentOrderQuoteSize":null,
      "filledBaseSize":0,
      "totalFilledBaseSize":0,
      "remainingBaseSize":10,
      "remainingQuoteSize":null,
      "orderCurrency":"base"
    }
}

```

通过订阅主题 `notificationApiV3` 来接收交易通知。WebSocket订阅 将向订阅者推送交易级别的通知。如果在未经身份验证的情况下订阅主题，则不会发送任何消息。

### 响应内容

| 名称              | 类型    | 是否必须     | 描述                                                         |
| ---               | ---     | ---      | ---                                                         |
| symbol            | String  | Yes      | 市场符号                                                     |
| orderID           | String  | Yes      | 内部订单ID                                                 |
| side              | String  | Yes      | 交易方向，BUY或SELL                                     |
| orderType         | Integer | Yes   | 订单类型。有效值为：<br/>76: 限价单<br/>77: 市价单<br/>80: 挂单/算法单  |
| price             | Double  | Yes      | 订单价格或交易价格                                       |
| avgFilledPrice    | Double  | Yes      | 平均成交价格                                               |
| status            | Integer    | Yes      | 状态，具体值如下：<br/>1: 市场不可用，市场目前不可用<br/>2: 订单已插入，订单已成功插入<br/>4: 订单已完全成交，订单已完全成交<br/>5: 订单已部分成交，订单已部分成交<br/>6: 订单已取消，订单已成功取消<br/>8: 余额不足，账户余额不足<br/>9: 触发订单已插入，触发订单已成功插入<br/>10: 触发订单已激活，触发订单已成功激活<br/>12: 更新风险限额出错，更新风险限额出错<br/>15: 订单修改失败，对订单的修改未成功<br/>27: 转账成功，期货和现货之间的资金转账成功<br/>28: 转账失败，现货和期货之间的资金转账未成功<br/>41: 风险限额无效，指定的风险限额无效<br/>64: 处于清算状态，账户正在进行清算<br/>101: 期货订单价格超出清算价格，期货订单价格超出了清算价格<br/>1003: 订单清算，订单正在进行清算<br/>1004: 订单ADL，订单正在进行ADL |
| clOrderID         | String  | Yes      | 自定义订单ID                                                       |
| maker             | Boolean | Yes      | 指示交易是否为做市商交易的指示器                                     |
| time_in_force     | String  | Yes      | 订单的有效性                                                      |
| timestamp         | Long    | Yes      | 订单时间戳或已成交时间戳                                           |
| txType            | Integer    | Yes      | 用于触发或OCO订单的字段。</br>0: Limit</br>1: Stop</br>2: Trigger</br>3: OCO</br>STOP 表示停止订单，TAKEPROFIT 表示止盈订单，LIMIT 表示不是上述任何一种情况。 |
| orderType         | Integer | Yes      | 用于触发或OCO订单的字段。STOP 表示停止订单，TAKEPROFIT 表示止盈订单，LIMIT 表示不是上述任何一种情况。 |
| stealth           | Double  | Yes      | 在订单簿上显示的订单的百分比。仅用于算法订单。                        |
| pegPriceDeviation | Double  | Yes      | 偏差百分比。仅用于算法订单。                                         |
| triggerPrice      | Double  | Yes      | 触发价格                                                            |
| originalOrderBaseSize         | Double | Yes | 以基础货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| originalOrderQuoteSize        | Double | Yes | 以报价货币计算的原始订单数量。即使后续进行了调整，此数值也不会改变 |
| currentOrderBaseSize          | Double | Yes | 以基础货币计算的当前订单数量。表示已成交数量与剩余未成交数量的总和 |
| currentOrderQuoteSize         | Double | Yes | 以报价货币计算的当前订单数量，表示已成交数量与剩余未成交数量的总和 |
| remainingOrderBaseSize        | Double | Yes | 以基础货币计算的剩余订单数量 = 当前订单基础货币数量 - 已成交的基础货币数量 |
| remainingOrderQuoteSize       | Double | Yes | 以报价货币计算的剩余订单数量 = 当前订单报价货币数量 - 已成交的报价货币数量 |
| filledBaseSize                | Double | Yes | 订单中已成交的基础货币数量 |
| totalFilledBaseSize           | Double | Yes | 此订单以基础货币计算的累计成交数量 |
| orderCurrency                 | Double | Yes | "base" 或 "quote" |

## 用户交易成交

> 请求

```json
{
    "op":"subscribe",
    "args":["fills"]
}

```

> 响应

```json
{
  "topic": "fills",
  "data": [{
    "orderId": "order id",
    "serialId": "serial ID after insertion into DB",
    "clOrderId": "Client Order ID",
    "type": "order type",
    "symbol": "ex: BTC-USD",
    "side": "BUY|SELL",
    "price": "filled price",
    "size": "filled size",
    "feeAmount": "Fees charged to user, value to be String on API",
    "feeCurrency": "Fee currency, eg. Buy would be BTC, Sell would be USD",
    "base": "Base currency, eg. BTC",
    "quote": "Quote currency eg. USD",
    "maker": "maker or taker",
    "timestamp": "Time trade was matched in the engine",
    "tradeId": "Trade Unique ID"
  }]
}


```

当一笔交易已经完成时，该主题将向订阅者发送交易信息。

### 响应内容

| 名称        | 类型    | 是否必须     | 描述                                                                                          |
| ---         | ---     | ---      | ---                                                                                          |
| symbol      | String  | Yes      | 市场符号                                                                                    |
| orderId     | String  | Yes      | 内部订单ID                                                                                  |
| clOrderId   | String  | Yes      | 自定义订单ID                                                                                |
| serialId    | String  | Yes      | 交易序列ID                                                                                |
| tradeId     | String  | Yes      | 交易的唯一标识符                                                                           |
| type        | Integer    | Yes      | 订单类型。有效值为：<br/>76: 限价单<br/>77: 市价单<br/>80: 挂单/算法单                |
| side        | String  | Yes      | 交易方向，BUY或SELL                                                                      |
| price       | Double  | Yes      | 成交价格                                                                                    |
| size        | Double  | Yes      | 成交数量                                                                                    |
| feeAmount   | Double  | Yes      | 手续费金额                                                                                  |
| feeCurrency | String  | Yes      | 手续费货币                                                                                  |
| base        | String  | Yes      | 基准货币                                                                                    |
| quote       | String  | Yes      | 报价货币                                                                                    |
| maker       | Boolean  | Yes      | 指示交易是否为做市商交易                                                               |
| timestamp   | Long  | Yes      | 订单时间戳或成交时间戳                                                                   |

</section>
