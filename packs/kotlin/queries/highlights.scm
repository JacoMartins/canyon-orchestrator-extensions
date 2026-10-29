; Kotlin colours for Canyon Orchestrator, written for tree-sitter-kotlin-ng 1.1 (which ships no
; highlight query). Canyon reads these as editors do: for one node, a later pattern wins, and an
; inner node keeps its own colour over the one around it.

; Names first, so the more precise patterns below win.
(identifier) @variable

(this_expression) @variable.builtin
(super_expression) @variable.builtin

; Types and declarations.
(user_type (identifier) @type)
(class_declaration name: (identifier) @type)
(object_declaration name: (identifier) @type)
(type_alias type: (identifier) @type)
(type_parameter (identifier) @type)
(enum_entry (identifier) @constant)
(import (qualified_identifier (identifier) @type .)
  (#match? @type "^[A-Z]"))

(function_declaration name: (identifier) @function)
(call_expression (identifier) @function.call)
(navigation_expression (identifier) @property .)
(call_expression (navigation_expression (identifier) @function.method .))
(parameter (identifier) @parameter)
(class_parameter (identifier) @parameter)
(value_argument (identifier) @parameter)
(label) @label

; The grammar reads these as names: they are what they spell, wherever they stand.
((identifier) @constant
  (#match? @constant "^[A-Z][A-Z0-9_]+$"))

((identifier) @constant.builtin
  (#any-of? @constant.builtin "true" "false" "null"))

(annotation) @attribute
(annotation (user_type (identifier) @attribute))

; Literals.
(number_literal) @number
(float_literal) @number
(character_literal) @character
(string_literal) @string
(multiline_string_literal) @string
(escape_sequence) @string.escape
(interpolation) @punctuation.special
(interpolation (_) @variable)
(line_comment) @comment
(block_comment) @comment
(shebang) @comment

; Keywords.
[
  "package" "import" "class" "interface" "object" "fun" "val" "var" "typealias" "constructor"
  "companion" "init" "by" "where" "get" "set" "field" "property" "receiver" "param" "setparam"
  "delegate" "file" "dynamic"
] @keyword

[
  "if" "else" "when" "for" "while" "do" "try" "catch" "finally" "throw" "return" "return@"
  "in" "!in" "is" "!is" "as" "as?" "this@" "super@"
] @keyword

(class_modifier) @keyword
(member_modifier) @keyword
(function_modifier) @keyword
(property_modifier) @keyword
(visibility_modifier) @keyword
(inheritance_modifier) @keyword
(parameter_modifier) @keyword
(platform_modifier) @keyword
(variance_modifier) @keyword
(reification_modifier) @keyword
"enum" @keyword

[
  "+" "-" "*" "/" "%" "=" "+=" "-=" "*=" "/=" "%=" "==" "!=" "===" "!==" "<" ">" "<=" ">="
  "&&" "||" "!" "!!" "?:" "?." "." "::" ".." "..<" "->" "++" "--"
] @operator

["(" ")" "[" "]" "{" "}"] @punctuation.bracket
["," ";" ":"] @punctuation.delimiter
