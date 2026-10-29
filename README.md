# Canyon Orchestrator extensions

Opt-in languages for [Canyon Orchestrator](https://github.com/JacoMartins/canyon-orchestrator).
Canyon ships with C, Java, Rust, Python and JavaScript (with TypeScript and TSX); everything
else is a pack here, downloaded by the app only when you choose to install it.

| Pack | Reads | Grammar |
|---|---|---|
| `kotlin` | `.kt`, `.kts` | tree-sitter-kotlin-ng (MIT) |
| `csharp` | `.cs` | tree-sitter-c-sharp (MIT) |
| `sql` | `.sql` (MySQL and other dialects) | tree-sitter-sequel (MIT) |
| `astro` | `.astro` | tree-sitter-astro-next (MIT or Apache-2.0) |
| `html` | `.html`, `.htm` | tree-sitter-html (MIT) |
| `css` | `.css` | tree-sitter-css (MIT) |

## How a pack works

A pack is a tree-sitter grammar compiled as a native library for each platform
(`linux-x86_64`, `linux-arm64`, `windows-x86_64`, `windows-arm64`, `macos-arm64`, `macos-x86_64`). It exports two functions,
the *pack ABI*:

```rust
#[no_mangle] pub extern "C" fn canyon_pack_abi() -> u32;      // 1
#[no_mangle] pub extern "C" fn canyon_grammar() -> *const ();  // the TSLanguage
```

The app knows how to analyse each language (imports, declarations, links); the pack brings the
grammar and its colours: `packs/<id>/queries/highlights.scm`, the grammar's own highlight query
with a short Canyon section at its end (or, for Kotlin, one written for Canyon). Each pack's test
(`cargo test --workspace`) checks that its query compiles against its grammar. Every release publishes `registry.json` with each library's URL, SHA-256 and size,
and the same for each query file (published as `<id>-highlights.scm`); the app refuses a
download whose hash does not match.

## What an extension asks for

An entry in `packs.json` may say what it needs beyond its grammar, under `needs`: `read` and
`write` (repo-relative globs), `commands` (programs it runs), `network` (hosts) and `backend`
(a program of its own). The app shows that before installing, and installs only what the person
allowed; an update that asks for more is asked again. Grammar packs ask for none, and the dialog
says so, along with the fact that the pack is a native library Canyon loads.

## Publishing

1. Change a pack (or add one under `packs/`, with its `queries/highlights.scm`, and list it in
   `packs.json`).
2. Bump the pack's `version` (installed copies are offered the update) and `release` in
   `packs.json`.
3. Push to the `release` branch, or run **Actions → Release → Run workflow**.

The workflow builds every pack on every platform and publishes `packs-<release>` as the latest
release, which is where the app looks.

## Licences

The grammars are third-party work under their own licences (MIT, and MIT or Apache-2.0 for Astro, listed above), and so are the highlight queries copied from them, which name their source at the top. The glue
code in `packs/` and `scripts/` belongs to the Canyon Orchestrator project.
