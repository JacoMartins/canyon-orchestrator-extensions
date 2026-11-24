#!/usr/bin/env python3
"""Writes the data packs (`data/<id>.json`) and their catalog (`data/index.json`).

A data pack is pure data: nothing in it runs. The first kind, `new-items`, adds what Files'
"+" can create in a language (a Java class, a Kotlin data class, a React component): where the
new file goes and its starting text, with placeholders the app fills in (see the main repo's
`crates/canyon-engine/src/items.rs`). The catalog lists each pack with its version, size and
SHA-256, which the app checks before keeping a download.

Run after editing a pack: `python3 scripts/data_packs.py`.
"""
import hashlib
import json
import os

BASE = "https://raw.githubusercontent.com/JacoMartins/canyon-orchestrator-extensions/main/data"
HERE = os.path.join(os.path.dirname(__file__), "..", "data")


def item(id, name, path, text, name_kind="identifier", hint=None, about=None):
    out = {"id": id, "name": name, "path": path, "text": text, "name_kind": name_kind}
    if hint:
        out["hint"] = hint
    if about:
        out["about"] = about
    return out


# Java, as Eclipse's "New" wizards: each item asks for the source folder, the package and what
# Eclipse asks (modifiers, superclass, interfaces, method stubs, comments), and the file goes to
# its package's folder under the source folder. Fields and `{{#…}}` sections are explained in the
# main repo's `crates/canyon-engine/src/items.rs`.
def field(id, kind, label, about=None, hint=None, default=None, **extra):
    out = {"id": id, "kind": kind, "label": label}
    for k, v in (("about", about), ("hint", hint), ("default", default)):
        if v is not None:
            out[k] = v
    out.update(extra)
    return out


def source(roots=("src/main/java",)):
    return field("source", "source", "Source folder", hint="src/main/java", roots=list(roots))


PACKAGE = field("package", "package", "Package", about="Empty for the default package.", hint="com.example.shop")
ACCESS = field("access", "choice", "Access", options=[{"value": "public ", "label": "public"}, {"value": "", "label": "package"}])
COMMENTS = field("comments", "check", "Generate comments", about="A Javadoc comment above the type.")


def jitem(id, name, text, fields, hint, about=None, name_kind="identifier", path="{{package_path}}/{{NamePascal}}.java", **extra):
    out = item(id, name, path, text, name_kind=name_kind, hint=hint, about=about)
    out["place"] = "source"
    out["fields"] = fields
    out.update(extra)
    return out


