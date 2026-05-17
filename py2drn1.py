import ast
import sqlite3
import os

class PurePyToDrakonConverter:
    def __init__(self, drn_path="microgpt.drn"):
        self.drn_path = drn_path
        # Если файл существовал, удалим его, чтобы создать чистую корректную базу
        if os.path.exists(self.drn_path):
            os.remove(self.drn_path)
            
        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._create_exact_tables()

    def _create_exact_tables(self):
        """Создание таблиц в строгом соответствии со структурой DRAKONEditor"""
        self.cursor.execute("CREATE TABLE info (p TEXT, v TEXT);")
        self.cursor.execute("INSERT INTO info VALUES ('version', '1.33');")
        self.cursor.execute("INSERT INTO info VALUES ('type', 'drakon');")

        self.cursor.execute("""
            CREATE TABLE diagrams (
                diagram_id INTEGER PRIMARY KEY,
                name TEXT,
                origin TEXT,
                description TEXT,
                zoom DOUBLE
            );
        """)

        # В DRAKONEditor иконы хранятся в таблице items.
        # Поля: item_id, diagram_id, type, text, x, y, w, h, а также связи (links)
        self.cursor.execute("""
            CREATE TABLE items (
                item_id INTEGER PRIMARY KEY,
                diagram_id INTEGER,
                type TEXT,
                text TEXT,
                x INTEGER,
                y INTEGER,
                w INTEGER,
                h INTEGER,
                line_to INTEGER,
                link_type TEXT
            );
        """)

        # Дерево проекта (левая панель) — без него редактор не видит диаграммы
        self.cursor.execute("""
            CREATE TABLE tree_nodes (
                node_id INTEGER PRIMARY KEY,
                parent_id INTEGER,
                name TEXT,
                type TEXT,
                diagram_id INTEGER
            );
        """)
        
        # Системные таблицы для сохранения состояния редактора
        self.cursor.execute("CREATE TABLE state (p TEXT, v TEXT);")
        self.cursor.execute("CREATE TABLE diagram_info (diagram_id INTEGER, p TEXT, v TEXT);")
        self.conn.commit()

    def convert(self, py_source_path="microgpt.py"):
        """Парсинг оригинального microgpt.py без изменения логики"""
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        # Парсим оригинальный код в AST
        tree = ast.parse(source_code)
        
        # Сначала создаем корневой узел в дереве проекта
        self.cursor.execute("INSERT INTO tree_nodes (parent_id, name, type, diagram_id) VALUES (0, 'microgpt', 'folder', NULL);")
        folder_id = self.cursor.lastrowid

        diagram_count = 1
        item_id_counter = 1

        # Извлекаем все функции (например, gpt, rmsnorm, linear, Value.backward и т.д.)
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                
                # 1. Запись в diagrams
                self.cursor.execute(
                    "INSERT INTO diagrams (diagram_id, name, origin, description, zoom) VALUES (?, ?, 'python', '', 1.0);",
                    (diagram_count, func_name)
                )
                
                # 2. Регистрируем в дереве проекта, привязывая к созданной диаграмме
                self.cursor.execute(
                    "INSERT INTO tree_nodes (parent_id, name, type, diagram_id) VALUES (?, ?, 'diagram', ?);",
                    (folder_id, func_name, diagram_count)
                )

                # Начальные координаты "шампура" ДРАКОН
                current_y = 60
                center_x = 500
                
                # 3. Создаем заголовок автомата (икона "Начало")
                # В DRAKONEditor заголовок обычно имеет тип 'header'
                self.cursor.execute("""
                    INSERT INTO items (item_id, diagram_id, type, text, x, y, w, h)
                    VALUES (?, ?, 'header', ?, ?, ?, 140, 60);
                """, (item_id_counter, diagram_count, func_name, center_x, current_y))
                
                prev_item_id = item_id_counter
                item_id_counter += 1
                current_y += 80

                # 4. Переносим внутренние выражения функции «как есть» в виде последовательных икон action
                for stmt in node.body:
                    stmt_text = ast.unparse(stmt).strip()
                    
                    # Размещаем икону "Процесс" (action)
                    self.cursor.execute("""
                        INSERT INTO items (item_id, diagram_id, type, text, x, y, w, h)
                        VALUES (?, ?, 'action', ?, ?, ?, 200, 50);
                    """, (item_id_counter, diagram_count, stmt_text, center_x, current_y))
                    
                    # Связываем предыдущую икону с текущей по вертикали
                    self.cursor.execute("""
                        UPDATE items SET line_to = ? WHERE item_id = ?;
                    """, (item_id_counter, prev_item_id))
                    
                    prev_item_id = item_id_counter
                    item_id_counter += 1
                    current_y += 80

                # 5. Создаем икону "Конец" (end)
                self.cursor.execute("""
                    INSERT INTO items (item_id, diagram_id, type, text, x, y, w, h)
                    VALUES (?, ?, 'end', 'Конец', ?, ?, 140, 60);
                """, (item_id_counter, diagram_count, center_x, current_y))
                
                # Связываем последнюю операцию с концом
                self.cursor.execute("""
                    UPDATE items SET line_to = ? WHERE item_id = ?;
                """, (item_id_counter, prev_item_id))
                
                item_id_counter += 1
                diagram_count += 1

        self.conn.commit()
        self.conn.close()
        print(f"[Успех] Исходный {py_source_path} детерминированно перенесен в {self.drn_path}")
      

if __name__ == "__main__":
    converter = PurePyToDrakonConverter("microgpt.drn")
    converter.convert("microgpt.py")
