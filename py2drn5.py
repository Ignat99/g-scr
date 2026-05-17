import ast
import sqlite3
import os

class DrakonTimelineConverterV5:
    def __init__(self, drn_path="rmsnorm.drn"):
        self.drn_path = drn_path
        if os.path.exists(self.drn_path):
            os.remove(self.drn_path)
            
        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._build_exact_schema()

    def _build_exact_schema(self):
        """Создание оригинальной структуры таблиц согласно дампу 2.sql"""
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

    def convert_with_timeline(self, py_source_path="rmsnorm.py"):
        """Трансляция с сохранением сквозного шампура времени"""
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        
        diagram_id = 1
        item_id = 1

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "rmsnorm":
                func_name = node.name
                
                # Системная регистрация в дереве drakon_qt
                self.cursor.execute("INSERT INTO tree_nodes VALUES (?, 0, 'item', NULL, ?);", (diagram_id, diagram_id))
                self.cursor.execute("INSERT INTO state VALUES (?, ?, NULL);", (diagram_id, diagram_id))
                self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 120.0);", (diagram_id, func_name))
                self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (diagram_id,))
                self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (diagram_id,))

                # Главная вертикальная ось времени (шампур)
                center_x = 510

                # Разделяем логику: вычисления отдельно, финальный return — в терминальный узел
                action_lines = []
                return_text = "Конец"

                for stmt in node.body:
                    if isinstance(stmt, ast.Return):
                        return_text = ast.unparse(stmt).strip()
                    else:
                        action_lines.append(ast.unparse(stmt).strip())

                pure_computation_text = "\n".join(action_lines)

                # 1. Икона «Начало» (y=420) — дает старт шампуру
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, ?, 420, 50, 20, 60, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, func_name, center_x))
                item_id += 1

                # 2. Икона «Процесс» (y=550) — шампур проходит сквозь вычисления
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, 550, 170, 40, 0, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, pure_computation_text, center_x))
                item_id += 1

                # 3. Икона «Конец» (y=710) — принимает return и замыкает шампур времени
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, ?, 710, 50, 20, 60, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, return_text, center_x))
                
                item_id += 1
                diagram_id += 1

        self.conn.commit()
        self.conn.close()
        print(f"[Успех] Ось времени восстановлена. Скрипт py2drn5.py сформировал непрерывный шампур.")

if __name__ == "__main__":
    converter = DrakonTimelineConverterV5("rmsnorm.drn")
    converter.convert_with_timeline("rmsnorm.py")
  
