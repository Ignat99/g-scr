import ast
import sqlite3
import os
#import string


label_counter = 0
letters = "QWERTYUIOPASDFGHJKLZXCVBN"


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


    # === ID ГЕНЕРАЦИЯ ===
    def _next_diagram_id(self):
        val = self._diagram_id
        self._diagram_id += 1
        return val


    def _get_next_item_id(self, increment=1):
        val = self._item_id
        self._item_id += increment
        return val


    # === СБОР FOR ===
    def _collect_top_level_fors(self, node):
        result = []
        for n in ast.walk(node):
            if isinstance(n, ast.For):
                is_nested = False
                for parent in ast.walk(n):
                    if parent is not n and isinstance(parent, ast.For):
                        is_nested = True
                        break
                if not is_nested:
                    result.append(n)
        return result

    # === ГРУППИРОВКА ПО 3 ===
#    def _split_for_groups(self, for_nodes):
#        return [for_nodes[i:i+3] for i in range(0, len(for_nodes), 3)]

    # === ОСНОВНОЙ ПАРСЕР ===
    def _process_for_blocks(self, root):
        for_nodes = self._collect_top_level_fors(root)
        if not for_nodes:
            return

#        groups = self._split_for_groups(for_nodes)
#        silhouette_ids = []

#        for idx, group in enumerate(groups):
#            dia_id = self._next_diagram_id()
#            self._create_for_silhouette(dia_id, group, idx)
#            silhouette_ids.append(dia_id)

#        self._create_master_for_sequence(silhouette_ids)

    # === СИЛУЭТ ===
#    def _create_for_silhouette(self, dia_id, for_group, idx):
#        self.cursor.execute(
#            "INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 100.0);",
#            (dia_id, f"for_silhouette_{idx}")
#        )

#        print("============================================================================================")
#        for i, for_node in enumerate(for_group):
#            item_id = self._get_next_item_id()
#            code = ast.unparse(for_node)
#            print(code)
#            print("=====")

#            self.cursor.execute(
#                "INSERT INTO items VALUES (?, ?, ?, ?);",
#                (item_id, dia_id, f"FOR_{idx}_{i}", code)
#            )

    # === MASTER ===
#    def _create_master_for_sequence(self, silhouette_ids):
#        if not silhouette_ids:
#            return

#        dia_id = self._next_diagram_id()
#        self.cursor.execute(
#            "INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 100.0);",
#            (dia_id, "for_master_sequence")
#        )

#        for sid in silhouette_ids:
#            item_id = self._get_next_item_id()
#            self.cursor.execute(
#                "INSERT INTO items VALUES (?, ?, ?, ?);",
#                (item_id, dia_id, f"CALL_{sid}", f"CALL {sid}")
#            )



# =====================================================================================


        # === ДОБАВЛЕН ПАРСЕР ===
#        self.branch_label_map = {}
#        self._label_gen = self._label_generator()

    # === ДОБАВЛЕН ПАРСЕР ===
#    def _label_generator(self):
##        letters = string.ascii_uppercase
#        letters = "QWERTYUIOPASDFGHJKLZXCVBN"
#        for a in letters:
#            for b in letters:
#                yield a + b

    # === ДОБАВЛЕН ПАРСЕР ===
#    def _get_label(self, text):
#        label = next(self._label_gen)
#        self.branch_label_map[label] = text
#        return label


    # === ПАРСЕР ВЕТОК ===
#    def _parse_chunks(self, chunks):
#        parsed = []

#        for name, nodes in chunks:
#            code_text = "\n".join([ast.unparse(n).strip() for n in nodes])

            # замена имени на двухбуквенный маркер
#            label = self._get_label(name)

#            parsed.append((label, code_text))

#        return parsed


    # === ДЕТЕКЦИЯ СЛОЖНЫХ FOR ===
#    def _is_complex_loop(self, node):
#        if not isinstance(node, ast.For):
#            return False

        # вложенные for
#        for n in ast.walk(node):
#            if isinstance(n, ast.For) and n is not node:
#                return True

        # больше одного if
#        if_count = sum(isinstance(n, ast.If) for n in ast.walk(node))
#        return if_count > 1



# =====================================================================




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




    # =========================================================
    #  ВСТРОЕННЫЙ ПАРСЕР (ГЛАВНОЕ ДОБАВЛЕНИЕ)
    # =========================================================
    def _parse_into_branches(self, func_node):
