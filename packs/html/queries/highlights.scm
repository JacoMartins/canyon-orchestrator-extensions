; Colours for Canyon Orchestrator. The first part is tree-sitter-html-0.23.2's own highlights.scm
; (MIT, Copyright (c) 2014 Max Brunsfeld), with Lua patterns (`%d`) written as regular expressions; the last part is
; Canyon's. As editors do, Canyon lets a later pattern win for one node, so the
; additions at the end take precedence.

(tag_name) @tag
(erroneous_end_tag_name) @tag.error
(doctype) @constant
(attribute_name) @attribute
(attribute_value) @string
(comment) @comment

[
  "<"
  ">"
  "</"
  "/>"
] @punctuation.bracket

; ---- Canyon Orchestrator
; The doctype and entities (`&amp;`).
(doctype) @keyword
(entity) @constant
