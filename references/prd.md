# Formal PRD Module

Use this module only when the demand is ready for implementation-level review. Strictly reuse this PRD structure unless the user explicitly asks to remove sections.

## Required Information

Do not write a formal PRD body until these are known or explicitly marked as unavailable:

- One-sentence demand.
- Release scope.
- Alignment object or comparable existing capability.
- Supported abilities and unsupported abilities.
- Whether FG is needed.
- Launch date or date to be confirmed.
- Related documents, summarized in the page rather than dumped as raw links.
- Terms that need definitions.
- Background, current state, customer/user feedback.
- Competitive/reference analysis when relevant.
- Qualitative and quantitative goals.
- Product framework and detailed requirements.
- State rules, error rules, route rules, permissions, and cross-end behavior where relevant.
- Metrics/logging.
- Copy requirements.
- Delivery rhythm.

## PRD Structure

```markdown
## Changelog

| 时间 | 更新内容 | 更新人 |
|---|---|---|

## 评审记录

| 时间 | 参会人 | 会议目标 | 会议结论 & 纪要 |
|---|---|---|---|

## 需求基本信息

| 字段 | 内容 |
|---|---|
| 一句话需求 |  |
| 发布范围 |  |
| 对齐对象 |  |
| 本期支持能力 |  |
| 本期不支持能力 |  |
| 是否需要 FG |  |
| 上线时间 |  |
| 其他相关文档 |  |

## 名词解释

| 名词 | 解释 |
|---|---|

## 需求背景

### 一句话需求描述

### 现状和客户反馈

### 竞品是怎么解决的

### 总结

## 需求目标及价值度量

- 定性目标：
- 定量目标：

## 产品方案

### 支持范围

### 产品框架

### 需求详述

#### 入口与首屏

| 模块 | 需求说明 | 示意图 |
|---|---|---|

#### 会话与跨端关系

| 模块 | 需求说明 | 示意图 |
|---|---|---|

#### 能力路由规则

| 用户意图 | 路由结果 | 处理方式 |
|---|---|---|

#### 中间态与过程展示

| 模块 | 需求说明 |
|---|---|

#### 结果展示

| 模块 | 需求说明 |
|---|---|

## FG 方案与灰度策略

## 埋点

## 文案

## 落地节奏

| 版本/阶段 | 时间 | 目标 | 具体计划 |
|---|---|---|---|
```

## PRD Writing Rules

- Keep "本期不支持" explicit.
- Explain why unsupported abilities are excluded when it affects user expectation or cross-end behavior.
- For AI requirements, write route rules, supported agents/abilities, unsupported intents, intermediate states, failure states, result shapes, and continuation behavior.
- For mobile requirements, write supported platforms and cross-end relationship.
- For results or cards, define max height, scrolling/expansion, retry, stop generation, and fallback behavior when relevant.
- For metrics, include exposure, click, submit, conversion, success, failure, retry, stop, and result-consumption metrics when relevant.