#        label_counter = 0
        diagrams = []

        def next_label():
            global label_counter
            global letters
#            a = letters[label_counter // 26]
            a = letters[label_counter % len(letters)]
#            b = letters[label_counter % 25]
            label_counter += 1
#            return a + b
            return a

        branches = []

        # == 1. Collect code before for in one Active
        pre_block = []
        post_block = []
        for_nodes = []
        seen_for = []


        # == Split
        for node in func_node.body:
            # --- FOR → отдельная диаграмма ---
            if isinstance(node, ast.For):
#                rest_nodes.append(node)
                send_for = True
                for_nodes.append(node)
            else:
                if not seen_for:
                    pre_block.append(node)
                else:
                    post_block.append(node)

        # == 2. Befor For - one Active
        if pre_block:
            sh = next_label()
            branches.append((sh, "\n".join(ast.unparse(n) for n in pre_block)))


        # == 3. Work with For
        for node in func_node.body:

            # --- FOR → отдельная диаграмма ---
            if isinstance(node, ast.For):

                d_name = f"D{len(diagrams)+1}"

                sh_main = next_label()
                print(sh_main)
                sh_if = next_label()
                print(sh_if)
                sh_end = next_label()
                print(sh_end)

                has_if = any(isinstance(n, ast.If) for n in node.body)

                sub_blocks = {
#                    sh1: [],
 #                   sh2: [],
  #                  sh3: []
                }

                for_header = f"FOR {ast.unparse(node.target)} in {ast.unparse(node.iter)}"

                if not has_if:
                    # All for in one blok 
                    sub_blocks[sh_main] = [for_header] + [ast.unparse(n) for n in node.body] #or ["pass"]
                else:
                    # Separate by IF
                    sub_blocks[sh_main] = [for_header]
                    sub_blocks[sh_if] = []

                for n in node.body:
                    if isinstance(n, ast.If):
                        sub_blocks[sh_if].append(f"IF {ast.unparse(n.test)}")
                        for x in n.body:
                            sub_blocks[sh_if].append(ast.unparse(x))
                    else:
                        sub_blocks[sh_main].append(ast.unparse(n))

#                for k in sub_blocks:
 #                   if not sub_blocks[k]:
  #                      sub_blocks[k] = ["pass"]
   #             if not sub_blocks[sh1]:
    #                sub_blocks[sh1] = ["pass"]
     #           if not sub_blocks[sh2]:
      #              sub_blocks[sh2] = ["pass"]

                diagrams.append((d_name, sub_blocks))

                branches.append((f"{sh_main}_{sh_end}", f"{for_header}\nCALL {d_name}"))

            else:
                continue
#                sh1 = next_label()
 #               print(sh1)
  #              sh2 = next_label()
   #             print(sh2)
    #            branches.append((sh1, ast.unparse(node)))
        # == 4. After For - one Active
        if post_block:
            sh = next_label()
            branches.append((sh, "\n".join(ast.unparse(n) for n in post_block)))

        return branches, diagrams

    # =========================================================



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


    def next_label():
        global label_counter
        global letters
        a = letters[label_counter % len(letters)]
        label_counter += 1
        return a


    def _generate_tomashik_states(self):
        """Генератор фиксированных двухбуквенных векторов Томашика"""
        return [next_label(), next_label(), next_label()]


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

# =============================================================================================================


#        """Парсинг исходного Python-кода и чистая генерация по нашей топологии"""
#        if not os.path.exists(py_source_path):
#            # Заглушка для генерации структуры, если физический файл отсутствует
#            source_code = "def gpt(x):\n    x = x + 1\n    for i in range(10):\n        x += i\n    return x\n\def main():\n    pass"
#        else:
#            with open(py_source_path, "r", encoding="utf-8") as f:
#                source_code = f.read()

#        tree = ast.parse(source_code)

#        header_lines = []
#        footer_lines = []
#        class_node = None
#        global_functions = {}



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



        # Разбор структуры верхнего уровня
#        for node in ast.iter_child_nodes(tree):
#            if isinstance(node, ast.FunctionDef):
#                global_functions[node.name] = node
#            elif isinstance(node, ast.ClassDef):
#                class_node = node
#            elif isinstance(node, (ast.Import, ast.ImportFrom)):
#                header_lines.append(ast.unparse(node).strip())




        # Сбор метаданных и разбор AST верхнего уровня
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                global_functions[node.name] = node
            elif isinstance(node, ast.ClassDef):
                class_node = node
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                header_lines.append(ast.unparse(node).strip())
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and getattr(node.value.func, 'name', '') == 'main':
                footer_lines.append(ast.unparse(node).strip())