HEAD = "{{java_package_line}}{{java_imports}}"
DOC = "{{#comments}}/**\n * {{NamePascal}}.\n */\n{{/comments}}"
JAVA = [
    jitem("class", "Class", HEAD + DOC +
          "{{access}}{{#abstract}}abstract {{/abstract}}{{#final}}final {{/final}}class {{NamePascal}}"
          "{{#superclass}} extends {{superclass}}{{/superclass}}{{#interfaces}} implements {{interfaces}}{{/interfaces}} {\n"
          "{{#constructor}}\n    {{access}}{{NamePascal}}() {\n    }\n{{/constructor}}"
          "{{#main}}\n    public static void main(String[] args) {\n    }\n{{/main}}}\n",
          [source(), PACKAGE, ACCESS,
           field("abstract", "check", "abstract", off=["final"]),
           field("final", "check", "final", off=["abstract"]),
           field("superclass", "type", "Superclass", about="With its package to import it.", hint="java.util.AbstractList<String>"),
           field("interfaces", "types", "Interfaces", about="Separated by commas.", hint="java.io.Serializable, Comparable<Cart>"),
           field("main", "check", "public static void main(String[] args)"),
           field("constructor", "check", "Constructor", about="An empty one, with no arguments."),
           COMMENTS],
          hint="Cart"),
    jitem("interface", "Interface", HEAD + DOC +
          "{{access}}interface {{NamePascal}}{{#interfaces}} extends {{interfaces}}{{/interfaces}} {\n}\n",
          [source(), PACKAGE, ACCESS,
           field("interfaces", "types", "Extended interfaces", about="Separated by commas.", hint="java.io.Serializable"),
           COMMENTS],
          hint="PaymentGateway"),
    jitem("enum", "Enum", HEAD + DOC +
          "{{access}}enum {{NamePascal}}{{#interfaces}} implements {{interfaces}}{{/interfaces}} {\n"
          "{{#constants}}    {{constants}};\n{{/constants}}}\n",
          [source(), PACKAGE, ACCESS,
           field("constants", "text", "Constants", about="Separated by commas.", hint="NEW, PAID, SHIPPED"),
           field("interfaces", "types", "Interfaces", hint="java.io.Serializable"),
           COMMENTS],
          hint="OrderStatus"),
    jitem("record", "Record", HEAD + DOC +
          "{{access}}record {{NamePascal}}({{components}}){{#interfaces}} implements {{interfaces}}{{/interfaces}} {\n}\n",
          [source(), PACKAGE, ACCESS,
           field("components", "text", "Components", about="Its fields, as in a method's parameters.", hint="String id, int quantity"),
           field("interfaces", "types", "Interfaces", hint="Comparable<Item>"),
           COMMENTS],
          hint="LineItem", about="Java 16 and later."),
    jitem("annotation", "Annotation", HEAD +
          "import java.lang.annotation.ElementType;\nimport java.lang.annotation.Retention;\n"
          "import java.lang.annotation.RetentionPolicy;\nimport java.lang.annotation.Target;\n\n" + DOC +
          "@Retention(RetentionPolicy.{{retention}})\n@Target(ElementType.{{target}})\n{{access}}@interface {{NamePascal}} {\n}\n",
          [source(), PACKAGE, ACCESS,
           field("retention", "choice", "Retention", options=[{"value": v, "label": v.lower()} for v in ("RUNTIME", "CLASS", "SOURCE")]),
           field("target", "choice", "Target", options=[{"value": v, "label": v.lower()} for v in ("TYPE", "METHOD", "FIELD", "PARAMETER", "CONSTRUCTOR")]),
           COMMENTS],
          hint="Audited"),
    jitem("exception", "Exception", HEAD + DOC +
          "{{access}}class {{NamePascal}} extends {{superclass}} {\n"
          "    {{access}}{{NamePascal}}(String message) {\n        super(message);\n    }\n"
          "{{#cause}}\n    {{access}}{{NamePascal}}(String message, Throwable cause) {\n        super(message, cause);\n    }\n{{/cause}}}\n",
          [source(), PACKAGE, ACCESS,
           field("superclass", "type", "Superclass", about="Checked: Exception. Unchecked: RuntimeException.", default="RuntimeException"),
           field("cause", "check", "Constructor with a cause", default=True),
           COMMENTS],
          hint="OutOfStockException"),
    jitem("test", "JUnit 5 test case", HEAD +
          "import static org.junit.jupiter.api.Assertions.*;\n\n"
          "{{#after}}import org.junit.jupiter.api.AfterEach;\n{{/after}}"
          "{{#before}}import org.junit.jupiter.api.BeforeEach;\n{{/before}}import org.junit.jupiter.api.Test;\n\n" + DOC +
          "class {{NamePascal}} {\n"
          "{{#under}}\n    private {{under}} subject;\n{{/under}}"
          "{{#before}}\n    @BeforeEach\n    void setUp() {\n{{#under}}        subject = new {{under}}();\n{{/under}}    }\n{{/before}}"
          "{{#after}}\n    @AfterEach\n    void tearDown() {\n    }\n{{/after}}"
          "\n    @Test\n    void works() {\n        fail(\"Not yet implemented\");\n    }\n}\n",
          [source(("src/test/java",)), PACKAGE,
           field("under", "type", "Class under test", hint="Cart"),
           field("before", "check", "setUp() with @BeforeEach"),
           field("after", "check", "tearDown() with @AfterEach"),
           COMMENTS],
          hint="CartTest", about="Made in src/test/java, in the same package."),
    jitem("package", "Package", "{{#comments}}/**\n * {{Name}}.\n */\n{{/comments}}package {{Name}};\n",
          [source(), field("comments", "check", "Create package-info.java comment", about="A Javadoc comment for the package.")],
          hint="com.example.shop.cart", about="Its folders, with a package-info.java.",
          name_kind="dotted", path="{{name_path}}/package-info.java", name_start="{{package.}}"),
]

K = "{{kotlin_package_line}}"
KOTLIN = [
    item("class", "Class", "{{NamePascal}}.kt", K + "class {{NamePascal}} {\n}\n", hint="Cart"),
    item("data", "Data class", "{{NamePascal}}.kt", K + "data class {{NamePascal}}(\n    val id: String,\n)\n", hint="Product"),
    item("interface", "Interface", "{{NamePascal}}.kt", K + "interface {{NamePascal}} {\n}\n", hint="PaymentGateway"),
    item("object", "Object", "{{NamePascal}}.kt", K + "object {{NamePascal}} {\n}\n", hint="Config"),
    item("enum", "Enum class", "{{NamePascal}}.kt", K + "enum class {{NamePascal}} {\n}\n", hint="OrderStatus"),
    item("sealed", "Sealed interface", "{{NamePascal}}.kt", K + "sealed interface {{NamePascal}} {\n}\n", hint="Result"),
    item("test", "Test", "{{NamePascal}}.kt",
         K + "import kotlin.test.Test\nimport kotlin.test.assertTrue\n\nclass {{NamePascal}} {\n"
         "    @Test\n    fun works() {\n        assertTrue(true)\n    }\n}\n",
         hint="CartTest", about="kotlin.test, in a test folder."),
    item("file", "File", "{{NamePascal}}.kt", K, hint="Extensions", about="An empty Kotlin file in this package."),
]

