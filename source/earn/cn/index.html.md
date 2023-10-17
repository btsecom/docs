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

## 版本 1.0（2021年12月8日）

* 发布 earn（投资）API 的初始版本

## 版本 1.1（2021年12月13日）

* 在查询投资历史的请求和响应中添加了缺少的分页描述
* 在存款/赎回投资的响应中添加了处理结果


# 概述

## 生成API密钥

在使用经过身份验证的API之前，您需要在BTSE平台上创建API密钥。要创建API密钥，您可以按照以下步骤操作：

* 使用您的用户名/电子邮件和密码登录BTSE网站
* 单击右上角的“账户”
* 选择API选项卡
* 单击“新API”按钮以创建API密钥和密码。 （注意：密码仅会出现一次）
* 使用您的API密钥和密码构建签名。

## 终端点

* 正式环境
  * HTTP
     * `https://api.btse.com/spot`
* 测试网络
  * HTTP
     * `https://testapi.btse.io/spot`

## 身份验证

* API密钥（request-api）
  * 参数名称：`request-api`，位置：标题。API密钥以string形式从BTSE平台获取

* API密钥（request-nonce）
  * 参数名称：`request-nonce`，位置：标题。当前时间戳的长格式表示

* API密钥（request-sign）
  * 参数名称：`request-sign`，位置：标题。基于以下算法生成的复合签名：Signature=HMAC.Sha384（secretkey，（urlpath + request-nonce + bodyStr））（注意：当没有数据时，bodyStr = ''）：


# 投资终端点

## 查询投资产品

> 响应

```json
[
  {
    "id": "OPENETH00001",
    "name": "ETH Flex Savings",
    "currency": "ETH",
    "type": "Flex",
    "startDate": 1610685918000,
    "interestStartDate": 1610719200000,
    "rates":
    [
      {
        "days": 1,
        "rate": 1.15
      }
    ],
    "compounding": true,
    "autoRenewSupported": false,
    "dailyLimit": 10.0,
    "minSize": 1.00000000,
    "incrementalSize": 1.00000000
  }
]
```

`GET /api/v3.2/invest/products`

获取所有投资产品

### 请求参数

(无)

### 响应内容

| 名称               | 类型         | 是否必须 | 描述                              |
| ---                | ---          | ---  | ---                             |
| id                 | string       | Yes   | 产品编号                         |
| name               | string       | Yes   | 产品名称                         |
| currency           | string       | Yes   | 货币                             |
| type               | string       | Yes   | 产品类型                         |
| startDate          | long       | Yes   | 投资开始日期                     |
| interestStartDate  | long       | Yes   | 利息开始日期                     |
| rates              | RateObject[] | Yes   | 利息率信息                       |
| compounding        | double       | Yes   | 产品是否复利                     |
| autoRenewSupported | double       | Yes   | 产品是否支持自动续约             |
| dailyLimit         | double       | Yes   | 每日投资金额限制                 |
| minSize            | double       | Yes   | 最低投资额                       |
| incrementalSize    | double       | Yes   | 投资步进大小                     |

### RateObject

| 名称 | 类型    | 是否必须 | 描述         |
| ---  | ---     | ---  | ---         |
| days | integer | Yes   | 天数         |
| rate | double  | Yes   | 利率         |


## 存款投资

> 请求

```json
{
    "productId": "OPENUSDT0001",
    "amount": 100.99,
    "renew": true,
    "day": 7
}
```

> Reponse

```json
{
    "success": true
}
```

`POST /api/v3.2/invest/deposit`

存款投资

### 请求参数

| 名称      | 类型    | 是否必须 | 描述                  |
| ---       | ---     | ---  | ---                  |
| productId | string  | Yes   | 投资产品编号        |
| amount    | double  | Yes   | 投资金额             |
| renew     | boolean  | Yes   | 自动续约             |
| day       | integer    | Yes   | 天数                  |

### 响应内容

| 名称    | 类型    | 是否必须 | 描述                  |
| ---     | ---     | ---  | ---                  |
| success | boolean  | Yes   | 处理结果              |


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

`POST /api/v3.2/invest/renew`

续投资订单

### 请求参数

| 名称      | 类型    | 是否必须 | 描述                  |
| ---       | ---     | ---  | ---                  |
| orderId   | integer    | Yes   | 投资订单编号         |
| autoRenew | boolean  | Yes   | 自动续约             |

### 响应内容

| 名称      | 类型    | 是否必须 | 描述                     |
| ---       | ---     | ---  | ---                     |
| orderId   | integer    | Yes   | 投资订单编号             |
| autoRenew | boolean  | Yes   | 自动续约标志的状态      |


