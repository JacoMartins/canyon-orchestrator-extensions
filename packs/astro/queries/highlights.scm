; Colours for Canyon Orchestrator. The first part is tree-sitter-astro-next-0.1.1's own highlights.scm
; (MIT or Apache-2.0, Copyright (c) the tree-sitter-astro-next contributors), with Lua patterns (`%d`) written as regular expressions; the last part is
; Canyon's. As editors do, Canyon lets a later pattern win for one node, so the
; additions at the end take precedence.

(tag_name) @tag
(erroneous_end_tag_name) @keyword
(doctype) @tag.doctype
(attribute_name) @property
(attribute_value) @string
(comment) @comment

[
  (attribute_value)
  (quoted_attribute_value)
] @string

"=" @operator

[
  "{"
  "}"
] @punctuation.bracket

[
  "<"
  ">"
  "</"
  "/>"
] @tag.delimiter

; ---- Canyon Orchestrator
; Attributes as in HTML (the grammar calls them properties).
(attribute_name) @attribute
; The frontmatter fences.
(frontmatter "---" @punctuation.delimiter)
