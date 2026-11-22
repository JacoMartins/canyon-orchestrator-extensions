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


J = "{{java_package_line}}"
JAVA = [
    item("class", "Class", "{{NamePascal}}.java", J + "public class {{NamePascal}} {\n}\n", hint="Cart"),
    item("interface", "Interface", "{{NamePascal}}.java", J + "public interface {{NamePascal}} {\n}\n", hint="PaymentGateway"),
    item("enum", "Enum", "{{NamePascal}}.java", J + "public enum {{NamePascal}} {\n}\n", hint="OrderStatus"),
    item("record", "Record", "{{NamePascal}}.java", J + "public record {{NamePascal}}() {\n}\n", hint="Point", about="Java 16 and later."),
    item("abstract", "Abstract class", "{{NamePascal}}.java", J + "public abstract class {{NamePascal}} {\n}\n", hint="Shape"),
    item("annotation", "Annotation", "{{NamePascal}}.java",
         J + "import java.lang.annotation.ElementType;\nimport java.lang.annotation.Retention;\n"
         "import java.lang.annotation.RetentionPolicy;\nimport java.lang.annotation.Target;\n\n"
         "@Retention(RetentionPolicy.RUNTIME)\n@Target(ElementType.TYPE)\npublic @interface {{NamePascal}} {\n}\n",
         hint="Audited"),
    item("exception", "Exception", "{{NamePascal}}.java",
         J + "public class {{NamePascal}} extends RuntimeException {\n"
         "    public {{NamePascal}}(String message) {\n        super(message);\n    }\n}\n",
         hint="OutOfStockException"),
    item("main", "Main class", "{{NamePascal}}.java",
         J + "public class {{NamePascal}} {\n    public static void main(String[] args) {\n    }\n}\n", hint="App"),
    item("test", "JUnit 5 test", "{{NamePascal}}.java",
         J + "import static org.junit.jupiter.api.Assertions.*;\n\nimport org.junit.jupiter.api.Test;\n\n"
         "class {{NamePascal}} {\n    @Test\n    void works() {\n    }\n}\n",
         hint="CartTest", about="In a test folder (src/test/java/…)."),
    item("package", "Package", "{{name_path}}/package-info.java", "package {{package.}}{{Name}};\n",
         name_kind="dotted", hint="cart.checkout", about="A package (folder) under this one."),
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
    ("java", "Java: new classes and packages", "Class, interface, enum, record, annotation, exception, JUnit test and package, with the package line from the folder.", ["java"], JAVA),
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
