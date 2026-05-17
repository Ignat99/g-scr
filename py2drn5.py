import ast
import sqlite3
import os

class DrakonLineConnectorConverterV5:
    def __init__(self, drn_path="rmsnorm.drn"):
        self.drn_path = drn_path
        if os.path.exists(self.drn_path):
            os.remove(self.drn_path)
            
        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._build_exact_schema()

    def _build_exact_schema(self):
        """Создание оригинальной структуры таблиц согласно спецификации drakon_qt"""
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

    def convert_with_lines(self, py_source_path="rmsnorm.py"):
        """Трансляция rmsnorm.py с явным добавлением графических линий связи"""
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        
        diagram_id = 1
        item_id = 1

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "rmsnorm":
                func_name = node.name
                
                # Метаданные дерева проекта
                self.cursor.execute("INSERT INTO tree_nodes VALUES (?, 0, 'item', NULL, ?);", (diagram_id, diagram_id))
                self.cursor.execute("INSERT INTO state VALUES (?, ?, NULL);", (diagram_id, diagram_id))
                self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 120.0);", (diagram_id, func_name))
                self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (diagram_id,))
                self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (diagram_id,))

                # Координата центральной вертикальной оси алгоритма
                center_x = 510

                # Икона 1: Начало (тип: 'beginend', y=420)
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, ?, 420, 50, 20, 60, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, func_name, center_x))
                item_id += 1

                # Икона 2: Конец (тип: 'beginend', y=750, текст: 'Конец')
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'beginend', 'Конец', 0, ?, 750, 50, 20, 60, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, center_x))
                item_id += 1

                # Извлекаем полный текст тела функции без изменения логики
                body_lines = [ast.unparse(stmt).strip() for stmt in node.body]
                function_body_text = "\n".join(body_lines)

                # Икона 3: Процесс (тип: 'action', y=550)
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, 550, 170, 40, 0, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, function_body_text, center_x))
                item_id += 1

                # --- ДОБАВЛЕНИЕ ЛИНИЙ (ШАМПУРА) ---
                # В drakon_qt примитив линии часто задается типом 'vertical' или 'line' 
                # с указанием стартовой точки (x, y) и смещения или конечной точки.
                
                # Линия 1: от Начала (y=420) до Процесса (y=550)
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'vertical', '', 0, ?, 420, 0, 0, 0, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, center_x))
                item_id += 1

                # Линия 2: от Процесса (y=550) до Конца (y=750)
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'vertical', '', 0, ?, 550, 0, 0, 0, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, center_x))
                item_id += 1

                diagram_id += 1

        self.conn.commit()
        self.conn.close()
        print(f"[Выполнение] Скрипт py2drn5.py успешно сгенерировал файл {self.drn_path}")

if __name__ == "__main__":
    converter = DrakonLineConnectorConverterV5("rmsnorm.drn")
    converter.convert_with_lines("rmsnorm.py")
    
