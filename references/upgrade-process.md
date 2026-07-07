# Upgrade Process

Use this module when the user gives feedback about this skill or asks to improve it.

## Feedback Classification

Classify each feedback item into one or more buckets:

- Routing: wrong stage selection or missing total-entry behavior.
- Questioning: asked too many, too few, or low-quality clarifying questions.
- Brainstorm: failed to challenge first, missed blind spots, or weak creative options.
- Template: missing section, wrong structure, or unclear output shape.
- Base knowledge: missing Base-specific product concepts or review habits.
- Writing standard: violated language, formatting, or document quality rules.
- Feishu output: poor cloud document structure or tool usage.
- Upgrade workflow: git, validation, summary, commit, or push behavior.

## Upgrade Steps

1. Restate the feedback and classify it.
2. Decide which files need changes.
3. Apply local edits.
4. Run validation.
5. Optionally run a small forward test with a realistic Base demand prompt.
6. Summarize:
   - changed files;
   - behavior before and after;
   - validation result;
   - remaining risk.
7. Ask for explicit confirmation before git commit and push.

## Git Rules

- Keep the skill in a git repository.
- Do not commit or push unrelated changes.
- Do not push without a remote URL, branch, network permission, and explicit user confirmation.
- Prefer commit messages in this format: `Improve prd-helper <area>`.
- If the user asks for rollback, use git history carefully and never discard uncommitted user changes without explicit approval.

## No Separate Changelog

Do not create a changelog file by default. Use git history and the final user-facing summary as the upgrade record.
