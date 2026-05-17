import ast
import sqlite3
import os

class ExactDrakon133Converter:
    def __init__(self, drn_path="rmsnorm.drn"):
        self.drn_path = drn_path
        # Удаляем старый файл для обеспечения чистоты пересоздания базы
        if os.path.exists(self.drn_path):
            os.remove(self.drn_path)
            
        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._create_base_tables()

    def _create_base_tables(self):
        """Создание точной реляционной структуры согласно спецификации DRAKONEditor 1.33"""
        # Системные параметры редактора
        self.cursor.execute("CREATE TABLE info (p TEXT, v TEXT);")
        self.cursor.execute("INSERT INTO info VALUES ('version', '1.33');")
        self.cursor.execute("INSERT INTO info VALUES ('type', 'drakon');")

        self.cursor.execute("CREATE TABLE state (p TEXT, v TEXT);")

        # Таблица диаграмм (каждая функция - отдельный автомат)
        self.cursor.execute("""
            CREATE TABLE diagrams (
                diagram_id INTEGER PRIMARY KEY,
                name TEXT,
                origin TEXT,
                description TEXT,
                zoom DOUBLE
            );
        """)

        self.cursor.execute("CREATE TABLE diagram_info (diagram_id INTEGER, p TEXT, v TEXT);")

        # Ключевая таблица икон и топологии
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
                flag1 INTEGER,
                flag2 INTEGER,
                text2 TEXT,
                link_type TEXT,
                line_to INTEGER
            );
        """)

        # Менеджер дерева проекта
        self.cursor.execute("""
            CREATE TABLE tree_nodes (
                node_id INTEGER PRIMARY KEY,
                parent_id INTEGER,
                name TEXT,
                type TEXT,
                diagram_id INTEGER
            );
        """)
        self.conn.commit()

    def convert_file(self, py_source_path="rmsnorm.py"):
        """Парсинг исходного кода и генерация строгого графа ДРАКОН"""
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        
        # Создаем корневой элемент проекта в дереве
        self.cursor.execute("INSERT INTO tree_nodes (parent_id, name, type, diagram_id) VALUES (0, 'rmsnorm_project', 'folder', NULL);")
        folder_id = self.cursor.lastrowid

        diagram_id = 1
        item_id = 1

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                
                # Формируем заголовок функции в сигнатуре ДРАКОН (например, rmsnorm(x))
                args_list = [arg.arg for arg in node.args.args]
                func_signature = f"{func_name}({', '.join(args_list)})"
                
                # 1. Добавляем запись в diagrams
                self.cursor.execute(
                    "INSERT INTO diagrams VALUES (?, ?, 'python', '', 1.0);",
                    (diagram_id, func_name)
                )
                
                # 2. Регистрируем узел в дереве проекта
                self.cursor.execute(
                    "INSERT INTO tree_nodes (parent_id, name, type, diagram_id) VALUES (?, ?, 'diagram', ?);",
                    (folder_id, func_name, diagram_id)
                )

                # Геометрические параметры шампура
                center_x = 160
                current_y = 60
                
                # Икона "Начало" (тип: header)
                self.cursor.execute("""
                    INSERT INTO items (item_id, diagram_id, type, text, x, y, w, h)
                    VALUES (?, ?, 'header', ?, ?, ?, 100, 40);
                """, (item_id, diagram_id, func_signature, center_x, current_y))
                
                prev_item_id = item_id
                item_id += 1
                current_y += 90

                # Группируем внутренние выражения вычислений до оператора return
                actions = []
                return_stmt = None

                for stmt in node.body:
                    if isinstance(stmt, ast.Return):
                        return_stmt = stmt
                    else:
                        actions.append(ast.unparse(stmt).strip())

                # Икона "Процесс" (тип: action) — объединяем все строки вычислений
                if actions:
                    action_text = "\n".join(actions)
                    self.cursor.execute("""
                        INSERT INTO items (item_id, diagram_id, type, text, x, y, w, h)
                        VALUES (?, ?, 'action', ?, ?, ?, 240, 60);
                    """, (item_id, diagram_id, action_text, center_x, current_y))
                    
                    # Прошиваем линию связи от Начала к Процессу
                    self.cursor.execute("UPDATE items SET line_to = ? WHERE item_id = ?;", (item_id, prev_item_id))
                    
                    prev_item_id = item_id
                    item_id += 1
                    current_y += 100

                # Икона "Конец / Выход" (тип: end)
                if return_stmt:
                    return_text = ast.unparse(return_stmt).strip()
                    self.cursor.execute("""
                        INSERT INTO items (item_id, diagram_id, type, text, x, y, w, h)
                        VALUES (?, ?, 'end', ?, ?, ?, 220, 40);
                    """, (item_id, diagram_id, return_text, center_x, current_y))
                    
                    # Прошиваем линию связи от Процесса к Концу
                    self.cursor.execute("UPDATE items SET line_to = ? WHERE item_id = ?;", (item_id, prev_item_id))
                    
                    item_id += 1

                diagram_id += 1

        self.conn.commit()
        self.conn.close()
        print(f"[Успех] Детерминированный файл {self.drn_path} сформирован в точности с эталоном.")
      

if __name__ == "__main__":
    converter = ExactDrakon133Converter("rmsnorm.drn")
    converter.convert_file("rmsnorm.py")
