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

## 版本 1.1.3 (2025年7月10日)

* [**重要**] BTSE 将于 2025年7月10日 起逐步停止支持以下两个 Open API 接口。以下接口将被弃用:
  - [`查询货币的可用加密网络列表`](#40af277644)
  - [`查询资产间的汇率`](#9dbf83fe7f)

  我们鼓励开发者尽快停止使用这些接口，因为它们将在 7 月底之后不再受支持。可点击此处访问用于替代的全新升级接口：
  
  - [`查询加密货币网络信息`](#3526dbe03b)
  - [`资产兑换汇率查询`](#52edd98764)

## 版本 1.1.2 (2024年4月10日)

* 更新 [`查询钱包历史`](#bc1c4a9961) 中的 `status` 與 `type` 的描述

## 版本 1.1.1 (2024年04月08日)

* 新增[`子帐号转帐历史纪录`](#dfc184460c)API

## 版本 1.1.0 (2022年11月16日)

* [重要] BTSE 将在 **2022年12月** 更改期货市场命名约定，以便为零售用户提供更多清晰度，以下是规则：
  - 将永续市场的后缀从 `PFC` 更改为 `PERP`（例如：BTCPFC -> BTC-PERP）
  - 将基于时间的市场的后缀从 `交货月份+年份` 更改为 `结算日期 (YYMMDD)`（例如：BTCZ22 -> BTC-221230）
  - 在 [`查询钱包历史`](#bc1c4a9961) 和 [`转账资金`](#fff748076e) 中增加了一个新的可选查询参数 `useNewSymbolNaming`，如果用户想要使用新的市场名称

## 版本 1.0.4 (2022年8月25日)

* 调整API中货币的参数描述：[`获取钱包地址`](#b13bcdd685)，[`创建钱包地址`](#b8b48f9d66)。

## 版本 1.0.3 (2022年5月13日)

* 为 [`提款资金`](#debc5b7760) 添加参数 `includeWithdrawFee`，以设置费用将包含/额外增加。

## 版本 1.0.2 (2022年3月16日)

* [`提款资金`](#debc5b7760) 支持的最大小数位数为8，如果超过将返回 `CRYPTO_WITHDRAW_INVALID_AMOUNT (错误代码: 3506)`

## 版本 1.0.1 (2022年1月25日)

* 添加 [`查询资产间的汇率`](#9dbf83fe7f) API以获取资产之间的当前汇率

## 版本 1.0.0 (2022年1月13日)

* 将钱包相关的端点迁移到此部分

# 概览

## 生成 API 密钥

您需要在 BTSE 平台上创建一个 API 密钥，然后才能使用认证的 API。要创建 API 密钥，您可以按照以下步骤操作：

* 使用您的用户名/电子邮件和密码登录 BTSE 网站
* 点击右上角的“帐户”
* 选择 API 选项卡
* 点击 `新建 API` 按钮创建 API 密钥和密码短语。（注意：密码短语只会出现一次）
* 使用您的 API 密钥和密码短语构建一个签名。

## 端点

* 生产
  * HTTP
     * `https://api.btse.com/spot`
  * HTTP (用于[`查询加密货币网络信息`](#3526dbe03b) and [`资产兑换汇率查询`](#52edd98764))
       * `https://api.btse.com/`
  * Websocket
     * `wss://ws.btse.com/ws/spot`
  * Websocket (用于订单簿流)
     * `wss://ws.btse.com/ws/oss/spot` (用于订单簿增量更新流)
* 测试网络
  * HTTP
     * `https://testapi.btse.io/spot`
  * HTTP (用于[`查询加密货币网络信息`](#3526dbe03b) and [`资产兑换汇率查询`](#52edd98764))
       * `https://api.btse.io/`
  * Websocket
     * `wss://testws.btse.io/ws/spot`
  * Websocket (用于订单簿流)
    * `wss://testws.btse.io/ws/oss/spot` (用于订单簿增量更新流)

## 身份验证

* API 密钥 (request-api)
  * 参数名称：`request-api`，在：头部。API 密钥以字符串形式从 BTSE 平台获得

* API 密钥 (request-nonce)
  * 参数名称：`request-nonce`，在：头部。当前时间戳的长格式表示

* API 密钥 (request-sign)
  * 参数名称：`request-sign`，在：头部。基于以下算法产生的复合签名：Signature=HMAC.Sha384 (secretkey, (urlpath + request-nonce + bodyStr)) (注意：当没有数据时 bodyStr = ''):

### 示例 1：获取钱包

> **HMAC SHA384 签名**

```shell
$ echo -n "/api/v3.2/user/wallet1624984297330" | openssl dgst -sha384 -hmac "848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx"
(stdin)= 14b986706a4368221e0af14a6725377161805e7a57d568220478cb3590ce532d4fad4ac68e6c02a14afced6a0619bfd3
```

* 获取钱包的端点是 `https://api.btse.com/spot/api/v3.2/user/wallet`
* 假设我们有以下值：
  * request-nonce: `1624984297330`
  * request-api: `4e9536c79f0fdd72bf04f2430982d3f61d9d76c996f0175bbba470d69d59816x`
  * secret: `848db84ac252b6726e5f6e7a711d9c96d9fd77d020151b45839a5b59c37203bx`
  * Path: `/api/v3.2/user/wallet`
* 生成的签名将是：
  * request-sign: `14b986706a4368221e0af14a6725377161805e7a57d568220478cb3590ce532d4fad4ac68e6c02a14afced6a0619bfd3`

## 速率限制

* 以下速率限制正在执行：

BTSE 的速率限制如下：

**钱包操作**

* 每个用户：`5次请求/秒`

## API 状态码

每个 API 将返回以下其中之一的 HTTP 状态：

* 200 - API 请求成功，请参考特定 API 响应以获得预期的有效载荷
* 400 - 请求错误。服务器不会处理此请求。这通常是由于请求中发送的无效参数
* 401 - 未授权的请求。服务器不会处理此请求，因为它没有有效的身份验证凭据
* 403 - 禁止的请求。提供了凭据，但它们不足以执行请求
* 404 - 未找到。表示服务器理解请求，但找不到目标资源的正确表示
* 405 - 方法不允许。表示请求方法对所请求的服务器是未知的
* 408 - 请求超时。表示服务器未完成请求。BTSE API 的超时设置为 30 秒
* 429 - 请求过多。表示客户端超过了服务器设置的速率限制。有关详细信息，请参阅速率限制
* 500 - 内部服务器错误。表示服务器遇到意外情况，不能完成请求

# 公共端点

## 查询货币的可用加密网络列表（弃用）

> 响应

```json
[
  "Bitcoin",
  "Liquid"
]
```

`GET /api/v3.2/availableCurrencyNetworks`

获取货币的可用加密网络列表。

### 请求参数

| 名称     | 类型   | 必填 | 描述        |
| ---      | ---    | ---  | ---         |
| currency | string | Yes  | 示例：BTC   |

### 响应内容

| 名称     | 类型   | 必填 | 描述         |
| ---      | ---    | ---  | ---         |
| $network | string | Yes  | 网络名称    |

## 查询资产间的汇率（弃用）

> 响应

```json
{
  "code": 1,
  "msg": "Success",
  "time": 1643085970137,
  "data": 36051.55950285,
  "success": true
}
```

`GET /api/v3.2/exchangeRate`

获取资产之间的汇率。

### 请求参数

| 名称             | 类型     | 必填   | 描述        |
| ---------------- | -------- | ------ | ----------- |
| srcCurrency      | string   | Yes    | 示例：BTC   |
| targetCurrency   | string   | Yes    | 示例：USD   |

### 响应内容

| 名称              | 类型      | 必填   | 描述                       |
| ---------------- | ----------| ------ | ------------------------ |
| code             | integer   | Yes    | 返回码                    |
| msg              | string    | Yes    | 返回消息                  |
| time             | long      | Yes    | Unix时间戳                |
| data             | float     | Yes    | 资产之间的汇率             |
| success          | boolean   | Yes    | 是 或 否                  |

## 查询加密货币网络信息

> 响应

```json
{
  "success": true,
  "code": 1,
  "msg": "Success",
  "time": 1624989977940,
  "data": [
    {
      "network": "ERC20",
      "name": "Ethereum (ERC20)",
      "depositEnable": true,
      "withdrawEnable": true,
      "confirmationTime": 15,
      "depositAmtMin": "0",
      "depositFeeMin": "0",
      "depositFeeRate": "0",
      "depositExtFees": "0",
      "depositExtFeeRate": "0",
      "needAddressExtension": false,
      "withdrawAmtMin": "36.41",
      "withdrawFeeMin": "6.41",
      "withdrawFeeRate": "0",
      "withdrawExtFees": "0",
      "withdrawExtFeeRate": "0"
    },
    {
      "network": "RIPPLE",
      "name": "Ripple",
      "depositEnable": true,
      "withdrawEnable": true,
      "confirmationTime": 10,
      "depositAmtMin": "0",
      "depositFeeMin": "0",
      "depositFeeRate": "0",
      "depositExtFees": "0",
      "depositExtFeeRate": "0",
      "needAddressExtension": true,
      "addressExtensionTypeName": "tag",
      "withdrawAmtMin": "0.25",
      "withdrawFeeMin": "20",
      "withdrawFeeRate": "0",
      "withdrawExtFees": "0",
      "withdrawExtFeeRate": "0"
    }
  ]
}
```

`GET /public-api/wallet/v1/crypto/networks`

获取加密货币对应的加密网络列表。

此 API 可在无需任何安全标头的情况下公开访问，以获取默认的网络列表。

如果使用具有 `Read` 权限的身份验证访问，结果将根据账户设置更为准确。
在公开访问环境下， `depositEnable` 和 `withdrawEnable` 的响应默认为 true。

* 总的充值手续费为： `max(depositFeeMin, (amount * depositFeeRate)) + (depositExtFees + depositExtFeeRate * amount)`
* 总的提现手续费为： `max(withdrawFeeMin, (amount * withdrawFeeRate)) + (withdrawExtFees + withdrawExtFeeRate * amount)`

### 请求参数

| Name             | Type     | Required   | Description   |
| ---------------- | -------- | ---------- | ------------- |
| crypto           | string   | Yes        | 示例：BTC       |


### 响应内容

| Name             | Type      | Required   | Description                                             |
| ---------------- | --------- | ---------- | ------------------------------------------------------- |
| data             | object    | Yes        | 物件陣列 (CryptoNetworkItem)                    |
| success          | boolean   | Yes        |請求校驗是否成功。當 HTTP 狀態為 `200`  時，該欄位將設為 `true`                                                                        |
| code             | integer   | Yes        | 請求狀態碼。當請求成功處理時，該欄位設為 `1`；失敗時則會返回錯誤碼。                               |
| msg              | string    | Yes        | 請求狀態訊息。當請求成功處理時，該欄位為 `Success`；失敗時會顯示錯誤訊息。                 |
| time             | long      | Yes        | 當前的 unix 時間戳記。                                 |

### 数据对象

| Name                     | Type     | Required | Description                          |
|--------------------------|----------|----------|--------------------------------------|
| network                  | string   | Yes      | 网络                                  |
| name                     | string   | Yes      | 网络名称                              |
| depositEnable            | boolean  | Yes      | 是否允许充值                           |
| withdrawEnable           | boolean  | Yes      | 是否允许提现                           |
| confirmationTime         | integer  | No       | 区块确认预计时间                        |
| depositAmtMin            | string   | Yes      | 最小充值金额                           |
| depositFeeMin            | string   | Yes      | 最低充值手续费                         |
| depositFeeRate           | string   | Yes      | 充值手续费率                           |
| depositExtFees           | string   | Yes      | 额外充值手续费                         |
| depositExtFeeRate        | string   | Yes      | 额外充值手续费率                       |
| needAddressExtension     | boolean  | Yes      | 是否支持地址扩展                        |
| addressExtensionTypeName | string   | No       | 地址扩展类型（如 `tag`）                |
| withdrawAmtMin           | string   | Yes      | 最小提现金额                           |
| withdrawFeeMin           | string   | Yes      | 最低提现手续费                         |
| withdrawFeeRate          | string   | Yes      | 提现手续费率                           |
| withdrawExtFees          | string   | Yes      | 额外提现手续费                         |
| withdrawExtFeeRate       | string   | Yes      | 额外提现手续费率                        |

## 资产兑换汇率查询

> 响应

```json
{
  "success": true,
  "code": 1,
  "msg": "Success",
  "time": 1624989977940,
  "data": {
    "rate": "19026.12846161"
  }
}
```

`GET /public-api/wallet/v1/assets/exchangeRate`

获取特定交易对的汇率。例如：`baseCurrency` 和 `quoteCurrency`.

### Request Parameters

| Name             | Type     | Required   | Description                                                    |
| ---------------- | -------- | ---------- | -------------------------------------------------------------  |
| baseCurrency     | string   | Yes        | 示例：baseCurrency=BTC</br>基础币种，例如:BTC                     |
| amount           | string   | Yes        | 示例：amount=2</br>`baseCurrency` 的数量                         |
| quoteCurrency    | string   | Yes        | 示例：quoteCurrency=USDT</br>报价币种，例如:USDT                   |

### 响应内容

| Name             | Type      | Required   | Description                                             |
| ---------------- | --------- | ---------- | ------------------------------------------------------- |
| data             | object    | Yes        | 物件陣列 (CryptoNetworkItem)                             |
| success          | boolean   | Yes        |請求校驗是否成功。當 HTTP 狀態為 `200`  時，該欄位將設為 `true`                                                                                                |
| code             | integer   | Yes        | 請求狀態碼。當請求成功處理時，該欄位設為 `1`；失敗時則會返回錯誤碼。                                                                                                   |
| msg              | string    | Yes        | 請求狀態訊息。當請求成功處理時，該欄位為 `Success`；失敗時會顯示錯誤訊息。                                                                                                   |
| time             | long      | Yes        | 當前的 unix 時間戳記。                                     |

### Data Object
| Name                     | Type     | Required | Description                                        |
|--------------------------|----------|----------|--------------------------------------------------- |
| rate                     | string   | No       | base-currency 对 quote-currency 的汇率              |

# 钱包端点

## 查询钱包余额

> 响应

```json
[
  {
    "available": 520.52,
    "currency": "USD",
    "total": 5566.5566
  }
]
```

`GET /api/v3.2/user/wallet`

查询用户的钱包余额。API密钥需要`读取`权限。

### 响应内容

| 名称      | 类型   | 必填 | 描述           |
| ---       | ---    | ---  | ---            |
| currency  | string | Yes  | 货币           |
| total     | double | Yes  | 总余额         |
| available | double | Yes  | 可用余额       |

## 查询钱包历史

> 响应

```json
[
  {
    "amount": 21.35823825,
    "currency": "USD",
    "description": "string",
    "fees": 0.06,
    "orderId": 20181213000239,
    "status": "COMPLETED",
    "timestamp": 1571630174639,
    "type": "Transfer_In",
    "username": "btseUser",
    "wallet": "Wallet",
    "txid": "<Blockchain Transaction ID>",
    "currencyNetwork": "<Blockchain currency network>"
  }
]
```

`GET /api/v3.2/user/wallet_history`

获取用户现货钱包的历史记录

### 请求参数

| 名称               | 类型    | 必填 | 描述                                                                                                                                 |
| ---                | ---     | ---  | ---                                                                                                                                  |
| currency           | string  | No   | 货币，如果未指定则返回所有货币                                                                                                        |
| startTime          | long    | No   | 起始时间（以毫秒为单位，例如 1624987283000）                                                                                          |
| endTime            | long    | No   | 结束时间（以毫秒为单位，例如 1624987283000）                                                                                          |
| count              | integer | No   | 要返回的记录数                                                                                                                        |
| useNewSymbolNaming | boolean | No   | 如果为 True，则以新格式返回期货市场名称，默认为 False                                                                                 |


### 响应内容

| 名称         | 类型    | 必填  | 描述                          |
| ---         | ---     | ---  | ---                          |
| currency    | string  | Yes  | 货币                          |
| amount      | double  | Yes  | 记录中的金额                   |
| fees        | double  | Yes  | 如有，将收取的费用              |
| orderId     | string  | Yes  | 内部钱包订单 ID                |
| wallet      | string  | Yes  | 钱包类型。对于现货将返回 `@SPOT` |
| description | string  | Yes  | 交易描述                      |
| status      | string  | Yes  | 记录的状态如下<br/>`PROCESSING`<br/>`CANCELLED`<br/>`COMPLETED`<br/>`EXPIRED`<br/>`FAILURE`<br/>`PENDING` |
| type        | string  | Yes  | 记录的类型如下<br/>`Deposit`<br/>`Withdraw`<br/>`Convert fiat`<br/>`Transfer_Out`<br/>`Transfer_In`<br/>`ReferralEarning`<br/>`Trading Fee Stake Freeze`<br/>`Trading Fee Stake Unfreeze`<br/>`Sub Account Transfer In`<br/>`Sub Account Transfer Out`<br/>`express buy`<br/>`Strategy Income`<br/>`Strategy Pay`<br/>`token voucher in`<br/>`spot trading fee rebate`<br/>`futures trading fee rebat`<br/>`trial fund`<br/>`general trading fee rebate`<br/>`token voucher out` |

## 创建钱包地址

> 请求

```json
{
  "currency": "BTC-LIQUID"
}
```

> 响应

```json
[
  {
    "address": "Blockchain address",
    "created": 1592627542
  }
]
```

`POST /api/v3.2/user/wallet/address`

创建钱包地址。如果创建的地址之前未被使用，将返回一个400错误，并带有现有的未使用地址。要使用此API，需要`钱包`权限。

### 请求参数

| 名称     | 类型   | 必填 | 描述   |
| ---      | ---    | ---  | ---    |
| currency | string | Yes  | 例如：BTC  |
| network  | string | Yes  | 例如：BITCOIN |

### 响应内容

| 名称    | 类型   | 必填 | 描述            |
| ---     | ---    | ---  | ---            |
| address | string | Yes  | 区块链地址       |
| created | long   | Yes  | 创建的时间戳     |

## 删除钱包地址

> 请求

```json
{
  "currency": "BTC",
  "network": "LIQUID",
  "address": "Blockchain address"
}
```

`DELETE /api/v3.2/user/wallet/address`

删除地址。如果删除的地址已经被删除 ，将返回一个400错误。要使用此API，需要`钱包`权限。

### 请求参数

| 名称     | 类型   | 必填 | 描述   |
| ---      | ---    | ---  | ---    |
| currency | string | Yes      | Ex: BTC     |
| network  | string | Yes      | Ex: BITCOIN |
| address  | string | Yes      | Ex: 地址 |

## 获取钱包地址

> 请求

```json
{
  "currency": "BTC",
  "network": "LIQUID"
}
```

> 响应

```json
[
  {
    "address": "Blockchain address",
    "created": 1592627542
  }
]
```

`GET /api/v3.2/user/wallet/address`

获取钱包地址。要使用此API，需要`钱包`权限。

### 请求参数

| 名称     | 类型   | 必填 | 描述   |
| ---      | ---    | ---  | ---    |
| currency | string | Yes  | 例如：BTC  |
| network  | string | Yes  | 例如：BITCOIN |

### 响应内容

| 名称    | 类型   | 必填 | 描述            |
| ---     | ---    | ---  | ---            |
| address | string | Yes  | 区块链地址       |
| created | long   | Yes  | 创建的时间戳     |

## 提款资金

> 请求

```json
{
  "currency": "BTC-Bitcoin",
  "address": "BTCAddress",
  "tag": "Tag",
  "amount": "0.001"
}
```

> 响应

```json
{
  "withdraw_id": "<withdrawal ID>"
}
```

`POST /api/v3.2/user/wallet/withdraw`

执行钱包提款。要使用此API，需要`提币`权限。

### 请求参数

| 名称               | 类型    | 必填     | 描述                                                                                                                                                                                                                                                                                                       |
| ---                | ---     | ---     | ---                                                                                                                                                                                                                                                                                                       |
| currency           | string  | Yes     | 币种-网络对 <br> 币种列表可以从[可用的币种列表中获取操作](#query-available-currency-list-for-wallet-action) <br> 网络列表可以从[获取货币的可用网络列表](#query-available-crypto-network-list-for-currency)中检索                                        |
| address            | string  | Yes     | 区块链地址                                                                                                                                                                                                                                                                                                |
| tag                | string  | Yes     | 标签，仅由某些区块链使用（例如：XRP）                                                                                                                                                                                                                                                                       |
| amount             | string  | Yes     | 提款金额（所有货币的最大小数位为`8`）。如果超出，将返回无效的提现金额（代码：3506）                                                                                                                                                                                                                         |
| includeWithdrawFee | boolean | No      | 如果为true或字段不存在，则费用包含在金额中。否则，费用会额外增加，扣除的金额可能大于所声明的金额                                                                                                                                                                                                             |

### 响应内容

| 名称        | 类型   | 必填     | 描述                                                                                                                                                                                                        |
| ---         | ---    | ---     | ---                                                                                                                                                                                                        |
| withdraw_id | string | Yes     | 内部提款ID。参考`wallet_history` API中的`orderID`字段。由于提现不会立即处理。用户可以查询钱包历史API来检查提现的状态                                                                                           |


## 查询钱包操作的可用货币列表

> 响应

```json
[
  "USD",
  "JPY",
  "GBP",
  "HKD",
  "SGD"
]
```

`GET /api/v3.2/availableCurrencies`

获取钱包操作的可用货币列表。

### 请求参数

| 名称   | 类型 | 必填     | 描述                                      |
| ---    | ---  | ---     | ---                                      |
| action | enum | Yes     | CONVERT（转换）, WITHDRAW（提币）, SEND（发送/转账）|

### 响应内容

| 名称          | 类型   | 必填     | 描述              |
| ---           | ---    | ---     | ---              |
| $currencyName | string | Yes     | 货币的名称         |


## 转换资金

> 请求

```json
{
  "amount": "1",
  "fromAsset": "BTC",
  "toAsset": "USD"
}
```

> 响应

```json
{
    "amount": 1.0,
    "settlementAmount": 66680.43282,
    "amountCurrency": "BTC",
    "settlementCurrency": "USD",
    "rate": 66680.43282
}
```

`POST /api/v3.2/user/wallet/convert`

执行钱包内的货币转换。要使用此API，需要`钱包`权限。要获取支持的货币列表，请查看[查询钱包操作的可用货币列表](#0ab39c1d97)

### 请求参数

| 名称      | 类型   | 必填    | 描述                     |
| ---       | ---    | ---     | ---                      |
| amount    | string | Yes     | 要转换的货币金额          |
| fromAsset | string | Yes     | 要转换的源货币            |
| toAsset   | string | Yes     | 目标货币                  |

### 响应内容

| 名称               | 类型   | 必填    | 描述                        |
| ---                | ---    | ---     | ---                        |
| amount             | float  | Yes     | 要转换的源货币金额           |
| settlementAmount   | float  | Yes     | 转换后的目标货币金额         |
| amountCurrency     | string | Yes     | 源货币                        |
| settlementCurrency | string | Yes     | 目标货币                     |
| rate               | float  | Yes     | 汇率                         |

## 转账资金

> 请求

```json
{
  "amount": "1.0",
  "asset": "BTC",
  "toUser": "jamesbond",
  "toUserMail": "james.bond@google.com"
}
```

> 响应

```json
{
  "amount": "1",
  "asset": "BTC",
  "toUser": "jamesbond",
  "toUserMail": "james.bond@google.com"
}
```

`POST /api/v3.2/user/wallet/transfer`

执行钱包内的货币转给其他用户的操作。要使用此API，需要`转账`权限。要获取支持的货币列表，请查看[查询钱包操作的可用货币列表](#0ab39c1d97)

### 请求参数

| 名称               | 类型    | 必填    | 描述                                                           |
| ---                | ---     | ---     | ---                                                            |
| amount             | string  | Yes     | 要转账的货币金额                                                 |
| asset              | string  | Yes     | 要转账的货币                                                     |
| toUser             | string  | Yes     | 接收者的账号                                                     |
| toUserMail         | string  | Yes     | 接收者的电子邮件                                                  |
| useNewSymbolNaming | boolean | No      | 若使用新的期货市场名称在资产字段中为真，默认为假                  |

### 响应内容

| 名称       | 类型   | 必填    | 描述                           |
| ---        | ---    | ---     | ---                           |
| amount     | string | Yes     | 要转账的货币金额                |
| asset      | string | Yes     | 要转账的货币                    |
| toUser     | string | Yes     | 接收者的账号                    |
| toUserMail | string | Yes     | 接收者的电子邮件                |

## 子帐号转账历史纪录

> 响应

```json
{
  "code": 1,
  "msg": "Success",
  "time": 1653964265608,
  "success": true,
  "data": {
    "totalRows": 2,
    "pageSize": 10,
    "currentPage": 1,
    "totalPages": 1,
    "data": [
      {
        "timestamp": 1711707874850,
        "fromUser": "uuooxxsub00002",
        "receiver": "uuooxx",
        "currency": "USDT",
        "amount": 11
      }
    ]
  }
}
```

`POST /api/v3.2/subaccount/wallet/history`

查询子帐号转帐历史纪录

### 请求参数

| 名称               | 类型    | 必填    | 描述                                                           |
| ---                | ---     | ---     | ---                                                            |
| startTime             | string  | Yes     | 要转账的货币金额                                                 |
| endTime              | string  | Yes     | 要转账的货币                                                     |
| page             | string  | Yes     | 接收者的账号                                                     |
| pageSize         | string  | Yes     | 接收者的电子邮件                                                  |

### 响应内容

| 名称       | 类型   | 必填    | 描述                           |
| ---        | ---    | ---     | ---                           |
| totalRows | integer | Yes     | 接收者的电子邮件                |
| pageSize | integer | Yes     | 接收者的电子邮件                |
| currentPage | integer | Yes     | 目前页数                |
| timestamp | integer | Yes     | 发送时间                |
| fromUser | string | Yes     | 发送者的账号                |
| receiver | string | Yes     | 接收者的账号                |
| currency | string | Yes     | 转账的货币                |
| amount | integer | Yes     | 转账的货币金额                |