REACT = [
    item("component", "Component", "{{NamePascal}}.jsx",
         "export default function {{NamePascal}}() {\n  return <div>{{NamePascal}}</div>\n}\n", hint="ProductCard"),
    item("component-ts", "Component (TypeScript)", "{{NamePascal}}.tsx",
         "type {{NamePascal}}Props = {}\n\nexport default function {{NamePascal}}({}: {{NamePascal}}Props) {\n"
         "  return <div>{{NamePascal}}</div>\n}\n", hint="ProductCard"),
    item("hook", "Hook", "use{{NamePascal}}.js",
         "import { useState } from 'react'\n\nexport function use{{NamePascal}}() {\n  const [value, setValue] = useState(null)\n"
         "  return [value, setValue]\n}\n", hint="Cart", about="Named use…, as React expects."),
    item("context", "Context", "{{NamePascal}}Context.jsx",
         "import { createContext, useContext } from 'react'\n\nconst {{NamePascal}}Context = createContext(null)\n\n"
         "export function {{NamePascal}}Provider({ children }) {\n"
         "  return <{{NamePascal}}Context.Provider value={null}>{children}</{{NamePascal}}Context.Provider>\n}\n\n"
         "export function use{{NamePascal}}() {\n  return useContext({{NamePascal}}Context)\n}\n", hint="Cart"),
    item("test", "Test (Vitest)", "{{NamePascal}}.test.jsx",
         "import { describe, it, expect } from 'vitest'\n\ndescribe('{{NamePascal}}', () => {\n"
         "  it('works', () => {\n    expect(true).toBe(true)\n  })\n})\n", hint="ProductCard"),
]

PYTHON = [
    item("module", "Module", "{{name_snake}}.py", '"""{{Name}}."""\n', hint="pricing"),
    item("class", "Class", "{{name_snake}}.py",
         '"""{{NamePascal}}."""\n\n\nclass {{NamePascal}}:\n    def __init__(self) -> None:\n        pass\n', hint="Cart"),
    item("dataclass", "Dataclass", "{{name_snake}}.py",
         '"""{{NamePascal}}."""\n\nfrom dataclasses import dataclass\n\n\n@dataclass\nclass {{NamePascal}}:\n    id: str\n',
         hint="Product"),
    item("package", "Package", "{{name_snake}}/__init__.py", '"""{{Name}}."""\n', hint="checkout",
         about="A folder with __init__.py."),
    item("test", "Test (pytest)", "test_{{name_snake}}.py", "def test_{{name_snake}}():\n    assert True\n", hint="cart"),
]

RUST = [
    item("module", "Module", "{{name_snake}}.rs", "//! {{Name}}.\n", hint="pricing",
         about="Add `mod …;` to its parent to use it."),
    item("test", "Integration test", "{{name_snake}}.rs",
         "#[test]\nfn {{name_snake}}() {\n    assert!(true);\n}\n", hint="checkout", about="In the tests/ folder."),
    item("bin", "Binary", "{{name_snake}}.rs", "fn main() {\n}\n", hint="import_data", about="In src/bin/: `cargo run --bin …`."),
]

PACKS = [
    ("java", "Java: new classes and packages", "As in Eclipse: class, interface, enum, record, annotation, exception, JUnit 5 test case and package, each with its source folder, package and options. Fits Maven and Gradle projects.", ["java"], JAVA),
    ("kotlin", "Kotlin: new classes and files", "Class, data class, interface, object, enum, sealed interface and test, with the package line from the folder.", ["kt"], KOTLIN),
    ("react", "React: new components and hooks", "Component (JSX or TSX), hook, context and Vitest test.", ["jsx", "tsx"], REACT),
    ("python", "Python: new modules and classes", "Module, class, dataclass, package and pytest test.", ["py"], PYTHON),
    ("rust", "Rust: new modules", "Module, integration test and binary.", ["rs"], RUST),
]

index = []
for id, name, about, file_types, items in PACKS:
    pack = {"format": 1, "kind": "new-items", "id": id, "name": name, "version": "1.0.0", "about": about,
            "file_types": file_types, "items": items}
    text = json.dumps(pack, indent=2, ensure_ascii=False) + "\n"
    with open(os.path.join(HERE, f"{id}.json"), "w") as f:
        f.write(text)
    data = text.encode()
    index.append({"id": id, "name": name, "kind": "new-items", "version": "1.0.0", "about": about,
                  "file_types": file_types, "url": f"{BASE}/{id}.json", "size": len(data),
                  "sha256": hashlib.sha256(data).hexdigest()})

with open(os.path.join(HERE, "index.json"), "w") as f:
    json.dump({"format": 1, "packs": index}, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("\n".join(f"{p['id']}: {len(next(i for (x, _, _, _, i) in PACKS if x == p['id']))} items, {p['size']} bytes" for p in index))
