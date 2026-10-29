//! Canyon Orchestrator extension: the css grammar, as a native library.
//!
//! The app loads this library and calls the two functions below (the "pack ABI").

/// The pack ABI this library follows. The app refuses a library with another number.
#[no_mangle]
pub extern "C" fn canyon_pack_abi() -> u32 {
    1
}

/// The tree-sitter grammar (a `TSLanguage` pointer).
#[no_mangle]
pub extern "C" fn canyon_grammar() -> *const () {
    // SAFETY: the grammar crate's language function has no preconditions.
    unsafe { (tree_sitter_css::LANGUAGE.into_raw())() }
}

#[cfg(test)]
mod tests {
    /// The colours the app reads beside the library: they must compile against this grammar,
    /// or the app falls back to its own rules for the language.
    #[test]
    fn highlights_query_compiles() {
        let language: tree_sitter::Language = tree_sitter_css::LANGUAGE.into();
        if let Err(e) = tree_sitter::Query::new(&language, include_str!("../queries/highlights.scm")) {
            panic!("highlights.scm: {e}");
        }
    }
}
