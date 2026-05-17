import ast
import sqlite3
import os

class DrakonParamsConverterV6:
    def __init__(self, drn_path="rmsnorm.drn"):
        self.drn_path = drn_path
        if os.path.exists(self.drn_path):
            os.remove(self.drn_path)
            
        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._build_exact_schema()

    def _build_exact_schema(self):
        """Создание реляционной структуры таблиц drakon_qt"""
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

    def convert_with_formal_params(self, py_source_path="rmsnorm.py"):
        """Трансляция с динамическим выделением параметров функции в выносное крыло"""
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        diagram_id = 1

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "rmsnorm":
                func_name = node.name
                
                # Извлекаем имена аргументов функции через AST
                # Для def rmsnorm(x) это даст список ['x']
                arg_names = [arg.arg for arg in node.args.args]
                params_text = ", ".join(arg_names) if arg_names else ""
                
                # Системное дерево проекта
                self.cursor.execute("INSERT INTO tree_nodes VALUES (1, 0, 'item', NULL, ?);", (diagram_id,))
                self.cursor.execute("INSERT INTO state VALUES (1, 1, NULL);")
                self.cursor.execute("INSERT INTO diagrams VALUES (1, ?, '0 250', NULL, 120.0);", (func_name,))
                self.cursor.execute("INSERT INTO diagram_info VALUES (1, 'papersize', 'a4');")
                self.cursor.execute("INSERT INTO diagram_info VALUES (1, 'orientation', 'portrait');")

                # Центральная ось шампура
                center_x = 500

                # Извлекаем полный текст тела функции
                body_lines = [ast.unparse(stmt).strip() for stmt in node.body]
                function_body_text = "\n".join(body_lines)

                # Икона 1: Начало (x=500, y=420, текст — чистое имя функции)
                self.cursor.execute("""
                    INSERT INTO items VALUES (1, 1, 'beginend', ?, 0, ?, 420, 50, 20, 60, 0, NULL, '', NULL, '');
                """, (func_name, center_x))

                # Икона 2: Конец (x=500, y=750, текст — 'Конец')
                self.cursor.execute("""
                    INSERT INTO items VALUES (2, 1, 'beginend', 'Конец', 0, ?, 750, 50, 20, 60, 0, NULL, '', NULL, '');
                """, (center_x,))

                # Икона 3: Процесс (x=500, y=550, содержит весь исполняемый код)
                self.cursor.execute("""
                    INSERT INTO items VALUES (3, 1, 'action', ?, 0, ?, 550, 170, 40, 0, 0, NULL, '', NULL, '');
                """, (function_body_text, center_x))

                # Графический элемент: Вертикальный шампур (item_id=6, h=340)
                self.cursor.execute("""
                    INSERT INTO items VALUES (6, 1, 'vertical', '', 0, 500, 420, 0, 340, 0, 0, NULL, NULL, NULL, NULL);
                """)

                # Если у функции обнаружены аргументы, строим выносное правое крыло параметров
                if params_text:
                    # Элемент 8: Горизонтальный мост связи (тип 'horizontal', x=530, y=420, w=140)
                    self.cursor.execute("""
                        INSERT INTO items VALUES (8, 1, 'horizontal', '', 0, 530, 420, 140, 0, 0, 0, NULL, NULL, NULL, NULL);
                    """)
                    
                    # Элемент 9: Выносная икона параметров (тип 'action', x=690, y=420, текст — имена аргументов)
                    # Ставим selected=1 (или 0), color=None, format=None согласно оригинальному диффу
                    self.cursor.execute("""
                        INSERT INTO items VALUES (9, 1, 'action', ?, 1, 690, 420, 50, 20, 0, 0, NULL, NULL, NULL, NULL);
                    """, (params_text,))

                diagram_id += 1

        self.conn.commit()
        self.conn.close()
        print(f"[Выполнение] Скрипт py2drn6.py детерминированно собрал схему с выносными параметрами '{params_text}'.")

if __name__ == "__main__":
    converter = DrakonParamsConverterV6("rmsnorm.drn")
    converter.convert_with_formal_params("rmsnorm.py")

