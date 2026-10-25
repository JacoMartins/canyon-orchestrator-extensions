# Canyon Orchestrator extensions

Opt-in languages for [Canyon Orchestrator](https://github.com/JacoMartins/canyon-orchestrator).
Canyon ships with C, Java, Rust, Python and JavaScript (with TypeScript and TSX); everything
else is a pack here, downloaded by the app only when you choose to install it.

| Pack | Reads | Grammar |
|---|---|---|
| `kotlin` | `.kt`, `.kts` | tree-sitter-kotlin-ng (MIT) |
| `csharp` | `.cs` | tree-sitter-c-sharp (MIT) |
| `sql` | `.sql` (MySQL and other dialects) | tree-sitter-sequel (MIT) |

## How a pack works

A pack is a tree-sitter grammar compiled as a native library for each platform
(`linux-x86_64`, `windows-x86_64`, `macos-arm64`, `macos-x86_64`). It exports two functions,
the *pack ABI*:

```rust
#[no_mangle] pub extern "C" fn canyon_pack_abi() -> u32;      // 1
#[no_mangle] pub extern "C" fn canyon_grammar() -> *const ();  // the TSLanguage
```

The app knows how to analyse each language (imports, declarations, links); the pack brings only
the grammar. Every release publishes `registry.json` with each library's URL, SHA-256 and size,
and the app refuses a download whose hash does not match.

## Publishing

1. Change a pack (or add one under `packs/` and list it in `packs.json`).
2. Bump `release` in `packs.json`.
3. Push to the `release` branch, or run **Actions → Release → Run workflow**.

The workflow builds every pack on every platform and publishes `packs-<release>` as the latest
release, which is where the app looks.

## Licences

The grammars are third-party work under their own licences (all MIT, listed above). The glue
code in `packs/` and `scripts/` belongs to the Canyon Orchestrator project.
