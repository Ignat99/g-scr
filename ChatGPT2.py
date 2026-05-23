import ast
import string


# =========================
# LABEL SYSTEM (две буквы)
# =========================

class Label2:
    def __init__(self):
        self.counter = 0
        self.letters = string.ascii_uppercase

    def next(self):
        a = self.letters[self.counter // 26]
        b = self.letters[self.counter % 26]
        self.counter += 1
        return a + b


# =========================
# PARSER
# =========================

class DrakonParser:

    def __init__(self):
        self.label_gen = Label2()
        self.diagrams = {}
        self.diagram_counter = 0

    def new_diagram_name(self):
        self.diagram_counter += 1
        return f"D{self.diagram_counter}"

    # ---------------------
    # ENTRY
    # ---------------------

    def parse(self, source):
        tree = ast.parse(source)

        result = []

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                result.append(self.parse_function(node))

        return result

    # ---------------------
    # FUNCTION → MAIN
    # ---------------------

    def parse_function(self, func):
        main_diagram = {
            "name": func.name,
            "type": "main",
            "shampurs": {
                "AA": [],
            }
        }

        for node in func.body:
            block = self.parse_node(node)
            main_diagram["shampurs"]["AA"].append(block)

        return main_diagram

    # ---------------------
    # NODE PARSER
    # ---------------------

    def parse_node(self, node):

        if isinstance(node, ast.For):
            return self.handle_for(node)

        return {
            "type": "action",
            "code": self.to_code(node)
        }

    # ---------------------
    # FOR → NEW DIAGRAM
    # ---------------------

    def handle_for(self, node):

        name = self.new_diagram_name()

        sh1 = self.label_gen.next()
        sh2 = self.label_gen.next()
        sh3 = self.label_gen.next()

        diagram = {
            "name": name,
            "type": "loop",
            "shampurs": {
                sh1: [],
                sh2: [],
                sh3: []
            }
        }

        # Раскладка
        for n in node.body:
            if isinstance(n, ast.If):
                diagram["shampurs"][sh2].append(self.parse_if(n))
            else:
                diagram["shampurs"][sh1].append({
                    "type": "action",
                    "code": self.to_code(n)
                })

        # если пустые шампуры → pass
        for k in diagram["shampurs"]:
            if not diagram["shampurs"][k]:
                diagram["shampurs"][k].append({"type": "pass"})

        self.diagrams[name] = diagram

        return {
            "type": "call",
            "diagram": name
        }

    # ---------------------
    # IF
    # ---------------------

    def parse_if(self, node):
        return {
            "type": "if",
            "cond": self.to_code(node.test),
            "body": [self.to_code(n) for n in node.body]
        }

    # ---------------------
    # CODE
    # ---------------------

    def to_code(self, node):
        try:
            return ast.unparse(node)
        except:
            return str(type(node))


# =========================
# TEST
# =========================

if __name__ == "__main__":
    code = """
def test():
    x = 0
    for i in range(10):
        y = i * 2
        if y > 5:
            x += y
    return x
"""

    parser = DrakonParser()
    result = parser.parse(code)

    print("MAIN:")
    print(result)

    print("\nDIAGRAMS:")
    for k, v in parser.diagrams.items():
        print(k, v)