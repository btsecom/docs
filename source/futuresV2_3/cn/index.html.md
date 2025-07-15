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

## 版本 1.0.0（2025年7月10日）

* 释出 v2.3 API。此更改将于2025年7月16日生效。

# 概览

## 从 v2.2 到 v2.3 的迁移

我们正在更新多个与订单相关的 API 接口，以提升字段的一致性与清晰度。请仔细查阅以下变更内容，部分现有字段将被弃用并由新字段取代。

### 订单操作接口字段更新 

以下接口中，字段 `size`、`fillSize` 和 `originalSize` 将被弃用，并由以下新字段替代：

  * `originalOrderSize`
  * `currentOrderSize`
  * `filledSize`
  * `totalFilledSize`

**影响接口**

  * [`创建新订单`](#8be954be0d)
  * [`修改订单`](#89e5b08e91)
  * [`取消订单`](#3eedd32d80)
  * [`创建新的算法订单`](#a78f1cdd03)
  * [`绑定止盈/止损`](#3a59fc75d3)
  * [`平仓仓位`](#b1f6ce457c)

### 订单查询接口字段更新

以下接口中，字段 `size` 和 `filledSize` 将被弃用，并由以下新字段替代：

  * `originalOrderSize`
  * `currentOrderSize`
  * `totalFilledSize`

**影响接口**

  * [`查询订单`](#90376e83a0)
  * [`查询未完成订单`](#72485acdf4)

**通知字段更新** 

在 [`通知`](#7a66c0d036) 中, 字段 `size`、 `fillSize`和 `originalSize` 将被弃用，并由以下字段替代：

* `originalOrderSize`
* `currentOrderSize`
* `filledSize`
* `totalFilledSize`

### WebSocket 一致性优化

We 我们将同步优化 WebSocket 的订阅请求与数据通知之间的字段一致性。


## 生成 API 密钥

在使用经过身份验证的 API 之前，您需要在 BTSE 平台上创建一个 API 密钥。要创建 API 密钥，您可以按照以下步骤操作：

* 使用您的用户名/电子邮件和密码登录 BTSE 网站
* 单击右上角的“帐户”
* 选择 API 选项卡
* 单击“新 API” 按钮以创建 API 密钥和密码（注意：密码仅会显示一次）
* 使用您的 API 密钥和密码构建签名。

## 端点

* 生产环境
  * HTTP
     * `https://api.btse.com/futures`
  * Websocket
     * `wss://ws.btse.com/ws/futures`
  * Websocket（用于订单簿流）
     * `wss://ws.btse.com/ws/oss/futures`（用于订单簿增量更新流）
* 测试网络
  * HTTP
     * `https://testapi.btse.io/futures`
  * Websocket
     * `wss://testws.btse.io/ws/futures`
  * Websocket（用于订单簿流）
     * `wss://testws.btse.io/ws/oss/futures`（用于订单簿增量更新流）

## 身份验证

 * API密钥（request-api）
   * 参数名称：`request-api`，位置：标头。API密钥以字符串形式从BTSE平台获取

 * API密钥（request-nonce）
   * 参数名称：`request-nonce`，位置：标头。当前时间戳的长格式表示

 * API密钥（request-sign）
   * 参数名称：`request-sign`，位置：标头。基于以下算法生成的复合签名：Signature=HMAC.Sha384 (secretkey, (urlpath + request-nonce + bodyStr))（注意：当没有数据时，bodyStr = ''）：

### 示例 1：获取钱包

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v2.3/user/wallet1624984297330" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 2c41ab59d24d4e807ab035ef2fd4619c928320cac319751e7be2ecd03e5bf6dd31a4c85db88535bbe3e012b22d312290
```

* 获取钱包的端点是 `https://api.btse.com/futures/api/v2.3/user/wallet`
* 假设我们有以下值：
  * request-nonce: `1624984297330`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v2.3/user/wallet`
* 生成的签名将是:
  * request-sign: `2c41ab59d24d4e807ab035ef2fd4619c928320cac319751e7be2ecd03e5bf6dd31a4c85db88535bbe3e012b22d312290`

### 示例 2：下订单

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v2.3/order1624985375123{\"postOnly\":false,\"price\":8500.0,\"reduceOnly\":false,\"side\":\"BUY\",\"size\":1,\"stopPrice\":0.0,\"symbol\":\"BTC-PERP\",\"time_in_force\":\"GTC\",\"trailValue\":0.0,\"triggerPrice\":0.0,\"txType\":\"LIMIT\",\"type\":\"LIMIT\"}" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 1794da8c6090ed2d97a85f5b3bae89d7993b4f2db809da7abe24be5fb70b63fea7320b321929c4ee9e3eda083ecf837f
```

* 下订单的端点是 `https://api.btse.com/futures/api/v2.3/order`
* 假设我们有以下值：
  * request-nonce: `1624985375123`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v2.3/order`
  * Body: `{"postOnly":false,"price":8500.0,"reduceOnly":false,"side":"BUY","size":1,"stopPrice":0.0,"symbol":"BTC-PERP","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
  * Encrypted Text: `/api/v2.3/order1624985375123{"postOnly":false,"price":8500.0,"reduceOnly":false,"side":"BUY","size":1,"stopPrice":0.0,"symbol":"BTC-PERP","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
* 生成的签名将是：
  * request-sign: `1794da8c6090ed2d97a85f5b3bae89d7993b4f2db809da7abe24be5fb70b63fea7320b321929c4ee9e3eda083ecf837f`


## 速率限制

* 强制执行以下速率限制：

BTSE 的速率限制如下：

**查询**

* 每个API：每秒 `15次请求`
* 每个用户：每秒 `30次请求`

**订单**

* 每个API：每秒 `75次请求`
* 每个用户：每秒 `75次请求`

### 机制描述

我们的系统实现了一个分层封锁机制，有三个不同的封锁时长：1秒、5分钟 和 15分钟。封锁时长的计算从第一次封锁开始时算起。
此外，如果 IP 地址或用户在 1 小时内或 15 分钟的封锁时长结束后没有超过速率限制，封锁时长的计算将被重置。

在返回 429 响应时，会包含一个 Retry-After 头部，并提供解锁的时间戳。

#### 速率限制等级

* 1秒
* 5分钟
* 15分钟

## API状态代码

每个API将返回以下HTTP状态之一：

* 200 - API请求成功，参考特定API响应以获取预期的有效负载
* 400 - 错误请求。服务器不会处理此请求。通常是因为请求中包含了无效的参数
* 401 - 未经授权的请求。服务器不会处理此请求，因为它没有有效的身份验证凭据
* 403 - 禁止的请求。提供了凭据，但它们不足以执行请求
* 404 - 未找到。表示服务器理解请求但无法找到目标资源的正确表示
* 405 - 不允许的方法。表示请求方法未被请求的服务器知道
* 408 - 请求超时。表示服务器未完成请求。BTSE API的超时设置为30秒
* 429 - 请求过多。表示客户端已超过服务器设置的速率限制。有关更多详细信息，请参阅速率限制
* 451 - 基于法律原因不可用。表示客户端因异常行为而被禁止
* 500 - 服务器内部错误。表示服务器遇到意外情况，无法满足请求

## API枚举

在连接到BTSE API时，您将遇到代表BTSE中不同状态或状态类型的数字代码。以下部分提供了您预计会看到的代码列表。

* 1: MARKET_UNAVAILABLE = 期货市场不可用
* 2: ORDER_INSERTED = 订单已成功插入
* 4: ORDER_FULLY_TRANSACTED = 订单已完全交易
* 5: ORDER_PARTIALLY_TRANSACTED = 订单已部分交易
* 6: ORDER_CANCELLED = 订单已成功取消
* 7: ORDER_REFUNDED = 订单已退款
* 8: INSUFFICIENT_BALANCE = 账户余额不足
* 9: TRIGGER_INSERTED = 触发订单已成功插入
* 10: TRIGGER_ACTIVATED = 触发订单已成功激活
* 11: ERROR_INVALID_CURRENCY = 无效货币错误
* 12: ERROR_UPDATE_RISK_LIMIT = 更新风险限额时出现错误
* 13: ERROR_INVALID_LEVERAGE = 无效杠杆错误
* 15: ORDER_REJECTED = 订单被拒绝
* 16: ORDER_NOTFOUND = 未找到订单，使用提供的订单ID或clOrderID
* 17: REQUEST_FAILED = 未能完成请求，请检查订单状态
* 20: SUCCESS = 操作成功
* 21: FREEZE_SUCCESSFUL = 冻结成功
* 27: TRANSFER_SUCCESSFUL = 期货和现货之间的资金转移成功
* 28: TRANSFER_UNSUCCESSFUL = 现货和期货之间的资金转移失败
* 29: QUERY_GET_ORDERS = 查询获取订单
* 31: QUERY_GET_POSITIONS = 查询获取持仓
* 33: QUERY_GET_ALL_POSITIONS_ORDERS = 查询获取所有持仓订单
* 34: QUERY_WALLET = 查询钱包
* 36: QUERY_FUTURES_MARGIN = 查询期货保证金
* 41: ERROR_INVALID_RISK_LIMIT = 指定了无效的风险限额
* 51: QUERY_GET_ORDERS_WITH_LIMIT = 查询获取带有限制的订单
* 64: STATUS_LIQUIDATION = 帐户正在清算
* 65: STATUS_ACITVE = 订单处于活动状态
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
* 123: AMEND_ORDER = 订单已修改
* 124: UNFREEZE_SUCCESSFUL = 解冻成功
* 129: FUTURES_CONFIG_MODE_CHANGE = 期货仓位模式更改
* 131: FUTURES_STATUS_PROCESSING_LEVERAGE = 期货杠杆更改中
* 132: FUTURES_STATUS_PROCESSING_RISK_LIMIT = 风险限额更改中
* 133: FUTURES_POSITION_MODE_INVALID = 期货仓位模式错误
* 134: POSITION_MODE_UNCHANGEABLE = 无法更改期货仓位模式
* 138: POSITION_MODE_CHANGE_PROCESSING = 期货仓位模式更改中
* 300: ERROR_MAX_ORDER_SIZE_EXCEEDED = 超过最大订单大小错误
* 301: ERROR_INVALID_ORDER_SIZE = 无效订单大小错误
* 302: ERROR_INVALID_ORDER_PRICE = 无效订单价格错误
* 303: ERROR_RATE_LIMITS_EXCEEDED = 超过速率限制错误
* 304: ERROR_MAX_OPEN_ORDER_EXCEEDED = 超过最大开放订单数错误
* 305: ERROR_ORDER_PRICE_OUT_OF_PRICE_PROTECTION_RANGE = 价格超过开放订单范围
* 1003: ORDER_LIQUIDATION = 订单正在进行清算
* 1004: ORDER_ADL = 订单正在进行ADL
* 30410: BLOCK_TRADE_COMPLETE_SUCCESS = 区块交易已成功完成

## 垃圾订单

垃圾订单是指大量的小订单大小。为了确保平台和用户的利益不受恶意用户的侵害，我们将对下列情况的用户采取以下措施，这些用户下单小额订单。

[垃圾订单检测机制 : BTSE Support](https://support.btse.com/en/support/solutions/articles/43000720904-spam-order-detection-mechanism)

* 订单的名义价值低于5美元的将被标记为垃圾订单，并自动变为隐藏订单。
* 被标记为垃圾的订单始终支付吃单费。
* 被标记为垃圾的Post-Only API订单将被拒绝而不是被隐藏。
* 太多的垃圾订单可能导致暂时封禁交易账户。
* 放置 >= 4 个挂单，总大小小于 20 美元的API账户有可能被标记为垃圾账户。
* 被标记为垃圾的账户可能会对账户施加限制，包括订单速率限制、持仓限制，或禁用API功能。如对新的垃圾订单机制有疑问，请发送电子邮件至 mm@btse.com。

# 公共端点

## 市场摘要

> 响应

```json
[
  {
    "symbol": "BTC-PERP",
    "last": 36365,
    "lowestAsk": 36377,
    "highestBid": 36376,
    "percentageChange": 4.973731309,
    "volume": 172418318.7575521,
    "high24Hr": 36447,
    "low24Hr": 33989.5,
    "base": "BTC",
    "quote": "USDT",
    "active": true,
    "size": 4916.8266,
    "minValidPrice": 0.00001,
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
    "fundingIntervalMinutes": 480,
    "fundingTime": 1699347600000
  }
]
```

`GET /api/v2.3/market_summary`

获取市场摘要信息。如果未发送`symbol`参数，则将检索所有市场。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                    |
| ---                | ---     | ---      | ---                                                                    |
| symbol               | String  | No       | 市场符号                                                                |
| listFullAttributes | Boolean | No       | 为True时返回市場摘要的所有屬性， 默认为False |

### 响应内容

| 名称                | 类型    | 是否必须 | 描述                                                                                                   |
| ---                 | ---     | ---      | ---                                                                                                   |
| symbol              | String  | Yes      | 市场符号                                                                                               |
| last                | Double  | Yes      | 最新价格                                                                                               |
| lowestAsk           | Double  | Yes      | 订单簿中的最低卖价                                                                                      |
| highestBid          | Double  | Yes      | 订单簿中的最高买价                                                                                      |
| percentageChange    | Double  | Yes      | 过去24小时内相对于价格的百分比变化                                                                       |
| volume              | Double  | Yes      | 交易量                                                                                                  |
| high24Hr            | Double  | Yes      | 过去24小时的最高价格                                                                                    |
| low24Hr             | Double  | Yes      | 过去24小时的最低价格                                                                                    |
| base                | String  | Yes      | 基础货币                                                                                                |
| quote               | String  | Yes      | 报价货币                                                                                                |
| active              | Boolean | Yes      | 表示市场是否活跃的指标                                                                                   |
| size                | Double  | Yes      | 交易尺寸                                                                                                |
| minValidPrice       | Double  | Yes      | 最小有效价格                                                                                            |
| minPriceIncrement   | Double  | Yes      | 价格增量                                                                                                |
| minOrderSize        | Double  | Yes      | 最小交易尺寸                                                                                            |
| minSizeIncrement    | Double  | Yes      | 交易尺寸增量                                                                                            |
| maxOrderSize        | Double  | Yes      | 最大订单尺寸                                                                                            |
| openInterest        | Double  | No       | 期货市场的未平仓位数量                                                                                   |
| openInterestUSD     | Double  | No       | 期货市场未平仓位的美元名义值                                                                              |
| contractStart       | Long    | No       | 合同开始时间                                                                                            |
| contractEnd         | Long    | No       | 合同结束时间                                                                                            |
| timeBasedContract   | Boolean | No       | 指示是否为基于时间的合同                                                                                |
| openTime            | Long    | Yes      | 市场开放时间                                                                                            |
| closeTime           | Long    | Yes      | 市场关闭时间                                                                                            |
| startMatching       | Long    | Yes      | 匹配开始时间                                                                                            |
| inactiveTime        | Long    | Yes      | 市场不活跃时间                                                                                          |
| fundingRate         | Double  | No       | 资金费率                                                                                    |
| contractSize        | Double  | No       | 一个合同的尺寸                                                                                          |
| maxPosition         | Double  | No       | 用户允许拥有的最大头寸 `风险限额调整后将不再适用`                                                         |
| minRiskLimit        | Double  | No       | 合同大小的最小风险限额 `将更改为美元价值`                                                                 |
| maxRiskLimit        | Double  | No       | 合同大小的最大风险限额 `将更改为美元价值`                                                                 |
| availableSettlement | Array   | No       | 用于结算的可用货币                                                                                      |
| futures             | Boolean | Yes      | 符号是否为期货合同的指标                                                                                  |
| fundingIntervalMinutes             | Integer | No      | 资金费率间隔，仅在参数 listFullAttributes 为 true 时显示|
| fundingTime             | Long | No      | 下一个资金费率时间，仅在参数 listFullAttributes 为 true 时显示|

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

`GET /api/v2.3/ohlcv`

获取蜡烛图表数据。默认情况下，每次将返回300个数据点。

### 请求参数

| 名称                | 类型    | 是否必须 | 描述                                                                                                                                           |
| ---                | ---     | ---      |----------------------------------------------------------------------------------------------------------------------------------------------|
| symbol             | String  | Yes      | 市场符号                                                                                                                                         |
| start              | Long    | No       | 以毫秒为单位的开始时间 (例如 1624987283000)                                                                                                               |
| end                | Long    | No       | 以毫秒为单位的结束时间 (例如 1624987283000)                                                                                                               |
| resolution         | String  | Yes      | 支持的分辨率包括：<br/> 1: 1分钟<br/> 5: 5分钟<br/> 15: 15分钟<br/>30: 30分钟<br/>60: 60分钟<br/>240: 4小时<br/>360: 6小时<br/>1440: 1天<br/>10080: 1周<br/>43200: 1月 |


### 响应内容

返回一个包含下表描述的索引的二维数组

| 索引 | 类型    | 是否必须 | 描述       |
| ---  | ---     | ---      | ---        |
| 0    | Long    | Yes      | Unix 时间  |
| 1    | Double  | Yes      | 开盘价格   |
| 2    | Double  | Yes      | 最高价格   |
| 3    | Double  | Yes      | 最低价格   |
| 4    | Double  | Yes      | 收盘价格   |
| 5    | Double  | Yes      | 交易量     |


## 查询市场价格

> 响应

```json
[
  {
    "symbol": "BTC-PERP",
    "indexPrice": 36288.949684967,
    "lastPrice": 36286.5,
    "markPrice": 0
  }
]
```

`GET /api/v2.3/price`

检索平台上的当前价格。如果未指定符号，则将返回所有符号。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                    |
| ---                | ---     | ---      | ---                                                                     |
| symbol             | String  | Yes      | 市场符号                                                                 |

### 响应内容

| 名称       | 类型   | 是否必须 | 描述                 |
| ---        | ---    | ---      | ---                  |
| symbol     | String | Yes      | 市场符号              |
| indexPrice | Double | Yes      | 指数价格              |
| lastPrice  | Double | Yes      | 最后成交价格           |
| markPrice  | Double | Yes      | 标记价格              |

## 订单簿（按分组）

> 响应

```json
{
  "buyQuote": [
    {
      "price": "36371.0",
      "size": "100"
    }
  ],
  "sellQuote": [
    {
      "price": "36380.5",
      "size": "100"
    }
  ],
  "timestamp": 1624989459489,
  "symbol": "BTC-PERP"
}
```

`GET /api/v2.3/orderbook`

检索订单簿的快照。

### 请求参数

| 名称                | 类型    | 是否必须 | 描述                                                                                                                                                                                                                      |
| ---                 | ---     | ---      | ---                                                                                                                                                                                                                       |
| symbol             | String  | Yes      | 市场符号，作为路径变量输入                                                                                                                                                                                                |
| group              | Integer | No       | 订单簿分组。有效值为：<br/>0-8，其中0表示0级分组（例如，对于BTC-PERP，它将为0.1）<br/>BTC-PERP的1级分组为0.5<br/>BTC-PERP的2级分组为1<br/>                                                                            |

### 响应内容

#### 订单簿

| 名称       | 类型          | 是否必须 | 描述                    |
| ---       | ---           | ---      | ---                    |
| symbol    | String        | Yes      | 市场符号                |
| buyQuote  | Quote Object  | Yes      | 买入报价的数组          |
| sellQuote | Quote Object  | Yes      | 卖出报价的数组          |
| timestamp | Long          | Yes      | 订单簿的时间戳          |

#### 报价物件

| 名称   | 类型    | 是否必须 | 描述      |
| ---   | ---     | ---      | ---       |
| price | Double  | Yes      | 订单价格  |
| size  | Double  | Yes      | 订单尺寸  |


## 订单簿

> 响应

```json
{
  "buyQuote": [
    {
      "price": "36235.0",
      "size": "700"
    }
  ],
  "sellQuote": [
    {
     "price": "36241.5",
      "size": "600"
    }
  ],
  "timestamp": 1624989977940,
  "symbol": "BTC-PERP"
}
```

`GET /api/v2.3/orderbook/L2`

获取订单簿的Level 2快照

### 请求参数

| 名称                | 类型    | 是否必须 | 描述                                                                                     |
| ---                | ---     | ---      | ---                                                                                     |
| symbol             | String  | Yes      | 市场符号                                                                                 |
| depth              | Long    | No       | 订单簿深度                                                                               |

### 响应内容

#### 订单簿

| 名称       | 类型         | 是否必须 | 描述                    |
| ---       | ---          | ---      | ---                    |
| symbol    | String       | Yes      | 市场符号                |
| buyQuote  | Quote Object | Yes      | 购买报价的数组          |
| sellQuote | Quote Object | Yes      | 出售报价的数组          |
| timestamp | Long         | Yes      | 订单簿的时间戳          |

#### 报价物件

| 名称   | 类型    | 是否必须 | 描述      |
| ---   | ---     | ---      | ---       |
| price | Double  | Yes      | 订单价格  |
| size  | Double  | Yes      | 订单尺寸  |


## 查询成交记录

> 响应

```json
[
  {
    "price": 36164,
    "size": 100,
    "side": "SELL",
    "symbol": "BTC-PERP",
    "serialId": 85997835,
    "timestamp": 1624990097000
  }
]
```

`GET /api/v2.3/trades`

获取由`symbol`指定的市场的交易成交记录

### 请求参数

| 名称                | 类型    | 是否必须 | 描述                                                                                                        |
| ---                | ---     | ---      | ---                                                                                                        |
| symbol             | String  | Yes      | 市场符号                                                                                                    |
| startTime          | Long    | No       | 以毫秒为单位的开始时间 (例如 1624987283000)                                                                 |
| endTime            | Long    | No       | 以毫秒为单位的结束时间 (例如 1624987283000)                                                                 |
| beforeSerialId     | Long  | No      | 用于分页检索记录，适用于**订单量每毫秒超过500**的情况。对于大多数场景，建议使用 `startTime` 和 `endTime` 参数 |
| afterSerialId      | Long  | No      | 用于分页检索记录，适用于**订单量每毫秒超过500**的情况。对于大多数场景，建议使用 `startTime` 和 `endTime` 参数 |
| count              | Long    | Yes      | 返回的记录数                                                                                                |
| includeOld         | Boolean | Yes      | 获取过去7天的交易历史记录                                                                                   |

### 响应内容

| 名称       | 类型    | 是否必须 | 描述                                         |
| ---       | ---     | ---      | ---                                         |
| symbol    | String  | Yes      | 市场符号                                     |
| side      | String  | Yes      | 交易方向: [`BUY`, `SELL`]            |
| price     | Double  | Yes      | 交易价格                                     |
| size      | Double  | Yes      | 交易尺寸                                     |
| serialId  | Long    | Yes      | 序列ID，运行序列号                           |
| timestamp | Long    | Yes      | 交易时间戳                                   |


## 查询资金费率

> 响应

```json
{
  "BTC-PERP": [
    {
      "time": 1706515200,
      "rate": 0.000011405,
      "symbol": "BTC-PERP"
    }
  ]
}
```

`GET /api/v2.3/funding_history`

获取市场的资金费率历史

### Request Parameters

| 名称                | 类型    | 是否必须 | 描述                                                         |
| ---                | ---     | ---      | ---                                                        |
| symbol             | String  | No       | 市场符号                                                    |
| count              | Integer     | No       | 返回的记录数 (此设置与 from/to 互斥)                           |
| from               | Long    | No       | 以毫秒为单位的开始时间 (例如 1624987283000; 此设置与 count 互斥) |
| to                 | Long    | No       | 以毫秒为单位的结束时间 (例如 1624987283000; 此设置与 count 互斥) |

### Response Content

| 名称       | 类型   | 是否必须   | 描述                 |
| ---       | ---    | ---      | ---                  |
| symbol    | String | Yes      | 市场符号              |
| time      | Long   | Yes      | 以秒为单位的资金费率时间 |
| rate      | Double | Yes      | 资金费率              |

## 查询市场风险限额设置

> 响应 (成功)

```json
{
    "code": 1,
    "msg": "Success",
    "time": 1747207591721,
    "data": [
        {
            "symbol": "SOL-PERP",
            "riskLevel": 1,
            "riskLimitValue": 10000,
            "initialMarginRate": 0.02,
            "maintenanceMarginRate": 0.015,
            "maxLeverage": 50
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 2,
            "riskLimitValue": 20000,
            "initialMarginRate": 0.025,
            "maintenanceMarginRate": 0.02,
            "maxLeverage": 40
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 3,
            "riskLimitValue": 30000,
            "initialMarginRate": 0.03,
            "maintenanceMarginRate": 0.025,
            "maxLeverage": 33.33
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 4,
            "riskLimitValue": 40000,
            "initialMarginRate": 0.035,
            "maintenanceMarginRate": 0.03,
            "maxLeverage": 28.57
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 5,
            "riskLimitValue": 50000,
            "initialMarginRate": 0.04,
            "maintenanceMarginRate": 0.035,
            "maxLeverage": 25
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 6,
            "riskLimitValue": 60000,
            "initialMarginRate": 0.045,
            "maintenanceMarginRate": 0.04,
            "maxLeverage": 22.22
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 7,
            "riskLimitValue": 70000,
            "initialMarginRate": 0.05,
            "maintenanceMarginRate": 0.045,
            "maxLeverage": 20
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 8,
            "riskLimitValue": 80000,
            "initialMarginRate": 0.055,
            "maintenanceMarginRate": 0.05,
            "maxLeverage": 18.18
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 9,
            "riskLimitValue": 90000,
            "initialMarginRate": 0.06,
            "maintenanceMarginRate": 0.055,
            "maxLeverage": 16.67
        },
        {
            "symbol": "SOL-PERP",
            "riskLevel": 10,
            "riskLimitValue": 100000,
            "initialMarginRate": 0.065,
            "maintenanceMarginRate": 0.06,
            "maxLeverage": 15.38
        }
    ],
    "success": true
}
```

> 响应 (未找到对应的市场信息)

```json
{
    "code": -2,
    "msg": "Invalid request parameters",
    "time": 1747207833879,
    "data": null,
    "success": false
}
```

`GET /api/v2.3/market/risk_limit`

获取所有市场的默认设置，包括每个市场和每个风险等级的初始保证金率和维持保证金率。如果未传入 symbol 参数，则会返回所有市场的数据。

### Request Parameters

| 名称                | 类型    | 是否必须 | 描述                                                         |
| ---                | ---     | ---      | ---                                                        |
| symbol             | String  | No       | 市场符号                                                    |

### Response Content

| 名称                     | 类型     | 是否必须 | 描述                                                                                                    |
| ---                      | ---      | ---      | ---                                                                                                   |
| code                     | Integer   | Yes     | 响应代码                                                                                                     |
| msg                      | Integer  | Yes      | 响应消息                                                                                                     |
| time                     | Integer  | Yes      | 响应时间                                                                                                     |
| data                     | 数据对象   | No      | 参见下面的数据对象                                                                                                     |
| success                  | Boolean   | Yes     | 是否成功                                                                                                     |

### 数据对象

| 名称                     | 类型     | 是否必须 | 描述                                                                                                    |
| ---                      | ---      | ---      | ---                                                                                                   |
| symbol                   | String   | Yes      | 市场符号                                                                                                    |
| riskLevel                | Integer  | Yes      | 风险等级                                                                                                    |
| riskLimitValue           | Integer  | Yes      | 当前风险等级下的风险限额（以币本位计算）                                                                                                  |
| initialMarginRate        | Double   | Yes      | 初始保证金率                                                                                                    |
| maintenanceMarginRate    | Double   | Yes      | 维持保证金率                                                                                                    |
| maxLeverage              | Double   | Yes      | 当前风险等级下的最大杠杆倍数 

# 交易端点

## 创建新订单

> 请求（创建`市价`订单）

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "side": "BUY",
  "type": "MARKET"
}
```
> 请求（创建`限价`订单）

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "price": 21000,
  "side": "BUY",
  "type": "LIMIT"
}
```
> 请求（创建`限价` `触发` 订单）

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "price": 21000,
  "side": "BUY",
  "type": "LIMIT",
  "txType": "TRIGGER",
  "triggerPrice": 30000
}
```
> 请求（创建`限价` `止损` 订单）

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "price": 21000,
  "side": "BUY",
  "type": "LIMIT",
  "txType": "STOP",
  "triggerPrice": 30000
}
```
> 请求（创建 `OCO` 订单）

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "price": 21000,
  "side": "BUY",
  "type": "OCO",
  "txType": "LIMIT",
  "trigger": "markPrice",
  "stopPrice": 30010,
  "triggerPrice": 30000
}
```
> 请求 (创建`限价`订单并设置`止盈/止损（TP/SL）`)

```json
{
    "symbol": "BTC-PERP",
    "size": 10,
    "price": 29000,
    "side": "BUY",
    "type": "LIMIT",
    "takeProfitPrice": 31000,
    "takeProfitTrigger": "markPrice",
    "stopLossPrice": 27000,
    "stopLossTrigger": "lastPrice"
}
```
> 请求（仅使用`TP`创建`限价`订单）

```json
{
    "symbol": "BTC-PERP",
    "size": 10,
    "price": 29000,
    "side": "BUY",
    "type": "LIMIT",
    "takeProfitPrice": 31000,
    "takeProfitTrigger": "markPrice"
}
```

> 请求（仅使用`SL`创建`限价`订单）

```json
{
    "symbol": "BTC-PERP",
    "size": 10,
    "price": 29000,
    "side": "BUY",
    "type": "LIMIT",
    "stopLossPrice": 27000,
    "stopLossTrigger": "lastPrice"
}
```

> 请求 (创建买侧双向持仓`市价`订单)

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "side": "BUY",
  "type": "MARKET",
  "positionMode": "HEDGE"
}
```


> 请求 (创建卖侧双向持仓`市价`减仓订单)

```json
{
  "symbol": "BTC-PERP",
  "size": 10,
  "side": "BUY",
  "type": "MARKET",
  "reduceOnly": true,
  "positionMode": "HEDGE"
}
```


> 响应（通用）

```json
[
  {
    "status": 4,
    "symbol": "BTC-PERP",
    "orderType": 77,
    "price": 111199.8,
    "side": "BUY",
    "orderID": "52cdd4ce-bf2e-4b8c-b286-4129ad1ab662",
    "timestamp": 1752138139421,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 111199.8,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 1,
    "totalFilledSize": 1,
    "remainingSize": 0,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

> 响应（用于 `OCO` 订单）

```json
[
  {
    "status": 9,
    "symbol": "BTC-PERP",
    "orderType": 76,
    "price": 111255.6,
    "side": "BUY",
    "orderID": "977e8486-64c3-4faa-9d44-ed187785f594",
    "timestamp": 1752138472048,
    "triggerPrice": 111255.6,
    "trigger": true,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 0,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  },
  {
    "status": 2,
    "symbol": "BTC-PERP",
    "orderType": 76,
    "price": 111055.6,
    "side": "BUY",
    "orderID": "9c1dea07-e7b7-448a-a16d-40c11809cee1",
    "timestamp": 1752138472047,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 1,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

> 响应（用于双向持仓订单）

```json
[
  {
    "status": 2,
    "symbol": "BTC-PERP",
    "orderType": 76,
    "price": 110078.1,
    "side": "BUY",
    "orderID": "738ef757-88e1-46d4-87b2-b24dd43e01db",
    "timestamp": 1752141497172,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 1,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "HEDGE",
    "positionDirection": "LONG",
    "positionId": "BTC-PERP-USDT|LONG",
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.3/order`

创建一个新的订单。需要`交易`权限。

### 请求参数

| 名称           | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                                                                                     |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                                                                                     |
| symbol        | String  | Yes      | 市场符号                                                                                                                                                                                                                                                                                                                                                                 |
| price         | Double  | No       | 除非创建市场订单，否则为必填。订单价格                                                                                                                                                                                                                                                                                                                                  |
| size          | Long    | Yes      | 订单尺寸以`合同大小`表示（即使在风险限额调整后也保持不变）                                                                                                                                                                                                                                                                                                               |
| side          | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                                                                                                                                                                                                                                                                                                        |
| time_in_force | String  | No       | 订单的时间有效性<br/>GTC: 有效直至取消<br/>IOC: 立即或取消<br/>FOK: 全部成交或取消<br/>HALFMIN: 订单有效30秒<br/>FIVEMIN: 订单有效5分钟<br/>HOUR: 订单有效一个小时<br/>TWELVEHOUR: 订单有效12小时<br/>DAY: 订单有效一天<br/>WEEK: 订单有效一周<br/>MONTH: 订单有效一个月                                                                                                              |
| type          | String  | Yes      | 订单类型<br/>LIMIT: 限价订单<br/>MARKET: 市价订单<br/>OCO: 一个取消另一个                                                                                                                                                                                                                                                                                               |
| txType        | String  | No       | 用于停止订单或触发订单<br/>STOP: 停止订单，`triggerPrice` 是必填项<br/>TRIGGER: 触发订单，`triggerPrice` 是必填项<br/>LIMIT: 默认值，当其既不是停止订单也不是触发订单时使用                                                                                                                                                                                              |
| stopPrice     | Double  | No       | 创建OCO订单时为必填。表示停止价格                                                                                                                                                                                                                                                                                                                                      |
| triggerPrice  | Double  | No       | 创建停止、触发、OCO订单时为必填。表示触发价格                                                                                                                                                                                                                                                                                                                          |
| trailValue    | Double  | No       | 跟踪价值                                                                                                                                                                                                                                                                                                                                                                  |
| postOnly      | Boolean | No       | 布尔值，表示这是否只做Maker(Post only) 订单，交易者将支付Maker手续费                                                                                                                                                                                                                                                                                                  |
| reduceOnly    | Boolean | No       | 布尔值，将这笔订单设置为只减仓, 在双向持仓时，买方`BUY`减少空头仓位，卖方`SELL`则减少多头仓位                                                                                                                                                                                                                                                                                                                                       |
| clOrderID     | String  | No       | 自定义订单ID                                                                                                                                                                                                                                                                                                                                                            |
| trigger       | String  | No       | 用于创建txType: `STOP` 或 `TRIGGER` 的订单。有效选项: `markPrice` (默认) 或 `lastPrice`  |
| takeProfitPrice  | Double  | No       | 在创建带有止盈订单时强制执行。指示触发价格
| takeProfitTrigger  | String  | No       | 用于创建带有止盈订单的订单。有效选项：`标记价格`（默认）或`最新价格`|
| stopLossPrice  | Double  | No       | 在创建带有止损订单时强制执行。指示触发价格
| stopLossTrigger  | String  | No       | 用于创建带有止损订单的订单。有效选项：`标记价格`（默认）或`最新价格`|
| positionMode  | String  | No       | 用于创建指定仓位模式订单。有效选项：单向持仓`ONE_WAY`（默认）或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                          |

### 响应内容

| 名称            | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                |
| symbol        | String  | Yes      | 市场符号                                                                                                                                                                                                                                                                                           |
| clOrderID     | String  | Yes      | 交易者发送的客户标签                                                                                                                                                                                                                                                                               |
| orderID       | String  | Yes      | 订单ID                                                                                                                                                                                                                                                                                             |
| orderType     | Integer | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: Algo订单                                                                                                                                                                                                                                       |
| postOnly      | Boolean | Yes      | 表明订单是否为只做Maker(Post only) 订单                                                                                                                                                                                                                                                                           |
| price         | Double  | Yes      | 订单价格                                                                                                                                                                                                                                                                                           |
| side          | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                                                                                                                                                                                                                           |
| status        | Integer    | Yes      | 订单状态<br/>2: 订单已插入<br/>3: 订单已交易<br/>4: 订单已完全交易<br/>5: 订单部分交易<br/>6: 订单已取消<br/>7: 订单已退款<br/>9: 触发已插入<br>10: 触发已激活<br/>15: 订单被拒绝<br/>16: 订单未找到<br/>17: 请求失败<br/>請参照[`API Enum`](#api-enum)                                                                                        |
| time_in_force | String  | Yes      | 订单有效性                                                                                                                                                                                                                                                                                         |
| timestamp     | Long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                                         |
| trigger       | Boolean | Yes      | 如果订单是触发订单的指示器                                                                                                                                                                                                                                                                        |
| triggerPrice  | Double  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                                          |
| avgFilledPrice  | Double  | Yes      | 平均成交价格。对于部分交易的订单返回平均成交价格                                                                                                                                                                                                                                                  |
| message       | String  | Yes      | 交易消息                                                                                                                                                                                                                                                                                           |
| stealth       | Double  | Yes      | 仅对Algo订单有效                                                                                                                                                                                                                                                                                   |
| deviation     | Double  | Yes      | 仅对Algo订单有效                                                                                                                                                                                                                                                                                   |
| remainingSize     | Integer  | Yes      | 剩余订单数量 = 当前订单数量 - 已成交数量                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | 原始订单数量。即使后续有调整，此值也不会变化                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | 当前最新的订单数量，表示已成交数量与未成交剩余数量的总和                                                                                                                                                                                                                                                                             |
| filledSize          | Integer  | Yes      | 订单已成交的数量                                                                                                                                                                                                                                                                               |
| totalFilledSize      | Integer  | Yes      | 该订单的累计成交数量                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | 仓位模式<br/> 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                                                  |
| positionDirection | String  | Yes      | 仓位方向<br/>  多头仓位`LONG` 或 空头仓位`SHORT`                                                                                                                                                                                                                                                                             |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |

## 创建新的算法订单

> 请求

```json
{
  "symbol": "BTC-PERP",
  "price": 21500,
  "size": 10,
  "side": "BUY",
  "clOrderID": "60a30188-f2a2-4498-b061-7d72126c18c2",
  "stealth": 10,
  "deviation": -10
}
```

> 响应

```json
[
  {
    "status": 2,
    "symbol": "BTC-PERP",
    "orderType": 80,
    "price": 111541.9,
    "side": "BUY",
    "orderID": "7080613e-2d15-42fd-ba25-340c755065fa",
    "timestamp": 1752214790589,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 10,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 1,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.3/order/peg`

创建新的算法订单。算法订单是一种价格会根据市场价格变化的订单。要创建算法订单，用户需要输入额外的参数：

* `price`：用户愿意将订单列出的最低价格（卖单）或最高价格（买单）
* `deviation`：订单价格与指数价格的偏差程度。该值以百分比表示，范围从 `-10` 到 `10`
* `stealth`：订单簿上要显示多少百分比的订单量。

此API需要具有`交易`权限。

### 请求参数

| 名称       | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                            |
| ---       | ---     | ---      | ---                                                                                                                                                                                                                                            |
| symbol    | String  | Yes      | 市场符号                                                                                                                                                                                                                                       |
| price     | Double  | Yes      | 卖单的最低价，这是用户愿意出售的最低价格。买单的最高价，这是用户愿意购买的最高价格。                                                                                                                                                        |
| side      | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                                                                                                                                                                       |
| clOrderID | String  | No       | 自定义订单ID                                                                                                                                                                                                                                    |
| deviation | Double  | No       | 订单价格应与指数价格偏离多少。该值以百分比表示，范围从`-10`到`10`                                                                                                                                                                             |
| stealth   | Double  | No       | 订单中应在订单簿上显示的百分比是多少。                                                                                                                                                                                                        |
| positionMode  | String  | No       | 用于创建指定仓位模式订单。有效选项：单向持仓`ONE_WAY`（默认）或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                          |

### 响应内容

| 名称            | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                |
| symbol        | String  | Yes      | 市场符号                                                                                                                                                                                                                                                                                           |
| clOrderID     | String  | Yes      | 交易者发送的客户标签                                                                                                                                                                                                                                                                               |
| orderID       | String  | Yes      | 订单ID                                                                                                                                                                                                                                                                                             |
| orderType     | Integer | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: Algo订单                                                                                                                                                                                                                                       |
| postOnly      | Boolean | Yes      | 表明订单是否为只做Maker(Post only) 订单                                                                                                                                                                                                                                                                           |
| price         | Double  | Yes      | 订单价格                                                                                                                                                                                                                                                                                           |
| side          | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                                                                                                                                                                                                                           |
| size          | Long    | Yes      | 订单大小以`合同大小`表示（即使在风险限额调整后也保持不变）                                                                                                                                                                                                                                          |
| status        | Integer    | Yes      | 订单状态<br/>2: 订单已插入<br/>3: 订单已交易<br/>4: 订单已完全交易<br/>5: 订单部分交易<br/>6: 订单已取消<br/>7: 订单已退款<br/>9: 触发已插入<br>10: 触发已激活<br/>15: 订单被拒绝<br/>16: 订单未找到<br/>17: 请求失败<br/>請参照[`API Enum`](#api-enum)                                                                                        |
| time_in_force | String  | Yes      | 订单有效性                                                                                                                                                                                                                                                                                         |
| timestamp     | Long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                                         |
| trigger       | Boolean | Yes      | 如果订单是触发订单的指示器                                                                                                                                                                                                                                                                        |
| triggerPrice  | Double  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                                          |
| avgFilledPrice  | Double  | Yes      | 平均成交价格。对于部分交易的订单返回平均成交价格                                                                                                                                                                                                                                                  |
| message       | String  | Yes      | 交易消息                                                                                                                                                                                                                                                                                           |
| stealth       | Double  | Yes      | 订单的隐秘值                                                                                                                                                                                                                                                                                       |
| deviation     | Double  | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                                       |
| remainingSize     | Integer  | Yes      | 剩余订单数量 = 当前订单数量 - 已成交数量                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | 原始订单数量。即使后续有调整，此值也不会变化                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | 当前最新的订单数量，表示已成交数量与未成交剩余数量的总和                                                                                                                                                                                                                                                                             |
| filledSize          | Integer  | Yes      | 订单已成交的数量                                                                                                                                                                                                                                                                               |
| totalFilledSize      | Integer  | Yes      | 该订单的累计成交数量                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | 仓位模式<br/> 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                                                  |
| positionDirection | String  | Yes      | 仓位方向<br/>  多头仓位`LONG` 或 空头仓位`SHORT`                                                                                                                                                                                                                                                                             |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |

## 查询订单

> 响应

```json
{
    "orderType": 80,
    "price": 111541.9,
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "totalFilledSize": 1,
    "remainingSize": 0,
    "side": "BUY",
    "orderValue": 1.115419,
    "pegPriceMin": 1,
    "pegPriceMax": 111541.9,
    "pegPriceDeviation": 0.1,
    "timestamp": 1752138591588,
    "orderID": "956a4e97-c229-42e8-a065-54c8b96f0732",
    "stealth": 1,
    "triggerOrder": false,
    "triggered": false,
    "triggerPrice": 0,
    "triggerOriginalPrice": 0,
    "triggerOrderType": 0,
    "triggerTrailingStopDeviation": 0,
    "triggerStopPrice": 0,
    "symbol": "BTC-PERP",
    "trailValue": 0,
    "clOrderID": "",
    "reduceOnly": false,
    "status": 4,
    "triggerUseLastPrice": false,
    "avgFilledPrice": 111126.6,
    "contractSize": 0.00001,
    "timeInForce": "GTC",
    "closeOrder": false
}

```

`GET /api/v2.3/order`

查询指定orderID/clOrderID的订单详情，请注意已取消的订单仅保留30分钟。需要`交易`权限。

### 请求参数

| 名称       | 类型    | 是否必须     | 描述                                                                         |
| ---       | ---    | ---      | ---                                                                             |
| orderID   | String  | No       | 订单的唯一标识符。当未提供clOrderID时，此项为必填。如果提供了orderID，则将忽略clOrderID。 |
| clOrderID | String  | No       | 客户自定义订单ID。当未提供orderID时，此项为必填。                                     |

### 响应内容

| 名称       | 类型    | 是否必须     | 描述                                                             |
| ---                           | ---     | ---      | ---                                            |
| orderID                       | String  | Yes      | 内部订单ID                                      |
| symbol                        | String  | Yes      | 市场交易对标识符                                   |
| quote                         | String  | Yes      | 报价货币的符号                                   |
| orderType                     | Integer | Yes      | 订单类型                                      |
| side                          | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                      |
| price                         | Double  | Yes      | 订单价格                                      |
| size                          | Double  | Yes      | 订单数量                                      |
| orderValue                    | Double  | Yes      | 此订单的总价值                                 |
| filledSize                    | Double  | Yes      | 已成交数量                                    |
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
| remainingSize                 | Double  | Yes      | 订单上剩余的大小                              |
| status                        | Integer | Yes      | 订单状态。请参照[`API Enum`](#api-enum)      |
| takeProfitOrder               | TakeProfitOrder object | No | 止盈订单信息 |
| stopLossOrder                 | StopLossOrder object   | No | 止损订单信息 |
| closeOrder                    | Boolean | Yes                | 是否为关闭此持仓的订单 |
| timeInForce                   | String  | Yes      | 订单有效期                                    |
| contractSize                  | Double  | Yes      | 订单合约规模                                                                |

## 修改订单

> 请求（修改价格）

```json
{
  "symbol": "BTC-PERP",
  "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
  "type": "PRICE",
  "value": 22000
}
```

> 请求（修改大小）

```json
{
  "symbol": "BTC-PERP",
  "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
  "type": "SIZE",
  "value": 100
}
```

> 请求（全部修改 - 触发单）

```json
{
  "symbol": "BTC-PERP",
  "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
  "type": "ALL",
  "orderPrice": 30010,
  "orderSize": 10,
  "triggerPrice": 30000
}
```

> 请求（全部修改 - 非触发单）

```json
{
  "symbol": "BTC-PERP",
  "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
  "type": "ALL",
  "orderPrice": 30010,
  "orderSize": 10
}
```

> 响应

```json
[
    {
        "status": 123,
        "symbol": "BTC-PERP",
        "orderType": 76,
        "price": 10104.1,
        "side": "BUY",
        "orderID": "39ff44d2-513a-4ea6-858c-e07498d424fd",
        "timestamp": 1752138774052,
        "triggerPrice": 0,
        "trigger": false,
        "deviation": 100,
        "stealth": 100,
        "message": "",
        "avgFilledPrice": 0,
        "clOrderID": "",
        "originalOrderSize": 1,
        "currentOrderSize": 1,
        "filledSize": 0,
        "totalFilledSize": 0,
        "remainingSize": 1,
        "postOnly": false,
        "orderDetailType": null,
        "positionMode": "ONE_WAY",
        "positionDirection": null,
        "positionId": "BTC-PERP-USDT",
        "time_in_force": "GTC"
    }
]
```

`PUT /api/v2.3/order`

修改订单的价格、数量或触发价格。对于触发订单，如果订单已经被触发，触发价格将无法进一步修改。修订订单不适用于算法订单。需要`交易`权限。

### 请求参数

| 名称          | 类型    | 是否必须 | 描述                                                                                                                                                                                                       |
| ---          | ---     | ---      | ---                                                                                                                                                                                                       |
| symbol       | String  | Yes      | 市场符号                                                                                                                                                                                                  |
| orderID      | String  | No       | 内部订单ID。当未提供`clOrderID`时为必填项。如果提供了`orderID`，将忽略`clOrderID`。                                                                                                                        |
| clOrderID    | String  | No       | 自定义订单ID。当未提供`orderID`时为必填项。                                                                                                                                                               |
| type         | String  | Yes      | 修改类型<br/>`PRICE`: 修改订单价格<br/>`SIZE`: 修改订单大小<br/>`TRIGGERPRICE`: 修改触发价格，仅适用于触发单。<br/>`ALL`: 修改多个字段。注意：`TRIGGERPRICE` 仅可在订单为触发单时修改，意味着如果不是触发单，请不要传入`TRIGGERPRICE`。                                                                                     |
| value        | Double  | Yes      | 要修改的值。其值取决于设置的类型。                                                                                                                                                                       |
| orderPrice   | Double  | No       | 对于类型：`ALL`，要修改的订单价格                                                                                                                                                                        |
| orderSize    | Integer  | No       | 对于类型：`ALL`，要修改的合同大小订单尺寸                                                                                                                                                                |
| triggerPrice | Double  | No       | 对于类型：`ALL`，要修改的触发价格                                                                                                                                                                        |


### 响应内容

| 名称            | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                |
| symbol        | String  | Yes      | 市场符号                                                                                                                                                                                                                                                                                           |
| clOrderID     | String  | Yes      | 交易者发送的客户标签                                                                                                                                                                                                                                                                               |
| orderID       | String  | Yes      | 订单ID                                                                                                                                                                                                                                                                                             |
| orderType     | Integer | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: Algo订单                                                                                                                                                                                                                                       |
| postOnly      | Boolean | Yes      | 表明订单是否为只做Maker(Post only) 订单                                                                                                                                                                                                                                                                           |
| price         | Double  | Yes      | 订单价格                                                                                                                                                                                                                                                                                           |
| side          | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                                                                                                                                                                                                                           |
| status        | Integer    | Yes      | 订单状态<br/>2: 订单已插入<br/>3: 订单已交易<br/>4: 订单已完全交易<br/>5: 订单部分交易<br/>6: 订单已取消<br/>7: 订单已退款<br/>9: 触发已插入<br>10: 触发已激活<br/>15: 订单被拒绝<br/>16: 订单未找到<br/>17: 请求失败<br/>請参照[`API Enum`](#api-enum)                                                                                        |
| time_in_force | String  | Yes      | 订单有效性                                                                                                                                                                                                                                                                                         |
| timestamp     | Long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                                         |
| trigger       | String  | Yes      | 如果订单是触发订单的指示器                                                                                                                                                                                                                                                                        |
| triggerPrice  | String  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                                          |
| avgFilledPrice  | String  | Yes      | 平均成交价格。对于部分交易的订单返回平均成交价格                                                                                                                                                                                                                                                  |
| message       | String  | Yes      | 交易消息                                                                                                                                                                                                                                                                                           |
| stealth       | Double  | Yes      | 订单的隐秘值                                                                                                                                                                                                                                                                                       |
| deviation     | String  | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                                       |
| remainingSize     | Integer  | Yes      | 剩余订单数量 = 当前订单数量 - 已成交数量                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | 原始订单数量。即使后续有调整，此值也不会变化                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | 当前最新的订单数量，表示已成交数量与未成交剩余数量的总和                                                                                                                                                                                                                                                                             |
| filledSize          | Integer  | Yes      | 订单已成交的数量                                                                                                                                                                                                                                                                               |
| totalFilledSize      | Integer  | Yes      | 该订单的累计成交数量                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | 仓位模式<br/> 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                                                  |
| positionDirection | String  | Yes      | 仓位方向<br/>  多头仓位`LONG` 或 空头仓位`SHORT`                                                                                                                                                                                                                                                                             |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |

## 取消订单

> 请求 (取消单个订单)

```
/api/v2.3/order?symbol=BTC-USD&clOrderID=my-order-id
```

> 响应

```json
[
  {
    "status": 6,
    "symbol": "BTC-PERP",
    "orderType": 76,
    "price": 100090.6,
    "side": "BUY",
    "orderID": "7a64ab37-313e-4313-bf1b-e909ebe9b976",
    "timestamp": 1752139128547,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 1,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

`DELETE /api/v2.3/order`

取消尚未成交的待定订单。orderID是取消特定订单的唯一标识符。clOrderID是交易者发送的自定义ID。通过clOrderID取消时，所有具有相同ID的订单都将被取消。如果未发送orderID和clOrderID，则取消将针对当前市场中的所有订单。需要`交易`权限。

### 请求参数

| 名称       | 类型    | 是否必须 | 描述                                                                                                                                                                    |
| ---        | ---     | ---      | ---                                                                                                                                                                    |
| symbol     | String  | Yes      | 市场符号                                                                                                                                                               |
| orderID    | String  | No       | 订单的唯一标识符。当未提供`clOrderID`时为必填项。如果提供了`orderID`，将忽略`clOrderID`。                                                                                |
| clOrderID  | String  | No       | 客户端自定义订单ID。当未提供`orderID`时为必填项。                                                                                                                                                  |


### 响应内容

| 名称            | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                        |
| ---             | ---     | ---      | ---                                                                                                                                                                                                                                                                                                        |
| symbol          | String  | Yes      | 市场符号                                                                                                                                                                                                                                                                                                   |
| clOrderID       | String  | Yes      | 交易者发送的客户标签                                                                                                                                                                                                                                                                                       |
| orderID         | String  | Yes      | 订单ID                                                                                                                                                                                                                                                                                                     |
| orderType       | Integer | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: 算法订单                                                                                                                                                                                                                                               |
| postOnly        | Boolean | Yes      | 表明订单是否为只做Maker(Post only) 订单                                                                                                                                                                                                                                                                                   |
| price           | Double  | Yes      | 订单价格                                                                                                                                                                                                                                                                                                   |
| side            | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                                                                                                                                                                                                                                   |
| status          | Integer    | Yes      | 订单状态<br/>2: 订单已插入<br/>3: 订单已交易<br/>4: 订单已完全交易<br/>5: 订单部分交易<br/>6: 订单已取消<br/>7: 订单已退款<br/>9: 触发已插入<br>10: 触发已激活<br/>15: 订单被拒绝<br/>16: 订单未找到<br/>17: 请求失败<br/>請参照[`API Enum`](#api-enum)                                                                                              |
| time_in_force   | String  | Yes      | 订单有效性                                                                                                                                                                                                                                                                                                |
| timestamp       | Long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                                                |
| trigger         | Boolean | Yes      | 表明订单是否为触发订单的指示器                                                                                                                                                                                                                                                                            |
| triggerPrice    | Double  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                                                  |
| avgFilledPrice    | Double  | Yes      | 平均成交价格。对于部分交易的订单返回平均成交价格                                                                                                                                                                                                                                                          |
| message         | String  | Yes      | 交易消息                                                                                                                                                                                                                                                                                                  |
| stealth         | Double  | Yes      | 订单的隐秘值                                                                                                                                                                                                                                                                                              |
| deviation       | Double  | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                                              |
| remainingSize     | Integer  | Yes      | 剩余订单数量 = 当前订单数量 - 已成交数量。                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | 原始订单数量。即使后续有调整，此值也不会变化                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | 当前最新的订单数量，表示已成交数量与未成交剩余数量的总和                                                                                                                                                                                                                                                                            |
| filledSize          | Integer  | Yes      | 订单已成交的数量                                                                                                                                                                                                                                                                               |
| totalFilledSize      | Integer  | Yes      | 该订单的累计成交数量                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | 仓位模式<br/> 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                                                  |
| positionDirection | String  | Yes      | 仓位方向<br/>  多头仓位`LONG` 或 空头仓位`SHORT`                                                                                                                                                                                                                                                                             |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |

## 延时自动取消所有

> 请求

```json
{
  "timeout": 60000
}
```

`POST /api/v2.3/order/cancelAllAfter`

允许交易员发送一个超时值，这是一个订单的生存时间（TTL）值。通过发送另一个“cancelAllAfter”请求来延长超时时间。如果服务器在超时时间到达之前没有收到另一个请求，那么所有订单将被取消。需要`交易`权限。

### 请求参数

| 名称     | 类型  | 是否必须 | 描述                         |
| ---      | ---   | ---      | ---                          |
| timeout  | Long  | Yes      | 超时值，以毫秒为单位          |


> 响应内容

* 如果设置正确，将返回HTTP 200响应代码

## 查询未完成订单

> 请求

```
/api/v2.3/user/open_orders?symbol=BTC-PERP
```

> Response

```json
[
  {
    "vendorName": null,
    "botID": null,
    "orderType": 76,
    "price": 10104.1,
    "side": "BUY",
    "orderValue": 0.101041,
    "pegPriceMin": 0,
    "pegPriceMax": 0,
    "pegPriceDeviation": 1,
    "cancelDuration": 0,
    "timestamp": 1752138665358,
    "orderID": "39ff44d2-513a-4ea6-858c-e07498d424fd",
    "stealth": 1,
    "triggerOrder": false,
    "triggered": false,
    "triggerPrice": 0,
    "triggerOriginalPrice": 0,
    "triggerOrderType": 0,
    "triggerTrailingStopDeviation": 0,
    "triggerStopPrice": 0,
    "symbol": "BTC-PERP",
    "trailValue": 0,
    "contractSize": 0.00001,
    "clOrderID": "",
    "reduceOnly": false,
    "orderState": "STATUS_ACTIVE",
    "triggerUseLastPrice": false,
    "avgFilledPrice": 0,
    "timeInForce": "GTC",
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "totalFilledSize": 0,
    "remainingSize": 1,
    "orderDetailType": null,
    "takeProfitOrder": null,
    "stopLossOrder": null,
    "closeOrder": false,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT"
  }
]
```

`GET /api/v2.3/user/open_orders`

检索尚未匹配或最近已匹配的未完成订单。需要`读取`权限。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                    |
| ---                | ---     | ---      | ---                                                                                     |
| symbol             | String  | No       | 市场符号                                                                                 |
| orderID            | String  | No       | 使用内部订单ID查询                                                                        |
| clOrderID          | String  | No       | 使用自定义订单ID查询。如果提供了`orderID`，`clOrderID`将被忽略。                                   |

### 响应内容

| 名称                         | 类型    | 是否必须 | 描述                                                                                  |
| ---                          | ---     | ---      | ---                                                                                   |
| symbol                       | String  | Yes      | 市场符号                                                                               |
| clOrderID                    | String  | Yes      | 交易员发送的客户标签                                                                   |
| orderValue                   | Double  | Yes      | 名义价值                                                                               |
| pegPriceMin                  | Double  | Yes      | 最小挂钩价格                                                                           |
| pegPriceMax                  | Double  | Yes      | 最大挂钩价格                                                                           |
| pegPriceDeviation            | Double  | Yes      | 偏差百分比。仅适用于Algo订单                                                           |
| cancelDuration               | Long    | Yes      | 以毫秒为单位的过期时间。<br/>0: GTC<br/>-1: IOC                                        |
| orderID                      | String  | Yes      | 订单ID                                                                                 |
| orderType                    | Integer | Yes      | 订单类型 <br/>76: 限价单<br/>77: 市价单<br/>80: Algo订单                               |
| timeInForce                  | String  | Yes      | 订单有效期                                                                             |
| price                        | Double  | Yes      | 订单价格                                                                               |
| side                         | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                               |
| originalOrderSize            | Integer  | Yes      | 原始订单数量。即使后续有调整，此值也不会变化 |
| currentOrderSize             | Integer  | Yes      | 当前最新的订单数量，表示已成交数量与未成交剩余数量的总和 |
| totalFilledSize              | Integer  | Yes      | 该订单的累计成交数量 |
| timestamp                    | Long    | Yes      | 订单时间戳                                                                             |
| triggerOrder                 | Boolean    | Yes      | 指示这是否为触发订单                                                                   |
| triggered                    | Boolean    | Yes      | 指示此订单是否已被触发                                                                 |
| triggerUseLastPrice          | Boolean    | Yes      | 指示此触发订单是否使用最后价格                                                         |
| triggerPrice                 | Double  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                              |
| triggerOriginalPrice         | Double  | Yes      | 原始触发价格                                                                           |
| triggerOrderType             | String  | Yes      | 触发订单类型 <br/>1001: 触发止损 <br/>1002: 触发获利                                   |
| triggerTrailingStopDeviation | Double  | Yes      | 保止损价格的百分比偏差                                                                               |
| triggerStopPrice             | Double  | Yes      | 保止损价格，仅适用于算法订单                                                                               |
| trailValue                   | Double  | Yes      | 跟踪价值                                                                               |
| reduceOnly                   | Boolean    | Yes      | 指示此订单是否仅为减少                                                                 |
| avgFilledPrice               | Double  | Yes      | 平均成交价格。返回部分交易订单的平均成交价格                                           |
| stealth                      | Double  | Yes      | 订单的隐身值                                                                           |
| orderState                   | String  | Yes      | `STATUS_ACTIVE`, `STATUS_INACTIVE`                                                     |
| takeProfitOrder    | TakeProfitOrder对象  | No | 止盈订单信息 |
| stopLossOrder      | StopLossOrder对象    | No | 止损订单信息 |
| closeOrder         | Boolean                | Yes | 是否为关闭此持仓的订单 |
| positionMode      | String  | Yes      | 仓位模式<br/> 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                                                  |
| positionDirection | String  | Yes      | 仓位方向<br/>  多头仓位`LONG` 或 空头仓位`SHORT`                                                                                                                                                                                                                                                                             |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |
| contractSize                 | Double   | Yes      | 订单合约规模                                                              |

## 查询成交记录

> 请求

```
/api/v2.3/user/trade_history?symbol=BTC-PERP
```

> 响应

```json
[
  {
    "tradeId": "9d661ee3-eaf8-4068-8d6a-5d3dfef6ef5f",
    "orderId": "bf07eeff-afdc-433a-a0ca-f41a2433e323",
    "username": "xxx",
    "side": "SELL",
    "orderType": 77,
    "triggerType": null,
    "price": 0,
    "size": 99,
    "filledPrice": 100000,
    "filledSize": 99,
    "triggerPrice": 0,
    "base": "BTC",
    "quote": "USDT",
    "symbol": "BTC-PERP",
    "feeCurrency": "USDT",
    "feeAmount": 0.0198,
    "wallet": "VIRTUAL|1@BTC-PERP-USDT#1",
    "realizedPnl": -0.99,
    "total": -1.0098,
    "serialId": 374029591,
    "timestamp": 1752204538247,
    "orderDetailType": null,
    "contractSize": 0.00001,
    "clOrderID": "_W_pip1752204538116",
    "positionId": "BTC-PERP-USDT",
    "avgFilledPrice": 100000
  }
]
```

`GET /api/v2.3/user/trade_history`

获取用户的交易历史。需要`读取`权限。

### 请求参数

| 名称              | 类型    | 是否必须 | 描述                                                                                               |
| ---               | ---     | ---      | ---                                                                                                |
| symbol            | String  | No       | 市场符号                                                                                            |
| startTime         | Long    | No       | 开始时间 (例如：1624987283000)                                                                      |
| endTime           | Long    | No       | 结束时间 (例如：1624987283000)                                                                      |
| beforeSerialId    | Long  | No      | 用于分页检索记录，适用于**订单量每毫秒超过500**的情况。对于大多数场景，建议使用 `startTime` 和 `endTime` 参数 |
| afterSerialId     | Long  | No      | 用于分页检索记录，适用于**订单量每毫秒超过500**的情况。对于大多数场景，建议使用 `startTime` 和 `endTime` 参数 |
| count             | Long    | No       | 返回的记录数量                                                                                      |
| includeOld        | Boolean | No       | 检索过去7天的交易历史记录                                                                            |
| orderID           | String  | No       | 通过订单ID查询交易历史                |
| clOrderID         | String  | No       | 通过自定义订单ID查询交易历史                                                                         |

* 交易历史纪录最大天数

| 时间区间              | 最大天数      | 说明                                                  |
| ---                 | :---:       | ---                                                   |
| startTime / endTime | 7           | 在指定区间中最多**7**天记录，若指定区间超过**7**天，则**开始时间**将设为**结束时间**的前**7**天                            |
| startTime /    -    | 7           | 未指定**结束时间**, 则从**开始时间**往后**7**天           |
|      -    / endTime | 7           | 未指定**开始时间**, 则从**结束时间**往前**7**天           |
|      -    /    -    | 7           | 都未指定时间, 则使用**当前时间**作为**结束时间**往前**7**天 |

### 响应内容

| 名称             | 类型    | 是否必须 | 描述                                                                                                                                                                                 |
| ---              | ---     | ---      | ---                                                                                                                                                                                  |
| symbol           | String  | Yes      | 市场符号                                                                                                                                                                            |
| side             | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                                                                                                  |
| price            | Double  | Yes      | 成交价格                                                                                                                                                                             |
| size             | Long    | Yes      | 原始订单数量                                                                                                                                                                             |
| serialId         | Long    | Yes      | 序列号，连续的序列号                                                                                                                                                                 |
| tradeId          | String  | Yes      | 交易标识符                                                                                                                                                                          |
| timestamp        | Long    | Yes      | 成交时间戳                                                                                                                                                                          |
| base             | String  | Yes      | 基础货币                                                                                                                                                                            |
| quote            | String  | Yes      | 报价货币                                                                                                                                                                            |
| wallet           | String  | Yes      | 钱包名称<br/>`CROSS@`: 跨钱包<br/>`ISOLATED@market`: Market指的是当前的符号，后面跟`-USD`。例如，BTC-PERP的独立钱包为`ISOLATED@BTC-PERP-USDT`                                               |
| clOrderID        | String  | Yes      | 自定义订单ID                                                                                                                                                                         |
| orderId          | String  | Yes      | 订单ID                                                                                                                                                                              |
| username         | String  | Yes      | btse 用户名                                                                                                                                                                          |
| triggerType      | Long    | Yes      | 触发类型<br/>1001: 止损<br/>1002: 获利                                                                                                                                              |
| feeAmount        | Double    | Yes      | 费用金额                                                                                                                                                                            |
| feeCurrency      | String    | Yes      | 费用货币                                                                                                                                                                            |
| filledPrice      | Double  | Yes      | 平均成交价格                                                                                                                                                                        |
| avgFilledPrice | Double  | Yes      | 平均成交价格                                                                                                                                                                        |
| triggerPrice     | Double  | Yes      | 触发价格                                                                                                                                                                            |
| filledSize       | Long    | Yes      | 成交大小                                                                                                                                                                            |
| orderType        | Integer | Yes      | 订单类型                                                                                                                                                                            |
| realizedPnL      | Double  | Yes      | 现货中未使用                                                                                                                                                                        |
| total            | Long    | Yes      | 现货中未使用                                                                                                                                                                        |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |
| contractSize     | Double  | Yes      | 交易合约规模                                                                                                                                                           |


## 查询持仓

> 请求

```
/api/v2.3/user/positions?symbol=BTC-PERP
```

> 响应

```json
[
  {
    "marginType": 0,
    "entryPrice": 0,
    "markPrice": 29286.4,
    "symbol": "BTC-PERP",
    "side": "BUY",
    "orderValue": 441.8492,
    "settleWithAsset": "BTC",
    "unrealizedProfitLoss": -0.23538014,
    "totalMaintenanceMargin": 2.366912551,
    "size": 62,
    "liquidationPrice": 0,
    "isolatedLeverage": 25,
    "adlScoreBucket": 2,
    "liquidationInProgress": false,
    "timestamp": 1576661434072,
    "currentLeverage": 0,
    "takeProfitOrder": {
        "orderId": "ea1ab233-c79a-4503-a475-f8633ecc9d79",
        "side": "SELL",
        "triggerPrice": 31000.0,
        "triggerUseLastPrice": false
    },
    "stopLossOrder": {
        "orderId": "48523190-77b9-44ea-bee0-d67a428a51b8",
        "side": "SELL",
        "triggerPrice": 27000.0,
        "triggerUseLastPrice": true
    },
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT"
  },{
     "marginType": 91,
     "entryPrice": 1631.106666667,
     "markPrice": 1630.398947255,
     "symbol": "ETH-PERP",
     "side": "BUY",
     "orderValue": 48.9119684176,
     "settleWithAsset": "USDT",
     "unrealizedProfitLoss": -0.02123158,
     "totalMaintenanceMargin": 0.254871114,
     "size": 3,
     "liquidationPrice": 0,
     "isolatedLeverage": 0,
     "adlScoreBucket": 2,
     "liquidationInProgress": false,
     "timestamp": 0,
     "takeProfitOrder": null,
     "stopLossOrder": null,
     "positionMode": "HEDGE",
     "positionDirection": "LONG",
     "positionId": "ETH-PERP-USDT|LONG",
     "currentLeverage": 0.0340349245,
     "takeProfitOrder": null,
     "stopLossOrder": null
     }
]
```

`GET /api/v2.3/user/positions`

查询用户当前的仓位。当未指定交易对时，将返回所有市场的仓位。需要`读取`权限。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                     |
| ---                | ---     | ---      | ---                                                                                      |
| symbol             | String  | No       | 市场符号                                                                                  |

### 响应内容

| 名称                   | 类型    | 是否必须 | 描述                                                                                              |
| ---                    |---------| ---      | ---                                                                                               |
| symbol                 | String  | Yes      | 市场符号                                                                                           |
| side                   | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                 |
| size                   | Long    | Yes      | 仓位大小                                                                                           |
| entryPrice             | Double  | Yes      | 入场价格                                                                                           |
| markPrice              | Double  | Yes      | 标记价格                                                                                           |
| marginType             | Integer    | Yes      | 保证金类型。值如下<br/>91: CROSS钱包<br/>92: 独立钱包                                                 |
| orderValue             | Double  | Yes      | 名义价值                                                                                           |
| settleWithAsset        | String  | Yes      | 结算货币                                                                                           |
| totalMaintenanceMargin | Double  | Yes      | 维持保证金                                                                                         |
| unrealizedProfitLoss   | Double  | Yes      | 未实现的利润和损失                                                                                  |
| liquidationPrice       | Double  | Yes      | 清算价格                                                                                           |
| isolatedLeverage       | Double  | Yes      | 独立杠杆值                                                                                         |
| adlScoreBucket         | Double  | Yes      | ADL得分概率                                                                                        |
| liquidationInProgress  | Boolean | Yes      | 指示是否正在进行清算                                                                               |
| currentLeverage        | Double  | Yes      | 当前杠杆                                                                                           |
| timestamp              | Long    | Yes      | 查询仓位时的时间戳                                                                                 |
| takeProfitOrder  | TakeProfitOrder对象 | No | 止盈订单信息 |
| stopLossOrder    | StopLossOrder对象   | No | 止损订单信息 |
| positionMode      | String  | Yes      | 仓位模式<br/> 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                                                  |
| positionDirection | String  | Yes      | 仓位方向<br/>  多头仓位`LONG` 或 空头仓位`SHORT`                                                                                                                                                                                                                                                                             |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |


## 平仓仓位

> 请求

```json
{
  "price": 0,
  "symbol": "BTC-PERP",
  "type": "MARKET"
}
```
> 请求（用于双向持仓订单）

```json
{
  "price": 0,
  "symbol": "BTC-PERP",
  "type": "MARKET",
  "positionId": "BTC-PERP-USDT|LONG"
}
```
> Response

```json
[
  {
    "status": 4,
    "symbol": "ETH-PERP",
    "orderType": 77,
    "price": 3900,
    "side": "SELL",
    "orderID": "21d2de4d-b133-4e22-81ae-afde5c95d227",
    "timestamp": 1752205761546,
    "triggerPrice": 0,
    "trigger": false,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 3900,
    "clOrderID": "_W_mizmtpf1752205761471",
    "postOnly": false,
    "originalOrderSize": 1,
    "currentOrderSize": 1,
    "totalFilledSize": 1,
    "remainingSize": 0,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "ETH-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.3/order/close_position`

平仓用户在特定市场上指定的仓位。如果指定类型为LIMIT，则价格是必须的。当类型为MARKET时，以市场价格平仓仓位。需要`交易`权限。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                                                 |
|--------------------| ---     | ---      | --------------------------------------------------------------------------------------------------------------------|
| symbol             | String  | Yes      | 市场符号                                                                                                             |
| type               | String  | Yes      | 平仓类型，其值为：<br/>LIMIT: 以`price`价格平仓<br/>MARKET: 以市价平仓                                                 |
| price              | Double  | No       | 平仓价格。当类型为`LIMIT`时，此字段为必填                                                                           |
| postOnly           | Boolean | No       | 布尔值，表示这是否只做Maker(Post only) 订单，交易者将支付Maker手续费                                           |
| positionId         | String  | No       | 想要平仓的仓位ID。在非单向持仓时为必填项                        |

### 响应内容

| 名称           | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                          |
| ---            | ---     | ---      | ---                                                                                                                                                                                                                                                                           |
| symbol         | String  | Yes      | 市场符号                                                                                                                                                                                                                                                                     |
| clOrderID      | String  | Yes      | 交易员发送的客户标签                                                                                                                                                                                                                                                        |
| orderID        | String  | Yes      | 订单ID                                                                                                                                                                                                                                                                       |
| orderType      | Integer | Yes      | 订单类型 <br/>76: 限价单<br/>77: 市价单<br/>80: Algo订单                                                                                                                                                                                                                     |
| postOnly       | Boolean | Yes      | 表示订单是否仅为只做Maker(Post only) 订单                                                                                                                                                                                                                                                     |
| price          | Double  | Yes      | 订单价格                                                                                                                                                                                                                                                                     |
| side           | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                                                                                                                                                                                                    |
| status         | Integer    | Yes      | 订单状态<br/>2: 已插入订单<br/>3: 已交易订单<br/>4: 订单已全部交易<br/>5: 订单部分交易<br/>6: 已取消订单<br/>7: 已退款订单<br/>9: 触发器已插入<br>10: 触发器已激活<br/>15: 订单被拒绝<br/>16: 找不到订单<br/>17: 请求失败<br/>請参照[`API Enum`](#api-enum)                                                   |
| time_in_force  | String  | Yes      | 订单有效性                                                                                                                                                                                                                                                                  |
| timestamp      | Long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                  |
| trigger        | String  | Yes      | 指示订单是否为触发订单                                                                                                                                                                                                                                                      |
| triggerPrice   | String  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                   |
| avgFilledPrice   | String  | Yes      | 平均成交价格。返回部分交易订单的平均成交价格                                                                                                                                                                                                                                |
| message        | String  | Yes      | 交易消息                                                                                                                                                                                                                                                                    |
| stealth        | Double  | Yes      | 订单的隐身值                                                                                                                                                                                                                                                                |
| deviation      | String  | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                |
| remainingSize     | Integer  | Yes      | 剩余订单数量 = 当前订单数量 - 已成交数量                                                                                                                                                                                                                                                                      |
| originalOrderSize      | Integer  | Yes      | 原始订单数量。即使后续有调整，此值也不会变化                                                                                                                                                                                                                                                                             |
| currentOrderSize      | Integer  | Yes      | 当前最新的订单数量，表示已成交数量与未成交剩余数量的总和                                                                                                                                                                                                                                                                             |
| filledSize          | Integer  | Yes      | 订单已成交的数量                                                                                                                                                                                                                                                                              |
| totalFilledSize      | Integer  | Yes      | 该订单的累计成交数量                                                                                                                                                                                                                                                                             |
| positionMode      | String  | Yes      | 仓位模式<br/> 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                                                  |
| positionDirection | String  | Yes      | 仓位方向<br/>  多头仓位`LONG` 或 空头仓位`SHORT`                                                                                                                                                                                                                                                                             |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |


## 获取风险限制

> 请求

```
/api/v2.3/risk_limit?symbol=BTC-PERP
```

> 响应

```json
{
    "symbol": "BTC-PERP",
    "riskLimit": 100000
}
```
`GET /api/v2.3/risk_limit`

查询指定市场的风险限制。需要`读取`权限。

### 请求参数

| 名称     | 类型    | 是否必须 | 描述       |
| ---      | ---     | ---      | ---        |
| symbol   | String  | Yes      | 市场符号   |

### 响应内容

| 名称       | 类型    | 是否必须 | 描述                                                                                                         |
| ---        | ---     | ---      | ---                                                                                                          |
| symbol     | String  | Yes      | 市场符号                                                                                                     |
| riskLimit  | Long    | Yes      | 当前的风险限制值以仓位大小表示，但随着期货市场名称的变化，它将转变为USD值                                      |

## 设置风险限制

> 请求

```json
{
  "symbol": "BTC-PERP",
  "riskLimit": 0
}
```

> 请求 (当双向持仓时)

```json
{
    "symbol": "BTC-PERP",
    "riskLimit": 100000,
    "positionMode": "HEDGE"
}
```

> 响应

```json
{
  "symbol": "BTC-PERP",
  "timestamp": 1577093486551,
  "status": 20,
  "type": 94,
  "message": "false"
}
```

`POST /api/v2.3/risk_limit`

更改指定市场的风险限制。需要`交易`权限。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                                                                   |
| ---                | ---     | ---      | ---                                                                                                                                    |
| symbol             | String  | Yes      | 市场符号                                                                                                                               |
| riskLimit          | Long    | Yes      | 当前的风险限制值以仓位大小表示，但它将在将来转变为USD值。                                                                                  |
| positionMode       | String  | no       | 单向持仓`ONE_WAY`（默认）或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`, 在非单向持仓时为必填项                                                            |

### 响应内容

| 名称       | 类型    | 是否必须 | 描述                                                                                                                                                     |
| ---        | ---     | ---      | ---                                                                                                                                                      |
| symbol     | String  | Yes      | 市场符号                                                                                                                                                 |
| status     | Integer    | Yes      | 请求的状态。可取值为：<br/>8: 余额不足<br/>12: 更新风险限额时出错<br/>20: 成功<br/>41: 风险限额无效                                                                                          |
| type       | Double  | Yes      | 值将为94，表示类型为`风险限额`                                                                                                                           |
| timestamp  | Long    | Yes      | 设置风险限额的时间戳                                                                                                                                      |
| message    | Long    | Yes      | 消息                                                                                                                                                     |

## 设置杠杆

> 请求

```json
{
  "symbol": "BTC-PERP",
  "leverage": 0,
  "marginMode": "CROSS"
}
```

> 请求 (当双向持仓时)

```json
{
    "symbol": "BTC-PERP",
    "leverage": 0,
    "positionMode": "HEDGE",
    "marginMode": "CROSS"
}
```

> 响应

```json
{
  "symbol": "BTC-PERP",
  "timestamp": 1660711246942,
  "status": 20,
  "type": 93,
  "message": ""
}
```

`POST /api/v2.3/leverage`

更改指定市场的杠杆值。需要`交易`权限。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                     |
| ---                | ---     | ---      | ---                                                                                      |
| symbol             | String  | Yes      | 市场符号                                                                                 |
| leverage           | Long    | Yes      | 杠杆值                                                                                   |
| positionMode       | String  | no       | 单向持仓`ONE_WAY`（默认）或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`, 在非单向持仓时为必填项                                                            |
| positionId         | String  | No       | 在逐仓保证金模式想要设置的仓位ID。                       |
| marginMode       | String  | no       | `CROSS` 或 `ISOLATED`(默认)                                                            |

### 响应内容

| 名称       | 类型    | 是否必须 | 描述                                                                                                                                                          |
| ---        | ---     | ---      | ---                                                                                                                                                           |
| symbol     | String  | Yes      | 市场符号                                                                                                                                                      |
| status     | Integer    | Yes      | 请求的状态。可取值为：<br/>8: 余额不足<br/>13: 无效的杠杆<br/>20: 成功<br/>64: 正在进行的清算                                                                                             |
| type       | Double  | Yes      | 值将为93，表示类型为`杠杆`                                                                                                                                    |
| timestamp  | Long    | Yes      | 设置杠杆的时间戳                                                                                                                                               |
| message    | Long    | Yes      | 消息                                                                                                                                                          |

## 获取杠杆

> 响应

```json
[
  {
    "symbol": "BTC-PERP",
    "leverage": 10,
    "marginMode": "ISOLATED",
    "positionDirection": "LONG"
  },
  {
    "symbol": "BTC-PERP",
    "leverage": 3,
    "marginMode": "ISOLATED",
    "positionDirection": "SHORT"
  }
]
```

`Get /api/v2.3/leverage`

获取指定市场的杠杆值。需要`读取`权限。

### 请求参数

| 名称     | 类型    | 是否必须 | 描述       |
| ---      | ---     | ---      | ---        |
| symbol   | String  | Yes      | 市场符号   |

### 响应内容

| 名称               | 类型   | 是否必须 | 描述                                        |
| ---               | ---    | ---    | ---                                         |
| symbol            | String | Yes    | 市场符号                                     |
| leverage          | Double | Yes    | 当前市场的杠杆值，返回 0 表示杠杆是最大的全仓杠杆。 |
| marginMode        | String | Yes    | 当前保证金模式                                |
| positionDirection | String | Yes    | 当前头寸模式为对冲时返回头寸方向，否则返回空值。    |

## 更改合同结算货币

> 请求

```json
{
  "symbol": "BTC-PERP",
  "currency": "BTC"
}
```

> 请求 (当双向持仓时)

```json
{
    "symbol": "BTC-PERP",
    "currency": "USDT",
    "positionId": "BTC-PERP-USDT|LONG"
}
```

> 响应（仅在发生错误时可用）

```json
{
  "status": 0,
  "errorCode": 0,
  "message": "String"
}
```

`POST /api/v2.3/settle_in`

更改当前市场中持仓的结算货币。需要`交易`权限。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                     |
| ---                | ---     | ---      | ---                                                                                      |
| symbol             | String  | Yes      | 市场符号                                                                                 |
| currency           | String  | Yes      | 要设置的结算货币                                                                         |
| positionId         | String  | No       | 想要设置的仓位ID。在非单向持仓时为必填项                        |

### 响应内容

| 名称       | 类型    | 是否必须 | 描述                                                    |
| ---        | ---     | ---      | ---                                                     |
| status     | Integer    | No       | 状态。仅在发生错误时可用。                                |
| errorCode  | Long    | No       | 错误代码。仅在发生错误时可用。                            |
| message    | String  | No       | 响应消息。仅在发生错误时可用。                            |

## 查询帐户费用

> 响应

```json
{
  "makerFee": 0,
  "symbol": "BTC-PERP",
  "takerFee": 0
}
```

`GET /api/v2.3/user/fees`

查询用户的交易费用。需要`读取`权限。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                     |
| ---                | ---     | ---      | ---                                                                                      |
| symbol             | String  | No       | 市场符号                                                                                 |

### 响应内容

| 名称      | 类型   | 是否必须 | 描述       |
| ---       | ---    | ---      | ---        |
| symbol    | String | Yes      | 市场符号   |
| makerFee  | Double | Yes      | 制造商费用 |
| takerFee  | Double | Yes      | 接受者费用 |


## 绑定止盈/止损
> 请求

```json
{
    "symbol": "BTC-PERP",
    "takeProfitPrice": 31000,
    "takeProfitTrigger": "markPrice",
    "stopLossPrice": 22000,
    "stopLossTrigger": "lastPrice"
}
```

> 响应

```json
[
  {
    "status": 9,
    "symbol": "BTC-PERP",
    "orderType": 77,
    "price": 0,
    "side": "SELL",
    "orderID": "00fcb6e9-5c89-4c20-8b85-b9789dc4d2c7",
    "timestamp": 1752140292632,
    "triggerPrice": 50000,
    "trigger": true,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 8,
    "currentOrderSize": 8,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 0,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  },
  {
    "status": 9,
    "symbol": "BTC-PERP",
    "orderType": 77,
    "price": 0,
    "side": "SELL",
    "orderID": "2eb18277-0625-47d6-b4c9-5d898a33e2f7",
    "timestamp": 1752140292632,
    "triggerPrice": 120000,
    "trigger": true,
    "deviation": 100,
    "stealth": 100,
    "message": "",
    "avgFilledPrice": 0,
    "clOrderID": "",
    "originalOrderSize": 8,
    "currentOrderSize": 8,
    "filledSize": 0,
    "totalFilledSize": 0,
    "remainingSize": 8,
    "postOnly": false,
    "orderDetailType": null,
    "positionMode": "ONE_WAY",
    "positionDirection": null,
    "positionId": "BTC-PERP-USDT",
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.3/order/bind/tpsl`

绑定止盈/止损与已有持仓。需要`交易`权限。

### 请求参数

| 名称               | 类型    | 是否必需 | 描述 |
| ---                | ---     | ---      | --- |
| symbol             | String  | Yes       | 市场交易对 |
| side               | String  | Yes       | `BUY` 或 `SELL` 在双向持仓时为必填项, 在双向持仓时，买方`BUY`綁定至空头仓位，卖方`SELL`则綁定至多头仓位 |
| takeProfitPrice    | Double  | No       | 创建带有止盈订单时强制执行。指示触发价格。在使用此API时，必须至少设置`takeProfitPrice`或`stopLossPrice`。 |
| takeProfitTrigger  | String  | No       | 用于创建带有止盈订单的选项。有效选项：`标记价格`（默认）或`最新价格` |
| stopLossPrice      | Double  | No       | 创建带有止损订单时强制执行。指示触发价格 |
| stopLossTrigger     | String  | No       | 用于创建带有止损订单的选项。有效选项：`标记价格`（默认）或`最新价格` |
| positionMode       | String  | no       | 单向持仓`ONE_WAY`（默认）或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`, 在非单向持仓时为必填项                                                            |
| positionId         | String  | No       | 想要设置的仓位ID。 在逐仓保证金模式为必填项                      |

### 响应内容

| 名称          | 类型    | 是否必需 | 描述 |
| ---           | ---     | ---      | --- |
| symbol        | String  | Yes       | 市场交易对 |
| clOrderID     | String  | Yes       | 交易员发送的客户标签 |
| orderID       | String  | Yes       | 订单ID |
| orderType     | String  | Yes       | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: 算法订单 |
| postOnly      | Boolean  | Yes       | 指示订单是否为只做Maker(Post only) 订单  |
| price         | Double  | Yes       | 订单价格 |
| side          | String  | Yes       | 交易方向: [`BUY`, `SELL`] |
| status        | Integer  | Yes       | 订单状态<br/>2: 订单已插入<br/>3: 订单已成交<br/>4: 订单已完全成交<br/>5: 订单部分成交<br/>6: 订单已取消<br/>7: 订单已退款<br/>9: 触发已插入<br>10: 触发已激活<br>15: 订单已拒绝<br>16: 未找到订单<br>17: 请求失败<br/>請参照[`API Enum`](#api-enum) |
| time_in_force | String  | Yes       | 订单有效期 |
| timestamp     | Long  | Yes       | 订单时间戳  |
| trigger       | Boolean  | Yes       | 指示订单是否为触发订单 |
| triggerPrice  | Double  | Yes       | 订单触发价格，如果订单不是触发订单，则返回0 |
| avgFilledPrice  | Double  | Yes       | 平均成交价格。对于部分成交订单，返回平均成交价格 |
| message       | String  | Yes       | 交易消息  |
| stealth       | String  | Yes       | 仅适用于算法订单 |
| deviation     | Double  | Yes       | 仅适用于算法订单 |
| remainingSize | Integer  | Yes      | 剩余订单数量 = 当前订单数量 - 已成交数量|
| originalOrderSize      | Integer  | Yes      | 原始订单数量。即使后续有调整，此值也不会变化|
| currentOrderSize      | Integer  | Yes      | 当前最新的订单数量，表示已成交数量与未成交剩余数量的总和|
| filledSize          | Integer  | Yes      | 订单已成交的数量|
| totalFilledSize      | Integer  | Yes      | 该订单的累计成交数量|
| positionMode      | String  | Yes      | 仓位模式<br/> 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                                                  |
| positionDirection | String  | Yes      | 仓位方向<br/>  多头仓位`LONG` 或 空头仓位`SHORT`                                                                                                                                                                                                                                                                             |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |

## 查询仓位模式

> 响应

```json
[
    {
        "symbol": "ETH-PERP",
        "positionMode": "HEDGE"
    },
    {
        "symbol": "BTC-PERP",
        "positionMode": "ONE_WAY"
    }
]
```

`GET /api/v2.3/position_mode`

查询用户的仓位模式。需要`读取`权限。

**请求参数**

| Name               | Type    | Required | Description |
| ---                | ---     | ---      | ------------|
| symbol             | String  | No       | 市场交易对    |

**响应内容**

| Name         | Type   | Required | Description                       |
| ---          | ---    | ---      | --- ------------------------------|
| symbol       | String | Yes      | 市场交易对                         |
| positionMode | String | Yes      | 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED` |

## 更改仓位模式

> 响应

```json
{
  "symbol": "BTC-PERP",
  "positionMode": "HEDGE"
}
```

`POST /api/v2.3/position_mode`

更改仓位模式。需要`交易`权限。

**请求参数**

| Name               | Type    | Required | Description                 |
| ---                | ---     | ---      |-----------------------------|
| symbol              | String | Yes      | 市场交易对                       |
| positionMode        | String | Yes      | 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED` |

**响应内容**

| Name      | Type    | Required | Description           |
| ---       | ---     | ---      |-----------------------|
| symbol    | String  | Yes      | 市场交易对                 |
| timestamp | Long    | No       | 订单时间戳                 |
| status    | Integer  | No       | 订单状态 <br>20: 成功       |
| type      | String  | No       | 数值为129，表示为“期货仓位模式更改”。 |
| message   | String  | No       | 交易消息                  |

## 查询用户初始保证金百分比和维持保证金百分比

> 响应

```json
[
    {
        "symbol": "ETH-PERP",
        "initialMarginPercentage": 0.01,
        "maintenanceMarginPercentage": 0.005
    },
    {
        "symbol": "BTC-PERP",
        "initialMarginPercentage": 0.01,
        "maintenanceMarginPercentage": 0.005
    }
]
```

`GET /api/v2.3/user/margin_setting`

查询用户的初始保证金百分比和维持保证金百分比。如果未指定特定的市场符号，则将返回所有市场的保证金百分比。需要`读取`权限。

**请求参数**

| 名称                | 类型     | 是否必须   | 描述    |
| ---                | ---      | ---      | ---     |
| symbol             | String   | 否       | 市场符号  |

**响应内容**

| 名称                         | 类型    | 是否必须 | 描述               |
| ---                         | ---    | ---     | ---                |
| symbol                      | String | 是      | 市场符号            |
| initialMarginPercentage     | Double | 是      | 当前的初始保证金百分比 |
| maintenanceMarginPercentage | Double | 是      | 当前的维持保证金百分比 |

# 钱包端点

## 查询钱包余额

> 响应

```json
[
  {
    "trackingID": 0,
    "queryType": 0,
    "activeWalletName": "String",
    "wallet": "CROSS@",
    "username": "String",
    "walletTotalValue": 0,
    "totalValue": 100,
    "marginBalance": 100,
    "availableBalance": 100,
    "unrealisedProfitLoss": 0,
    "maintenanceMargin": 0,
    "leverage": 0,
    "openMargin": 0,
    "assets": [
      {
        "balance": 0.20183537,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ],
    "assetsInUse": [
      {
        "balance": 0.01,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ]
  }
]
```

`GET /api/v2.3/user/wallet`

查询用户的钱包余额。API密钥需要`读取`权限。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                                                                                                 |
| ---                | ---     | ---      | ---                                                                                                                                                                  |
| wallet             | String  | Yes      | 钱包名称<br/>`CROSS@`: 全仓钱包<br/>`ISOLATED@市场`: 市场指当前符号后附加`-USD`。例如，BTC-PERP的隔离钱包将是`ISOLATED@BTC-PERP-USDT`                                             |

### 响应内容

#### 钱包

| 名称                 | 类型         | 是否必须 | 描述                               |
| ---                  | ---          | ---      | ---                                |
| wallet               | String       | Yes      | 钱包名称                           |
| activeWalletName     | String       | Yes      | 活跃的钱包名称                      |
| queryType            | Integer      | Yes      | 查询类型                           |
| trackingID           | Long         | Yes      | 内部跟踪ID，未被使用                |
| walletTotalValue     | Double       | Yes      | 钱包总值                           |
| totalValue           | Double       | Yes      | 总值                               |
| marginBalance        | Double       | Yes      | 保证金余额                         |
| availableBalance     | Double       | Yes      | 可用余额                           |
| unrealisedProfitLoss | Double       | Yes      | 未实现的利润/损失                  |
| maintenanceMargin    | Double       | Yes      | 维护保证金                         |
| leverage             | Double       | Yes      | 杠杆。在全仓钱包中，此栏位为当前杠杆，而非杠杆设置。|
| openMargin           | Double       | Yes      | 开放保证金                         |
| assets               | Asset 对象   | Yes      | 可用资产                           |
| assetsInUse          | Asset 对象   | Yes      | 使用中的资产                       |

#### 资产 / 使用中的资产

| 名称       | 类型   | 是否必须 | 描述       |
| ---        | ---    | ---      | ---        |
| balance    | Double | Yes      | 余额       |
| assetPrice | Double | Yes      | 资产价格   |
| currency   | String | Yes      | 货币       |


## 查询钱包历史记录

> 响应

```json
[
  {
    "amount": 21.35823825,
    "currency": "USD",
    "description": "String",
    "fees": 0.06,
    "orderId": 20181213000239,
    "status": 10,
    "timestamp": 1571630174639,
    "type": 1,
    "username": "btseUser",
    "wallet": "Wallet",
    "txid": "<Blockchain Transaction ID>",
    "currencyNetwork": "<Blockchain currency network>"
  }
]
```

`GET /api/v2.3/user/wallet_history`

获取期货钱包上的用户钱包历史记录。需要`读取`权限。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                                                                                                              |
| ---                | ---     | ---      | ---                                                                                                                                                                               |
| wallet             | String  | No       | 钱包，如果未指定将返回所有钱包。有效值为：<br/>`CROSS@`: 全仓钱包<br/>`ISOLATED@BTC-PERP-USDT`: 隔离钱包                                                                                        |
| startTime          | Long    | No       | 以毫秒为单位的开始时间（例如 1624987283000）                                                                                                                                       |
| endTime            | Long    | No       | 以毫秒为单位的结束时间（例如 1624987283000）                                                                                                                                       |
| count              | Integer | No       | 要返回的记录数量                                                                                                                                                                  |


### 响应内容

| 名称        | 类型    | 是否必须 | 描述                                                                                                              |
| ---         | ---     | ---      | ---                                                                                                               |
| currency    | String  | Yes      | 货币                                                                                                              |
| amount      | Double  | Yes      | 记录中的金额                                                                                                       |
| fees        | Double  | Yes      | 如有收费                                                                                                          |
| orderId     | String  | Yes      | 内部钱包订单ID                                                                                                     |
| wallet      | String  | Yes      | 钱包类型。对于期货将返回 `CROSS@` 或 `ISOLATED@`                                                                   |
| description | String  | Yes      | 交易描述                                                                                                          |
| status      | Integer | Yes      | 1: 待处理<br/>2: 处理中<br/>10: 完成<br/>16: 取消                                                                  |
| type        | Integer | Yes      | 105: 钱包转账<br/>106: 钱包清算<br/>108: 已实现的PnL<br/>110: 资金<br/>121: 资产转换                                |

## 查询统一期货钱包保证金

> 响应

```json
{
  "symbol": "BTC-PERP",
  "walletTotalValue": 1535.10700567,
  "walletTotalUnrealizedProfitLoss": -49.90799449,
  "futuresTotalAvailableBalance": 1836.521306109,
  "wallets": [
    {
      "activeWalletName": "VIRTUAL|5@BTC-PERP-USDT#4",
      "unrealisedProfitLoss": 49.88502177,
      "walletTotalValue": 956.43166194,
      "marginBalance": 1006.31668371,
      "availableBalance": 993.201492938,
      "maintenanceMargin": 13.115190772
    }
  ]
}
```

`GET /api/v2.3/user/unifiedWallet/margin`

**此 API 适用于已升级钱包的用户**

获取指定钱包或仓位的保证金信息。需要`读取`权限。


### 请求参数

| 名称         | 类型     | 是否必须   | 描述      |
|------------|--------|--------|---------|
| symbol     | String | No     | 市场交易对   |
| positionId | String | No     | 仓位唯一ID  |

### 响应内容

| 名称         | 类型     | 是否必须   | 描述      |
|---------------------------------|---------------|---------|---------|
| symbol                          | String        | Yes     | 市场交易对   |
| walletTotalValue                | Double        | Yes     | 钱包总价值   |
| walletTotalUnrealizedProfitLoss | Double        | Yes     | 钱包总浮动盈亏 |
| futuresTotalAvailableBalance    | Double        | Yes     | 钱包总可用余额 |
| wallets                         | Wallet Object | Yes     | 钱包详情    |

#### 钱包详情

| Name                 | Type        | Require | Description |
|----------------------|-------------|---------|-------------|
| activeWalletName     | String      | Yes     | 钱包名称        |
| unrealisedProfitLoss | Double      | Yes     | 钱包浮动盈亏      |
| walletTotalValue     | Double      | Yes     | 钱包总价值       |
| marginBalance        | Double      | Yes     | 保证金余额       |
| availableBalance     | Double      | Yes     | 可用余额        |
| maintenanceMargin    | Double      | Yes     | 维持保证金       |


## 查询钱包保证金

> 响应

```json
[
  {
    "trackingID": 0,
    "requestId": 0,
    "queryType": 0,
    "wallet": "CROSS@",
    "walletTotalValue": 0,
    "totalValue": 100,
    "marginBalance": 100,
    "availableBalance": 100,
    "unrealisedProfitLoss": 0,
    "maintenanceMargin": 0,
    "leverage": 0,
    "openMargin": 0,
    "assets": [
      {
        "balance": 0.20183537,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ],
    "assetsInUse": [
      {
        "balance": 0.01,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ]
  }
]
```

`GET /api/v2.3/user/margin`

已升级至统一钱包的用户无法使用此 API。请使用 [`统一期货钱包`](#7877d0f154)

获取指定钱包的保证金信息，以便用户知道他们当前在市场上使用的是哪个钱包。需要`读取`权限。

### 请求参数

| 名称                | 类型    | 是否必须   | 描述                         |
| ---                | ---     | ---      | ---                          |
| symbol             | String  | Yes      | 市场符号                      |

### 响应内容

#### 钱包

| 名称                 | 类型         | 是否必须 | 描述                              |
| ---                  | ---          | ---      | ---                               |
| wallet               | String       | Yes      | 钱包名称                          |
| queryType            | Integer      | Yes      | 查询类型                          |
| trackingID           | Long         | Yes      | 内部跟踪ID，未被使用               |
| requestId            | Long         | Yes      | 内部請求ID，未被使用               |
| walletTotalValue     | Double       | Yes      | 钱包总值                          |
| totalValue           | Double       | Yes      | 总值                              |
| marginBalance        | Double       | Yes      | 保证金余额                        |
| availableBalance     | Double       | Yes      | 可用余额                          |
| unrealisedProfitLoss | Double       | Yes      | 未实现的利润/损失                 |
| maintenanceMargin    | Double       | Yes      | 维护保证金                        |
| leverage             | Double       | Yes      | 杠杆                              |
| openMargin           | Double       | Yes      | 开放保证金                        |
| assets               | Asset 对象   | Yes      | 可用资产                          |
| assetsInUse          | Asset 对象   | Yes      | 使用中的资产                      |

#### 资产 / 使用中的资产

| 名称       | 类型   | 是否必须 | 描述       |
| ---        | ---    | ---      | ---        |
| balance    | Double | Yes      | 余额       |
| assetPrice | Double | Yes      | 资产价格   |
| currency   | String | Yes      | 货币       |

## 在期货钱包之间转账资金

> 请求

```json
{
  "walletSrc": "",
  "walletSrcType": "SPOT",
  "walletDest": "",
  "walletDestType": "CROSS",
  "apiWallets": [
    {
      "currency": "USD",
      "allBalance": true
    },
    {
      "currency": "BTC",
      "allBalance": true
    }
  ]
}
```

> 响应

```json
[
  {
    "trackingID": 0,
    "queryType": 0,
    "activeWalletName": "",
    "wallet": "CROSS@",
    "username": "String",
    "walletTotalValue": 0,
    "totalValue": 100,
    "marginBalance": 100,
    "availableBalance": 100,
    "unrealisedProfitLoss": 0,
    "maintenanceMargin": 0,
    "leverage": 0,
    "openMargin": 0,
    "assets": [
      {
        "balance": 0.20183537,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ],
    "assetsInUse": [
      {
        "balance": 0.01,
        "assetPrice": 7158.844999999999,
        "currency": "BTC"
      }
    ]
  }
]
```

`POST /api/v2.3/user/wallet/transfer`

在用户的钱包之间转移资金。用户可以指定源钱包和目标钱包进行资金转账。需要`转账`权限。

### 请求参数

#### 钱包请求

| 名称           | 类型          | 是否必须 | 描述                                                                                                            |
| ---            | ---           | ---      | ---                                                                                                          |
| walletSrc      | String        | No       | 源钱包，如果`walletSrcType`为`ISOLATED`则为必须                                                                 |
| walletSrcType  | String        | Yes      | 源类型，有效值为：<br/>`SPOT`：现货钱包<br/>`CROSS`：全仓钱包<br/>`ISOLATED`：市场的隔离钱包，其中市场为市场符号   |
| walletDest     | String        | No       | 目标钱包，如果`walletDestType`为`ISOLATED`则为必须                                                               |
| walletDestType | String        | Yes      | 目标类型，有效值为：<br/>`SPOT`：现货钱包<br/>`CROSS`：全仓钱包<br/>`ISOLATED`：市场的隔离钱包，其中市场为市场符号 |
| apiWallets     | 钱包明细       | Yes      | 转账详细信息                                                                                                   |

#### 钱包明细请求

| 名称       | 类型   | 是否必须 | 描述                                                                     |
| ---        | ---    | ---      | ---                                                                      |
| currency   | String | Yes      | 钱包货币                                                                 |
| allBalance | Boolean| Yes      | 是否转移所有钱包余额的指示符                                               |
| balance    | Double | No       | 要转移的余额值，例如：10                                                  |


### 响应内容

#### 钱包

| 名称                 | 类型         | 是否必须 | 描述                              |
| ---                  | ---          | ---      | ---                               |
| wallet               | String       | Yes      | 钱包名称                          |
| activeWalletName     | String       | Yes      | 活跃的钱包名称                     |
| queryType            | Integer      | Yes      | 查询类型                          |
| trackingID           | Long         | Yes      | 内部跟踪ID，未被使用               |
| walletTotalValue     | Double       | Yes      | 钱包总值                          |
| totalValue           | Double       | Yes      | 总值                              |
| marginBalance        | Double       | Yes      | 保证金余额                        |
| availableBalance     | Double       | Yes      | 可用余额                          |
| unrealisedProfitLoss | Double       | Yes      | 未实现的利润/损失                 |
| maintenanceMargin    | Double       | Yes      | 维护保证金                        |
| leverage             | Double       | Yes      | 杠杆                              |
| openMargin           | Double       | Yes      | 开放保证金                        |
| assets               | 资产对象     | Yes      | 可用资产                          |
| assetsInUse          | 资产对象     | Yes      | 使用中的资产                      |

#### 资产 / 使用中的资产

| 名称       | 类型   | 是否必须 | 描述       |
| ---        | ---    | ---      | ---        |
| balance    | Double | Yes      | 余额       |
| assetPrice | Double | Yes      | 资产价格   |
| currency   | String | Yes      | 货币       |


## 子账户钱包转账

`POST /api/v2.3/subaccount/wallet/transfer`

在用户和子账户钱包之间转移资金。用户可以指定源钱包和目标钱包进行资金转账。

需要`钱包`权限。要获取支持的货币列表，请查看[用于操作的可用货币列表](#查询钱包操作的可用货币列表)。

### 请求参数

#### 钱包请求

| 名称           | 类型          | 是否必须 | 描述                                                                                                                                                                                                  |
|----------------| ---           | ---      | ---                                                                                                                                                                                                  |
| walletSrc      | String        | No       | 源钱包，如果`walletSrcType`为`ISOLATED`则为必须                                                                 |
| walletSrcType  | String        | Yes      | 源类型，有效值为：<br/>`SPOT`：现货钱包<br/>`CROSS`：全仓钱包<br/>`ISOLATED`：市场的隔离钱包，其中市场为市场符号   |
| walletDest     | String        | No       | 目标钱包，如果`walletDestType`为`ISOLATED`则为必须                                                               |
| walletDestType | String        | Yes      | 目标类型，有效值为：<br/>`SPOT`：现货钱包<br/>`CROSS`：全仓钱包<br/>`ISOLATED`：市场的隔离钱包，其中市场为市场符号 |
| fromUser       | String        | Yes      | 源用户名                                                                                                                                                                                            |
| receiver       | String        | Yes      | 接收者用户名                                                                                                                                                                                        |
| apiWallets     | 钱包明细       | Yes      | 转账详细信息                                                                                                                                                                                         |

#### 钱包明细请求

| 名称       | 类型   | 是否必须 | 描述                                                                     |
| ---        | ---    | ---      | ---                                                                      |
| currency   | String | Yes      | 钱包货币                                                                 |
| allBalance | Boolean| Yes      | 是否转移所有钱包余额的指示符                                               |
| balance    | Double | No       | 要转移的余额值，例如：10                                                  |


### 响应内容

#### 钱包

| 名称                 | 类型     | 是否必须 | 描述               |
|----------------------|----------|----------|---------------------|
| code                 | Integer  | Yes      | 响应代码            |
| msg                  | String   | Yes      | 响应消息            |
| time                 | Long     | Yes      | 响应时间            |
| data                 | Object   | No       |                     |
| success              | Boolean  | Yes      | 转账是否成功         |


#### 转账错误代码

| 代码  | 描述                                                        |
|-------|-------------------------------------------------------------|
| -2    | 无效的请求参数                                             |
| -1046 | 将fromUser期货资产转移到DestWallet失败                    |
| -1047 | fromUser到receiver的转账失败                               |
| -1048 | receiver现货钱包到期货钱包的转账失败                        |



# 订单簿 WebSocket 数据流

## 端点
  * 生产环境
    * `wss://ws.btse.com/ws/oss/futures`
  * 测试网络
    * `wss://testws.btse.io/ws/oss/futures`

## OSS L1 快照 (按分组)

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "snapshotL1:BTC-PERP_0"
  ]
}

{
  "op": "unsubscribe",
  "args": [
    "snapshotL1:BTC-PERP_0"
  ]
}
```

> 响应

```json
{
  "topic": "snapshotL1:BTC-PERP_0",
  "data": {
    "bids": [
      [
          "28064.9",
          "1268"
      ]
    ],
    "asks": [
      [
          "28065.0",
          "1015"
      ]
    ],
    "type": "snapshotL1",
    "symbol": "BTC-PERP",
    "timestamp": 1680751558529
  }
}
```

通过端点`wss://ws.btse.com/ws/oss/futures`订阅Level 1订单簿。订阅的格式将为`symbol_grouping`。

* `symbol`表示市场符号
* `grouping`表示分组的粒度。有效值为0-8。

### 响应内容

#### 订单簿对象

| 名称   | 类型        | 是否必须 | 描述                    |
| ---    | ---         | ---      | ---                     |
| topic  | String      | Yes      | Websocket主题           |
| data   | 数据对象    | Yes      | 参见下面的数据对象      |

#### 数据对象

| 名称      | 类型        | 是否必须 | 描述                                                                                    |
| ---       | ---         | ---      | ---                                                                                    |
| bids      | 报价对象    | Yes      | 买入报价                                                                                |
| asks      | 报价对象    | Yes      | 卖出报价                                                                                |
| symbol    | String      | Yes      | 市场符号                                                                                |
| type      | String      | Yes      | `snapshotL1` - L1数据指的是交易对订单簿的最佳买入/最佳卖出价。                                   |
| timestamp | Long        | Yes      | 订单簿时间戳                                                                           |

## 订单簿增量更新

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "update:BTC-PERP_0"
  ]
}
```

```json
{
  "op": "unsubscribe",
  "args": [
    "update:BTC-PERP_0"
  ]
}
```

> 响应

```json
{
  "topic": "update:BTC-PERP_0",
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
        "59278.5",
        "0.01472"
      ]
    ],
    "seqNum": 628282,
    "prevSeqNum": 628281,
    "type": "snapshot",
    "timestamp": 1565135165600,
    "symbol": "BTC-PERP"
  }
}
```

```json
{
  "topic": "update:BTC-PERP",
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
    "symbol": "BTC-PERP"
  }
}
```

通过端点`wss://ws.btse.com/ws/oss/futures`订阅订单簿增量更新。主题的格式将为`update:symbol_grouping`（例如`update:BTC-PERP_0`）。首次收到的响应将是当前订单簿的快照（这在`type`字段中有标示），并将返回50个级别。随后的数据包中将发送增量更新，类型为`delta`。

买入和卖出将以`price`和`size`的元组形式发送。发送的大小将是价格的新更新大小。如果发送了一个`0`的值，则应从订单簿的本地副本中删除该价格。

为确保按顺序接收到更新，`seqNum`指示当前序列，而`prevSeqNum`指前一个数据包。`seqNum`总是在`prevSeqNum`之后。如果序列是乱序的，您将需要取消订阅并再次订阅该主题。

如果当最佳买入价高于或等于最佳卖出价时发生[交叉订单簿](https://en.wikipedia.org/wiki/Order_book#Crossed_book)，请取消订阅并重新订阅该主题。

### 响应内容

#### 订单簿对象

| 名称      | 类型       | 是否必须 | 描述                 |
| ---       | ---        | ---      | ---                  |
| topic     | String     | Yes      | Websocket主题        |
| data      | Data Object | Yes      | 参见下面的数据对象   |

#### 数据对象

| 名称       | 类型        | 是否必须 | 描述                                                                                                               |
| ---        | ---         | ---      | ---                                                                                                               |
| bids       | Quote Object | Yes      | 买入报价                                                                                                           |
| asks       | Quote Object | Yes      | 卖出报价                                                                                                           |
| seqNum     | Integer         | Yes      | 当前序列号                                                                                                         |
| prevSeqNum | Integer         | Yes      | 上一个序列号                                                                                                       |
| type       | String      | Yes      | `snapshot` - 订单簿的快照，最多有50个级别<br/> `delta` - 订单簿的更新                                                |
| timestamp  | Long        | Yes      | 订单簿的时间戳                                                                                                     |
| symbol     | String      | Yes      | 订单簿符号                                                                                                         |

#### 订单簿错误响应

| 错误码  | 消息                                                                                                  |
| ---     | ---                                                                                                  |
| 1000    | 提供的市场对当前不受支持。                                                                           |
| 1001    | 提供的操作当前不受支持。                                                                             |
| 1002    | 请求无效。请再次检查您的请求并提供所有所需的信息。                                                   |
| 1005    | 提供的主题不存在。                                                                                   |
| 1007    | 用户消息缓冲区已满。                                                                                 |
| 1008    | 达到最大失败尝试，关闭会话。                                                                         |


# Websocket流

## 端点
  * 生产环境
    * `wss://ws.btse.com/ws/futures`
  * 测试网络
    * `wss://testws.btse.io/ws/futures`

## Ping/Pong
对于我们所有的WebSocket服务器，只需发送一个'ping'消息，如果WebSocket连接已建立并处于活动状态，WebSocket服务器将以'pong'消息进行响应。
> 请求

```
ping
```

> 响应

```
pong
```

## 订阅

以下是一个主题订阅的示例。

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "tradeHistoryApiV3:BTC-PERP"
  ]
}
```

> 响应

```json
{
  "event": "subscribe",
  "channel": [
    "tradeHistoryApiV3:BTC-PERP"
  ]
}
```

订阅Websocket的公开交易成交信息

### 请求参数

| 名称 | 类型  | 是否必须 | 描述                                                                                                       |
| ---  | ---   | ---     | ---                                                                                                       |
| op   | String | Yes     | 操作。`subscribe` 将订阅在`args`中提供的主题。`unsubscribe` 将取消订阅主题                               |
| args | Array  | Yes     | 要订阅的主题。                                                                                             |

### 响应内容

| 名称    | 类型  | 是否必须 | 描述                                       |
| ---     | ---   | ---     | ---                                       |
| event   | String | Yes     | 响应的事件类型                             |
| channel | Array  | Yes     | 已成功订阅的主题                           |




## 公开成交记录

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "tradeHistoryApiV3:BTC-PERP"
  ]
}
```

> 响应 – 订阅确认

```json
{
  "event": "subscribe",
  "channel": [
    "tradeHistoryApiV3:BTC-PERP"
  ]
}
```

> 响应 – 数据通知

```json
{
  "topic": "tradeHistoryApiV3:BTC-PERP",
  "data": [
      {
        "price": 111144.8,
        "size": 152,
        "side": "SELL",
        "symbol": "BTC-PERP",
        "tradeId": 927002515,
        "timestamp": 1752129545326
      }
  ]
}
```

订阅市场的最近交易提要。主题将是 `tradeHistoryApiV3:<market>`，其中`<market>` 是市场符号。

### 响应内容

#### TradeHistory 对象

| 名称  | 类型        | 是否必须 | 描述                             |
| ---   | ---         | ---     | ---                             |
| topic | String      | Yes     | Websocket 主题                   |
| data  | Data Object | Yes     | 请参考下面的数据对象             |

#### 数据对象

| 名称      | 类型   | 是否必须 | 描述                     |
| ---       | ---    | ---      | ---                     |
| symbol    | String | Yes      | 市场符号                 |
| side      | String | Yes      | 交易方向: [`BUY`, `SELL`]   |
| size      | Integer | Yes      | 交易量                   |
| price     | Double | Yes      | 交易价格                 |
| tradeId   | Long   | Yes      | 交易序列号               |
| timestamp | Long   | Yes      | 交易时间戳               |

## 认证

> 请求

```json
{
  "op":"authKeyExpires",
  "args":["APIKey", "nonce", "signature"]
}
```

认证 websocket 会话以订阅已认证的 websocket 主题。假设我们有以下的值:

* `request-nonce`: 1624985375123
* `request-api`: 4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x
* `secret`: 848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx

我們的訂閱請求將是：

```
{
  "op":"authKeyExpires",
  "args":["4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x", "1624985375123", "c410d38c681579adb335885800cff24c66171b7cc8376cfe43da1408c581748156b89bcc5a115bb496413bda481139fb"]
}
```

### 请求参数

以下详细描述了需要发送的参数。

| 索引 | 类型   | 是否必须 | 描述                                   |
| ---  | ---    | ---      | ---                                    |
| 0    | String | Yes       | 第一个参数是 API 密钥                   |
| 1    | Long   | Yes       | Nonce，即当前的时间戳                    |
| 2    | String | Yes       | 生成的签名                             |

> 生成签名

```shell
echo -n "/ws/futures1624985375123"  | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= bd8afb8bee58ba0a2c67f84dcfe6e64d0274f55d064bb26ea84a0fe6dd8c621b541b511982fb0c0b8c244e9521a80ea1
```


## 通知

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "notificationApiV4"
  ]
}
```

> 响应

```json
{
  "topic": "notificationApiV4",
  "data": [
    {
      "symbol": "BTC-PERP",
      "orderID": "45e8bb8d-d708-4a90-a428-c61583f90efe",
      "side": "BUY",
      "orderType": 77,
      "type": 0,
      "price": 111085.1,
      "triggerPrice": 0,
      "pegPriceDeviation": 1,
      "stealth": 1,
      "status": 4,
      "timestamp": 1752147101805,
      "avgFilledPrice": 111085.1,
      "clOrderID": "",
      "postOnly": false,
      "maker": false,
      "positionId": "BTC-PERP-USDT",
      "orderDetailType": null,
      "orderUserInitiated": true,
      "originalOrderSize": 900,
      "currentOrderSize": 900,
      "filledSize": 900,
      "totalFilledSize": 900,
      "remainingSize": 0,
      "time_in_force": "GTC"
    }
  ]
}

```

接收交易通知，请订阅 `notificationApiV3`或 `notificationApiV4` 主题。建议使用 `notificationApiV4`，它包含与订单数量变动（例如：原始数量、已成交数量、剩余数量）相关的结构化且定义清晰的字段，有助于与最新的 API 字段更新保持更好的一致性。
WebSocket 将向已认证的订阅者推送实时交易级别的通知。Websocket将向订阅者推送交易级别的通知。如果在未经认证的情况下订阅主题，将不会发送任何消息。

### 响应内容

| 名称              | 类型    | 必须 | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---               | ---     | ---  | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| symbol            | String  | Yes      | 市场符号                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| orderID           | String  | Yes      | 内部订单ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| side              | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| type              | Integer     | Yes      | 订单类型。有效值为：<br/>76: 限价订单<br/>77: 市价订单<br/>80: 算法订单                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| price             | Double  | Yes      | 订单价格或交易价格                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| originalOrderSize              | Integer  | Yes      | 原始订单数量。即使后续有调整，此值也不会变化                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| currentOrderSize      | Integer  | Yes      | 当前最新的订单数量，表示已成交数量与未成交剩余数量的总和                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| avgFilledPrice    | Double  | Yes      | 平均成交价格                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| filledSize          | Integer  | Yes      | 订单已成交的数量                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| totalFilledSize          | Integer  | Yes      | 该订单的累计成交数量                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| status            | Integer | Yes      | 状态值如下：<br/>1: 市场不可用<br/>2: 订单成功插入<br/>4: 订单全部交易<br/>5: 订单部分交易<br/>6: 订单成功取消<br/>8: 账户余额不足<br/>9: 触发订单成功插入<br/>10: 触发订单成功激活<br/>12: 更新风险限额时出错<br/>15: 订单被拒绝<br/>20: 交易成功完成<br/>27: 期货和现货之间转账成功<br/>28: 期货和现货之间转账失败<br/>41: 指定了无效的风险限额<br/>64: 账户正在进行清算<br/>96: 设置期货结算货币<br/>101: 期货订单超出清算价格<br/>305: 价格超过开放订单范围<br/>1003: 订单正在清算<br/>1004: 订单正在ADL<br/>請参照[`API Enum`](#api-enum) |
| clOrderID         | String  | Yes      | 自定义订单ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| maker             | Boolean | Yes      | 指示交易是否为做市商交易                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| remainingSize     | Integer  | Yes      | 订单上的剩余大小                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| time_in_force     | String  | Yes      | 订单的有效期                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| timestamp         | Long    | Yes      | 订单时间戳或交易时间戳                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| txType            | String  | Yes      | 用于触发或OCO订单。STOP 表示它是一个停止订单，TAKEPROFIT 表示它是一个止盈订单，LIMIT 表示它不是上述任何一个                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| stealth           | Double  | Yes      | 在订单簿上显示的订单百分比。仅用于算法订单                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| pegPriceDeviation | Double  | Yes      | 偏差百分比。仅用于算法订单                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |

## 用户交易记录

> 请求

```json
{
  "op":"subscribe",
  "args":["fillsV2"]
}
```

> 响应

```json
{
    "topic": "fillsV2",
    "id": "",
    "data": [
        {
            "orderId": "6aa36da1-0ed8-46c1-9327-c9d6313b3d12",
            "serialId": 189349157,
            "clOrderId": "_W_ekxogc1711427518228",
            "type": "77",
            "symbol": "BTC-PERP",
            "side": "BUY",
            "price": "69704.4",
            "size": "1.0",
            "feeAmount": "0.0348522",
            "feeCurrency": "USDT",
            "base": "BTC-PERP",
            "quote": "USDT",
            "maker": false,
            "timestamp": 1711427518338,
            "contractSize": 0.0001,
            "tradeId": "e094117f-9f84-4c82-b55d-d3d2a54d0dca"
        }
    ]
}


```

当交易完成后，此主题将把交易信息发回给订阅者。

### 响应内容

| 名称        | 类型    | 必须 | 描述                                                                                                      |
| ---         | ---     | ---  | ---                                                                                                      |
| symbol      | String  | Yes      | 市场符号                                                                                                  |
| orderId     | String  | Yes      | 内部订单ID                                                                                                |
| clOrderId   | String  | Yes      | 自定义订单ID                                                                                              |
| serialId    | Long    | Yes      | 交易序列ID                                                                                                |
| tradeId     | String  | Yes      | 交易唯一标识符                                                                                            |
| type        | Integer     | Yes      | 订单类型。有效值为：<br/>76: 限价订单<br/>77: 市价订单<br/>80: 算法订单                                   |
| side        | String  | Yes      | 交易方向: [`BUY`, `SELL`]                                                                                     |
| price       | Double  | Yes      | 交易价格                                                                                                  |
| size        | Double  | Yes      | 交易大小                                                                                                  |
| feeAmount   | Double  | Yes      | 所收费用                                                                                                  |
| feeCurrency | String  | Yes      | 费用货币                                                                                                  |
| base        | String  | Yes      | 基础货币                                                                                                  |
| quote       | String  | Yes      | 报价货币                                                                                                  |
| maker       | Boolean | Yes      | 指示交易是否为做市商交易                                                                                  |
| timestamp   | Long    | Yes      | 订单时间戳或交易时间戳                                                                                    |

## 所有仓位

> 请求

```json
{
  "op":"subscribe",
  "args":["allPositionV4"]
}
```

> 响应

```json
{
  "topic": "allPositionV4",
  "data": [
    {
      "requestId": 0,
      "username": "demonleader",
      "userCurrency": null,
      "marketName": "BTC-PERP-USDT",
      "orderType": 90,
      "orderMode": 66,
      "status": 65,
      "originalAmount": 0.00001,
      "maxPriceHeld": 0,
      "pegPriceMin": 0,
      "stealth": 1,
      "baseCurrency": null,
      "quoteCurrency": null,
      "quoteCurrencyFiat": false,
      "parents": null,
      "makerFeesRatio": null,
      "takerFeesRatio": [
        0.00055
      ],
      "orderID": "72528866-cd9b-4472-a06b-b2d5c5766f5f",
      "vendorName": null,
      "botID": null,
      "maxStealthDisplayAmount": 0,
      "sellexchangeRate": 0,
      "tag": null,
      "triggerPrice": 116682.3,
      "closeOrder": true,
      "dbBaseBalHeld": 0,
      "dbQuoteBalHeld": -5.738340149,
      "isFuture": true,
      "liquidationInProgress": false,
      "marginType": 91,
      "entryPrice": 111126,
      "liquidationPrice": 0,
      "markedPrice": 111115.5,
      "marginHeld": 0,
      "unrealizedProfitLoss": -0.094395,
      "totalMaintenanceMargin": 5.643945149,
      "totalContracts": 899,
      "marginChargedLongOpen": 0,
      "marginChargedShortOpen": 0,
      "unchargedMarginLongOpen": 0,
      "unchargedMarginShortOpen": 0,
      "isolatedCurrency": null,
      "isolatedLeverage": 0,
      "totalFees": 0,
      "totalValue": 998.928345,
      "adlScoreBucket": 1,
      "adlScorePercentile": 0.0070422535,
      "orderTypeName": "TYPE_FUTURES_POSITION",
      "orderModeName": "MODE_BUY",
      "marginTypeName": "FUTURES_MARGIN_CROSS",
      "currentLeverage": 0.009991421,
      "contractSize": 0.00001,
      "minimumRequiredMargin": 0,
      "filledSize": 0,
      "takeProfitOrder": {
        "orderId": "72528866-cd9b-4472-a06b-b2d5c5766f5f",
        "side": "SELL",
        "triggerPrice": 116682.3,
        "triggerUseLastPrice": false
      },
      "stopLossOrder": {
        "orderId": "dbd9cdb7-6b04-49e0-990a-7c21a87486e5",
        "side": "SELL",
        "triggerPrice": 110014.7,
        "triggerUseLastPrice": false
      },
      "positionId": "BTC-PERP-USDT",
      "activeWalletName": "CROSS@",
      "positionMode": "ONE_WAY",
      "positionDirection": "LONG",
      "serviceType": 0,
      "avgFilledPrice": 0,
      "future": true,
      "settleWithNonUSDAsset": "USDT"
    }
  ]
}
```

一旦仓位发生变化，所有期货仓位将通过这个主题推送。

### 响应内容

| 名称                    | 类型    | 必须 | 描述                                              |
| ---                     | ---     | ---  | ---                                              |
| requestId               | Integer | Yes      | 请求ID                                            |
| username                | String  | Yes      | btse 用户名                                        |
| marketName              | String  | Yes      | 市场名称                                           |
| orderType               | Integer | Yes      | 90: 期货头寸                                        |
| orderTypeName           | String  | Yes      | orderType的字符串表示                               |
| orderMode               | Integer | Yes      | 66: 买入<br/>83: 卖出                               |
| orderModeName           | String  | Yes      | orderModeName的字符串表示                           |
| originalAmount          | Double  | Yes      | 订单金额                                           |
| maxPriceHeld            | Double  | Yes      | 历史最高价格                                        |
| pegPriceMin             | Double  | Yes      | peg最小价格                                         |
| stealth                 | Double  | Yes      | 用于peg订单                                         |
| orderID                 | String  | Yes      | 订单ID                                              |
| maxStealthDisplayAmount | Double  | Yes      | 用于peg订单                                         |
| sellexchangeRate        | Double  | Yes      |                                                    |
| triggerPrice            | Double  | Yes      | OCO订单                                             |
| closeOrder              | Boolean | Yes      | 是否有关闭此持仓的订单
| liquidationInProgress   | Boolean | Yes      | 是否正在清算                                        |
| marginType              | Integer | Yes      | 钱包类型：<br/>91: 全仓<br/>92: 隔离                    |
| marginTypeName          | String  | Yes      | marginType的字符串表示                               |
| entryPrice              | Double  | Yes      | 进场价格                                            |
| liquidationPrice        | Double  | Yes      | 清算价格                                            |
| markPrice               | Double  | Yes      | 标记价格                                            |
| unrealizedProfitLoss    | Double  | Yes      | 未实现的利润和损失                                    |
| totalMaintenanceMargin  | Double  | Yes      | 维护保证金                                           |
| totalContract           | Double  | Yes      | 合约的大小                                           |
| isolatedLeverage        | Double  | Yes      |                                                    |
| totalFees               | Double  | Yes      |                                                    |
| totalValue              | Double  | Yes      |                                                    |
| adlScoreBucket          | Double  | Yes      |                                                    |
| currentLeverage         | Double  | Yes      |                                                    |
| avgFilledPrice            | Double  | Yes      |                                                    |
| settleWithNonUSDAsset   | String  | Yes      |                                                    |
| takeProfitOrder | TakeProfitOrder对象 | No | 止盈订单信息                                            |
| stopLossOrder | StopLossOrder对象 | No | 止损订单信息                                                |
| positionMode      | String  | Yes      | 仓位模式<br/> 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                                                  |
| positionDirection | String  | Yes      | 仓位方向<br/>  多头仓位`LONG` 或 空头仓位`SHORT`                                                                                                                                                                                                                                                                             |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |
| contractSize            | Double  | Yes      | 仓位合约规模                   |

## 仓位

> 请求

```json
{
  "op":"subscribe",
  "args":["positionsV3"]
}
```
> 响应

```json
{
  "topic": "positionsV3",
  "data": [
    {
      "requestId": 0,
      "username": "demonleader",
      "userCurrency": null,
      "marketName": "QA-PERP-USDT",
      "orderType": 90,
      "orderMode": 66,
      "status": 65,
      "originalAmount": 0.01,
      "maxPriceHeld": 0,
      "pegPriceMin": 0,
      "stealth": 1,
      "baseCurrency": null,
      "quoteCurrency": null,
      "quoteCurrencyFiat": false,
      "parents": null,
      "makerFeesRatio": null,
      "takerFeesRatio": [
        0.00055
      ],
      "orderID": null,
      "vendorName": null,
      "botID": null,
      "maxStealthDisplayAmount": 0,
      "sellexchangeRate": 0,
      "tag": null,
      "triggerPrice": 0,
      "closeOrder": false,
      "dbBaseBalHeld": 0,
      "dbQuoteBalHeld": -56.4435,
      "isFuture": true,
      "liquidationInProgress": false,
      "marginType": 91,
      "entryPrice": 1500,
      "liquidationPrice": 0,
      "markedPrice": 1500,
      "marginHeld": 0,
      "unrealizedProfitLoss": 0,
      "totalMaintenanceMargin": 56.4435,
      "totalContracts": 666,
      "marginChargedLongOpen": 0,
      "marginChargedShortOpen": 0,
      "unchargedMarginLongOpen": 0,
      "unchargedMarginShortOpen": 0,
      "isolatedCurrency": null,
      "isolatedLeverage": 0,
      "totalFees": 0,
      "totalValue": 9990,
      "adlScoreBucket": 2,
      "adlScorePercentile": 0.75,
      "orderTypeName": "TYPE_FUTURES_POSITION",
      "orderModeName": "MODE_BUY",
      "marginTypeName": "FUTURES_MARGIN_CROSS",
      "currentLeverage": 0.0999085912,
      "contractSize": 0.01,
      "minimumRequiredMargin": 0,
      "filledSize": 0,
      "takeProfitOrder": null,
      "stopLossOrder": null,
      "positionId": "QA-PERP-USDT",
      "activeWalletName": "CROSS@",
      "positionMode": "ONE_WAY",
      "positionDirection": "LONG",
      "serviceType": 0,
      "avgFilledPrice": 0,
      "settleWithNonUSDAsset": "USDT",
      "future": true
    }
  ]
}
```

> 响应 (仓位已关闭)

```json
{
  "topic": "positionsV3",
  "data": [
    {
      "requestId": 0,
      "username": "demonleader",
      "userCurrency": null,
      "marketName": "QA-PERP-USDT",
      "orderType": 0,
      "orderMode": 0,
      "status": 65,
      "originalAmount": 0,
      "maxPriceHeld": 0,
      "pegPriceMin": 0,
      "stealth": 0,
      "baseCurrency": null,
      "quoteCurrency": null,
      "quoteCurrencyFiat": false,
      "parents": null,
      "makerFeesRatio": null,
      "takerFeesRatio": null,
      "orderID": null,
      "vendorName": null,
      "botID": null,
      "maxStealthDisplayAmount": 0,
      "sellexchangeRate": 0,
      "tag": null,
      "triggerPrice": 0,
      "closeOrder": false,
      "dbBaseBalHeld": 0,
      "dbQuoteBalHeld": 0,
      "isFuture": false,
      "liquidationInProgress": false,
      "marginType": 0,
      "entryPrice": 0,
      "liquidationPrice": 0,
      "markedPrice": 0,
      "marginHeld": 0,
      "unrealizedProfitLoss": 0,
      "totalMaintenanceMargin": 0,
      "totalContracts": 0,
      "marginChargedLongOpen": 0,
      "marginChargedShortOpen": 0,
      "unchargedMarginLongOpen": 0,
      "unchargedMarginShortOpen": 0,
      "isolatedCurrency": null,
      "isolatedLeverage": 0,
      "totalFees": 0,
      "totalValue": 0,
      "adlScoreBucket": 0,
      "adlScorePercentile": 0,
      "orderTypeName": null,
      "orderModeName": null,
      "marginTypeName": null,
      "currentLeverage": 0,
      "contractSize": 0,
      "minimumRequiredMargin": 0,
      "filledSize": 0,
      "takeProfitOrder": null,
      "stopLossOrder": null,
      "positionId": "QA-PERP-USDT",
      "activeWalletName": null,
      "positionMode": null,
      "positionDirection": null,
      "serviceType": 0,
      "avgFilledPrice": 0,
      "settleWithNonUSDAsset": "USD",
      "future": false
    }
  ]
}
```

一旦仓位发生变化，所有期货仓位将通过这个主题推送。如果用户将仓位减少到0，该主题将推送一次totalContracts值为0的数据。

### 响应内容

| 名称                    | 类型    | 是否必须  | 描述                                  |
| ---                     | ---     | ---      | ---                                    |
| requestId               | Integer | Yes      | 请求ID                                |
| username                | String  | Yes      | btse 用户名                            |
| marketName              | String  | Yes      | 市场名称                              |
| orderType               | Integer | Yes      | 90: 期货仓位                          |
| orderTypeName           | String  | Yes      | orderType的字符串表示                  |
| orderMode               | Integer | Yes      | 66: 买入<br/>83: 卖出                 |
| orderModeName           | String  | Yes      | orderModeName的字符串表示              |
| originalAmount          | Double  | Yes      | 订单数量                              |
| maxPriceHeld            | Double  | Yes      | 历史最高价                            |
| pegPriceMin             | Double  | Yes      | Peg最低价                             |
| stealth                 | Double  | Yes      | 用于peg订单                           |
| orderID                 | String  | Yes      | 订单ID                                |
| maxStealthDisplayAmount | Double  | Yes      | 用于peg订单                           |
| sellexchangeRate        | Double  | Yes      |                                        |
| triggerPrice            | Double  | Yes      | OCO订单                               |
| closeOrder              | Boolean | Yes      | 是否有一个订单来关闭此仓位            |
| liquidationInProgress   | Boolean | Yes      | 是否正在进行清算                      |
| marginType              | Integer | Yes      | 钱包类型:<br/>91: 全仓<br/>92: 隔离仓  |
| marginTypeName          | String  | Yes      | marginType的字符串表示                |
| entryPrice              | Double  | Yes      | 入场价格                              |
| liquidationPrice        | Double  | Yes      | 清算价格                              |
| markPrice               | Double  | Yes      | 标记价格                              |
| unrealizedProfitLoss    | Double  | Yes      | 未实现盈亏                            |
| totalMaintenanceMargin  | Double  | Yes      | 维护保证金                            |
| totalContract           | Double  | Yes      | 合约的大小                            |
| isolatedLeverage        | Double  | Yes      |                                        |
| totalFees               | Double  | Yes      |                                        |
| totalValue              | Double  | Yes      |                                        |
| adlScoreBucket          | Double  | Yes      |                                        |
| currentLeverage         | Double  | Yes      |                                        |
| avgFilledPrice            | Double  | Yes      |                                        |
| settleWithNonUSDAsset   | String  | Yes      |                                        |
| takeProfitOrder         | TakeProfitOrder object | No       | 止盈订单信息              |
| stopLossOrder           | StopLossOrder object   | No       | 止损订单信息              |
| positionMode      | String  | Yes      | 仓位模式<br/> 单向持仓`ONE_WAY` 或  双向持仓`HEDGE` 或 逐仓保证金模式`ISOLATED`                                                                                                                                                                                                                                                                                  |
| positionDirection | String  | Yes      | 仓位方向<br/>  多头仓位`LONG` 或 空头仓位`SHORT`                                                                                                                                                                                                                                                                             |
| positionId        | String  | Yes      | 当前订单属于的仓位ID。                                                                                                                                                                                                                                                                             |
| contractSize            | Double  | Yes      | 仓位合约规模                   |

</section>
