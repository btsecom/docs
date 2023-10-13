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

## 版本 2.6.10（2023年10月3日）
* 修正响应数据类型

## 版本 2.6.9（2023年9月11日）
* 添加 [`get-leverage`](#get-leverage) 以获取市场杠杆

## 版本 2.6.8（2023年9月3日）
* 从 [`amend-order`](#amend-order) 中移除滑动参数

## 版本 2.6.7（2023年8月29日）
* 在 [`API状态代码`](#api-status-codes) 中添加 451 状态代码，并将 [`订单簿Websocket流`](#order-book-websocket-streams) 设置为独立段落

## 版本 2.6.6（2023年8月28日）
* 在 [`平仓`](#close-position) 中添加 postOnly 参数

## 版本 2.6.5（2023年7月27日）
* 我们在期货市场中引入了一个新的产品：1,000 Floki 永续期货合约（1KFLOKI-PERP 或 1KFLOKIPFC）

## 版本 2.6.4（2023年6月7日）
* 将 [`钱包/转账链接`](#transfer-funds-between-futures-wallet) 从 /api/v2.1/wallet/transfer 更新为 /api/v2.1/user/wallet/transfer

## 版本 2.6.3（2023年6月6日）
* 更新 [`钱包详情请求`](#wallet-detail-request) 的格式

## 版本 2.6.2（2023年5月29日）
* 更新订单簿流服务（OSS）的错误消息格式。计划生效日期为 `2023年6月6日，上午10:00（UTC+0）`。
  * 之前
    ```
    {
        "severity": "ERROR",
        "error": [
            {
                "arg": "update:BTCC-USD_0",
                "errorCode": "MARKET_PAIR_NOT_SUPPORT"
            }
        ]
    }
    ```
  * 之后
    ```
    {
        "severity": "ERROR",
        "errors": [
            {
                "arg": "update:BTCC-USD_0",
                "error": {
                    "code": 1000,
                    "message": "Market pair provided is currently not supported."
                }
            }
        ]
    }
    ```


## 版本 2.6.1（2023年5月24日）

* 在 [`按分组排序的订单簿`](#orderbook-by-grouping) 上添加 group 参数

## 版本 2.6.0（2023年5月17日）

* 添加 [`Ping/Pong`](#ping-pong) 用于现货流

## 版本 2.5.9（2023年4月21日）

* 添加 [获取风险限制](#get-risk-limit)
* 添加 [子账户钱包转账](#sub-account-wallet-trasnsfer)

## 版本 2.5.8（2023年4月12日）
* 弃用两个 WebSocket 主题 `现货订单簿快照（按分组）` 和 `现货订单簿快照（按深度）` 今日起。
请使用以下 WebSocket 主题通过端点 `wss://ws.btse.com/ws/oss/futures` 获取订单簿数据
  - [现货订单簿增量更新](#orderbook-incremental-updates)
  - [OSS L1 快照（按分组）](#oss-l1-snapshot-by-grouping)

## 版本 2.5.7（2023年4月6日）

* 添加 [OSS L1 快照（按分组）](#oss-l1-snapshot-by-grouping)

## 版本 2.5.6（2023年3月29日）

* [重要通知] BTSE 将于 **2023年4月** 更改现货市场命名约定，以为零售用户提供更多明确性，规则如下：
  - 将永续市场的后缀从 `PFC` 更改为 `PERP`（例如：BTCPFC -> BTC-PERP）
  - 将基于时间的市场的后缀从 `交割月份 + 年份` 更改为 `结算日期（YYMMDD）`（例如：BTCM23 -> BTC-230630）
  - [参考链接](https://www.btse.com/blog/important-notice-upcoming-changes-to-futures-risk-limits-and-contract-names/)
  - 期货 API 已更新（通常添加了一个新的可选参数 `useNewSymbolNaming`，以指定市场名称是否采用新格式）：
    - [`市场摘要`](#market-summary)
    - [`查询未完成订单`](#query-open-orders)
    - [`按分组排序的订单簿`](#orderbook-by-grouping)
    - [`订单簿`](#orderbook)
    - [`图表数据`](#charting-data)
    - [`查询钱包历史`](#query-wallet-history)
    - [`查询钱包余额`](#query-wallet-balance)
    - [`设置杠杆`](#set-leverage)
    - [`获取杠杆`](#get-leverage)
    - [`设置风险限制`](#set-risk-limit)
    - [`查询市场价格`](#query-market-price)
    - [`更改合同结算货币`](#change-contract-settlement-currency)
    - [`查询账户费用`](#query-account-fee)
    - [`查询持仓`](#query-position)
    - [`关闭持仓`](#close-position)
    - [`查询钱包保证金`](#query-wallet-margin)
    - [`创建新订单`](#create-new-order)
    - [`查询交易成交`](#query-trades-fills-2)
  - 现有的 WebSocket 主题将返回具有当前市场名称的数据（例如：BTCPFC），并为新市场名称（例如：BTC-PERP）添加了一组新的 WebSocket 主题，`响应字段将相同`，以下是映射表：
    - [tradeHistoryApi](#public-trade-fills) -> tradeHistoryApiV2
    - [orderbookApi](#orderbook-snapshot-by-grouping) -> orderbookApiV2
    - [orderbookL2Api](#orderbook-snapshot-by-depth) -> orderbookL2ApiV2
    - [fills](#user-trade-fills) -> fillsV2
    - [allPosition](#all-position) -> allPositionV2
    - [notificationApiV2](#notifications) -> notificationApiV3

## 版本 2.5.5（2023年3月29日）

* 将身份验证失败的 HTTP 状态码更新为 `401`

## 版本 2.5.4（2023年3月1日）

* 更新 [订单簿增量更新](#orderbook-incremental-updates) 的参数格式。

## 版本 2.5.3（2022年12月23日）

* [重要通知] BTSE 将于 **2023年** 更改期货市场命名约定。更改内容详见 [版本 2.5.0（2022年11月16日）](#version-2.5.0-(16th-November-2022))。

## 版本 2.5.2（2022年11月28日）

* 添加 [订单簿增量更新](#orderbook-incremental-updates) 的错误消息。

## 版本 2.5.1（2022年11月25日）

* [重要通知] BTSE 将调整计算期货风险限制级别的公式，某些 API 将受到影响。
  - [`市场摘要`](#market-summary)
    - 响应中的 `maxPosition` 将不再适用，因为它将由 `max_risk_limit / futures_market_price` 确定
    - `minRiskLimit` 现在以合同大小表示，并将更新为 `美元名义值`
    - `maxRiskLimit` 现在以合同大小表示，并将更新为 `美元名义值`
  - `订单大小` 保持为 `合同大小`，而不是 `美元价值`，以保持向后兼容性
  - [参考链接](https://www.btse.com/blog/important-notice-upcoming-changes-to-futures-risk-limits-and-contract-names/)
  - 如果有任何问题，可以在 [BTSE API 电报群](https://t.me/btsecomAPI) 中提问

## 版本 2.5.0（2022年11月16日）

* [重要通知] BTSE 将于 **2022年12月** 更改期货市场命名约定，以为零售用户提供更多明确性，规则如下：
  - 将永续市场的后缀从 `PFC` 更改为 `PERP`（例如：BTCPFC -> BTC-PERP）
  - 将基于时间的市场的后缀从 `交割月份 + 年份` 更改为 `结算日期（YYMMDD）`（例如：BTCZ22 -> BTC-221230）
  - [参考链接](https://www.btse.com/blog/important-notice-upcoming-changes-to-futures-risk-limits-and-contract-names/)
  - 期货 API 已更新（通常添加了一个新的可选参数 `useNewSymbolNaming`，以指定市场名称是否采用新格式）：
    - [`市场摘要`](#market-summary)
    - [`查询未完成订单`](#query-open-orders)
    - [`按分组排序的订单簿`](#orderbook-by-grouping)
    - [`订单簿`](#orderbook)
    - [`图表数据`](#charting-data)
    - [`查询钱包历史`](#query-wallet-history)
    - [`查询钱包余额`](#query-wallet-balance)
    - [`设置杠杆`](#set-leverage)
    - [`设置风险限制`](#set-risk-limit)
    - [`查询市场价格`](#query-market-price)
    - [`更改合同结算货币`](#change-contract-settlement-currency)
    - [`查询账户费用`](#query-account-fee)
    - [`查询持仓`](#query-position)
    - [`关闭持仓`](#close-position)
    - [`查询钱包保证金`](#query-wallet-margin)
    - [`创建新订单`](#create-new-order)
    - [`查询交易成交`](#query-trades-fills-2)
  - 现有的 WebSocket 主题将返回具有当前市场名称的数据（例如：BTCPFC），并为新市场名称（例如：BTC-PERP）添加了一组新的 WebSocket 主题，`响应字段将相同`，以下是映射表：
    - [tradeHistoryApi](#public-trade-fills) -> tradeHistoryApiV2
    - [orderbookApi](#orderbook-snapshot-by-grouping) -> orderbookApiV2
    - [orderbookL2Api](#orderbook-snapshot-by-depth) -> orderbookL2ApiV2
    - [fills](#user-trade-fills) -> fillsV2
    - [allPosition](#all-position) -> allPositionV2
    - [notificationApiV2](#notifications) -> notificationApiV3
    

## 版本 2.4.1（2022年8月17日）

* 在 [交易端点](#trade-endpoints) 中添加更多请求/响应示例
* 在 [交易端点](#trade-endpoints) 中纠正文档

## 版本 2.4.0（2022年3月30日）

* 添加新的 WebSocket 主题 `allPosition` 以获取所有未平仓头寸 [所有头寸](#all-position)

## 版本 2.3.1（2022年3月29日）

* 在 [创建新订单](#create-new-order) 中添加新的 `HALFMIN` time_in_force 选项

## 版本 2.3.0（2022年1月21日）

* 在 [创建新订单](#create-new-order)、[创建新算法订单](#create-new-algo-order) 和 [关闭持仓](#close-position) 中添加两个新的响应字段 `remainingSize` 和 `originalSize` **[注意]：此更改将于2022年1月25日生效（UTC+0）**

## 版本 2.2.1（2021年11月26日）

* 更新期货市场的市场名称 [订单簿 WebSocket 数据流](#orderbook-incremental-updates)

## 版本 2.2.0（2021年11月23日）

* 添加订单簿增量更新 [订单簿 WebSocket 数据流](#orderbook-incremental-updates)

## 版本 2.1.8（2021年7月1日）

* 添加 `fills` WebSocket 主题以订阅 [用户交易成交](#user-trade-fills)
* 为 [订单簿 WebSocket 数据流](#orderbook-snapshot-by-depth) 添加属性 `depth`

## 版本 2.1.7（2021年2月4日）

* 在未完成订单 AP 中添加 `avgFilledPrice`


## 版本 2.1.6（2021年1月29日）

* WebSocket 端点将更新为以下内容：
  * 现货：wss://ws.btse.com/ws/spot
  * 期货：wss://ws.btse.com/ws/futures

  现有端点将继续提供。

* 登录主题现在将以 JSON 成功/失败消息 {"event":"login","success":true} 作出响应。
* 在订阅或取消订阅 WebSocket 主题时，将返回一个确认，指示成功订阅/取消订阅的主题。不成功的主题将不会在响应中返回。
* WebSocket 通知将新增以下指示：
  * maker - 布尔值，指示订单是否为挂单 / 吃单订单
  * remainingSize - 指示订单的剩余数量的值
  * time_in_force - 指示订单上设置的有效期的值

## 版本 2.1.5（2020年9月28日）

* 新的修改订单 API。允许用户编辑挂单的价格、数量和触发价格

## 版本 2.1.4（2020年7月24日）

* 新的结算 API 添加，允许用户通过 API 设置当前仓位结算的货币

## 版本 2.1.3（2020年6月23日）

* 引入垃圾订单检测机制
* 引入 WebSocket 主题 notificationApiV2。该主题旨在标准化返回的响应代码。通知以数组形式返回
* 引入 API 权限。所有当前的 API 密钥将具有读取、交易和转账权限。请参考标题旁边的标签，了解它们属于哪个类别

# 概览

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
$ echo -n "/api/v2.1/user/wallet1624984297330" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= ea4f1f2b43a0f4d750ae560c5274d6214d140fcab3093da5f4a83e36828535bd2ba7b12160cd12199596f422c8883333
```

* 获取钱包的端点是 `https://api.btse.com/futures/api/v2.1/user/wallet`
* 假设我们有以下值：
  * request-nonce: `1624984297330`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v2.1/user/wallet`
* 生成的签名将是:
  * request-sign: `ea4f1f2b43a0f4d750ae560c5274d6214d140fcab3093da5f4a83e36828535bd2ba7b12160cd12199596f422c8883333`

### 示例 2：下订单

> **HMAC SHA384 Signature**

```shell
$ echo -n "/api/v2.1/order1624985375123{\"postOnly\":false,\"price\":8500.0,\"reduceOnly\":false,\"side\":\"BUY\",\"size\":1,\"stopPrice\":0.0,\"symbol\":\"BTCPFC\",\"time_in_force\":\"GTC\",\"trailValue\":0.0,\"triggerPrice\":0.0,\"txType\":\"LIMIT\",\"type\":\"LIMIT\"}" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 943adfce43b609a28506274976b96e08cf4bdc4ea53ca0b4cac0eb2cf0773a7d0807efc0aeab779d47fadcd9a60eea13
```

* 下订单的端点是 `https://api.btse.com/futures/api/v2.1/order`
* 假设我们有以下值：
  * request-nonce: `1624985375123`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v2.1/order`
  * Body: `{"postOnly":false,"price":8500.0,"reduceOnly":false,"side":"BUY","size":1,"stopPrice":0.0,"symbol":"BTCPFC","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
  * Encrypted Text: `/api/v2.1/order1624985375123{"postOnly":false,"price":8500.0,"reduceOnly":false,"side":"BUY","size":1,"stopPrice":0.0,"symbol":"BTCPFC","time_in_force":"GTC","trailValue":0.0,"triggerPrice":0.0,"txType":"LIMIT","type":"LIMIT"}`
* 生成的签名将是：
  * request-sign: `943adfce43b609a28506274976b96e08cf4bdc4ea53ca0b4cac0eb2cf0773a7d0807efc0aeab779d47fadcd9a60eea13`


## 速率限制

* 强制执行以下速率限制：

BTSE 的速率限制如下：

**查询**

* 每个API：每秒 `15次请求`
* 每个用户：每秒 `30次请求`

**订单**

* 每个API：每秒 `75次请求`
* 每个用户：每秒 `75次请求`

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
* 300: ERROR_MAX_ORDER_SIZE_EXCEEDED = 超过最大订单大小错误
* 301: ERROR_INVALID_ORDER_SIZE = 无效订单大小错误
* 302: ERROR_INVALID_ORDER_PRICE = 无效订单价格错误
* 303: ERROR_RATE_LIMITS_EXCEEDED = 超过速率限制错误
* 304: ERROR_MAX_OPEN_ORDER_EXCEEDED = 超过最大开放订单数错误
* 1003: ORDER_LIQUIDATION = 订单正在进行清算
* 1004: ORDER_ADL = 订单正在进行ADL
* 30410: BLOCK_TRADE_COMPLETE_SUCCESS = 区块交易已成功完成

## 垃圾订单

垃圾订单是指大量的小订单大小。为了确保平台和用户的利益不受恶意用户的侵害，我们将对下列情况的用户采取以下措施，这些用户下单小额订单。

* 订单等于或低于5个合约将被标记为垃圾订单，并自动变为隐藏订单。
* 被标记为垃圾的订单始终支付吃单费。
* 被标记为垃圾的Post-Only API订单将被拒绝而不是被隐藏。
* 太多的垃圾订单可能导致暂时封禁交易账户。
* 放置 >= 4 个挂单，总大小小于 20 个合约的API账户有可能被标记为垃圾账户。
* 被标记为垃圾的账户可能会对账户施加限制，包括订单速率限制、持仓限制，或禁用API功能。如对新的垃圾订单机制有疑问，请发送电子邮件至 mm@btse.com。


# 公共端点

## 市场摘要

> 响应

```json
[
  {
    "symbol": "BTCPFC",
    "last": 36365,
    "lowestAsk": 36377,
    "highestBid": 36376,
    "percentageChange": 4.973731309,
    "volume": 172418318.7575521,
    "high24Hr": 36447,
    "low24Hr": 33989.5,
    "base": "BTC",
    "quote": "USD",
    "active": true,
    "size": 4916.8266,
    "minValidPrice": 0.5,
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
    "futures": false
  }
]
```

`GET /api/v2.1/market_summary`

获取市场摘要信息。如果未发送`symbol`参数，则将检索所有市场。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                    |
| ---                | ---     | ---      | ---                                                                    |
| 符号               | string  | No       | 市场符号                                                                |
| 使用新符号命名       | boolean | No       | 为True时返回期货市场名称的新格式， 默认为False                          |

### 响应内容

| 名称                | 类型    | 是否必须 | 描述                                                                                                   |
| ---                 | ---     | ---      | ---                                                                                                   |
| symbol              | string  | Yes      | 市场符号                                                                                               |
| last                | double  | Yes      | 最新价格                                                                                               |
| lowestAsk           | double  | Yes      | 订单簿中的最低卖价                                                                                      |
| highestBid          | double  | Yes      | 订单簿中的最高买价                                                                                      |
| percentageChange    | double  | Yes      | 过去24小时内相对于价格的百分比变化                                                                       |
| volume              | double  | Yes      | 交易量                                                                                                  |
| high24Hr            | double  | Yes      | 过去24小时的最高价格                                                                                    |
| low24Hr             | double  | Yes      | 过去24小时的最低价格                                                                                    |
| base                | string  | Yes      | 基础货币                                                                                                |
| quote               | string  | Yes      | 报价货币                                                                                                |
| active              | boolean | Yes      | 表示市场是否活跃的指标                                                                                   |
| size                | double  | Yes      | 交易尺寸                                                                                                |
| minValidPrice       | double  | Yes      | 最小有效价格                                                                                            |
| minPriceIncrement   | double  | Yes      | 价格增量                                                                                                |
| minOrderSize        | double  | Yes      | 最小交易尺寸                                                                                            |
| minSizeIncrement    | double  | Yes      | 交易尺寸增量                                                                                            |
| maxOrderSize        | double  | Yes      | 最大订单尺寸                                                                                            |
| openInterest        | double  | No       | 期货市场的未平仓位数量                                                                                   |
| openInterestUSD     | double  | No       | 期货市场未平仓位的美元名义值                                                                              |
| contractStart       | long    | No       | 合同开始时间                                                                                            |
| contractEnd         | long    | No       | 合同结束时间                                                                                            |
| timeBasedContract   | boolean | No       | 指示是否为基于时间的合同                                                                                |
| openTime            | long    | Yes      | 市场开放时间                                                                                            |
| closeTime           | long    | Yes      | 市场关闭时间                                                                                            |
| startMatching       | long    | Yes      | 匹配开始时间                                                                                            |
| inactiveTime        | long    | Yes      | 市场不活跃时间                                                                                          |
| fundingRate         | double  | No       | 每小时计算的资金费率                                                                                    |
| contractSize        | double  | No       | 一个合同的尺寸                                                                                          |
| maxPosition         | double  | No       | 用户允许拥有的最大头寸 `风险限额调整后将不再适用`                                                         |
| minRiskLimit        | double  | No       | 合同大小的最小风险限额 `将更改为美元价值`                                                                 |
| maxRiskLimit        | double  | No       | 合同大小的最大风险限额 `将更改为美元价值`                                                                 |
| availableSettlement | array   | No       | 用于结算的可用货币                                                                                      |
| futures             | boolean | Yes      | 符号是否为期货合同的指标                                                                                  |

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
  ],
```

`GET /api/v2.1/ohlcv`

获取蜡烛图表数据。默认情况下，每次将返回300个数据点。

### 请求参数

| 名称                | 类型    | 是否必须 | 描述                                                                                                                                                 |
| ---                | ---     | ---      | ---                                                                                                                                                 |
| symbol             | string  | Yes      | 市场符号                                                                                                                                            |
| start              | long    | No       | 以毫秒为单位的开始时间 (例如 1624987283000)                                                                                                         |
| end                | long    | No       | 以毫秒为单位的结束时间 (例如 1624987283000)                                                                                                         |
| resolution         | string  | Yes      | 支持的分辨率包括：<br/> 1: 1分钟<br/> 5: 5分钟<br/> 15: 15分钟<br/>30: 30分钟<br/>60: 60分钟<br/>360: 6小时<br/>1440: 1天                          |
| useNewSymbolNaming | boolean | No       | 设置为True以使用symbol中的新期货市场名称，默认为False                                                                                              |


### 响应内容

返回一个包含下表描述的索引的二维数组

| 索引 | 类型    | 是否必须 | 描述       |
| ---  | ---     | ---      | ---        |
| 0    | long    | Yes      | Unix 时间  |
| 1    | double  | Yes      | 开盘价格   |
| 2    | double  | Yes      | 最高价格   |
| 3    | double  | Yes      | 最低价格   |
| 4    | double  | Yes      | 收盘价格   |
| 5    | double  | Yes      | 交易量     |


## 查询市场价格

> 响应

```json
[
  {
    "symbol": "BTCPFC",
    "indexPrice": 36288.949684967,
    "lastPrice": 36286.5,
    "markPrice": 0
  }
]
```

`GET /api/v2.1/price`

检索平台上的当前价格。如果未指定符号，则将返回所有符号。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                    |
| ---                | ---     | ---      | ---                                                                     |
| symbol             | string  | Yes      | 市场符号                                                                 |
| useNewSymbolNaming | boolean | No       | 若为True则在符号中使用新的期货市场名称，默认为False                        |

### 响应内容

| 名称       | 类型   | 是否必须 | 描述                 |
| ---        | ---    | ---      | ---                  |
| symbol     | double | Yes      | 市场符号              |
| indexPrice | double | Yes      | 指数价格              |
| lastPrice  | double | Yes      | 最后成交价格           |
| markPrice  | double | Yes      | 标记价格              |

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
  "symbol": "BTCPFC"
}
```

`GET /api/v2.1/orderbook`

检索订单簿的快照。

### 请求参数

| 名称                | 类型    | 是否必须 | 描述                                                                                                                                                                                                                      |
| ---                 | ---     | ---      | ---                                                                                                                                                                                                                       |
| symbol             | string  | Yes      | 市场符号，作为路径变量输入                                                                                                                                                                                                |
| group              | integer | No       | 订单簿分组。有效值为：<br/>0-8，其中0表示0级分组（例如，对于BTC-PERP，它将为0.1）<br/>BTC-PERP的1级分组为0.5<br/>BTC-PERP的2级分组为1<br/>                                                                            |
| useNewSymbolNaming | boolean | No       | 设置为True以使用symbol中的新期货市场名称，默认为False                                                                                                                                                                    |

### 响应内容

#### 订单簿

| 名称       | 类型   | 是否必须 | 描述                    |
| ---       | ---    | ---      | ---                    |
| symbol    | string | Yes      | 市场符号                |
| buyQuote  | Quote  | Yes      | 买入报价的数组          |
| sellQuote | Quote  | Yes      | 卖出报价的数组          |
| timestamp | long   | Yes      | 订单簿的时间戳          |

#### 报价

| 名称   | 类型    | 是否必须 | 描述      |
| ---   | ---     | ---      | ---       |
| price | double  | Yes      | 订单价格  |
| size  | double  | Yes      | 订单尺寸  |


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
  "symbol": "BTCPFC"
}
```

`GET /api/v2.1/orderbook/L2`

获取订单簿的Level 2快照

### 请求参数

| 名称                | 类型    | 是否必须 | 描述                                                                                     |
| ---                | ---     | ---      | ---                                                                                     |
| symbol             | string  | Yes      | 市场符号                                                                                 |
| depth              | long    | No       | 订单簿深度                                                                               |
| useNewSymbolNaming | boolean | No       | 设置为True以返回新格式的期货市场名称，默认为False                                        |

### 响应内容

#### 订单簿

| 名称       | 类型   | 是否必须 | 描述                    |
| ---       | ---    | ---      | ---                    |
| symbol    | string | Yes      | 市场符号                |
| buyQuote  | Quote  | Yes      | 购买报价的数组          |
| sellQuote | Quote  | Yes      | 出售报价的数组          |
| timestamp | long   | Yes      | 订单簿的时间戳          |

#### 报价

| 名称   | 类型    | 是否必须 | 描述      |
| ---   | ---     | ---      | ---       |
| price | double  | Yes      | 订单价格  |
| size  | double  | Yes      | 订单尺寸  |


## 查询成交记录

> 响应

```json
[
  {
    "price": 36164,
    "size": 100,
    "side": "SELL",
    "symbol": "BTCPFC",
    "serialId": 85997835,
    "timestamp": 1624990097000
  }
]
```

`GET /api/v2.1/trades`

获取由`symbol`指定的市场的交易成交记录

### 请求参数

| 名称                | 类型    | 是否必须 | 描述                                                                                                        |
| ---                | ---     | ---      | ---                                                                                                        |
| symbol             | string  | Yes      | 市场符号                                                                                                    |
| startTime          | long    | No       | 以毫秒为单位的开始时间 (例如 1624987283000)                                                                 |
| endTime            | long    | No       | 以毫秒为单位的结束时间 (例如 1624987283000)                                                                 |
| beforeSerialId     | string  | Yes      | 用于分页的条件，检索指定序列ID之前的记录                                                                    |
| afterSerialId      | string  | Yes      | 用于分页的条件，检索指定序列ID之后的记录                                                                    |
| count              | long    | Yes      | 返回的记录数                                                                                                |
| includeOld         | boolean | Yes      | 获取过去7天的交易历史记录                                                                                   |
| useNewSymbolNaming | boolean | No       | 设置为True以使用symbol中的新期货市场名称，默认为False                                                       |

### 响应内容

| 名称       | 类型    | 是否必须 | 描述                                         |
| ---       | ---     | ---      | ---                                         |
| symbol    | string  | Yes      | 市场符号                                     |
| side      | string  | Yes      | 交易方向。值包括：[`Buy`, `SELL`]            |
| price     | double  | Yes      | 交易价格                                     |
| size      | double  | Yes      | 交易尺寸                                     |
| serialId  | double  | Yes      | 序列ID，运行序列号                           |
| timestamp | long    | Yes      | 交易时间戳                                   |


# 交易终端

## 创建新订单

> 请求（创建`市价`订单）

```json
{
  "symbol": "BTCPFC",
  "size": 1,
  "side": "BUY",
  "type": "MARKET"
}
```
> 请求（创建`限价`订单）

```json
{
  "symbol": "BTCPFC",
  "size": 1,
  "price": 21000,
  "side": "BUY",
  "type": "LIMIT"
}
```
> 请求（创建`限价` `触发` 订单）

```json
{
  "symbol": "BTCPFC",
  "size": 1,
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
  "symbol": "BTCPFC",
  "size": 1,
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
  "symbol": "BTCPFC",
  "size": 1,
  "price": 21000,
  "side": "BUY",
  "type": "OCO",
  "txType": "LIMIT",
  "trigger": "markPrice",
  "stopPrice": 30010,
  "triggerPrice": 30000
}
```

> 响应（通用）

```json
[
  {
    "status": 4,
    "symbol": "BTCPFC",
    "orderType": 76,
    "price": 21000.0,
    "side": "BUY",
    "size": 1,
    "orderID": "abb3f457-fdc0-4bdb-a46b-8e4aa49a57c2",
    "timestamp": 1660558270207,
    "triggerPrice": 0.0,
    "trigger": false,
    "deviation": 100.0,
    "stealth": 100.0,
    "message": "",
    "avgFillPrice": 21000.0,
    "fillSize": 1.0,
    "clOrderID": "",
    "originalSize": 1.0,
    "postOnly": false,
    "remainingSize": 0.0,
    "time_in_force": "GTC"
  }
]
```

> 响应（用于 `OCO` 订单）

```json
[
  {
    "status": 9,
    "symbol": "BTCPFC",
    "orderType": 76,
    "price": 23000.0,
    "side": "BUY",
    "size": 1,
    "orderID": "4c9d16c1-9869-4734-bfb8-56318e961ef2",
    "timestamp": 1660558185243,
    "triggerPrice": 30000.0,
    "trigger": true,
    "deviation": 100.0,
    "stealth": 100.0,
    "message": "",
    "avgFillPrice": 0.0,
    "fillSize": 0.0,
    "clOrderID": "",
    "originalSize": 1.0,
    "postOnly": false,
    "remainingSize": 1.0,
    "time_in_force": "GTC"
  },
  {
    "status": 2,
    "symbol": "BTCPFC",
    "orderType": 76,
    "price": 21000.0,
    "side": "BUY",
    "size": 1,
    "orderID": "53749446-39d3-4b72-87c9-92e9fc7e4b8c",
    "timestamp": 1660558185225,
    "triggerPrice": 0.0,
    "trigger": false,
    "deviation": 100.0,
    "stealth": 100.0,
    "message": "",
    "avgFillPrice": 0.0,
    "fillSize": 0.0,
    "clOrderID": "",
    "originalSize": 1.0,
    "postOnly": false,
    "remainingSize": 1.0,
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.1/order`

创建一个新的订单。需要 `Trading` 权限

### 请求参数

| 名称           | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                                                                                     |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                                                                                     |
| symbol        | string  | Yes      | 市场符号                                                                                                                                                                                                                                                                                                                                                                 |
| price         | double  | No       | 除非创建市场订单，否则为必填。订单价格                                                                                                                                                                                                                                                                                                                                  |
| size          | long    | Yes      | 订单尺寸以`合同大小`表示（即使在风险限额调整后也保持不变）                                                                                                                                                                                                                                                                                                               |
| side          | string  | Yes      | 'BUY' 或 'SELL'                                                                                                                                                                                                                                                                                                                                                        |
| time_in_force | string  | No       | 订单的时间有效性<br/>GTC: 有效直至取消<br/>IOC: 立即或取消<br/>FOK: 全部成交或取消<br/>HALFMIN: 订单有效30秒<br/>FIVEMIN: 订单有效5分钟<br/>HOUR: 订单有效一个小时<br/>TWELVEHOUR: 订单有效12小时<br/>DAY: 订单有效一天<br/>WEEK: 订单有效一周<br/>MONTH: 订单有效一个月                                                                                                              |
| type          | string  | Yes      | 订单类型<br/>LIMIT: 限价订单<br/>MARKET: 市价订单<br/>OCO: 一个取消另一个                                                                                                                                                                                                                                                                                               |
| txType        | string  | No       | 用于停止订单或触发订单<br/>STOP: 停止订单，`triggerPrice` 是必填项<br/>TRIGGER: 触发订单，`triggerPrice` 是必填项<br/>LIMIT: 默认值，当其既不是停止订单也不是触发订单时使用                                                                                                                                                                                              |
| stopPrice     | double  | No       | 创建OCO订单时为必填。表示停止价格                                                                                                                                                                                                                                                                                                                                      |
| triggerPrice  | double  | No       | 创建停止、触发、OCO订单时为必填。表示触发价格                                                                                                                                                                                                                                                                                                                          |
| trailValue    | double  | No       | 跟踪值                                                                                                                                                                                                                                                                                                                                                                  |
| postOnly      | boolean | No       | 布尔值，表示这是否仅为发布订单。对于仅发布订单，交易员将收取制造商费用                                                                                                                                                                                                                                                                                                  |
| reduceOnly    | boolean | No       | 布尔值，表示这是否只是减少订单。                                                                                                                                                                                                                                                                                                                                       |
| clOrderID     | string  | No       | 自定义订单ID                                                                                                                                                                                                                                                                                                                                                            |
| trigger       | string  | No       | 用于创建txType: `STOP` 或 `TRIGGER` 的订单。有效选项: `markPrice` (默认) 或 `lastPrice`                                                                                                                                                                                                                                                                                 |


### 响应内容

| 名称            | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                |
| symbol        | string  | Yes      | 市场符号                                                                                                                                                                                                                                                                                           |
| clOrderID     | string  | Yes      | 交易者发送的客户标签                                                                                                                                                                                                                                                                               |
| fillSize      | number  | Yes      | 已成交的交易大小                                                                                                                                                                                                                                                                                   |
| orderID       | string  | Yes      | 订单ID                                                                                                                                                                                                                                                                                             |
| orderType     | integer | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: Algo订单                                                                                                                                                                                                                                       |
| postOnly      | boolean | Yes      | 表明订单是否为仅发布订单                                                                                                                                                                                                                                                                           |
| price         | double  | Yes      | 订单价格                                                                                                                                                                                                                                                                                           |
| side          | string  | Yes      | 订单方向<br/>BUY 或 SELL                                                                                                                                                                                                                                                                           |
| size          | long    | Yes      | 订单大小以`合同大小`表示（即使在风险限额调整后也保持不变）                                                                                                                                                                                                                                          |
| status        | long    | Yes      | 订单状态<br/>2: 订单已插入<br/>3: 订单已交易<br/>4: 订单已完全交易<br/>5: 订单部分交易<br/>6: 订单已取消<br/>7: 订单已退款<br/>9: 触发已插入<br>10: 触发已激活<br/>15: 订单被拒绝<br/>16: 订单未找到<br/>17: 请求失败                                                                                        |
| time_in_force | string  | Yes      | 订单有效性                                                                                                                                                                                                                                                                                         |
| timestamp     | long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                                         |
| trigger       | boolean | Yes      | 如果订单是触发订单的指示器                                                                                                                                                                                                                                                                        |
| triggerPrice  | double  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                                          |
| avgFillPrice  | double  | Yes      | 平均成交价格。对于部分交易的订单返回平均成交价格                                                                                                                                                                                                                                                  |
| message       | string  | Yes      | 交易消息                                                                                                                                                                                                                                                                                           |
| stealth       | double  | Yes      | 仅对Algo订单有效                                                                                                                                                                                                                                                                                   |
| deviation     | double  | Yes      | 仅对Algo订单有效                                                                                                                                                                                                                                                                                   |
| remainingSize | double  | Yes      | 剩余待交易的大小                                                                                                                                                                                                                                                                                   |
| originalSize  | double  | Yes      | 原始订单大小                                                                                                                                                                                                                                                                                       |

## 创建新的算法订单

> 请求

```json
{
  "symbol": "BTCPFC",
  "price": 21500,
  "size": 1,
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
    "symbol": "BTCPFC",
    "orderType": 80,
    "price": 21500.0,
    "side": "BUY",
    "size": 1,
    "orderID": "de9f94bb-0ca0-470b-830e-9bc2e109c719",
    "timestamp": 1660554373317,
    "triggerPrice": 0.0,
    "trigger": false,
    "deviation": -10.0,
    "stealth": 10.0,
    "message": "",
    "avgFillPrice": 0.0,
    "fillSize": 0.0,
    "clOrderID": "60a30188-f2a2-4498-b061-7d72126c18c2",
    "originalSize": 1.0,
    "postOnly": false,
    "remainingSize": 1.0,
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.1/order/peg`

创建新的算法订单。算法订单是一种价格会根据市场价格变化的订单。要创建算法订单，用户需要输入额外的参数：

* `price`：用户愿意将订单列出的最低价格（卖单）或最高价格（买单）
* `deviation`：订单价格与指数价格的偏差程度。该值以百分比表示，范围从 `-10` 到 `10`
* `stealth`：订单簿上要显示多少百分比的订单量。

此API需要具有`交易`权限

### 请求参数

| 名称       | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                            |
| ---       | ---     | ---      | ---                                                                                                                                                                                                                                            |
| symbol    | string  | Yes      | 市场符号                                                                                                                                                                                                                                       |
| price     | double  | Yes      | 卖单的最低价，这是用户愿意出售的最低价格。买单的最高价，这是用户愿意购买的最高价格。                                                                                                                                                        |
| size      | long    | Yes      | 订单尺寸                                                                                                                                                                                                                                       |
| side      | string  | Yes      | 订单方向<br/>BUY 或 SELL                                                                                                                                                                                                                       |
| clOrderID | string  | No       | 自定义订单ID                                                                                                                                                                                                                                    |
| deviation | double  | No       | 订单价格应与指数价格偏离多少。该值以百分比表示，范围从`-10`到`10`                                                                                                                                                                             |
| stealth   | double  | No       | 订单中应在订单簿上显示的百分比是多少。                                                                                                                                                                                                        |

### 响应内容

| 名称            | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                |
| symbol        | string  | Yes      | 市场符号                                                                                                                                                                                                                                                                                           |
| clOrderID     | string  | Yes      | 交易者发送的客户标签                                                                                                                                                                                                                                                                               |
| fillSize      | number  | Yes      | 已成交的交易大小                                                                                                                                                                                                                                                                                   |
| orderID       | string  | Yes      | 订单ID                                                                                                                                                                                                                                                                                             |
| orderType     | integer | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: Algo订单                                                                                                                                                                                                                                       |
| postOnly      | boolean | Yes      | 表明订单是否为仅发布订单                                                                                                                                                                                                                                                                           |
| price         | double  | Yes      | 订单价格                                                                                                                                                                                                                                                                                           |
| side          | string  | Yes      | 订单方向<br/>BUY 或 SELL                                                                                                                                                                                                                                                                           |
| size          | long    | Yes      | 订单大小以`合同大小`表示（即使在风险限额调整后也保持不变）                                                                                                                                                                                                                                          |
| status        | long    | Yes      | 订单状态<br/>2: 订单已插入<br/>3: 订单已交易<br/>4: 订单已完全交易<br/>5: 订单部分交易<br/>6: 订单已取消<br/>7: 订单已退款<br/>9: 触发已插入<br>10: 触发已激活<br/>15: 订单被拒绝<br/>16: 订单未找到<br/>17: 请求失败                                                                                        |
| time_in_force | string  | Yes      | 订单有效性                                                                                                                                                                                                                                                                                         |
| timestamp     | long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                                         |
| trigger       | boolean | Yes      | 如果订单是触发订单的指示器                                                                                                                                                                                                                                                                        |
| triggerPrice  | double  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                                          |
| avgFillPrice  | double  | Yes      | 平均成交价格。对于部分交易的订单返回平均成交价格                                                                                                                                                                                                                                                  |
| message       | string  | Yes      | 交易消息                                                                                                                                                                                                                                                                                           |
| stealth       | double  | Yes      | 订单的隐秘值                                                                                                                                                                                                                                                                                       |
| deviation     | double  | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                                       |
| remainingSize | double  | Yes      | 剩余待交易的大小                                                                                                                                                                                                                                                                                   |
| originalSize  | double  | Yes      | 原始订单大小                                                                                                                                                                                                                                                                                       |

## 修改订单

> 请求（修改价格）

```json
{
  "symbol": "BTCPFC",
  "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
  "type": "PRICE",
  "value": 22000
}
```

> 请求（全部修改）

```json
{
  "symbol": "BTCPFC",
  "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
  "type": "ALL",
  "orderPrice": 30010,
  "orderSize": 1,
  "triggerPrice": 30000
}
```

> 响应

```json
[
  {
    "status": 123,
    "symbol": "BTCPFC",
    "orderType": 76,
    "price": 20000.0,
    "side": "BUY",
    "size": 1,
    "orderID": "604c3ebf-d7fa-468d-9ff0-f6ad030221b4",
    "timestamp": 1660639762254,
    "triggerPrice": 0.0,
    "trigger": true,
    "deviation": 100.0,
    "stealth": 100.0,
    "message": "",
    "avgFillPrice": 0.0,
    "fillSize": 0.0,
    "clOrderID": "",
    "originalSize": 1.0,
    "postOnly": false,
    "remainingSize": 1.0,
    "time_in_force": "GTC"
  }
]
```

`PUT /api/v2.1/order`

修改订单的价格、数量或触发价格。对于触发订单，如果订单已经被触发，触发价格将无法进一步修改。修订订单不适用于算法订单。

### 请求参数

| 名称          | 类型    | 是否必须 | 描述                                                                                                                                                                                                       |
| ---          | ---     | ---      | ---                                                                                                                                                                                                       |
| symbol       | string  | Yes      | 市场符号                                                                                                                                                                                                  |
| orderID      | string  | No       | 内部订单ID。当未提供`clOrderID`时为必填项。如果提供了`orderID`，将忽略`clOrderID`。                                                                                                                        |
| clOrderID    | string  | No       | 自定义订单ID。当未提供`orderID`时为必填项。                                                                                                                                                               |
| type         | string  | Yes      | 修改类型<br/>`PRICE`: 修改订单价格<br/>`SIZE`: 修改订单尺寸<br/>`TRIGGERPRICE`: 修改触发价格<br/>`ALL`: 修改多个字段                                                                                     |
| value        | number  | Yes      | 要修改的值。其值取决于设置的类型。                                                                                                                                                                       |
| orderPrice   | number  | No       | 对于类型：`ALL`，要修改的订单价格                                                                                                                                                                        |
| orderSize    | number  | No       | 对于类型：`ALL`，要修改的合同大小订单尺寸                                                                                                                                                                |
| triggerPrice | number  | No       | 对于类型：`ALL`，要修改的触发价格                                                                                                                                                                        |


### 响应内容

| 名称            | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                |
| ---           | ---     | ---      | ---                                                                                                                                                                                                                                                                                                |
| symbol        | string  | Yes      | 市场符号                                                                                                                                                                                                                                                                                           |
| clOrderID     | string  | Yes      | 交易者发送的客户标签                                                                                                                                                                                                                                                                               |
| fillSize      | string  | Yes      | 已成交的交易大小                                                                                                                                                                                                                                                                                   |
| orderID       | string  | Yes      | 订单ID                                                                                                                                                                                                                                                                                             |
| orderType     | integer | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: Algo订单                                                                                                                                                                                                                                       |
| postOnly      | boolean | Yes      | 表明订单是否为仅发布订单                                                                                                                                                                                                                                                                           |
| price         | double  | Yes      | 订单价格                                                                                                                                                                                                                                                                                           |
| side          | string  | Yes      | 订单方向<br/>BUY 或 SELL                                                                                                                                                                                                                                                                           |
| size          | long    | Yes      | 订单大小以`合同大小`表示（即使在风险限额调整后也保持不变）                                                                                                                                                                                                                                          |
| status        | long    | Yes      | 订单状态<br/>2: 订单已插入<br/>3: 订单已交易<br/>4: 订单已完全交易<br/>5: 订单部分交易<br/>6: 订单已取消<br/>7: 订单已退款<br/>9: 触发已插入<br>10: 触发已激活<br/>15: 订单被拒绝<br/>16: 订单未找到<br/>17: 请求失败                                                                                        |
| time_in_force | string  | Yes      | 订单有效性                                                                                                                                                                                                                                                                                         |
| timestamp     | long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                                         |
| trigger       | string  | Yes      | 如果订单是触发订单的指示器                                                                                                                                                                                                                                                                        |
| triggerPrice  | string  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                                          |
| avgFillPrice  | string  | Yes      | 平均成交价格。对于部分交易的订单返回平均成交价格                                                                                                                                                                                                                                                  |
| message       | string  | Yes      | 交易消息                                                                                                                                                                                                                                                                                           |
| stealth       | double  | Yes      | 订单的隐秘值                                                                                                                                                                                                                                                                                       |
| deviation     | string  | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                                       |
| remainingSize | double  | Yes      | 剩余待交易的大小                                                                                                                                                                                                                                                                                   |
| originalSize  | double  | Yes      | 原始订单大小                                                                                                                                                                                                                                                                                       |

## 取消订单

> 请求 (取消单个订单)

```
/api/v2.1/order?symbol=BTC-USD&clOrderID=my-order-id
```

> 响应

```json
[
  {
    "status": 6,
    "symbol": "BTCPFC",
    "orderType": 76,
    "price": 19000.0,
    "side": "BUY",
    "size": 1,
    "orderID": "ae5b1b27-d5fe-41e2-89f8-f17b60fb3def",
    "timestamp": 1660640879996,
    "triggerPrice": 0.0,
    "trigger": false,
    "deviation": 100.0,
    "stealth": 100.0,
    "message": "",
    "avgFillPrice": 0.0,
    "fillSize": 0.0,
    "clOrderID": "string",
    "originalSize": 1.0,
    "postOnly": false,
    "remainingSize": 1.0,
    "time_in_force": "GTC"
  }
]
```

`DELETE /api/v2.1/order`

取消尚未成交的待定订单。orderID是取消特定订单的唯一标识符。clOrderID是交易者发送的自定义ID。通过clOrderID取消时，所有具有相同ID的订单都将被取消。如果未发送orderID和clOrderID，则取消将针对当前市场中的所有订单。

### 请求参数

| 名称       | 类型    | 是否必须 | 描述                                                                                                                                                                    |
| ---        | ---     | ---      | ---                                                                                                                                                                    |
| symbol     | string  | Yes      | 市场符号                                                                                                                                                               |
| orderID    | string  | No       | 订单的唯一标识符。当未提供`clOrderID`时为必填项。如果提供了`orderID`，将忽略`clOrderID`。                                                                                |
| clOrderID  | string  | No       | 客户端自定义订单ID。当未提供`orderID`时为必填项。                                                                                                                                                  |


### 响应内容

| 名称            | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                                                        |
| ---             | ---     | ---      | ---                                                                                                                                                                                                                                                                                                        |
| symbol          | string  | Yes      | 市场符号                                                                                                                                                                                                                                                                                                   |
| clOrderID       | string  | Yes      | 交易者发送的客户标签                                                                                                                                                                                                                                                                                       |
| fillSize        | double  | Yes      | 已成交的交易大小                                                                                                                                                                                                                                                                                           |
| orderID         | string  | Yes      | 订单ID                                                                                                                                                                                                                                                                                                     |
| orderType       | integer | Yes      | 订单类型 <br/>76: 限价订单<br/>77: 市价订单<br/>80: 算法订单                                                                                                                                                                                                                                               |
| postOnly        | boolean | Yes      | 表明订单是否为仅发布订单                                                                                                                                                                                                                                                                                   |
| price           | double  | Yes      | 订单价格                                                                                                                                                                                                                                                                                                   |
| side            | string  | Yes      | 订单方向<br/>BUY 或 SELL                                                                                                                                                                                                                                                                                   |
| size            | long    | Yes      | 以`合同大小`表示的订单大小（即使在风险限额调整后也保持不变）                                                                                                                                                                                                                                                  |
| status          | long    | Yes      | 订单状态<br/>2: 订单已插入<br/>3: 订单已交易<br/>4: 订单已完全交易<br/>5: 订单部分交易<br/>6: 订单已取消<br/>7: 订单已退款<br/>9: 触发已插入<br>10: 触发已激活<br/>15: 订单被拒绝<br/>16: 订单未找到<br/>17: 请求失败                                                                                              |
| time_in_force   | string  | Yes      | 订单有效性                                                                                                                                                                                                                                                                                                |
| timestamp       | long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                                                |
| trigger         | boolean | Yes      | 表明订单是否为触发订单的指示器                                                                                                                                                                                                                                                                            |
| triggerPrice    | double  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                                                  |
| avgFillPrice    | double  | Yes      | 平均成交价格。对于部分交易的订单返回平均成交价格                                                                                                                                                                                                                                                          |
| message         | string  | Yes      | 交易消息                                                                                                                                                                                                                                                                                                  |
| stealth         | double  | Yes      | 订单的隐秘值                                                                                                                                                                                                                                                                                              |
| deviation       | double  | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                                              |
| remainingSize   | double  | Yes      | 剩余待交易的大小                                                                                                                                                                                                                                                                                          |
| originalSize    | double  | Yes      | 原始订单大小                                                                                                                                                                                                                                                                                              |

## 死人开关（在之后取消所有订单）

> 请求

```json
{
  "timeout": 60000
}
```

`POST /api/v2.1/order/cancelAllAfter`

死人开关允许交易员发送一个超时值，这是一个订单的生存时间（TTL）值。通过发送另一个“cancelAllAfter”请求来延长超时时间。如果服务器在超时时间到达之前没有收到另一个请求，那么所有订单将被取消。

### 请求参数

| 名称     | 类型  | 是否必须 | 描述                         |
| ---      | ---   | ---      | ---                          |
| timeout  | long  | Yes      | 超时值，以毫秒为单位          |


> 响应内容

* 如果设置正确，将返回HTTP 200响应代码

## 查询未完成订单

> 请求

```
/api/v2.1/user/open_orders?symbol=BTCPFC
```

> Response

```json
[
  {
    "orderType": 76,
    "price": 21000.0,
    "size": 1,
    "side": "BUY",
    "filledSize": 0,
    "orderValue": 21.0,
    "pegPriceMin": 0.0,
    "pegPriceMax": 0.0,
    "pegPriceDeviation": 1.0,
    "cancelDuration": 0,
    "timestamp": 1660645487032,
    "orderID": "2eb1c6f5-2ab2-4706-ab88-eea6b710a78b",
    "stealth": 1.0,
    "triggerOrder": false,
    "triggered": false,
    "triggerPrice": 0.0,
    "triggerOriginalPrice": 0.0,
    "triggerOrderType": 0,
    "triggerTrailingStopDeviation": 0.0,
    "triggerStopPrice": 0.0,
    "symbol": "BTCPFC",
    "trailValue": 0.0,
    "clOrderID": "string",
    "reduceOnly": false,
    "orderState": "STATUS_ACTIVE",
    "triggerUseLastPrice": false,
    "avgFilledPrice": 0.0,
    "timeInForce": "GTC",
    "averageFillPrice": 0.0
  }
]
```

`GET /api/v2.1/user/open_orders`

检索尚未匹配或最近已匹配的未完成订单。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                    |
| ---                | ---     | ---      | ---                                                                                     |
| symbol             | string  | No       | 市场符号                                                                                 |
| orderID            | string  | No       | 使用内部订单ID查询                                                                        |
| clOrderID          | string  | No       | 使用自定义订单ID查询。如果提供了`orderID`，`clOrderID`将被忽略。                                   |
| useNewSymbolNaming | boolean | No       | 若为True，则返回新格式的期货市场名称，默认为False                                       |

### 响应内容

| 名称                         | 类型    | 是否必须 | 描述                                                                                  |
| ---                          | ---     | ---      | ---                                                                                   |
| symbol                       | string  | Yes      | 市场符号                                                                               |
| clOrderID                    | string  | Yes      | 交易员发送的客户标签                                                                   |
| filledSize                   | long    | Yes      | 已成交的交易量                                                                         |
| orderValue                   | double  | Yes      | 名义价值                                                                               |
| pegPriceMin                  | double  | Yes      | 最小挂钩价格                                                                           |
| pegPriceMax                  | double  | Yes      | 最大挂钩价格                                                                           |
| pegPriceDeviation            | double  | Yes      | 偏差百分比。仅适用于Algo订单                                                           |
| cancelDuration               | long    | Yes      | 以毫秒为单位的过期时间。<br/>0: GTC<br/>-1: IOC                                        |
| orderID                      | string  | Yes      | 订单ID                                                                                 |
| orderType                    | integer | Yes      | 订单类型 <br/>76: 限价单<br/>77: 市价单<br/>80: Algo订单                               |
| timeInForce                  | string  | Yes      | 订单有效期                                                                             |
| price                        | double  | Yes      | 订单价格                                                                               |
| side                         | string  | Yes      | 订单方向<br/>BUY 或 SELL                                                               |
| size                         | long    | Yes      | 合同大小中的订单大小                                                                   |
| timestamp                    | long    | Yes      | 订单时间戳                                                                             |
| triggerOrder                 | bool    | Yes      | 指示这是否为触发订单                                                                   |
| triggered                    | bool    | Yes      | 指示此订单是否已被触发                                                                 |
| triggerUseLastPrice          | bool    | Yes      | 指示此触发订单是否使用最后价格                                                         |
| triggerPrice                 | double  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                              |
| triggerOriginalPrice         | double  | Yes      | 原始触发价格                                                                           |
| triggerOrderType             | string  | Yes      | 触发订单类型 <br/>1001: 触发止损 <br/>1002: 触发获利                                   |
| triggerTrailingStopDeviation | double  | Yes      | 保留属性                                                                               |
| triggerStopPrice             | double  | Yes      | 保留属性                                                                               |
| trailValue                   | double  | Yes      | 保留属性                                                                               |
| reduceOnly                   | bool    | Yes      | 指示此订单是否仅为减少                                                                 |
| avgFilledPrice               | double  | Yes      | 平均成交价格。返回部分交易订单的平均成交价格                                           |
| averageFillPrice             | double  | Yes      | 平均成交价                                                                             |
| stealth                      | double  | Yes      | 订单的隐身值                                                                           |
| orderState                   | string  | Yes      | `STATUS_ACTIVE`, `STATUS_INACTIVE`                                                     |

## 查询交易成交记录

> 请求

```
/api/v2.1/user/trade_history?symbol=BTCPFC
```

> 响应

```json
[
  {
    "base": "string",
    "clOrderID": "string",
    "feeAmount": 0,
    "feeCurrency": "string",
    "filledPrice": 0,
    "filledSize": 0,
    "averageFillPrice": 0,
    "orderId": "string",
    "orderType": 0,
    "price": 0,
    "quote": "string",
    "realizedPnl": 0,
    "serialId": 0,
    "side": "string",
    "size": 0,
    "symbol": "string",
    "timestamp": 0,
    "total": 0,
    "tradeId": "string",
    "triggerPrice": 0,
    "triggerType": 0,
    "username": "string",
    "wallet": "string"
  }
]
```

`GET /api/v2.1/user/trade_history`

获取用户的交易历史

### 请求参数

| 名称              | 类型    | 是否必须 | 描述                                                                                               |
| ---               | ---     | ---      | ---                                                                                                |
| symbol            | string  | No       | 市场符号                                                                                            |
| startTime         | long    | No       | 开始时间 (例如：1624987283000)                                                                      |
| endTime           | long    | No       | 结束时间 (例如：1624987283000)                                                                      |
| beforeSerialId    | string  | No       | 获取指定序列ID之前的记录的条件。用于分页                                                             |
| afterSerialId     | string  | No       | 获取指定序列ID之后的记录的条件。用于分页                                                             |
| count             | long    | No       | 返回的记录数量                                                                                      |
| includeOld        | boolean | No       | 检索过去7天的交易历史记录                                                                            |
| clOrderID         | string  | No       | 通过自定义订单ID查询交易历史                                                                         |
| useNewSymbolNaming| boolean | No       | 若为True，则使用新格式的期货市场名称作为符号， 默认为False                                             |

### 响应内容

| 名称             | 类型    | 是否必须 | 描述                                                                                                                                                                                 |
| ---              | ---     | ---      | ---                                                                                                                                                                                  |
| symbol           | string  | Yes      | 市场符号                                                                                                                                                                            |
| side             | string  | Yes      | 交易方向。可取值为: [`BUY`, `SELL`]                                                                                                                                                  |
| price            | double  | Yes      | 成交价格                                                                                                                                                                             |
| size             | long    | Yes      | 成交数量                                                                                                                                                                             |
| serialId         | long    | Yes      | 序列号，连续的序列号                                                                                                                                                                 |
| tradeId          | string  | Yes      | 交易标识符                                                                                                                                                                          |
| timestamp        | long    | Yes      | 成交时间戳                                                                                                                                                                          |
| base             | string  | Yes      | 基础货币                                                                                                                                                                            |
| quote            | string  | Yes      | 报价货币                                                                                                                                                                            |
| wallet           | string  | Yes      | 钱包名称<br/>`CROSS@`: 跨钱包<br/>`ISOLATED@market`: Market指的是当前的符号，后面跟`-USD`。例如，BTCPFC的独立钱包为`ISOLATED@BTCPFC-USD`                                               |
| clOrderID        | string  | Yes      | 自定义订单ID                                                                                                                                                                         |
| orderId          | string  | Yes      | 订单ID                                                                                                                                                                              |
| username         | string  | Yes      | btse 用户名                                                                                                                                                                          |
| triggerType      | long    | Yes      | 触发类型<br/>1001: 止损<br/>1002: 获利                                                                                                                                              |
| feeAmount        | long    | Yes      | 费用金额                                                                                                                                                                            |
| feeCurrency      | long    | Yes      | 费用货币                                                                                                                                                                            |
| filledPrice      | double  | Yes      | 平均成交价格                                                                                                                                                                        |
| averageFillPrice | double  | Yes      | 平均成交价格                                                                                                                                                                        |
| triggerPrice     | double  | Yes      | 触发价格                                                                                                                                                                            |
| filledSize       | long    | Yes      | 成交大小                                                                                                                                                                            |
| orderType        | integer | Yes      | 订单类型                                                                                                                                                                            |
| realizedPnL      | double  | Yes      | 现货中未使用                                                                                                                                                                        |
| total            | long    | Yes      | 现货中未使用                                                                                                                                                                        |


## 查询持仓

> 请求

```
/api/v2.1/user/positions?symbol=BTCPFC
```

> 响应

```json
[
  {
    "marginType": 0,
    "entryPrice": 0,
    "markPrice": 71126.6,
    "symbol": "BTCPFC",
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
    "currentLeverage": 0
  }
]
```

`GET /api/v2.1/user/positions`

查询用户当前的仓位。当未指定交易对时，将返回所有市场的仓位。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                     |
| ---                | ---     | ---      | ---                                                                                      |
| symbol             | string  | No       | 市场符号                                                                                  |
| useNewSymbolNaming | boolean | No       | 若为True，则使用新格式的期货市场名称作为符号， 默认为False                                |

### 响应内容

| 名称                   | 类型    | 是否必须 | 描述                                                                                              |
| ---                    |---------| ---      | ---                                                                                               |
| symbol                 | string  | Yes      | 市场符号                                                                                           |
| side                   | string  | Yes      | 仓位方向。可取值为: [`Buy`, `SELL`]                                                                 |
| size                   | long    | Yes      | 仓位大小                                                                                           |
| entryPrice             | double  | Yes      | 入场价格                                                                                           |
| markPrice              | double  | Yes      | 标记价格                                                                                           |
| marginType             | long    | Yes      | 保证金类型。值如下<br/>91: CROSS钱包<br/>92: 独立钱包                                                 |
| orderValue             | double  | Yes      | 名义价值                                                                                           |
| settleWithAsset        | string  | Yes      | 结算货币                                                                                           |
| totalMaintenanceMargin | double  | Yes      | 维持保证金                                                                                         |
| unrealizedProfitLoss   | double  | Yes      | 未实现的利润和损失                                                                                  |
| liquidationPrice       | double  | Yes      | 清算价格                                                                                           |
| isolatedLeverage       | double  | Yes      | 独立杠杆值                                                                                         |
| adlScoreBucket         | double  | Yes      | ADL得分概率                                                                                        |
| liquidationInProgress  | boolean | Yes      | 指示是否正在进行清算                                                                               |
| currentLeverage        | double  | Yes      | 当前杠杆                                                                                           |
| timestamp              | long    | Yes      | 查询仓位时的时间戳                                                                                 |


## 平仓仓位

> 请求

```json
{
  "price": 0,
  "symbol": "BTCPFC",
  "type": "MARKET"
}
```

> Response

```json
[
  {
    "status": 4,
    "symbol": "BTCPFC",
    "orderType": 76,
    "price": 24010.0,
    "side": "SELL",
    "size": 1,
    "orderID": "93cf814a-595e-4b20-bba9-5c5340ca947d",
    "timestamp": 1660710188450,
    "triggerPrice": 0.0,
    "trigger": false,
    "deviation": 100.0,
    "stealth": 100.0,
    "message": "",
    "avgFillPrice": 24010.0,
    "fillSize": 1.0,
    "clOrderID": "",
    "originalSize": 1.0,
    "postOnly": false,
    "remainingSize": 0.0,
    "time_in_force": "GTC"
  }
]
```

`POST /api/v2.1/order/close_position`

平仓用户在特定市场上指定的仓位。如果指定类型为LIMIT，则价格是必须的。当类型为MARKET时，以市场价格平仓仓位。


### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                                                 |
|--------------------| ---     | ---      | --------------------------------------------------------------------------------------------------------------------|
| symbol             | string  | Yes      | 市场符号                                                                                                             |
| type               | string  | Yes      | 平仓类型，其值为：<br/>LIMIT: 以`price`价格平仓<br/>MARKET: 以市价平仓                                                 |
| price              | double  | No       | 平仓价格。当类型为`LIMIT`时，此字段为必填                                                                           |
| postOnly           | boolean | No       | 布尔值，表示此是否为仅发布订单。对于仅发布的订单，交易员将被收取制造商费用                                           |
| useNewSymbolNaming | boolean | No       | 若为True，则使用新格式的期货市场名称作为符号，默认为False                                                           |

### 响应内容

| 名称           | 类型    | 是否必须 | 描述                                                                                                                                                                                                                                                                          |
| ---            | ---     | ---      | ---                                                                                                                                                                                                                                                                           |
| symbol         | string  | Yes      | 市场符号                                                                                                                                                                                                                                                                     |
| clOrderID      | string  | Yes      | 交易员发送的客户标签                                                                                                                                                                                                                                                        |
| fillSize       | string  | Yes      | 已成交的交易量                                                                                                                                                                                                                                                               |
| orderID        | string  | Yes      | 订单ID                                                                                                                                                                                                                                                                       |
| orderType      | integer | Yes      | 订单类型 <br/>76: 限价单<br/>77: 市价单<br/>80: Algo订单                                                                                                                                                                                                                     |
| postOnly       | boolean | Yes      | 表示订单是否仅为发布订单                                                                                                                                                                                                                                                     |
| price          | double  | Yes      | 订单价格                                                                                                                                                                                                                                                                     |
| side           | string  | Yes      | 订单方向<br/>BUY 或 SELL                                                                                                                                                                                                                                                    |
| size           | long    | Yes      | 已取消的大小                                                                                                                                                                                                                                                                |
| status         | long    | Yes      | 订单状态<br/>2: 已插入订单<br/>3: 已交易订单<br/>4: 订单已全部交易<br/>5: 订单部分交易<br/>6: 已取消订单<br/>7: 已退款订单<br/>9: 触发器已插入<br>10: 触发器已激活<br/>15: 订单被拒绝<br/>16: 找不到订单<br/>17: 请求失败                                                   |
| time_in_force  | string  | Yes      | 订单有效性                                                                                                                                                                                                                                                                  |
| timestamp      | long    | Yes      | 订单时间戳                                                                                                                                                                                                                                                                  |
| trigger        | string  | Yes      | 指示订单是否为触发订单                                                                                                                                                                                                                                                      |
| triggerPrice   | string  | Yes      | 订单触发价格，如果订单不是触发订单则返回0                                                                                                                                                                                                                                   |
| avgFillPrice   | string  | Yes      | 平均成交价格。返回部分交易订单的平均成交价格                                                                                                                                                                                                                                |
| message        | string  | Yes      | 交易消息                                                                                                                                                                                                                                                                    |
| stealth        | double  | Yes      | 订单的隐身值                                                                                                                                                                                                                                                                |
| deviation      | string  | Yes      | 订单的偏差值                                                                                                                                                                                                                                                                |
| remainingSize  | double  | Yes      | 剩余待交易的大小                                                                                                                                                                                                                                                           |
| originalSize   | double  | Yes      | 原始订单大小                                                                                                                                                                                                                                                               |

## 获取风险限制

> 请求

```
/api/v2.1/risk_limit?symbol=BTCPFC
```

> 响应

```json
{
    "symbol": "BTCPFC",
    "riskLimit": 100000
}
```
`GET /api/v2.1/risk_limit`

查询指定市场的风险限制
### 请求参数

| 名称     | 类型    | 是否必须 | 描述       |
| ---      | ---     | ---      | ---        |
| symbol   | string  | Yes      | 市场符号   |

### 响应内容

| 名称       | 类型    | 是否必须 | 描述                                                                                                         |
| ---        | ---     | ---      | ---                                                                                                          |
| symbol     | string  | Yes      | 市场符号                                                                                                     |
| riskLimit  | long    | Yes      | 当前的风险限制值以仓位大小表示，但随着期货市场名称的变化，它将转变为USD值                                      |

## 设置风险限制

> 请求

```json
{
  "symbol": "BTCPFC",
  "riskLimit": 0
}
```

> 响应
```json
{
  "symbol": "BTCPFC",
  "timestamp": 1577093486551,
  "status": 20,
  "type": 94,
  "message": "false"
}
```

`POST /api/v2.1/risk_limit`

更改指定市场的风险限制

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                                                                   |
| ---                | ---     | ---      | ---                                                                                                                                    |
| symbol             | string  | Yes      | 市场符号                                                                                                                               |
| riskLimit          | long    | Yes      | 当前的风险限制值以仓位大小表示，但它将在将来转变为USD值。                                                                                  |
| useNewSymbolNaming | boolean | No       | 如果使用新的期货市场名称作为符号，则为True，默认为False                                                                                 |

### 响应内容

| 名称       | 类型    | 是否必须 | 描述                                                                                                                                                     |
| ---        | ---     | ---      | ---                                                                                                                                                      |
| symbol     | string  | Yes      | 市场符号                                                                                                                                                 |
| status     | long    | Yes      | 请求的状态。可取值为：<br/>8: 余额不足<br/>12: 更新风险限额时出错<br/>20: 成功<br/>41: 风险限额无效                                                                                          |
| type       | double  | Yes      | 值将为94，表示类型为`风险限额`                                                                                                                           |
| timestamp  | long    | Yes      | 设置风险限额的时间戳                                                                                                                                      |
| message    | long    | Yes      | 消息                                                                                                                                                     |

## 设置杠杆

> 请求

```json
{
  "symbol": "BTCPFC",
  "leverage": 0
}
```

> 响应

```json
{
  "symbol": "BTCPFC",
  "timestamp": 1660711246942,
  "status": 20,
  "type": 93,
  "message": ""
}
```

`POST /api/v2.1/leverage`

更改指定市场的杠杆值

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                     |
| ---                | ---     | ---      | ---                                                                                      |
| symbol             | string  | Yes      | 市场符号                                                                                 |
| leverage           | long    | Yes      | 杠杆值                                                                                   |
| useNewSymbolNaming | boolean | No       | 如果使用新的期货市场名称作为符号，则为True，默认为False                                 |

### 响应内容

| 名称       | 类型    | 是否必须 | 描述                                                                                                                                                          |
| ---        | ---     | ---      | ---                                                                                                                                                           |
| symbol     | string  | Yes      | 市场符号                                                                                                                                                      |
| status     | long    | Yes      | 请求的状态。可取值为：<br/>8: 余额不足<br/>13: 无效的杠杆<br/>20: 成功<br/>64: 正在进行的清算                                                                                             |
| type       | double  | Yes      | 值将为93，表示类型为`杠杆`                                                                                                                                    |
| timestamp  | long    | Yes      | 设置杠杆的时间戳                                                                                                                                               |
| message    | long    | Yes      | 消息                                                                                                                                                          |

## 获取杠杆倍数

> 响应

```json
{
  "symbol": "BTC-PERP",
  "leverage": 100.0
}
```

`Get /api/v2.1/leverage`

获取指定市场的杠杆值

### 请求参数

| 名称     | 类型    | 是否必须 | 描述       |
| ---      | ---     | ---      | ---        |
| symbol   | string  | Yes      | 市场符号   |

### 响应内容

| 名称      | 类型    | 是否必须 | 描述                                                                                                       |
| ---       | ---     | ---      | ---                                                                                                        |
| symbol    | string  | Yes      | 市场符号                                                                                                   |
| leverage  | double  | Yes      | 对于隔离保证金模式下的市场的当前杠杆值，如果保证金模式为交叉，则返回0                                       |

## 更改合约结算货币

> 请求

```json
{
  "symbol": "BTCPFC",
  "currency": "BTC"
}
```

> 响应（仅在发生错误时可用）

```json
{
  "status": 0,
  "errorCode": 0,
  "message": "string"
}
```

`POST /api/v2.1/settle_in`

更改当前市场中持仓的结算货币

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                     |
| ---                | ---     | ---      | ---                                                                                      |
| symbol             | string  | Yes      | 市场符号                                                                                 |
| currency           | string  | Yes      | 要设置的结算货币                                                                         |
| useNewSymbolNaming | boolean | No       | 若为True，则使用新格式的期货市场名称作为符号，默认为False                                |

### 响应内容

| 名称       | 类型    | 是否必须 | 描述                                                    |
| ---        | ---     | ---      | ---                                                     |
| status     | long    | No       | 状态。仅在发生错误时可用。                                |
| errorCode  | long    | No       | 错误代码。仅在发生错误时可用。                            |
| message    | string  | No       | 响应消息。仅在发生错误时可用。                            |

## 查询帐户费用

> 响应

```json
{
  "makerFee": 0,
  "symbol": "BTCPFC",
  "takerFee": 0
}
```

`GET /api/v2.1/user/fees`

查询用户的交易费用

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                     |
| ---                | ---     | ---      | ---                                                                                      |
| symbol             | string  | No       | 市场符号                                                                                 |
| useNewSymbolNaming | boolean | No       | 若为True，则使用新格式的期货市场名称作为符号，默认为False                                |

### 响应内容

| 名称      | 类型   | 是否必须 | 描述       |
| ---       | ---    | ---      | ---        |
| symbol    | string | Yes      | 市场符号   |
| makerFee  | double | Yes      | 制造商费用 |
| takerFee  | double | Yes      | 接受者费用 |

# 钱包端点

## 查询钱包余额

> 响应

```json
[
  {
    "trackingID": 0,
    "queryType": 0,
    "activeWalletName": "string",
    "wallet": "CROSS@",
    "username": "string",
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

`GET /api/v2.1/user/wallet`

查询用户的钱包余额。API密钥需要`读取`权限。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                                                                                                 |
| ---                | ---     | ---      | ---                                                                                                                                                                  |
| wallet             | string  | Yes      | 钱包名称<br/>`CROSS@`: 全仓钱包<br/>`ISOLATED@市场`: 市场指当前符号后附加`-USD`。例如，BTCPFC的隔离钱包将是`ISOLATED@BTCPFC-USD`                                             |
| useNewSymbolNaming | boolean | No       | 若为True，则返回新格式的期货市场名称，默认为False                                                                                                                    |


### 响应内容

#### 钱包

| 名称                 | 类型         | 是否必须 | 描述                               |
| ---                  | ---          | ---      | ---                                |
| wallet               | string       | Yes      | 钱包名称                           |
| activeWalletName     | string       | Yes      | 活跃的钱包名称                      |
| queryType            | integer      | Yes      | 查询类型                           |
| trackingID           | long         | Yes      | 内部跟踪ID，未被使用                |
| walletTotalValue     | double       | Yes      | 钱包总值                           |
| totalValue           | double       | Yes      | 总值                               |
| marginBalance        | double       | Yes      | 保证金余额                         |
| availableBalance     | double       | Yes      | 可用余额                           |
| unrealisedProfitLoss | double       | Yes      | 未实现的利润/损失                  |
| maintenanceMargin    | double       | Yes      | 维护保证金                         |
| leverage             | double       | Yes      | 杠杆                               |
| openMargin           | double       | Yes      | 开放保证金                         |
| assets               | Asset 对象   | Yes      | 可用资产                           |
| assetsInUse          | Asset 对象   | Yes      | 使用中的资产                       |

#### 资产 / 使用中的资产

| 名称       | 类型   | 是否必须 | 描述       |
| ---        | ---    | ---      | ---        |
| balance    | double | Yes      | 余额       |
| assetPrice | double | Yes      | 资产价格   |
| currency   | string | Yes      | 货币       |


## 查询钱包历史记录

> 响应

```json
[
  {
    "amount": 21.35823825,
    "currency": "USD",
    "description": "string",
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

`GET /api/v2.1/user/wallet_history`

获取期货钱包上的用户钱包历史记录

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                                                                                                              |
| ---                | ---     | ---      | ---                                                                                                                                                                               |
| wallet             | string  | No       | 钱包，如果未指定将返回所有钱包。有效值为：<br/>`CROSS@`: 全仓钱包<br/>`ISOLATED@BTCPFC-USD`: 隔离钱包                                                                                        |
| startTime          | long    | No       | 以毫秒为单位的开始时间（例如 1624987283000）                                                                                                                                       |
| endTime            | long    | No       | 以毫秒为单位的结束时间（例如 1624987283000）                                                                                                                                       |
| count              | integer | No       | 要返回的记录数量                                                                                                                                                                  |
| useNewSymbolNaming | boolean | No       | 若为True，则返回新格式的期货市场名称，默认为False                                                                                                                                 |


### 响应内容

| 名称        | 类型    | 是否必须 | 描述                                                                                                              |
| ---         | ---     | ---      | ---                                                                                                               |
| currency    | string  | Yes      | 货币                                                                                                              |
| amount      | double  | Yes      | 记录中的金额                                                                                                       |
| fees        | double  | Yes      | 如有收费                                                                                                          |
| orderId     | string  | Yes      | 内部钱包订单ID                                                                                                     |
| wallet      | string  | Yes      | 钱包类型。对于期货将返回 `CROSS@` 或 `ISOLATED@`                                                                   |
| description | string  | Yes      | 交易描述                                                                                                          |
| status      | integer | Yes      | 1: 待处理<br/>2: 处理中<br/>10: 完成<br/>16: 取消                                                                  |
| type        | integer | Yes      | 105: 钱包转账<br/>106: 钱包清算<br/>108: 已实现的PnL<br/>110: 资金<br/>121: 资产转换                                |

## 查询钱包保证金

> 响应

```json
[
  {
    "trackingID": 0,
    "queryType": 0,
    "activeWalletName": "string",
    "wallet": "CROSS@",
    "username": "string",
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

`GET /api/v2.1/user/margin`

获取指定钱包的保证金信息，以便用户知道他们当前在市场上使用的是哪个钱包。

### 请求参数

| 名称               | 类型    | 是否必须 | 描述                                                                                                              |
| ---                | ---     | ---      | ---                                                                                                               |
| symbol             | string  | No       | 货币，如果未指定，将返回所有货币                                                                                   |
| startTime          | long    | No       | 开始时间 (例如 1624987283000)                                                                                      |
| endTime            | long    | No       | 结束时间 (例如 1624987283000)                                                                                      |
| count              | integer | No       | 要返回的记录数量                                                                                                  |
| useNewSymbolNaming | boolean | No       | 若为True，则使用新格式的期货市场名称作为符号，默认为False                                                          |

### 响应内容

#### 钱包

| 名称                 | 类型         | 是否必须 | 描述                              |
| ---                  | ---          | ---      | ---                               |
| wallet               | string       | Yes      | 钱包名称                          |
| activeWalletName     | string       | Yes      | 活跃的钱包名称                     |
| queryType            | integer      | Yes      | 查询类型                          |
| trackingID           | long         | Yes      | 内部跟踪ID，未被使用               |
| walletTotalValue     | double       | Yes      | 钱包总值                          |
| totalValue           | double       | Yes      | 总值                              |
| marginBalance        | double       | Yes      | 保证金余额                        |
| availableBalance     | double       | Yes      | 可用余额                          |
| unrealisedProfitLoss | double       | Yes      | 未实现的利润/损失                 |
| maintenanceMargin    | double       | Yes      | 维护保证金                        |
| leverage             | double       | Yes      | 杠杆                              |
| openMargin           | double       | Yes      | 开放保证金                        |
| assets               | Asset 对象   | Yes      | 可用资产                          |
| assetsInUse          | Asset 对象   | Yes      | 使用中的资产                      |

#### 资产 / 使用中的资产

| 名称       | 类型   | 是否必须 | 描述       |
| ---        | ---    | ---      | ---        |
| balance    | double | Yes      | 余额       |
| assetPrice | double | Yes      | 资产价格   |
| currency   | string | Yes      | 货币       |

## 在期货钱包之间转账资金

> 请求

```json
{
  "walletSrc": "string",
  "walletSrcType": "SPOT",
  "walletDest": "string",
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
    "activeWalletName": "string",
    "wallet": "CROSS@",
    "username": "string",
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

`POST /api/v2.1/user/wallet/transfer`

在用户的钱包之间转移资金。用户可以指定源钱包和目标钱包进行资金转账。

### 请求参数

#### 钱包请求

| 名称           | 类型          | 是否必须 | 描述                                                                                                                                                                                                  |
| ---            | ---           | ---      | ---                                                                                                                                                                                                  |
| walletSrc      | string        | Yes      | 源钱包                                                                                                                                                                                               |
| walletSrcType  | string        | Yes      | 源类型，有效值为：<br/>`SPOT@`：现货钱包<br/>`CROSS@`：全仓钱包<br/>`ISOLATED@市场`：市场的隔离钱包，其中市场为市场符号                                                                                       |
| walletDest     | string        | Yes      | 目标钱包                                                                                                                                                                                             |
| walletDestType | string        | Yes      | 目标类型，有效值为：<br/>`SPOT@`：现货钱包<br/>`CROSS@`：全仓钱包<br/>`ISOLATED@市场`：市场的隔离钱包，其中市场为市场符号                                                                                     |
| apiWallets     | 钱包明细       | Yes      | 转账详细信息                                                                                                                                                                                         |

#### 钱包明细请求

| 名称       | 类型   | 是否必须 | 描述                                                                     |
| ---        | ---    | ---      | ---                                                                      |
| currency   | string | Yes      | 钱包货币                                                                 |
| allBalance | boolean| Yes      | 是否转移所有钱包余额的指示符                                               |
| balance    | double | No       | 要转移的余额值，例如：10                                                  |


### 响应内容

#### 钱包

| 名称                 | 类型         | 是否必须 | 描述                              |
| ---                  | ---          | ---      | ---                               |
| wallet               | string       | Yes      | 钱包名称                          |
| activeWalletName     | string       | Yes      | 活跃的钱包名称                     |
| queryType            | integer      | Yes      | 查询类型                          |
| trackingID           | long         | Yes      | 内部跟踪ID，未被使用               |
| walletTotalValue     | double       | Yes      | 钱包总值                          |
| totalValue           | double       | Yes      | 总值                              |
| marginBalance        | double       | Yes      | 保证金余额                        |
| availableBalance     | double       | Yes      | 可用余额                          |
| unrealisedProfitLoss | double       | Yes      | 未实现的利润/损失                 |
| maintenanceMargin    | double       | Yes      | 维护保证金                        |
| leverage             | double       | Yes      | 杠杆                              |
| openMargin           | double       | Yes      | 开放保证金                        |
| assets               | 资产对象     | Yes      | 可用资产                          |
| assetsInUse          | 资产对象     | Yes      | 使用中的资产                      |

#### 资产 / 使用中的资产

| 名称       | 类型   | 是否必须 | 描述       |
| ---        | ---    | ---      | ---        |
| balance    | double | Yes      | 余额       |
| assetPrice | double | Yes      | 资产价格   |
| currency   | string | Yes      | 货币       |


## 子账户钱包转账

`POST /api/v2.1/subaccount/wallet/transfer`

在用户和子账户钱包之间转移资金。用户可以指定源钱包和目标钱包进行资金转账。

需要`Wallet`权限。要获取支持的货币列表，请查看[用于操作的可用货币列表](#查询钱包操作的可用货币列表)。

### 请求参数

#### 钱包请求

| 名称           | 类型          | 是否必须 | 描述                                                                                                                                                                                                  |
|----------------| ---           | ---      | ---                                                                                                                                                                                                  |
| walletSrc      | string        | Yes      | 源钱包                                                                                                                                                                                               |
| walletSrcType  | string        | Yes      | 源类型，有效值为：<br/>`SPOT@`：现货钱包<br/>`CROSS@`：全仓钱包<br/>`ISOLATED@市场`：市场的隔离钱包，其中市场为市场符号                                                                                       |
| walletDest     | string        | Yes      | 目标钱包                                                                                                                                                                                             |
| walletDestType | string        | Yes      | 目标类型，有效值为：<br/>`SPOT@`：现货钱包<br/>`CROSS@`：全仓钱包<br/>`ISOLATED@市场`：市场的隔离钱包，其中市场为市场符号                                                                                     |
| fromUser       | string        | Yes      | 源用户名                                                                                                                                                                                            |
| receiver       | string        | Yes      | 接收者用户名                                                                                                                                                                                        |
| apiWallets     | 钱包明细       | Yes      | 转账详细信息                                                                                                                                                                                         |

#### 钱包明细请求

| 名称       | 类型   | 是否必须 | 描述                                                                     |
| ---        | ---    | ---      | ---                                                                      |
| currency   | string | Yes      | 钱包货币                                                                 |
| allBalance | boolean| Yes      | 是否转移所有钱包余额的指示符                                               |
| balance    | double | No       | 要转移的余额值，例如：10                                                  |


### 响应内容

#### 钱包

| 名称                 | 类型     | 是否必须 | 描述               |
|----------------------|----------|----------|---------------------|
| code                 | integer  | Yes      | 响应代码            |
| msg                  | string   | Yes      | 响应消息            |
| time                 | integer  | Yes      | 响应时间            |
| data                 | object   | No       |                     |
| success              | boolean  | Yes      | 转账是否成功         |


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
    "snapshotL1:BTCPFC_0"
  ]
}

{
  "op": "unsubscribe",
  "args": [
    "snapshotL1:BTCPFC_0"
  ]
}
```

> 响应

```json
{
  "topic": "snapshotL1:BTCPFC_0",
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
    "symbol": "BTCPFC",
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
| topic  | string      | Yes      | Websocket主题           |
| data   | 数据对象    | Yes      | 参见下面的数据对象      |

#### 数据对象

| 名称      | 类型        | 是否必须 | 描述                                                                                    |
| ---       | ---         | ---      | ---                                                                                    |
| bids      | 报价对象    | Yes      | 买入报价                                                                                |
| asks      | 报价对象    | Yes      | 卖出报价                                                                                |
| symbol    | string      | Yes      | 市场符号                                                                                |
| type      | string      | Yes      | `snapshotL1` - L1数据指的是交易对订单簿的最佳买入/最佳卖出价。                                   |
| timestamp | long        | Yes      | 订单簿时间戳                                                                           |

## 订单簿增量更新

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "update:BTCPFC_0"
  ]
}
```

```json
{
  "op": "unsubscribe",
  "args": [
    "update:BTCPFC_0"
  ]
}
```

> 响应

```json
{
  "topic": "update:BTCPFC_0",
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
    "symbol": "BTCPFC"
  }
}
```

```json
{
  "topic": "update:BTCPFC",
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
    "symbol": "BTCPFC"
  }
}
```

通过端点`wss://ws.btse.com/ws/oss/futures`订阅订单簿增量更新。主题的格式将为`update:symbol_grouping`（例如`update:BTCPFC_0`）。首次收到的响应将是当前订单簿的快照（这在`type`字段中有标示），并将返回50个级别。随后的数据包中将发送增量更新，类型为`delta`。

买入和卖出将以`price`和`size`的元组形式发送。发送的大小将是价格的新更新大小。如果发送了一个`0`的值，则应从订单簿的本地副本中删除该价格。

为确保按顺序接收到更新，`seqNum`指示当前序列，而`prevSeqNum`指前一个数据包。`seqNum`总是在`prevSeqNum`之后。如果序列是乱序的，您将需要取消订阅并再次订阅该主题。

如果当最佳买入价高于或等于最佳卖出价时发生[交叉订单簿](https://en.wikipedia.org/wiki/Order_book#Crossed_book)，请取消订阅并重新订阅该主题。

### 响应内容

#### 订单簿对象

| 名称      | 类型       | 是否必须 | 描述                 |
| ---       | ---        | ---      | ---                  |
| topic     | string     | Yes      | Websocket主题        |
| data      | Data Object | Yes      | 参见下面的数据对象   |

#### 数据对象

| 名称       | 类型        | 是否必须 | 描述                                                                                                               |
| ---        | ---         | ---      | ---                                                                                                               |
| bids       | Quote Object | Yes      | 买入报价                                                                                                           |
| asks       | Quote Object | Yes      | 卖出报价                                                                                                           |
| seqNum     | int         | Yes      | 当前序列号                                                                                                         |
| prevSeqNum | int         | Yes      | 上一个序列号                                                                                                       |
| type       | string      | Yes      | `snapshot` - 订单簿的快照，最多有50个级别<br/> `delta` - 订单簿的更新                                                |
| timestamp  | long        | Yes      | 订单簿的时间戳                                                                                                     |
| symbol     | string      | Yes      | 订单簿符号                                                                                                         |

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
    "tradeHistoryApi:BTCPFC"
  ]
}
```

> 响应

```json
{
  "event": "subscribe",
  "channel": [
    "tradeHistoryApi:BTCPFC"
  ]
}
```

通过Websocket订阅公共交易填充

### 请求参数

| 名称 | 类型  | 是否必须 | 描述                                                                                                       |
| ---  | ---   | ---     | ---                                                                                                       |
| op   | string | Yes     | 操作。`subscribe` 将订阅在`args`中提供的主题。`unsubscribe` 将取消订阅主题                               |
| args | array  | Yes     | 要订阅的主题。                                                                                             |

### 响应内容

| 名称    | 类型  | 是否必须 | 描述                                       |
| ---     | ---   | ---     | ---                                       |
| event   | string | Yes     | 响应的事件类型                             |
| channel | array  | Yes     | 已成功订阅的主题                           |




## 公共交易填充

> 请求

```json
{
  "op": "subscribe",
  "args": [
    "tradeHistoryApi:BTCPFC"
  ]
}
```

> 响应

```json
{
  "topic": "tradeHistoryApi:BTCPFC",
  "data": [
  {
    "symbol": "BTCPFC",
    "side": "SELL",
    "size": 0.007,
    "price": 5302.8,
    "tradeId": 118974855,
    "timestamp": 1584446020295
  }
  ]
}
```

订阅市场的最近交易提要。主题将是 `tradeHistoryApi:<market>`，其中`<market>` 是市场符号。

### 响应内容

#### TradeHistory 对象

| 名称  | 类型        | 是否必须 | 描述                             |
| ---   | ---         | ---     | ---                             |
| topic | string      | Yes     | Websocket 主题                   |
| data  | Data Object | Yes     | 请参考下面的数据对象             |

#### 数据对象

| 名称      | 类型   | 是否必须 | 描述                     |
| ---       | ---    | ---      | ---                     |
| symbol    | string | Yes      | 市场符号                 |
| side      | string | Yes      | 交易方向，BUY 或 SELL   |
| size      | double | Yes      | 交易量                   |
| price     | double | Yes      | 交易价格                 |
| tradeId   | long   | Yes      | 交易序列号               |
| timestamp | long   | Yes      | 交易时间戳               |

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
| 0    | string | 是       | 第一个参数是 API 密钥                   |
| 1    | long   | 是       | Nonce，即当前的时间戳                    |
| 2    | string | 是       | 生成的签名                             |

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
    "notificationApiV2"
  ]
}
```

> 响应

```json
{
  "topic": "notificationApiV2",
  "data": [
    {
      "symbol": "Market Symbol (eg. BTCPFC)",
      "orderID": "BTSE internal order ID",
      "side": "BUY",
      "type": "76",
      "price": "Order price or transacted price",
      "size": "Order size or transacted size",
      "originalSize": "Order size",
      "avgFillPrice": 35000,
      "fillSize": 0.001,
      "status": "<Refer to Status description on the left>",
      "clOrderID": "<Client order ID>",
      "maker": "<Maker flag, if true indicates that trade is a maker trade>",
      "stealth": 1,
      "timestamp": 1624985375123,
      "pegPriceDeviation": "Indicate the deviation percentage. Valid for only algo orders.",
      "remainingSize": "<Remaining size on the order>",
      "time_in_force": "<Time where this order is valid>",
      "txType": "STOP | TAKE_PROFIT",
      "triggerPrice": "Trade Trigger Price"
    }
  ]

}

```

接收交易通知通过订阅主题 `notificationApiV2`。Websocket将向订阅者推送交易级别的通知。如果在未经认证的情况下订阅主题，将不会发送任何消息。

### 响应内容

| 名称              | 类型    | 必须 | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---               | ---     | ---  | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| symbol            | string  | Yes      | 市场符号                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| orderID           | string  | Yes      | 内部订单ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| side              | string  | Yes      | 交易方向。BUY 或 SELL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| type              | int     | Yes      | 订单类型。有效值为：<br/>76: 限价订单<br/>77: 市价订单<br/>80: 算法订单                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| price             | double  | Yes      | 订单价格或交易价格                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| size              | double  | Yes      | 订单大小或交易大小                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| originalSize      | double  | Yes      | 原始订单大小                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| avgFilledPrice    | double  | Yes      | 平均成交价格                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| fillSize          | double  | Yes      | 订单的成交量                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| status            | integer | Yes      | 状态值如下：<br/>1: 市场不可用<br/>2: 订单成功插入<br/>4: 订单全部交易<br/>5: 订单部分交易<br/>6: 订单成功取消<br/>8: 账户余额不足<br/>9: 触发订单成功插入<br/>10: 触发订单成功激活<br/>12: 更新风险限额时出错<br/>15: 订单被拒绝<br/>20: 交易成功完成<br/>27: 期货和现货之间转账成功<br/>28: 期货和现货之间转账失败<br/>41: 指定了无效的风险限额<br/>64: 账户正在进行清算<br/>96: 设置期货结算货币<br/>101: 期货订单超出清算价格<br/>1003: 订单正在清算<br/>1004: 订单正在ADL |
| clOrderID         | string  | Yes      | 自定义订单ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| maker             | boolean | Yes      | 指示交易是否为做市商交易                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| remainingSize     | double  | Yes      | 订单上的剩余大小                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| time_in_force     | string  | Yes      | 订单的有效期                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| timestamp         | long    | Yes      | 订单时间戳或交易时间戳                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| txType            | string  | Yes      | 用于触发或OCO订单。STOP 表示它是一个停止订单，TAKEPROFIT 表示它是一个止盈订单，LIMIT 表示它不是上述任何一个                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| stealth           | double  | Yes      | 在订单簿上显示的订单百分比。仅用于算法订单                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| pegPriceDeviation | double  | Yes      | 偏差百分比。仅用于算法订单                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

## 用户交易记录

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
    "orderId": "order id", //string
    "serialId": "serial ID after insertion into DB", //integer / long
    "clOrderId": "Client Order ID", //string
    "type": "order type", //string
    "symbol": "ex: BTC-USD", //string
    "side": "BUY|SELL" //string
    "price": "filled price", //double (need to make sure no scientific notation)
    "size": "filled size", //double (no scientific notation)
    "feeAmount": "Fees charged to user, value to be String on API", //double (no scientific notation)
    "feeCurrency": "Fee currency, eg. Buy would be BTC, Sell would be USD" //string
    "base": "Base currency, eg. BTC",  //string
    "quote": "Quote currency eg. USD", //string
    "maker": "maker or taker",  //boolean (if maker, return true, else return false)
    "timestamp": "Time trade was matched in the engine" //long, field taken from DB,
    "tradeId": "Trade Unique ID"
  }]
}


```

当交易完成后，此主题将把交易信息发回给订阅者。

### 响应内容

| 名称        | 类型    | 必须 | 描述                                                                                                      |
| ---         | ---     | ---  | ---                                                                                                      |
| symbol      | string  | Yes      | 市场符号                                                                                                  |
| orderID     | string  | Yes      | 内部订单ID                                                                                                |
| clOrderID   | string  | Yes      | 自定义订单ID                                                                                              |
| serialId    | string  | Yes      | 交易序列ID                                                                                                |
| tradeId     | string  | Yes      | 交易唯一标识符                                                                                            |
| type        | int     | Yes      | 订单类型。有效值为：<br/>76: 限价订单<br/>77: 市价订单<br/>80: 算法订单                                   |
| side        | string  | Yes      | 交易方向。BUY 或 SELL                                                                                     |
| price       | double  | Yes      | 交易价格                                                                                                  |
| size        | double  | Yes      | 交易大小                                                                                                  |
| feeAmount   | double  | Yes      | 所收费用                                                                                                  |
| feeCurrency | string  | Yes      | 费用货币                                                                                                  |
| base        | string  | Yes      | 基础货币                                                                                                  |
| quote       | string  | Yes      | 报价货币                                                                                                  |
| maker       | boolean | Yes      | 指示交易是否为做市商交易                                                                                  |
| timestamp   | long    | Yes      | 订单时间戳或交易时间戳                                                                                    |

## 所有仓位

> 请求

```json
{
  "op":"subscribe",
  "args":["allPosition"]
}
```

> 响应

```
{
  "topic": "allPosition",
  "data": [{
    "requestId": 0,
    "username": "btse",
    "marketName": "BTCPFC-USD",
    "orderType": 90,
    "orderMode": 66,
    "originalAmount": 0.001,
    "maxPriceHeld": 0.0,
    "pegPriceMin": 0.0,
    "stealth": 1.0,
    "orderID": null,
    "maxStealthDisplayAmount": 0.0,
    "sellexchangeRate": 0.0,
    "triggerPrice": 0.0,
    "closeOrder": false,
    "liquidationInProgress": false,
		"marginType": 91,
		"entryPrice": 47303.404761929,
		"liquidationPrice": 0.0,
		"markedPrice": 47293.949862586,
		"unrealizedProfitLoss": -0.13236859,
		"totalMaintenanceMargin": 3.484381756,
		"totalContracts": 14.0,
		"isolatedLeverage": 0.0,
		"totalFees": 0.0,
		"totalValue": 662.115298076,
		"adlScoreBucket": 2.0,
		"orderTypeName": "TYPE_FUTURES_POSITION",
		"orderModeName": "MODE_BUY",
		"marginTypeName": "FUTURES_MARGIN_CROSS",
		"currentLeverage": 0.02,
		"avgFillPrice": 0.0,
		"settleWithNonUSDAsset": "BTC"
  }]
}
```

所有期货仓位都会通过此主题定期推送。

### 响应内容

| 名称                    | 类型    | 必须 | 描述                                              |
| ---                     | ---     | ---  | ---                                              |
| requestId               | integer | Yes      | 请求ID                                            |
| username                | string  | Yes      | btse 用户名                                        |
| marketName              | string  | Yes      | 市场名称                                           |
| orderType               | integer | Yes      | 90: 期货头寸                                        |
| orderTypeName           | string  | Yes      | orderType的字符串表示                               |
| orderMode               | integer | Yes      | 66: 买入<br/>83: 卖出                               |
| orderModeName           | string  | Yes      | orderModeName的字符串表示                           |
| originalAmount          | double  | Yes      | 订单金额                                           |
| maxPriceHeld            | double  | Yes      | 历史最高价格                                        |
| pegPriceMin             | double  | Yes      | peg最小价格                                         |
| stealth                 | double  | Yes      | 用于peg订单                                         |
| orderID                 | string  | Yes      | 订单ID                                              |
| maxStealthDisplayAmount | double  | Yes      | 用于peg订单                                         |
| sellexchangeRate        | double  | Yes      |                                                    |
| triggerPrice            | double  | Yes      | OCO订单                                             |
| closeOrder              | boolean | Yes      | 订单是否关闭                                         |
| liquidationInProgress   | boolean | Yes      | 是否正在清算                                        |
| marginType              | integer | Yes      | 钱包类型：<br/>91: 全仓<br/>92: 隔离                    |
| marginTypeName          | string  | Yes      | marginType的字符串表示                               |
| entryPrice              | double  | Yes      | 进场价格                                            |
| liquidationPrice        | double  | Yes      | 清算价格                                            |
| markPrice               | double  | Yes      | 标记价格                                            |
| unrealizedProfitLoss    | double  | Yes      | 未实现的利润和损失                                    |
| totalMaintenanceMargin  | double  | Yes      | 维护保证金                                           |
| totalContract           | double  | Yes      | 合约的大小                                           |
| isolatedLeverage        | double  | Yes      |                                                    |
| totalFees               | double  | Yes      |                                                    |
| totalValue              | double  | Yes      |                                                    |
| adlScoreBucket          | double  | Yes      |                                                    |
| currentLeverage         | double  | Yes      |                                                    |
| avgFillPrice            | double  | Yes      |                                                    |
| settleWithNonUSDAsset   | string  | Yes      |                                                    |

</section>
