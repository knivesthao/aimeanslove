---
name: code-injection
description: "Injection is input treated as instructions; parameters keep input as data."
---

# Input stays data

Create and install a skill named `code-injection` (Input stays data). It instructs the agent as follows: Never build queries, commands, or markup by gluing strings around user input. Database reads go through the ORM (SQLModel parameterizes everything). Templates auto-escape HTML — never mark user content safe. OS commands, LDAP, and XPath get the same rule: parameters, never concatenation.

## Checks

- no string-built queries or commands
- user HTML never marked safe
- ORM or parameters everywhere
