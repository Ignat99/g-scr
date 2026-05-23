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
        """Создание реляционной структуры таблиц drakon_qt (Слепок v8)"""
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

    # =========================
    # ДОБАВЛЕН ПАРСЕР (НЕ ТРОГАЕТ ВАШУ ЛОГИКУ)
    # =========================
    def parse_drakon_primitives(self, primitives):
        icons = {}
        verticals = []
        horizontals = []
        branches = {}

        for p in primitives:
            p_id, _, p_type, p_text, _, x, y, w, h, _, _, _, _, _, _ = p

            if p_type in ['beginend', 'branch', 'action', 'select', 'case', 'if', 'loopstart', 'loopend', 'address']:
                icons[p_id] = {
                    'id': p_id,
                    'type': p_type,
                    'text': p_text,
                    'x': x,
                    'y': y,
                    'w': w,
                    'h': h,
                    'next': None,
                    'branches': {}
                }
                if p_type == 'branch':
                    branches[p_text] = x

            elif p_type == 'vertical':
                verticals.append({'x': x, 'y': y})

            elif p_type == 'horizontal':
                horizontals.append({'x': x, 'y': y, 'w': w})

        shampurs_x = sorted(set(icon['x'] for icon in icons.values() if icon['type'] in ['branch', 'beginend']))

        def nearest_shampur(x):
            return min(shampurs_x, key=lambda sx: abs(sx - x))

        shampurs = {sx: [] for sx in shampurs_x}

        for icon in icons.values():
            sx = nearest_shampur(icon['x'])
            shampurs[sx].append(icon)

        for sx in shampurs:
            shampurs[sx].sort(key=lambda n: n['y'])

        for sx, chain in shampurs.items():
            for i in range(len(chain) - 1):
                if chain[i]['type'] != 'address':
                    chain[i]['next'] = chain[i + 1]['id']

        return {
            'shampurs': shampurs,
            'branches': branches,
            'icons': icons
        }
    # =========================

    def convert_source(self, py_source_path="rmsnorm.py"):
        """Парсинг исходного кода и генерация многошампурных силуэтов для длинных функций"""
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_lines = f.readlines()

        source_code = "".join(source_lines)
        tree = ast.parse(source_code)

        header_lines = []
        footer_lines = []
        class_node = None
        global_functions = {}

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                global_functions[node.name] = node
            elif isinstance(node, ast.ClassDef):
                class_node = node
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                header_lines.append(ast.unparse(node).strip())
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and getattr(node.value.func, 'name', '') == 'main':
                footer_lines.append(ast.unparse(node).strip())

        raw_headers = []
        for line in source_lines:
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("import") or not stripped:
                if "Autogenerated" not in line:
                    raw_headers.append(line.rstrip())
            else:
                break
        header_text = "\n".join(raw_headers).strip()

        class_text = ""
        if class_node:
            class_decl = f"class {class_node.name}:"
            body_parts = []
            for item in class_node.body:
                if isinstance(item, ast.Assign):
                    body_parts.append(f"    {ast.unparse(item).strip()}")
            class_text = class_decl + "\n" + "\n".join(body_parts)

        footer_text = "\n".join(footer_lines).strip() if footer_lines else "main()"
        state_description = f"=== header ===\n{header_text}\n\n=== class ===\n{class_text}\n\n=== footer ===\n{footer_text}"

        node_id = 1
        diagram_id = 1
        item_id = 1

        self.cursor.execute("INSERT INTO tree_nodes VALUES (?, 0, 'folder', 'microgpt', NULL);", (node_id,))
        root_folder_id = node_id
        node_id += 1

        if class_node:
            self.cursor.execute("INSERT INTO tree_nodes VALUES (?, ?, 'folder', ?, NULL);", (node_id, root_folder_id, class_node.name))
            class_folder_id = node_id
            node_id += 1
            
            for item in class_node.body:
                if isinstance(item, ast.FunctionDef):
                    self.cursor.execute("INSERT INTO tree_nodes VALUES (?, ?, 'item', '', ?);", (node_id, class_folder_id, diagram_id))
                    node_id += 1
                    
                    arg_names = [arg.arg for arg in item.args.args]
                    body_text = "\n".join([ast.unparse(stmt).strip() for stmt in item.body])
                    method_params = "#method\n" + "\n".join(arg_names)
                    
                    self._insert_primitive_diagram(diagram_id, item.name, body_text, method_params, item_id)
                    item_id += 10
                    diagram_id += 1

        for func_name, node in global_functions.items():
            self.cursor.execute("INSERT INTO tree_nodes VALUES (?, ?, 'item', ?, ?);", (node_id, root_folder_id, func_name, diagram_id))
            node_id += 1

            arg_names = [arg.arg for arg in node.args.args]
            params_text = ", ".join(arg_names) if arg_names else ""

            if func_name in ['gpt', 'main']:
                self._insert_silhouette_diagram(diagram_id, func_name, node, params_text, item_id)
                item_id += 100
            else:
                body_text = "\n".join([ast.unparse(stmt).strip() for stmt in node.body])
                self._insert_primitive_diagram(diagram_id, func_name, body_text, params_text, item_id)
                item_id += 10

            diagram_id += 1

        self.cursor.execute("INSERT INTO state VALUES (1, ?, ?);", (diagram_id - 1, state_description))
        self.conn.commit()
        self.conn.close()
        print(f"[Успех] База {self.drn_path} успешно сгенерирована. Функции 'gpt' и 'main' разложены на силуэты.")

    def _insert_primitive_diagram(self, dia_id, name, body, params, item_start):
        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 100.0);", (dia_id, name))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (dia_id,))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (dia_id,))
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, 170, 60, 50, 20, 60, 0, NULL, '', NULL, '');", (item_start, dia_id, name))
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', 'End', 0, 170, 390, 50, 20, 60, 0, NULL, '', NULL, '');", (item_start + 1, dia_id))
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'vertical', '', 0, 170, 80, 0, 290, 0, 0, NULL, '', NULL, '');", (item_start + 2, dia_id))

        if params:
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'horizontal', '', 0, 200, 60, 80, 0, 0, 0, NULL, '', NULL, '');", (item_start + 3, dia_id))
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, 310, 60, 50, 40, 0, 0, NULL, '', NULL, '');", (item_start + 4, dia_id, params))

        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, 170, 170, 110, 40, 0, 0, NULL, '', NULL, '');", (item_start + 5, dia_id, body))


if __name__ == "__main__":
    converter = DrakonBuranSilhouetteConverterV10("rmsnorm.drn")
    converter.convert_source("rmsnorm.py")
