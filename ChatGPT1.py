import ast
import string

# ----------------------------
# LABEL SYSTEM (буквы + кеш)
# ----------------------------

class LabelManager:
    def __init__(self):
        self.label_map = {}
        self.reverse_map = {}
        self.counter = 0

    def _next_label(self):
        # A, B, ... Z, AA, AB ...
        letters = string.ascii_uppercase
        n = self.counter
        result = ""
        while True:
            result = letters[n % 26] + result
            n = n // 26 - 1
            if n < 0:
                break
        self.counter += 1
        return result

    def get(self, text):
        if text in self.reverse_map:
            return self.reverse_map[text]

        key = self._next_label()
        self.label_map[key] = text
        self.reverse_map[text] = key
        return key


# ----------------------------
# COMPLEXITY CHECK
# ----------------------------

def is_complex_for(node):
    return (
        isinstance(node, ast.For)
        and (
            len(node.body) > 1
            or any(isinstance(n, ast.For) for n in node.body)
        )
    )


# ----------------------------
# MAIN BUILDER
# ----------------------------

class DrakonBuilder:

    def __init__(self):
        self.labels = LabelManager()
        self.sub_diagrams = {}

    def build_function(self, func_node):
        name = func_node.name

        chunks = []

        for node in func_node.body:
            if isinstance(node, ast.For) and is_complex_for(node):
                chunk = self._extract_loop(node)
                chunks.append(chunk)
            else:
                label = self.labels.get(self._node_to_text(node))
                chunks.append((label, [node]))

        return {
            "name": name,
            "chunks": chunks
        }

    # ----------------------------
    # LOOP EXTRACTION
    # ----------------------------

    def _extract_loop(self, node):
        entry = self.labels.get("loop_entry")
        exit_ = self.labels.get("loop_exit")

        diagram_name = f"{entry}_{exit_}_loop"

        # создаем поддиаграмму
        self.sub_diagrams[diagram_name] = self._build_loop_diagram(node)

        return (diagram_name, [node])

    def _build_loop_diagram(self, node):
        chunks = []

        for n in node.body:
            if isinstance(n, ast.For) and is_complex_for(n):
                chunk = self._extract_loop(n)
                chunks.append(chunk)
            else:
                label = self.labels.get(self._node_to_text(n))
                chunks.append((label, [n]))

        return {
            "type": "loop",
            "chunks": chunks
        }

    # ----------------------------
    # NODE TEXT EXTRACTION
    # ----------------------------

    def _node_to_text(self, node):
        try:
            return ast.unparse(node)
        except:
            return node.__class__.__name__


# ----------------------------
# HIGH LEVEL API
# ----------------------------

def build_drakon_from_code(source_code):
    tree = ast.parse(source_code)

    builder = DrakonBuilder()

    functions = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append(builder.build_function(node))

    return {
        "functions": functions,
        "labels": builder.labels.label_map,
        "sub_diagrams": builder.sub_diagrams
    }


# ----------------------------
# TEST
# ----------------------------

if __name__ == "__main__":
    code = """
def example():
    x = 0
    for i in range(10):
        y = i * 2
        for j in range(5):
            z = j + y
    return x
"""

    result = build_drakon_from_code(code)

    print("=== FUNCTIONS ===")
    for f in result["functions"]:
        print(f)

    print("\n=== LABELS ===")
    for k, v in result["labels"].items():
        print(k, "->", v)

    print("\n=== SUB DIAGRAMS ===")
    for k, v in result["sub_diagrams"].items():
        print(k, "->", v)