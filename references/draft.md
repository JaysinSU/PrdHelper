# Draft Module

Use Draft when the direction is mostly accepted and non-PM collaborators need enough context to judge workload, difficulty, and risk before formal PRD.

## Product Draft Goal

Expand the product deliberately, but do not force completion. The draft must make key functions, main user flow, and key-path wireframes concrete enough for Design and RD to participate early.

## Design Draft Goal

Start design in parallel after Product Draft is basically established. Focus on key pages, key states, and decision-making interaction questions, not visual polish.

## Required Information

Ask questions until these are clear enough:

- Key functions, not abstract capability names.
- Main execution path or user flow.
- Key-path wireframe or precise page/state description.
- Expected benefit and current baseline where available.
- Major dependencies and risks.
- Which supporting details may be delayed.
- Which abilities can be split into multiple Draft rounds.

## Product Draft Template

```markdown
## 1. 结论

- 一句话需求：
- 当前方案判断：
- 预期收益：
- 本轮 Draft 目标：

## 2. 背景与问题

- 当前现状：
- 用户/客户反馈：
- 为什么现在需要做：

## 3. 范围与边界

| 类型 | 内容 |
|---|---|
| 本期支持 |  |
| 本期不支持 |  |
| 可后置 |  |
| 依赖项 |  |

## 4. 核心功能

| 功能 | 用户价值 | 关键规则 | 风险 |
|---|---|---|---|

## 5. 主流程

1. 
2. 
3. 

## 6. 关键页面与状态

| 页面/状态 | 说明 | 决策问题 |
|---|---|---|

## 7. 风险与待确认

| 问题 | 影响 | Owner | 下一步 |
|---|---|---|---|

## 8. 可后置内容

- 埋点：
- 文案：
- 监控：
- 配置项：
```

## Design Draft Template

```markdown
## 1. 设计目标

- 需要验证的交互复杂度：
- 需要暴露的结构性问题：

## 2. 关键页面

| 页面 | 核心信息 | 关键决策 |
|---|---|---|

## 3. 关键状态

| 状态 | 触发条件 | 用户感知 | 待确认 |
|---|---|---|---|

## 4. 参考与目标产物

| 参考 | 借鉴点 | 决策帮助 |
|---|---|---|
```

## Quality Bar

After reading, collaborators should know roughly how much work there is, where the hard parts are, and where risk is concentrated.