#        state_description = f"=== header ===\n{chr(10).join(header_lines)}\n\n=== Status ===\nCompiled Invariant"

#        node_id = 1
#        root_folder_id = node_id



        # Сбор шабанга и комментариев верхнего уровня
        raw_headers = []
        for line in source_lines:
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("import") or not stripped:
                if "Autogenerated" not in line:
                    raw_headers.append(line.rstrip())
            else:
                break
        header_text = "\n".join(raw_headers).strip()

        # Формирование блока === class ===
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

        # Инициализация счетчиков ID
        node_id = 1
        diagram_id = 1
        item_id = 1






        # 1. Создаем корневую папку проекта
        self.cursor.execute("INSERT INTO tree_nodes VALUES (?, 0, 'folder', 'microgpt', NULL);", (node_id,))
        root_folder_id = node_id
        node_id += 1

        sub_diagrams_to_build = []



        # 2. Обработка класса Value (если есть) и его методов
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



        # 3. Обработка глобальных функций (gpt, main и т.д.)
        for func_name, node in global_functions.items():
            dia_id = self._next_diagram_id()
            self.cursor.execute("INSERT INTO tree_nodes VALUES (?, ?, 'item', ?, ?);", (node_id, root_folder_id, func_name, diagram_id))
            node_id += 1

            arg_names = [arg.arg for arg in node.args.args]
            params_text = ", ".join(arg_names) if arg_names else ""



            # Проверяем «тяжесть» функции: gpt и main превращаем в Силуэты (шампуры)
            # Ignat:TODO It depend from source
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
#                self._create_three_shampur_automat(dia_id, func_name, pre_code, for_node, post_code, sub_diagrams_to_build)
#Ignat    Test version
                print("0 ===")
                print(item_id)
                self._insert_silhouette_diagram1(diagram_id, func_name, node, params_text, item_id)
# Ignat:TODO make counter for item_id
                item_id += 360 # Выделяем большой пул ID под сложную структуру
            else:
#Ignat    Test version
                # Обычные функции (rmsnorm, softmax, linear) делаем простым шампуром
                # Простые функции укладываем в классический примитив
                body_text = "\n".join([ast.unparse(stmt).strip() for stmt in node.body])
                print("1 ===")
                print(item_id)
#                self._insert_primitive_diagram(dia_id, func_name, body_text, params_text)
                self._insert_primitive_diagram(diagram_id, func_name, body_text, params_text, item_id)
                item_id += 10

            diagram_id += 1


        # Компиляция дочерних изолированных диаграмм для сложных вложенных FOR
        for sub_id, sub_name, sub_node in sub_diagrams_to_build:
            self.cursor.execute("INSERT INTO tree_nodes VALUES (?, ?, 'item', ?, ?);", (node_id, root_folder_id, sub_name, sub_id))
            node_id += 1
            body_text = "\n".join([ast.unparse(n) for n in sub_node.body])
            self._insert_primitive_diagram(sub_id, sub_name, body_text, "")


        # Фиксация фокуса состояния системы
