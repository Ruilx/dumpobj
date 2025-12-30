# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [0.1.0] - 2025-12-31
### Added
- Initial public release of `dumpobj`.
- Core dumper (`Dump`) and convenience function (`dump`) to introspect Python objects and produce a neutral `Node` tree.
- Built-in handlers for common types: `dict`, `list`, `tuple`, `set`, `str`, `bool`, `int`, `float`, `complex`, `None`, `Ellipsis`, `BaseException`, `type`, and generic objects via MRO.
- Controls for traversal and output:
  - `set_inline(True/False)` for detailed tree vs inline summaries.
  - `set_head_count(n)` to limit items/characters shown.
  - `set_depth(n|None)` to cap recursion depth.
  - `set_str_if_recur(mark)` for recursion marking (`str`, `Ellipsis`, or `None`).
- Recursion detection with configurable display strategy and safe handling of circular references.
- Attribute collection per type (e.g., object id `@`, `__len__`, `__sizeof__`) with a simple `attr_config`.
- Pluggable formatter architecture (`Formatter` base class) with built-in formatters:
  - `PlainFormatter` (tree-style text)
  - `ColorFormatter` (ANSI-colored text)
  - `JsonFormatter` (structured JSON output)
- Public `Node` data model with helpers (`set_key`, `set_prop`, `set_attr`, `append_node`, etc.).
- Hook to register custom type handlers via `register_handle(t, handle)`.
- Lazy top-level exports of `Dump` and `dump` in the `dumpobj` package to avoid unnecessary imports.

### Notes
- Requires Python 3.11+.
- Zero third-party runtime dependencies.

[0.1.0]: https://github.com/Ruilx/dumpobj/releases/tag/v0.1.0
