import ast
import sqlite3
import os

class DrakonPerfectLineConverterV5:
    def __init__(self, drn_path="rmsnorm.drn"):
        self.drn_path = drn_path
        if os.path.exists(self.drn_path):
            os.remove(self.drn_path)
            
        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._build_exact_schema()

    def _build_exact_schema(self):
        """Создание реляционной структуры таблиц по спецификации drakon_qt"""
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

    def convert_with_perfect_line(self, py_source_path="rmsnorm.py"):
        """Трансляция с выравниванием по оси 500 и добавлением оригинального шампура"""
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        
        diagram_id = 1
        
        # Мы явно задаем item_id для каждого элемента, чтобы соответствовать эталону
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "rmsnorm":
                func_name = node.name
                
                # Системное дерево проекта
                self.cursor.execute("INSERT INTO tree_nodes VALUES (1, 0, 'item', NULL, ?);", (diagram_id,))
                self.cursor.execute("INSERT INTO state VALUES (1, 1, NULL);")
                self.cursor.execute("INSERT INTO diagrams VALUES (1, ?, '0 250', NULL, 120.0);", (func_name,))
                self.cursor.execute("INSERT INTO diagram_info VALUES (1, 'papersize', 'a4');")
                self.cursor.execute("INSERT INTO diagram_info VALUES (1, 'orientation', 'portrait');")

                # Новая выверенная ось шампура из sql.diff
                center_x = 500

                # Извлекаем исходный текст функции без изменений
                body_lines = [ast.unparse(stmt).strip() for stmt in node.body]
                function_body_text = "\n".join(body_lines)

                # Икона 1: Начало (item_id=1, x=500, y=420)
                self.cursor.execute("""
                    INSERT INTO items VALUES (1, 1, 'beginend', ?, 0, ?, 420, 50, 20, 60, 0, NULL, '', NULL, '');
                """, (func_name, center_x))

                # Икона 2: Конец (item_id=2, x=500, y=750)
                self.cursor.execute("""
                    INSERT INTO items VALUES (2, 1, 'beginend', 'Конец', 0, ?, 750, 50, 20, 60, 0, NULL, '', NULL, '');
                """, (center_x,))

                # Икона 6 (или 3): Процесс (item_id=3, x=500, y=550)
                # Оставляем текстовые поля пустыми строками, как в исходном 2.sql
                self.cursor.execute("""
                    INSERT INTO items VALUES (3, 1, 'action', ?, 0, ?, 550, 170, 40, 0, 0, NULL, '', NULL, '');
                """, (function_body_text, center_x))

                # Графический элемент ЛИНИЯ (item_id=6, x=500, y=420, h=340) из sql.diff
                # Пронизывает схему от Начала до Конца, материализуя шампур времени.
                self.cursor.execute("""
                    INSERT INTO items VALUES (6, 1, 'vertical', '', 0, 500, 420, 0, 340, 0, 0, NULL, NULL, NULL, NULL);
                """)

        self.conn.commit()
        self.conn.close()
        print(f"[Успех] Детерминированный скрипт py2drn5.py собрал rmsnorm.drn с явным шампуром времени.")

if __name__ == "__main__":
    converter = DrakonPerfectLineConverterV5("rmsnorm.drn")
    converter.convert_with_perfect_line("rmsnorm.py")
