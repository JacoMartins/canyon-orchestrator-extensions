; Colours for Canyon Orchestrator. The first part is tree-sitter-css-0.25.0's own highlights.scm
; (MIT, Copyright (c) 2018 Max Brunsfeld), with Lua patterns (`%d`) written as regular expressions; the last part is
; Canyon's. As editors do, Canyon lets a later pattern win for one node, so the
; additions at the end take precedence.

(comment) @comment

(tag_name) @tag
(nesting_selector) @tag
(universal_selector) @tag

"~" @operator
">" @operator
"+" @operator
"-" @operator
"*" @operator
"/" @operator
"=" @operator
"^=" @operator
"|=" @operator
"~=" @operator
"$=" @operator
"*=" @operator

"and" @operator
"or" @operator
"not" @operator
"only" @operator

(attribute_selector (plain_value) @string)

((property_name) @variable
 (#match? @variable "^--"))
((plain_value) @variable
 (#match? @variable "^--"))

(class_name) @property
(id_name) @property
(namespace_name) @property
(property_name) @property
(feature_name) @property

(pseudo_element_selector (tag_name) @attribute)
(pseudo_class_selector (class_name) @attribute)
(attribute_name) @attribute

(function_name) @function

"@media" @keyword
"@import" @keyword
"@charset" @keyword
"@namespace" @keyword
"@supports" @keyword
"@keyframes" @keyword
(at_keyword) @keyword
(to) @keyword
(from) @keyword
(important) @keyword

(string_value) @string
(color_value) @string.special

(integer_value) @number
(float_value) @number
(unit) @type

[
  "#"
  ","
  "."
  ":"
  "::"
  ";"
] @punctuation.delimiter

[
  "{"
  ")"
  "("
  "}"
] @punctuation.bracket

; ---- Canyon Orchestrator
; Selectors get Canyon's selector colour, not the property's.
(class_name) @selector
(id_name) @selector
(pseudo_class_selector (class_name) @selector)
(pseudo_element_selector (tag_name) @selector)
; A unit is part of its number (`4px`), and a colour is a value, as `none` is.
(integer_value (unit) @number)
(float_value (unit) @number)
(color_value) @constant
(plain_value) @constant
((plain_value) @variable
 (#match? @variable "^--"))
(attribute_selector (plain_value) @string)