#        self.cursor.execute("INSERT INTO state VALUES (1, ?, ?);", (self._diagram_id - 1, state_description))
#        self.conn.commit()
#        self.conn.close()

        # Фиксируем фокус на последней диаграмме
        self.cursor.execute("INSERT INTO state VALUES (1, ?, ?);", (diagram_id - 1, state_description))
        self.conn.commit()
        self.conn.close()
        print(f"\n[Успех] Авгиевы конюшни вычищены! База {self.drn_path} сформирована.")
        print("Структура пересобрана на базе 3-шампурных автоматов Томашика [A, B, C] с Крон-совместимой топологией.")
        print(f"[Успех] База {self.drn_path} успешно сгенерирована. Функции 'gpt' и 'main' разложены на силуэты.")

    def _insert_primitive_diagram(self, dia_id, name, body, params, item_start):
        print("2 ===")
        print(item_start)
        """Обычный линейный шампур (Примитив) для простых функций и методов"""
        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 100.0);", (dia_id, name))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (dia_id,))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (dia_id,))

        # Иконы начала и конца
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, 170, 60, 50, 20, 60, 0, NULL, '', NULL, '');", (item_start, dia_id, name))
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', 'End', 0, 170, 390, 50, 20, 60, 0, NULL, '', NULL, '');", (item_start + 1, dia_id))
        
        # Шампур (вертикальная связь)
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'vertical', '', 0, 170, 80, 0, 290, 0, 0, NULL, '', NULL, '');", (item_start + 2, dia_id))
        
        # Выносное крыло параметров
        if params:
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'horizontal', '', 0, 200, 60, 80, 0, 0, 0, NULL, '', NULL, '');", (item_start + 3, dia_id))
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, 310, 60, 50, 40, 0, 0, NULL, '', NULL, '');", (item_start + 4, dia_id, params))

        # Тело функции (Икона Процесс)
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, 170, 170, 110, 40, 0, 0, NULL, '', NULL, '');", (item_start + 5, dia_id, body))



    # =========================================================
    #  МОДИФИЦИРОВАННЫЙ СИЛУЭТ
    # =========================================================
    def _insert_silhouette_diagram2(self, dia_id, name, func_node, params, item_start):

        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 0', ?, 100.0);",
                            (dia_id, name, f"auto silhouette {name}"))

        branches, sub_diagrams = self._parse_into_branches(func_node)

        start_x = 150
        step_x = 300
        y = 100

        # Начало
        self.cursor.execute(
            "INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, ?, ?, 60, 20, 0, 0, NULL, '', NULL, '');",
            (item_start, dia_id, name, start_x, y)
        )
        item_start += 1

        for idx, (b_name, b_code) in enumerate(branches):

            cx = start_x + idx * step_x

            # шампур
            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, 'vertical', '', 0, ?, ?, 0, 300, 0, 0, NULL, '', NULL, '');",
                (item_start, dia_id, cx, y)
            )
            item_start += 1

            # branch
            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, 'branch', ?, 0, ?, ?, 120, 30, 0, 0, NULL, '', NULL, '');",
                (item_start, dia_id, b_name, cx, y + 40)
            )
            item_start += 1

            # action
            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 180, 60, 0, 0, NULL, '', NULL, '');",
                (item_start, dia_id, b_code, cx, y + 100)
            )
            item_start += 1

        # =========================================================
        #  ПОДДИАГРАММЫ
        # =========================================================
        for d_name, shampurs in sub_diagrams:

            dia_id += 1

            self.cursor.execute(
                "INSERT INTO diagrams VALUES (?, ?, '0 0', ?, 100.0);",
                (dia_id, d_name, "sub")
            )

            x = 150
            y = 100

            for sh, lines in shampurs.items():

                self.cursor.execute(
                    "INSERT INTO items VALUES (?, ?, 'branch', ?, 0, ?, ?, 120, 30, 0, 0, NULL, '', NULL, '');",
                    (item_start, dia_id, sh, x, y)
                )
                item_start += 1

                for line in lines:
                    y += 50
                    self.cursor.execute(
                        "INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 180, 40, 0, 0, NULL, '', NULL, '');",
                        (item_start, dia_id, line, x, y)
                    )
                    item_start += 1

                x += 250
                y = 100




# ================================================================



    def _insert_silhouette_diagram1(self, dia_id, name, func_node, params, item_start):

        """Генератор канонического многошампурного Силуэта ДРАКОН для gpt() и main()"""
        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 0', ?, 100.0);", (dia_id, name, f"auto silhouette {name}"))

#        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '-40 14', ?, 100.0);", (dia_id, name, f"Силуэт-карта функции {name}"))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (dia_id,))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (dia_id,))



        # 1. Разбиваем тело функции на логические куски для шампуров
        branches = []


        if name == 'gpt':
            # Логическое разделение для gpt()
            chunks = [
                ("Инициализация эмбеддингов", func_node.body[0:5]),
                ("Цикл по слоям нейросети", [func_node.body[5]]), # Сам For
                ("Вычисление Logits", func_node.body[6:])
            ]
        else:
            # Логическое разделение для main()
            chunks = [
                ("Подготовка данных и окружения", func_node.body[0:10]),
                ("Конфигурация сети и Adam", func_node.body[10:19]),
                ("Цикл оптимизации (Training)", [func_node.body[19]]),
                ("Генерация текста (Inference)", func_node.body[20:])
            ]



        # === ВСТАВКА ПАРСЕРА ===
