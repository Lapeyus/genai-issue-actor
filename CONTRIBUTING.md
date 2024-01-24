# Contributing
Please follow the below guidelines when considering making changes to this repo.

## Commit Messages
This project follows conventional commits. Commits should be of the form:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

The commit contains the following structural elements, to communicate intent to the consumers of your library:

**fix**: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning).
**feat**: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning).
**BREAKING CHANGE**: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
types other than fix: and feat: are allowed, for example @commitlint/config-conventional (based on the Angular convention) recommends **build**:, chore:, ci:, docs:, style:, refactor:, perf:, test:, and others.
*footers* other than `BREAKING CHANGE: <description>` may be provided and follow a convention similar to git trailer format.

### Examples
#### Commit message with description and breaking change footer
```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

#### Commit message with ! to draw attention to breaking change
```
feat!: send an email to the customer when a product is shipped
```

#### Commit message with scope and ! to draw attention to breaking change
```
feat(api)!: send an email to the customer when a product is shipped
```

#### Commit message with no body
```
docs: correct spelling of CHANGELOG
```
