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

        functions = [node for node in ast.iter_child_nodes(tree) if isinstance(node, ast.FunctionDef)]
        total_functions = len(functions)


        # Diagram index
        diagram_id = 1

        # Root folder of project
        self.cursor.execute("INSERT INTO tree_nodes VALUES (1, 0, 'folder', 'microgpt',  NULL);")
        # Diagram index iside tree
        diagram_tree_id = 2
        # Item index
        item_id = 1


        for idx, node in enumerate(functions):
#            diagram_id = idx + 1

            func_name = node.name
            print(f"func_name: {func_name}")
            print(f"diagram_id: {diagram_id}")


            # Извлекаем имена аргументов функции через AST
            # Для def rmsnorm(x) это даст список ['x']
            arg_names = [arg.arg for arg in node.args.args]
            params_text = ", ".join(arg_names) if arg_names else ""

            # Извлечение тела функции
            body_lines = [ast.unparse(stmt).strip() for stmt in node.body]
            function_body_text = "\n".join(body_lines)


            # Регистрация листа в системном дереве
            self.cursor.execute("INSERT INTO tree_nodes (node_id, parent, type, name, diagram_id) VALUES (?, 1, 'item', ?, ?);", (diagram_tree_id, func_name, diagram_id,))
            # Запись метаданных холста диаграммы
            self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 120.0);", (diagram_id, func_name,))
            self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (diagram_id,))
            self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (diagram_id,))

            # Дифференцированная геометрия и метаданные листов (Лист 1 vs Лист 2+)
            if idx == 0:
                # Первый лист (Каноническая сетка)
                origin_coords = "0 250"
                selected_flag = 1
                # Центральная ось шампура
                center_x = 500
                y_begin = 420
                y_action = 550
                y_end = 750
                
                # Координаты выносного крыла параметров
                bridge_x = 530
                bridge_w = 140
                param_x = 690
            else:
                # Второй и последующие листы (Смещенная сетка в левый верхний угол)
                origin_coords = "-41 -82"
                selected_flag = 0
                center_x = 170
                y_begin = 20
                y_action = 150
                y_end = 350
                
                # Координаты выносного крыла параметров
                bridge_x = 200
                bridge_w = 140
                param_x = 360





            # Икона Начало
            self.cursor.execute("""
                INSERT INTO items VALUES (?, ?, 'beginend', ?, ?, ?, ?, 50, 20, 60, 0, NULL, '', NULL, '');
            """, (item_id, diagram_id, func_name, selected_flag, center_x, y_begin))
            item_id += 1


            # Икона Конец
            self.cursor.execute("""
                INSERT INTO items VALUES (?, ?, 'beginend', 'Конец', ?, ?, ?, 50, 20, 60, 0, NULL, '', NULL, '');
            """, (item_id, diagram_id, selected_flag, center_x, y_end))
            item_id += 1


            # Икона Процесс (Код тела функции)
            self.cursor.execute("""
                INSERT INTO items VALUES (?, ?, 'action', ?, ?, ?, ?, 170, 40, 0, 0, NULL, '', NULL, '');
            """, (item_id, diagram_id, function_body_text, selected_flag, center_x, y_action))
            item_id += 1


            # Вертикальный шампур (длина h=340 неизменна, связывает y_begin и y_end)
            self.cursor.execute("""
                INSERT INTO items VALUES (?, ?, 'vertical', '', ?, ?, ?, 0, 340, 0, 0, NULL, NULL, NULL, NULL);
            """, (item_id, diagram_id, selected_flag, center_x, y_begin))
            item_id += 1



            # Если у функции обнаружены аргументы, строим выносное правое крыло параметров
            # Выносное крыло формальных параметров
            if params_text:
                # Элемент 8: Горизонтальный мост связи (тип 'horizontal', x=530, y=420, w=140)
                # Горизонтальный мост
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'horizontal', '', ?, ?, ?, ?, 0, 0, 0, NULL, NULL, NULL, NULL);
                """, (item_id, diagram_id, selected_flag, bridge_x, y_begin, bridge_w))
                item_id += 1
                
                # Элемент 9: Выносная икона параметров (тип 'action', x=690, y=420, текст — имена аргументов)
                # Ставим selected=1 (или 0), color=None, format=None согласно оригинальному диффу
                # Икона параметров (тип 'action' по канону drakon_qt)
                # Обратите внимание: для второй диаграммы selected=0 по вашему диффу
                self.cursor.execute("""
                    INSERT INTO items VALUES (?, ?, 'action', ?, ?, ?, ?, 50, 20, 0, 0, NULL, NULL, NULL, NULL);
                """, (item_id, diagram_id, params_text, selected_flag if idx == 0 else 0, param_x, y_begin))
                item_id += 1




            diagram_id += 1
            diagram_tree_id += 1

        #Last diagram id without last increment
#        self.cursor.execute("INSERT INTO state VALUES (1, ?, NULL);", (diagram_id-1,))


        # Фиксируем глобальный фокус на последней созданной диаграмме (Лист 2, current_dia = total_functions)
        active_dia = total_functions if total_functions > 0 else 1
        self.cursor.execute("INSERT INTO state VALUES (1, ?, NULL);", (active_dia,))
        self.conn.commit()
        self.conn.close()
        print(f"[Выполнение] Скрипт py2drn6.py детерминированно собрал схему с выносными параметрами '{params_text}'.")
        print(f"[Успех] Скрипт py2drn7.py развернул {total_functions} функций по независимым листам Римановой поверхности.")



if __name__ == "__main__":
    converter = DrakonParamsConverterV6("rmsnorm.drn")
    converter.convert_with_formal_params("rmsnorm.py")

