import ast
import sqlite3
import os

class FinalDrakonConverter:
    def __init__(self, drn_path="microgpt.drn"):
        self.drn_path = drn_path
        if os.path.exists(self.drn_path):
            os.remove(self.drn_path)
            
        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._create_exact_tables()

    def _create_exact_tables(self):
        """Создание реляционной структуры в точном соответствии с эталоном 2.sql"""
        self.cursor.execute("""
            CREATE TABLE tree_nodes (
                node_id integer primary key,
                parent integer,
                type text,
                name text,
                diagram_id integer
            );
        """)

        self.cursor.execute("""
            CREATE TABLE state (
                row integer primary key,
                current_dia integer,
                description text
            );
        """)

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

        self.cursor.execute("""
            CREATE TABLE info (
                key text primary key,
                value text
            );
        """)
        # Системные маркеры среды DRAKONEditor
        self.cursor.execute("INSERT INTO info VALUES ('type', 'drakon');")
        self.cursor.execute("INSERT INTO info VALUES ('version', '33');")
        self.cursor.execute("INSERT INTO info VALUES ('start_version', '1');")
        self.cursor.execute("INSERT INTO info VALUES ('language', 'Python 3.x');")

        self.cursor.execute("""
            CREATE TABLE diagrams (
                diagram_id integer primary key,
                name text unique,
                origin text,
                description text,
                zoom double
            );
        """)

        self.cursor.execute("""
            CREATE TABLE diagram_info (
                diagram_id integer,
                name text,
                value text,
                primary key (diagram_id, name)
            );
        """)
        self.conn.commit()

    def convert(self, py_source_path="microgpt.py"):
        """Парсинг Python-кода и точное мощение структуры ДРАКОН"""
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        
        diagram_id = 1
        item_id = 1

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                
                # 1. Запись в tree_nodes и state
                self.cursor.execute("INSERT INTO tree_nodes VALUES (?, 0, 'item', NULL, ?);", (diagram_id, diagram_id))
                self.cursor.execute("INSERT INTO state VALUES (?, ?, NULL);", (diagram_id, diagram_id))
                
                # 2. Запись в diagrams (origin '0 250' и zoom 120.0 строго по эталону)
                self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 120.0);", (diagram_id, func_name))
                
                # Метаданные разметки листа
                self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (diagram_id,))
                self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (diagram_id,))

                # Координатная сетка оси шампура (X = 510)
                center_x = 510
                
                # Икона «Начало» (тип: 'beginend', имя функции, y=420, w=50, h=20, a=60, b=0)
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, ?, 420, 50, 20, 60, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, func_name, center_x))
                item_id += 1

                # Икона «Конец» (тип: 'beginend', текст 'Конец', y=750, w=50, h=20, a=60, b=0)
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'beginend', 'Конец', 0, ?, 750, 50, 20, 60, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, center_x))
                item_id += 1

                # Извлекаем все строки внутренностей функции без изменений
                body_lines = [ast.unparse(stmt).strip() for stmt in node.body]
                function_body_text = "\n".join(body_lines)

                # Икона «Процесс» (тип: 'action', содержит ВЕСЬ код, y=550, w=170, h=40)
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, 550, 170, 40, 0, 0, NULL, '', NULL, '');
                """, (item_id, diagram_id, function_body_text, center_x))
                
                item_id += 1
                diagram_id += 1

        self.conn.commit()
        self.conn.close()
        print(f"[Детерминизм] Конвертация завершена. Файл {self.drn_path} полностью совместим с эталоном.")

if __name__ == "__main__":
    # Запуск обработки исходного файла
    converter = FinalDrakonConverter("microgpt.drn")
    converter.convert("microgpt.py")
  
