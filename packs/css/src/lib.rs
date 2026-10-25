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
    unsafe { (tree-sitter-css::LANGUAGE.into_raw())() }
}
