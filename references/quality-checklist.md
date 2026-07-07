# Quality Checklist

Use this checklist for every Base requirement artifact.

## Decision Quality

- Put key conclusion first.
- State the meeting goal or document goal.
- Make the expected benefit explicit in Smoke Review and Draft.
- Explain current baseline, target lift percentage, and absolute expected lift when data exists.
- Use user testimony as support, not as the only argument.
- For new capabilities, explain qualitative necessity and why it is a "must have".
- Brief important referenced documents into the current page.

## Reader Fit

- Identify the reader: decision owner, KP, RD, Design, dependent module, DA, or QA.
- Explain enough background for the reader to make a decision without chasing context.
- Avoid internal shorthand when a clearer Chinese term exists.
- Add `名词解释` when new demand-specific terms appear.

## Structure

- Use system-style ordered or unordered lists.
- Use unordered lists when order does not matter.
- Use ordered lists when priority, sequence, or weight matters.
- Keep titles concise. Avoid exclamation marks or exaggerated wording.
- Avoid excessive bold, underline, highlight, or text color.

## Language

- Add spaces between Chinese and English, numbers, and symbols.
- Keep language system consistent; prefer Chinese.
- Avoid vague quantifiers such as "很多", "少量", "大部分", "一些" when data or a clearer range can be given.
- Use "万" instead of "w", such as `100 万行` and `300 万 DAU`.
- Write dates as `X 月 X 日`; avoid ambiguous version/date expressions.

## Base-Specific

- If SV6 appears, write `SV6 按需版本` or `SV6 按需架构`.
- If large-table scale appears, remember the key boundary: `5 万行`.
- Clarify whether the demand affects records, fields, views, dashboards, forms, automations, workflows, permissions, or AI agents.
- Clarify endpoint differences only when relevant: PC, mobile, iPad, iOS, Android, HarmonyOS.
- Clarify FG, gray release, rollback, and monitoring when launch risk exists.

## Review Readiness

- Smoke Review readiness: collaborators can feel the product direction and challenge whether it is worth doing.
- Draft readiness: collaborators can judge workload, hard parts, and risk concentration.
- PRD readiness: RD can implement without guessing core rules or boundaries.
