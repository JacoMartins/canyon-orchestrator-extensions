# Canyon Orchestrator extensions

Language packs for Canyon Orchestrator: one tree-sitter grammar per pack, built as a native
library per platform and published with `registry.json`. See `README.md`.

- Keep the pack ABI (`canyon_pack_abi` = 1, `canyon_grammar`) in step with
  `crates/canyon-core/src/extensions.rs` in the main repo.
- A new pack also needs analysis rules in the main app (`analyze.rs`, `resolve.rs`) and an entry
  in `Lang::EXTENSION_LANGS`; the pack alone only brings the grammar.
- Commits carry no AI attribution.
