# Contributing

Welcome to our open-source project! We appreciate your interest in contributing to our codebase. By following these guidelines, you can help us maintain a high standard of quality and consistency.

## Code of Conduct

We expect all contributors to follow a code of conduct that promotes a welcoming, inclusive, and respectful environment for everyone involved. Please read our Code of Conduct before contributing to our project.

## Commit Messages

This project follows conventional commits. Commits should be of the form:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

The commit contains the following structural elements, to communicate intent to the consumers of your library:

- **fix**: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning).
- **feat**: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning).
- **BREAKING CHANGE**: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
- types other than fix: and feat: are allowed, for example @commitlint/config-conventional (based on the Angular convention) recommends **build**:, chore:, ci:, docs:, style:, refactor:, perf:, test:, and others.
- *footers* other than `BREAKING CHANGE: <description>` may be provided and follow a convention similar to git trailer format.

### Examples

#### Commit message with description and breaking change footer

```text
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

#### Commit message with ! to draw attention to breaking change

```text
feat!: send an email to the customer when a product is shipped
```

#### Commit message with scope and ! to draw attention to breaking change

```text
feat(api)!: send an email to the customer when a product is shipped
```

#### Commit message with no body

```text
docs: correct spelling of CHANGELOG
```

## Pull Requests

When creating a pull request, please follow these guidelines:

- **Ensure Your Code Changes Are Relevant:** Make sure that the changes you are proposing are relevant to the project and align with its goals. Avoid making unrelated or off-topic changes.
- **Write Clear and Concise Commit Messages:** Use descriptive commit messages that clearly explain the purpose and impact of your changes. Refer to the "Commit Messages" section above for more details.
- **Adhere to Coding Standards:** Follow the coding standards and conventions used in the project. This ensures consistency and readability of the codebase.
- **Test Your Changes Thoroughly:** Before submitting a pull request, ensure that you have tested your changes thoroughly to verify their correctness and functionality.
- **Document Your Changes:** Include appropriate documentation for new features or significant changes. Update existing documentation if necessary.

## Communication and Collaboration

We encourage open communication and collaboration among contributors. Feel free to ask questions, share ideas, and discuss potential improvements with the project maintainers and other contributors. Let's work together to make this project even better!