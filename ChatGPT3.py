import ast
import sqlite3
import os
import string


class DrakonBuranSilhouetteConverterV10:
    def __init__(self, drn_path="rmsnorm.drn"):
        self.drn_path = drn_path
        if os.path.exists(self.drn_path):
            os.remove(self.drn_path)

        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._build_exact_schema()

    def _build_exact_schema(self):
        self.cursor.execute("CREATE TABLE tree_nodes (node_id integer primary key, parent integer, type text, name text, diagram_id integer);")
        self.cursor.execute("CREATE TABLE state (row integer primary key, current_dia integer, description text);")

        self.cursor.execute("""
            CREATE TABLE items (
                item_id integer primary key,
                diagram_id integer,
                type text,
                text text,
                selected integer,
                x integer,
                y integer,
                w integer,
                h integer,
                a integer,
                b integer,
                aux_value integer,
                color text,
                format text,
                text2 text
            );
        """)

        self.cursor.execute("CREATE TABLE info (key text primary key, value text);")
        self.cursor.execute("INSERT INTO info VALUES ('type', 'drakon');")
        self.cursor.execute("INSERT INTO info VALUES ('version', '33');")
        self.cursor.execute("INSERT INTO info VALUES ('start_version', '1');")
        self.cursor.execute("INSERT INTO info VALUES ('language', 'Python 3.x');")

        self.cursor.execute("CREATE TABLE diagrams (diagram_id integer primary key, name text unique, origin text, description text, zoom double);")
        self.cursor.execute("CREATE TABLE diagram_info (diagram_id integer, name text, value text, primary key (diagram_id, name));")
        self.conn.commit()

    # =========================================================
    # 🔥 ВСТРОЕННЫЙ ПАРСЕР (ГЛАВНОЕ ДОБАВЛЕНИЕ)
    # =========================================================
    def _parse_into_branches(self, func_node):
        label_counter = 0
        diagrams = []

        def next_label():
            nonlocal label_counter
            letters = string.ascii_uppercase
            a = letters[label_counter // 26]
            b = letters[label_counter % 26]
            label_counter += 1
            return a + b

        branches = []

        for node in func_node.body:

            # --- FOR → отдельная диаграмма ---
            if isinstance(node, ast.For):

                d_name = f"D{len(diagrams)+1}"

                sh1 = next_label()
                sh2 = next_label()
                sh3 = next_label()

                sub_blocks = {
                    sh1: [],
                    sh2: [],
                    sh3: []
                }

                for n in node.body:
                    if isinstance(n, ast.If):
                        sub_blocks[sh2].append(f"IF {ast.unparse(n.test)}")
                        for x in n.body:
                            sub_blocks[sh2].append(ast.unparse(x))
                    else:
                        sub_blocks[sh1].append(ast.unparse(n))

                for k in sub_blocks:
                    if not sub_blocks[k]:
                        sub_blocks[k] = ["pass"]

                diagrams.append((d_name, sub_blocks))

                branches.append((f"{sh1}_{sh3}", f"CALL {d_name}"))

            else:
                branches.append(("AA", ast.unparse(node)))

        return branches, diagrams

    # =========================================================

    def convert_source(self, py_source_path="rmsnorm.py"):
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)

        node_id = 1
        diagram_id = 1
        item_id = 1

        self.cursor.execute("INSERT INTO tree_nodes VALUES (?, 0, 'folder', 'project', NULL);", (node_id,))
        root_id = node_id
        node_id += 1

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):

                self.cursor.execute("INSERT INTO tree_nodes VALUES (?, ?, 'item', ?, ?);",
                                    (node_id, root_id, node.name, diagram_id))
                node_id += 1

                self._insert_silhouette_diagram(diagram_id, node.name, node, "", item_id)

                item_id += 500
                diagram_id += 1

        self.conn.commit()
        self.conn.close()

    # =========================================================
    # 🔥 МОДИФИЦИРОВАННЫЙ СИЛУЭТ
    # =========================================================
    def _insert_silhouette_diagram(self, dia_id, name, func_node, params, item_start):

        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 0', ?, 100.0);",
                            (dia_id, name, f"auto silhouette {name}"))

        branches, sub_diagrams = self._parse_into_branches(func_node)

        start_x = 150
        step_x = 300
        y = 100

        # Начало
        self.cursor.execute(
            "INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, ?, ?, 60, 20, 0, 0, NULL, '', NULL, '');",
            (item_start, dia_id, name, start_x, y)
        )
        item_start += 1

        for idx, (b_name, b_code) in enumerate(branches):

            cx = start_x + idx * step_x

            # шампур
            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, 'vertical', '', 0, ?, ?, 0, 300, 0, 0, NULL, '', NULL, '');",
                (item_start, dia_id, cx, y)
            )
            item_start += 1

            # branch
            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, 'branch', ?, 0, ?, ?, 120, 30, 0, 0, NULL, '', NULL, '');",
                (item_start, dia_id, b_name, cx, y + 40)
            )
            item_start += 1

            # action
            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 180, 60, 0, 0, NULL, '', NULL, '');",
                (item_start, dia_id, b_code, cx, y + 100)
            )
            item_start += 1

        # =========================================================
        # 🔥 ПОДДИАГРАММЫ
        # =========================================================
        for d_name, shampurs in sub_diagrams:

            dia_id += 1

            self.cursor.execute(
                "INSERT INTO diagrams VALUES (?, ?, '0 0', ?, 100.0);",
                (dia_id, d_name, "sub")
            )

            x = 150
            y = 100

            for sh, lines in shampurs.items():

                self.cursor.execute(
                    "INSERT INTO items VALUES (?, ?, 'branch', ?, 0, ?, ?, 120, 30, 0, 0, NULL, '', NULL, '');",
                    (item_start, dia_id, sh, x, y)
                )
                item_start += 1

                for line in lines:
                    y += 50
                    self.cursor.execute(
                        "INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 180, 40, 0, 0, NULL, '', NULL, '');",
                        (item_start, dia_id, line, x, y)
                    )
                    item_start += 1

                x += 250
                y = 100


if __name__ == "__main__":
    converter = DrakonBuranSilhouetteConverterV10("out.drn")
    converter.convert_source("rmsnorm.py")