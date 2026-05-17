import ast
import sqlite3
import os

class PyToDrakonConverter:
    def __init__(self, drn_path="microgpt.drn"):
        self.drn_path = drn_path
        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._init_db_schema()

    def _init_db_schema(self):
        """
        Инициализация таблиц согласно фактической схеме DRAKONEditor.
        Если таблицы уже созданы редактором, они не будут перезаписаны.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS diagrams (
                diagram_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                origin TEXT,
                description TEXT,
                zoom DOUBLE DEFAULT 1.0
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                diagram_id INTEGER,
                type TEXT,
                text TEXT,
                x INTEGER,
                y INTEGER,
                w INTEGER,
                h INTEGER
            );
        """)
        self.conn.commit()

    def parse_and_convert(self, py_source_path="microgpt.py"):
        """
        Парсинг файла Python и генерация соответствующих DMM-диаграмм ДРАКОН
        """
        with open(py_source_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        # Получаем абстрактное синтаксическое дерево (AST) кода
        tree = ast.parse(source_code)
        
        # Перебираем функции верхнего уровня (например, gpt, softmax)
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                self._convert_function_to_diagram(node)

        self.conn.close()
        print(f"[Успех] Мощение завершено. Результат записан в {self.drn_path}")

    def _convert_function_to_diagram(self, func_node):
        """
        Конвертирует отдельную функцию Python в дракон-схему (автомат)
        """
        func_name = func_node.name
        print(f"Обработка функции (автомата): {func_name}")

        # 1. Регистрируем автомат в таблице diagrams
        try:
            self.cursor.execute(
                "INSERT INTO diagrams (name, origin, description) VALUES (?, 'python', ?);",
                (func_name, f"Автогенерированный систолический автомат {func_name}")
            )
            diagram_id = self.cursor.lastrowid
        except sqlite3.IntegrityError:
            self.cursor.execute("SELECT diagram_id FROM diagrams WHERE name = ?;", (func_name,))
            diagram_id = self.cursor.fetchone()[0]

        # Очистим старые элементы этой диаграммы, если они были
        self.cursor.execute("DELETE FROM items WHERE diagram_id = ?;", (diagram_id,))

        # Начальные координаты для мощения икон на плоскости
        current_y = 100
        center_x = 500

        # 2. Создаем заголовочную икону "Начало" (Икона типа 'header' или 'begin')
        self._insert_item(diagram_id, "header", func_name, center_x, current_y, 140, 60)
        current_y += 100

        # 3. Обходим тело функции и транслируем выражения в иконы 'action' или 'question'
        for stmt in func_node.body:
            # Извлекаем исходный текстовый фрагмент выражения
            stmt_text = ast.unparse(stmt).strip()

            if isinstance(stmt, ast.If):
                # Если встретили условие — это ромб Выбора ('question')
                # В детерминированной логике Сетуни это ветвление на [-1, +1]
                condition_text = ast.unparse(stmt.test).strip()
                self._insert_item(diagram_id, "question", condition_text, center_x, current_y, 160, 60)
                current_y += 120
                
                # Для простоты линейного сквозного генератора разворачиваем тело ветки True
                for sub_stmt in stmt.body:
                    sub_text = ast.unparse(sub_stmt).strip()
                    self._insert_item(diagram_id, "action", sub_text, center_x, current_y, 200, 50)
                    current_y += 100
            else:
                # Все стандартные присваивания и вызовы (например, расчет Паскаля) — это 'action'
                self._insert_item(diagram_id, "action", stmt_text, center_x, current_y, 200, 50)
                current_y += 100

        # 4. Завершающая икона "Конец"
        self._insert_item(diagram_id, "end", "Конец", center_x, current_y, 140, 60)
        self.conn.commit()

    def _insert_item(self, diagram_id, item_type, text, x, y, w, h):
        """Вспомогательный метод для записи иконы в таблицу items"""
        self.cursor.execute("""
            INSERT INTO items (diagram_id, type, text, x, y, w, h)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (diagram_id, item_type, text, x, y, w, h))

if __name__ == "__main__":
    # Инициализируем и запускаем трансляцию
    # Скрипт возьмет ваш microgpt.py и напрямую встроит его логику в таблицы microgpt.drn
    converter = PyToDrakonConverter(drn_path="microgpt.drn")
    converter.parse_and_convert(py_source_path="microgpt.py")
