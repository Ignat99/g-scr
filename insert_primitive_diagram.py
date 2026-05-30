def _insert_primitive_diagram(self, dia_id, name, body, params, item_start):
        """Обычный линейный шампур (Примитив) для простых функций и методов"""
        print("4 primitive diagram   ===")
        print(dia_id, " ", name)

        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 100.0);", (dia_id, name))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (dia_id,))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (dia_id,))

        # --- Входные геометрические параметры и инварианты сетки ---
        cx = 170       # Единая координата X (ось симметрии шампура)
        w_all = 110    # Единая ширина для всех икон (beginend и action)
        h_be = 20      # Высота икон начала и конца
        h_act = 100    # Высота иконы действия/процесса
        h_dop = 50     # Вертикальный технологический зазор между краями икон

        # --- Расчет вертикальных координат по цепочке сверху вниз ---
        # 1. Икона Начала
        y_begin = 60
        
        # 2. Икона Тела функции (Действие)
        y_action = y_begin + h_be + h_dop  # 60 + 20 + 50 = 130
        
        # 3. Икона Конца
        y_end = y_action + h_act + h_dop   # 130 + 100 + 50 = 280
        
        # 4. Вертикальный шампур (линия связи от низа Начала до верха Конца)
        y_vert = y_begin + h_be            # Точка старта линии (80)
        h_vert = y_end - y_vert            # Чистая длина линии (280 - 80 = 200)

        # --- Запись элементов в реляционную базу ---
        
        # Иконы начала и конца (параметр 'a' равен 0, так как ширина теперь фиксирована)
        self.cursor.execute(
            "INSERT INTO items VALUES (?, ?, 'beginend', ?, 0, ?, ?, ?, ?, 0, 0, NULL, '', NULL, '');", 
            (item_start, dia_id, name, cx, y_begin, w_all, h_be)
        )
        self.cursor.execute(
            "INSERT INTO items VALUES (?, ?, 'beginend', 'End', 0, ?, ?, ?, ?, 0, 0, NULL, '', NULL, '');", 
            (item_start + 1, dia_id, cx, y_end, w_all, h_be)
        )
        
        # Шампур (вертикальная связь)
        self.cursor.execute(
            "INSERT INTO items VALUES (?, ?, 'vertical', '', 0, ?, ?, 0, ?, 0, 0, NULL, '', NULL, '');", 
            (item_start + 2, dia_id, cx, y_vert, h_vert)
        )
        
        # Выносное крыло параметров (если они переданы в функцию)
        if params:
            # Горизонтальная линия связи отходит вправо от оси шампура
            x_hor_start = cx + 30
            w_hor_line = 80
            
            # Блок параметров смещается на правый край линии
            x_param_box = cx + 140  # 170 + 140 = 310
            
            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, 'horizontal', '', 0, ?, ?, ?, 0, 0, 0, NULL, '', NULL, '');", 
                (item_start + 3, dia_id, x_hor_start, y_begin, w_hor_line)
            )
            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 50, 40, 0, 0, NULL, '', NULL, '');", 
                (item_start + 4, dia_id, params, x_param_box, y_begin)
            )

        # Тело функции (Икона Процесс)
        self.cursor.execute(
            "INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, ?, ?, 0, 0, NULL, '', NULL, '');", 
            (item_start + 5, dia_id, body, cx, y_action, w_all, h_act)
        )