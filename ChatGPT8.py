import ast
import sqlite3
import os

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

    # === НОВЫЙ ПАРСЕР ===
    def _parse_into_letter_branches(self, func_node):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = []
        idx = 0
        current = []

        def flush():
            nonlocal idx, current
            if not current:
                return
            name = letters[idx % 26] + letters[(idx + 1) % 26]
            code = "\n".join([ast.unparse(n).strip() for n in current])
            result.append((name, code))
            current = []
            idx += 1

        for node in func_node.body:
            if isinstance(node, (ast.For, ast.While)):
                flush()
                name = letters[idx % 26] + letters[(idx + 1) % 26]
                code = ast.unparse(node).strip()
                result.append((name, code))
                idx += 1
            else:
                current.append(node)

        flush()
        return result

    def convert_source(self, py_source_path="rmsnorm.py"):
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_lines = f.readlines()

        tree = ast.parse("".join(source_lines))

        node_id = 1
        diagram_id = 1
        item_id = 1

        self.cursor.execute("INSERT INTO tree_nodes VALUES (?, 0, 'folder', 'microgpt', NULL);", (node_id,))
        root_folder_id = node_id
        node_id += 1

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                self.cursor.execute("INSERT INTO tree_nodes VALUES (?, ?, 'item', ?, ?);", (node_id, root_folder_id, node.name, diagram_id))
                node_id += 1

                if node.name in ['gpt', 'main']:
                    self._insert_silhouette_diagram(diagram_id, node.name, node, "", item_id)
                    item_id += 100
                else:
                    body = "\n".join([ast.unparse(n).strip() for n in node.body])
                    self._insert_primitive_diagram(diagram_id, node.name, body, "", item_id)
                    item_id += 10

                diagram_id += 1

        self.conn.commit()
        self.conn.close()

    def _insert_primitive_diagram(self, dia_id, name, body, params, item_start):
        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 100.0);", (dia_id, name))

        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, 170, 60, 50, 20, 60, 0, NULL, '', NULL, '');", (item_start, dia_id, name))
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', 'End', 0, 170, 390, 50, 20, 60, 0, NULL, '', NULL, '');", (item_start + 1, dia_id))
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'vertical', '', 0, 170, 80, 0, 290, 0, 0, NULL, '', NULL, '');", (item_start + 2, dia_id))
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, 170, 170, 110, 40, 0, 0, NULL, '', NULL, '');", (item_start + 3, dia_id, body))

    def _insert_silhouette_diagram(self, dia_id, name, func_node, params, item_start):

        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '-40 14', ?, 100.0);", (dia_id, name, "auto"))

        # === ВАШ КОД (СОХРАНЕН) ===
        """
        branches = []
        if name == 'gpt':
            chunks = [
                ("Инициализация эмбеддингов", func_node.body[0:5]),
                ("Цикл по слоям нейросети", [func_node.body[5]]),
                ("Вычисление Logits", func_node.body[6:])
            ]
        else:
            chunks = [
                ("Подготовка данных и окружения", func_node.body[0:10]),
                ("Конфигурация сети и Adam", func_node.body[10:19]),
                ("Цикл оптимизации (Training)", [func_node.body[19]]),
                ("Генерация текста (Inference)", func_node.body[20:])
            ]

        for b_name, nodes in chunks:
            code_text = "\n".join([ast.unparse(n).strip() for n in nodes])
            branches.append((b_name, code_text))
        """

        # === РАБОЧИЙ ПАРСЕР ===
        branches = self._parse_into_letter_branches(func_node)

        start_x = 150
        step_x = 300
        y = 120

        for i, (b_name, b_code) in enumerate(branches):
            x = start_x + i * step_x

            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'branch', ?, 0, ?, ?, 140, 30, 0, 0, NULL, '', NULL, '');",
                                (item_start, dia_id, b_name, x, y))
            item_start += 1

            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 180, 80, 0, 0, NULL, '', NULL, '');",
                                (item_start, dia_id, b_code, x, y + 80))
            item_start += 1


if __name__ == "__main__":
    converter = DrakonBuranSilhouetteConverterV10("rmsnorm.drn")
    converter.convert_source("rmsnorm.py")