## 赎回投资

> 请求

```json
{
    "orderId": 1,
    "amount": 12.34
}
```

> Reponse

```json
{
    "success": true
}
```

`POST /api/v3.2/invest/redeem`

赎回投资订单

### 请求参数

| 名称    | 类型    | 是否必须 | 描述                  |
| ---     | ---     | ---  | ---                  |
| orderId | integer    | Yes   | 投资订单编号         |
| amount  | double  | Yes   | 赎回金额             |

### 响应内容

| 名称    | 类型    | 是否必须 | 描述                  |
| ---     | ---     | ---  | ---                  |
| success | boolean  | Yes   | 处理结果              |


## 查询投资订单

> 响应

```json
[
  {
    "id": 456,
    "name": "ETH Flex Savings",
    "currency": "ETH",
    "type": "Flex",
    "rate": 1.15,
    "investAmt": 10.00000000,
    "interestEarned": 0.00031507,
    "nextInterestPayoutTime": 1610632800000,
    "startTime": 0,
    "endTime": 0,
    "duration": 86400000,
    "payoutLockTime": 300000,
    "autoRenew": false,
    "compounding": true,
    "autoRenewSupported": false,
    "dailyLimit": 0,
    "redemptionProcessing": false
  }
]
```

`GET /api/v3.2/invest/orders`

查询投资订单

### 响应内容

| 名称                   | 类型    | 是否必须 | 描述                          |
| ---                    | ---     | ---  | ---                          |
| id                     | integer    | Yes   | 订单编号                     |
| name                   | string  | Yes   | 产品名称                     |
| currency               | string  | Yes   | 货币                         |
| type                   | string  | Yes   | 产品类型                     |
| rate                   | boolean  | Yes   | 利率                         |
| investAmt              | boolean  | Yes   | 金额                         |
| interestEarned         | boolean  | Yes   | 赚取的利息                   |
| nextInterestPayoutTime | boolean  | Yes   | 下次利息支付时间             |
| startTime              | boolean  | Yes   | 开始时间                     |
| endTime                | boolean  | Yes   | 结束时间                     |
| duration               | boolean  | Yes   | 期限                         |
| payoutLockTime         | boolean  | Yes   | 支付锁定时间                 |
| autoRenew              | boolean  | Yes   | 自动续约                     |
| compounding            | boolean  | Yes   | 复利                         |
| autoRenewSupported     | boolean  | Yes   | 是否支持自动续约             |
| redemptionProcessing   | boolean  | Yes   | 是否正在赎回处理             |


## 查询投资历史

> 响应

```json
{
  "totalRows": 1,
  "pageNumber": 1,
  "pageSize": 10,
  "data": [
    {
      "txnTime": 1598918400000,
      "name": "USDT Flex Savings",
      "currency": "USDT",
      "rate": 0.5,
      "type": "Flex",
      "txnType": "INVEST_SERVICE_TYPE_DEPOSIT",
      "amount": 100,
      "totalAmount": 2000,
      "interestEarned": 1.22,
      "duration": 0
    }
  ]
}
```

`GET /api/v3.2/invest/history`

查询投资历史

### 请求参数

| 名称         | 类型    | 是否必须 | 描述                               |
| ---          | ---     | ---  | ---                               |
| pageNumber   | integer    | 否   | 要查询的页码，默认为1（从1开始）  |
| pageSize     | integer    | 否   | 每页记录数，默认为10，最大50条记录 |


### 响应内容

| 名称         | 类型                        | 是否必须 | 描述                   |
| ---          | ---                         | ---  | ---                   |
| totalRows    | string                      | Yes   | 总记录数               |w
| pageNumber   | string                      | Yes   | 当前页码               |
| pageSize     | string                      | Yes   | 每页记录数             |
| data         | InvestmentHistoryObject[]  | Yes   | 投资历史对象           |

### InvestmentHistoryObject

| 名称           | 类型    | 是否必须 | 描述                        |
| ---            | ---     | ---  | ---                        |
| txnTime        | integer    | Yes   | 交易时间                   |
| name           | string  | Yes   | 产品名称                   |
| currency       | string  | Yes   | 货币                       |
| rate           | string  | Yes   | 利率                       |
| type           | boolean  | Yes   | 产品类型                   |
| txnType        | boolean  | Yes   | 交易类型                   |
| amount         | boolean  | Yes   | 交易金额                   |
| totalAmount    | boolean  | Yes   | 投资总额                   |
| interestEarned | boolean  | Yes   | 赚取的利息                 |
| duration       | boolean  | Yes   | 期限                       |
