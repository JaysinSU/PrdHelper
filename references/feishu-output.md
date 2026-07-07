# Feishu Output

Use the Feishu docs tool to create or update cloud documents when available.

## Before Creating a Document

Confirm:

- Document stage and title.
- Whether to create a new document or update an existing one.
- Target location when the user cares: wiki node, wiki space, folder token, or personal space root.
- Required intake for the selected stage is sufficient.

If target location is not provided, create in the default personal space only when the user is comfortable with that.

## Creation Rules

- Do not repeat the title as the first H1 in the body.
- Do not hand-write a table of contents.
- Prefer Markdown tables for simple structured content.
- Use Feishu callouts sparingly for warnings, key conclusions, and open issues.
- Use Mermaid only for clear flows or state machines.
- Do not write direct `@张三`; use Feishu mention syntax only after resolving the user ID.
- Do not use token attributes for images or files; use URL attributes if media is needed.

## Default Document Shape

Start with conclusion and review target. Then follow the selected module template.

For long documents, create the document with the first stable sections and append later sections if needed.

## Fallback

If Feishu tools are unavailable, provide Feishu-ready Markdown and explicitly say that cloud document creation was not available in this environment.