#        branches = self._parse_chunks(chunks)
        # === ВСТАВКА ПАРСЕРА ===
        branches, sub_diagrams = self._parse_into_branches(func_node)
        print(branches)
        print("====Diagrams===")
        print(sub_diagrams)
        self._process_for_blocks(func_node)





        # Преобразуем блоки AST в текстовый код для икон
#        for b_name, nodes in chunks:
#            code_text = "\n".join([ast.unparse(n).strip() for n in nodes])
#            branches.append((b_name, code_text))

        num_branches = len(branches)
        print("num_branches")
        print(num_branches)
        
        # Координационная сетка Силуэта
        start_x = 150
        step_x = 350
        y_header = 60
        y_branch_line = 120
        y_nodes_start = 220

        # Главная икона Начало (всегда на 1-м шампуре)
#        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, ?, ?, 60, 20, 0, 0, NULL, '', NULL, '');", 
#                            (item_start, dia_id, name, start_x, y_header))
#        self.cursor.execute("INSERT INTO items                                                                                                VALUES (?, ?, 'beginend', ?, 0, 170, 60, 50, 20, 60, 0, NULL, '', NULL, '');", (item_start, dia_id, name))
        self.cursor.execute("INSERT INTO items (item_id, diagram_id, type, text, selected, x, y, w, h, a, b, aux_value, color, format, text2) VALUES (?, ?, 'beginend', ?, 0,   ?,  ?, 60, 20,  0, 0, NULL, '', NULL, '');", 
                            (item_start, dia_id, name, start_x, y_header))
        item_start += 1

        # Конечная точка Силуэта (находится на самом правом невидимом шампуре выхода)
        exit_x = start_x + (num_branches * step_x)
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'beginend', 'Конец', 0, ?, ?, 50, 20, 0, 0, NULL, '', NULL, '');", 
                            (item_start, dia_id, exit_x, y_nodes_start + 150))
        item_start += 1

        # Горизонтальная шина Силуэта (главный распределитель)
        self.cursor.execute("INSERT INTO items VALUES (?, ?, 'horizontal', '', 0, ?, ?, ?, 0, 0, 0, NULL, '', NULL, '');", 
                            (item_start, dia_id, start_x, y_branch_line, num_branches * step_x))
        item_start += 1

        # Вынос параметров (если есть)
        if params:
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'horizontal', '', 0, ?, ?, 80, 0, 0, 0, NULL, '', NULL, '');", (item_start, dia_id, start_x + 40, y_header))
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 80, 30, 0, 0, NULL, '', NULL, '');", (item_start + 1, dia_id, params, start_x + 160, y_header))
            item_start += 2











        # 2. Строим структуру шампуров
        for idx, (b_name, b_code) in enumerate(branches):
            cx = start_x + (idx * step_x)
            
            # Вертикальный шампур
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'vertical', '', 0, ?, ?, 0, 400, 0, 0, NULL, '', NULL, '');", 
                                (item_start, dia_id, cx, y_branch_line))
            item_start += 1

            # Икона «Ветка» (Заголовок шампура)
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'branch', ?, 0, ?, ?, 140, 30, 0, 0, NULL, '', NULL, '');", 
                                (item_start, dia_id, b_name, cx, y_branch_line + 40))
            item_start += 1

            # Икона «Процесс» с распарсенным телом кода на этом шампуре
            self.cursor.execute("INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 180, 80, 0, 0, NULL, '', NULL, '');", 
                                (item_start, dia_id, b_code, cx, y_nodes_start + 60))
            item_start += 1

            # Икона «Адрес» (Указатель куда идти дальше)
            if idx < num_branches - 1:
                next_branch_name = branches[idx + 1][0]
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'address', ?, 0, ?, ?, 140, 30, 0, 0, NULL, '', NULL, '');", 
                                    (item_start, dia_id, next_branch_name, cx, y_nodes_start + 200))
            else:
                # Последний шампур передает управление на «Конец»
                self.cursor.execute("INSERT INTO items VALUES (?, ?, 'address', 'Конец', 0, ?, ?, 140, 30, 0, 0, NULL, '', NULL, '');", 
                                    (item_start, dia_id, cx, y_nodes_start + 200))
            item_start += 1



if __name__ == "__main__":
    converter = DrakonBuranSilhouetteConverterV10("rmsnorm.drn")
    converter.convert_source("rmsnorm.py")






# ========================================================================================
# =======================================================================================
# =========================================================================================


