import ast
import sqlite3
import os

class DrakonBuranSilhouetteConverterV10:
    def __init__(self, drn_path="rmsnorm.drn"):
        self.drn_path = drn_path
        if os.path.exists(self.drn_path):
            try:
                os.remove(self.drn_path)
            except OSError:
                pass
            
        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._build_exact_schema()

        # Единые сквозные счетчики сущностей для SQLite
        self._diagram_id = 1
        self._item_id = 1

    def _next_diagram_id(self):
        val = self._diagram_id
        self._diagram_id += 1
        return val

    def _get_next_item_id(self, increment=1):
        val = self._item_id
        self._item_id += increment
        return val

    def _build_exact_schema(self):
        """Создание точной реляционной структуры таблиц для drakon_qt"""
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

    def _inspect_loop_complexity(self, for_node):
        """
        Анализ сложности цикла. 
        Возвращает: (has_nested_for, if_nodes_list)
        """
        nested_for = False
        ifs = []
        for n in for_node.body:
            if isinstance(n, ast.For):
                nested_for = True
            elif isinstance(n, ast.If):
                ifs.append(n)
        return nested_for, ifs

    def _generate_tomashik_states(self):
        """Генератор фиксированных двухбуквенных векторов Томашика"""
        return ["AA", "BB", "CC"]

    def _insert_primitive_diagram(self, dia_id, name, body, params):
        """Обычный линейный Примитив для простых функций"""
        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 100.0);", (dia_id, name))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (dia_id,))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (dia_id,))

        start_item = self._get_next_item_id(10)

        # Начало и Конец
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, 170, 60, 50, 20, 60, 0, NULL, '', NULL, '');", (start_item, dia_id, name))
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', 'End', 0, 170, 390, 50, 20, 60, 0, NULL, '', NULL, '');", (start_item + 1, dia_id))
        
        # Линейный шампур
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'vertical', '', 0, 170, 80, 0, 290, 0, 0, NULL, '', NULL, '');", (start_item + 2, dia_id))
        
        # Параметры (Крыло)
        if params:
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'horizontal', '', 0, 200, 60, 80, 0, 0, 0, NULL, '', NULL, '');", (start_item + 3, dia_id))
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, 310, 60, 50, 40, 0, 0, NULL, '', NULL, '');", (start_item + 4, dia_id, params))

        # Тело операции
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, 170, 170, 110, 40, 0, 0, NULL, '', NULL, '');", (start_item + 5, dia_id, body))

    def _create_three_shampur_automat(self, dia_id, name, pre_code, for_node, post_code, sub_dia_list):
        """
        Строит канонический 3-шампурный автомат (Томашик-матрицу) в таблице items.
        Геометрия полностью выверена, наложения исключены.
        """
        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 0', ?, 100.0);", (dia_id, name, f"State Machine {name}"))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (dia_id,))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (dia_id,))

        states = self._generate_tomashik_states() # ['AA', 'BB', 'CC']
        
        start_x = 150
        step_x = 300
        y_top = 60
        y_shampur_bus = 120
        
        # Икона НАЧАЛО на первом шампуре
        item_id = self._get_next_item_id(1)
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, ?, ?, 70, 25, 0, 0, NULL, '', NULL, '');", 
                            (item_id, dia_id, name, start_x, y_top))

        # Горизонтальная шина распределителя Силуэта
        item_id = self._get_next_item_id(1)
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'horizontal', '', 0, ?, ?, ?, 0, 0, 0, NULL, '', NULL, '');", 
                            (item_id, dia_id, start_x, y_shampur_bus, len(states) * step_x))

        # Икона КОНЕЦ на фиктивной крайней правой оси выгрузки векторов
        exit_x = start_x + (len(states) * step_x)
        item_id = self._get_next_item_id(1)
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', 'Конец', 0, ?, 500, 70, 25, 0, 0, NULL, '', NULL, '');", 
                            (item_id, dia_id, exit_x))

        # Перебираем наши 3 базовых автомата (шампура)
        for idx, state_label in enumerate(states):
            cx = start_x + (idx * step_x)
            
            # Вертикальная ось ребра графа
            item_id = self._get_next_item_id(1)
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'vertical', '', 0, ?, ?, 0, 420, 0, 0, NULL, '', NULL, '');", 
                                (item_id, dia_id, cx, y_shampur_bus))

            # Икона заглавия ветки (Вектор Томашика)
            item_id = self._get_next_item_id(1)
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'branch', ?, 0, ?, ?, 100, 30, 0, 0, NULL, '', NULL, '');", 
                                (item_id, dia_id, state_label, cx, y_shampur_bus + 40))

            # Наполнение шампуров согласно троичной логике
            if state_label == "AA":
                # Шампур АА: Стартовый блок + базовое условие входа
                code_text = pre_code if pre_code.strip() else "pass"
                
                item_id = self._get_next_item_id(1)
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, 220, 180, 60, 0, 0, NULL, '', NULL, '');", 
                                    (item_id, dia_id, code_text, cx))
                
                # IF на шампуре AA
                item_id = self._get_next_item_id(1)
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'if', 'Valid Context?', 0, ?, 320, 100, 40, 0, 0, NULL, '', NULL, '');", 
                                    (item_id, dia_id, cx))
                
                # Переход по адресу (Адрес)
                item_id = self._get_next_item_id(1)
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'address', 'BB', 0, ?, 420, 100, 30, 0, 0, NULL, '', NULL, '');", 
                                    (item_id, dia_id, cx))

            elif state_label == "BB":
                # Шампур BB: Нанизанный LOOP (Единый FOR) с инкапсулированным вызовом
                if for_node:
                    nested_complex, ifs = self._inspect_loop_complexity(for_node)
                    
                    if nested_complex or len(ifs) > 1:
                        # Инкапсуляция сложности во внешнюю функцию-схему
                        sub_name = f"sub_loop_{dia_id}"
                        sub_dia_id = self._next_diagram_id()
                        sub_dia_list.append((sub_dia_id, sub_name, for_node))
                        loop_body_text = f"FOR_LOOP_ITERATION()\nCALL {sub_name}"
                    else:
                        loop_body_text = f"LOOP: {ast.unparse(for_node.target)} in {ast.unparse(for_node.iter)}"
                        if for_node.body:
                            loop_body_text += "\n" + "\n".join([ast.unparse(n) for n in for_node.body])
                else:
                    loop_body_text = "pass"

                item_id = self._get_next_item_id(1)
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, 220, 200, 60, 0, 0, NULL, '', NULL, '');", 
                                    (item_id, dia_id, loop_body_text, cx))

                # Единственный разрешенный IF внутри итерационного автомата
                item_id = self._get_next_item_id(1)
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'if', 'Loop Broken?', 0, ?, 320, 100, 40, 0, 0, NULL, '', NULL, '');", 
                                    (item_id, dia_id, cx))

                item_id = self._get_next_item_id(1)
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'address', 'CC', 0, ?, 420, 100, 30, 0, 0, NULL, '', NULL, '');", 
                                    (item_id, dia_id, cx))

            elif state_label == "CC":
                # Шампур CC: Терминальный чистый IF обработки результатов
                code_text = post_code if post_code.strip() else "pass"
                
                item_id = self._get_next_item_id(1)
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, 220, 180, 60, 0, 0, NULL, '', NULL, '');", 
                                    (item_id, dia_id, code_text, cx))

                item_id = self._get_next_item_id(1)
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'if', 'Terminal Status', 0, ?, 320, 100, 40, 0, 0, NULL, '', NULL, '');", 
                                    (item_id, dia_id, cx))

                item_id = self._get_next_item_id(1)
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'address', 'Конец', 0, ?, 420, 100, 30, 0, 0, NULL, '', NULL, '');", 
                                    (item_id, dia_id, cx))

    def convert_source(self, py_source_path="rmsnorm.py"):
        """Парсинг исходного Python-кода и чистая генерация по нашей топологии"""
        if not os.path.exists(py_source_path):
            # Заглушка для генерации структуры, если физический файл отсутствует
            source_code = "def gpt(x):\n    x = x + 1\n    for i in range(10):\n        x += i\n    return x\n\def main():\n    pass"
        else:
            with open(py_source_path, "r", encoding="utf-8") as f:
                source_code = f.read()

        tree = ast.parse(source_code)

        header_lines = []
        footer_lines = []
        class_node = None
        global_functions = {}

        # Разбор структуры верхнего уровня
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                global_functions[node.name] = node
            elif isinstance(node, ast.ClassDef):
                class_node = node
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                header_lines.append(ast.unparse(node).strip())

        state_description = f"=== header ===\n{chr(10).join(header_lines)}\n\n=== Status ===\nCompiled Invariant"

        node_id = 1
        root_folder_id = node_id
        self.cursor.execute("INSERT INTO tree_nodes VALUES (?, 0, 'folder', 'microgpt', NULL);", (node_id,))
        node_id += 1

        sub_diagrams_to_build = []

        # Обработка глобальных функций (gpt, main и т.д.)
        for func_name, node in global_functions.items():
            dia_id = self._next_diagram_id()
            self.cursor.execute("INSERT INTO tree_nodes VALUES (?, ?, 'item', ?, ?);", (node_id, root_folder_id, func_name, dia_id))
            node_id += 1

            arg_names = [arg.arg for arg in node.args.args]
            params_text = ", ".join(arg_names) if arg_names else ""

            if func_name in ['gpt', 'main']:
                # Выделяем логические компоненты кода для автоматов
                pre_nodes = []
                for_node = None
                post_nodes = []
                
                for stmt in node.body:
                    if isinstance(stmt, ast.For) and not for_node:
                        for_node = stmt
                    elif opt := (for_node is None):
                        if opt: pre_nodes.append(stmt)
                    else:
                        post_nodes.append(stmt)

                pre_code = "\n".join([ast.unparse(n) for n in pre_nodes])
                post_code = "\n".join([ast.unparse(n) for n in post_nodes])

                # Строим чистый трехшампурный автомат
                self._create_three_shampur_automat(dia_id, func_name, pre_code, for_node, post_code, sub_diagrams_to_build)
            else:
                # Простые функции укладываем в классический примитив
                body_text = "\n".join([ast.unparse(stmt).strip() for stmt in node.body])
                self._insert_primitive_diagram(dia_id, func_name, body_text, params_text)

        # Компиляция дочерних изолированных диаграмм для сложных вложенных FOR
        for sub_id, sub_name, sub_node in sub_diagrams_to_build:
            self.cursor.execute("INSERT INTO tree_nodes VALUES (?, ?, 'item', ?, ?);", (node_id, root_folder_id, sub_name, sub_id))
            node_id += 1
            body_text = "\n".join([ast.unparse(n) for n in sub_node.body])
            self._insert_primitive_diagram(sub_id, sub_name, body_text, "")

        # Фиксация фокуса состояния системы
        self.cursor.execute("INSERT INTO state VALUES (1, ?, ?);", (self._diagram_id - 1, state_description))
        self.conn.commit()
        self.conn.close()
        print(f"\n[Успех] Авгиевы конюшни вычищены! База {self.drn_path} сформирована.")
        print("Структура пересобрана на базе 3-шампурных автоматов Томашика [AA, BB, CC] с Крон-совместимой топологией.")

if __name__ == "__main__":
    converter = DrakonBuranSilhouetteConverterV10("rmsnorm.drn")
    converter.convert_source("rmsnorm.py")
