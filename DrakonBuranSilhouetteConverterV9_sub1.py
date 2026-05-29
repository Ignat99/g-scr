def _create_sub_diagram(self, d_name, shampurs, item_start):
        """
        Создает изолированную поддиаграмму (Примитив) для простых функций и методов.
        Возвращает кортеж (dia_id, item_start) для сохранения сквозной нумерации объектов.
        """
        dia_id = self._next_dia_id()
        
        print("4 subdiagram 2 ===")
        print(dia_id, "   ", d_name)
        
        # Инициализация параметров листа в реляционной структуре
        self.cursor.execute("INSERT INTO diagrams VALUES (?, ?, '0 250', ?, 100.0);", (dia_id, d_name, "sub"))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (dia_id,))
        self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (dia_id,))
        
        # Топологические координаты осей (фиксированная инвариантная сетка)
        x = 150
        
        for sh, lines in shampurs.items():
            y = 100
            # Икона начала ветки (заголовок шампура)
            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, 'branch', ?, 0, ?, ?, 120, 30, 0, 0, NULL, '', NULL, '');",
                (item_start, dia_id, sh, x, y)
            )
            item_start += 1
            
            # Последовательное линейное заполнение иконами действий
            for line in lines:
                y += 100
                self.cursor.execute(
                    "INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 180, 40, 0, 0, NULL, '', NULL, '');",
                    (item_start, dia_id, line, x, y)
                )
                item_start += 1
                
            # Сдвиг оси X для следующего шампура (инвариантный шаг сетки)
            x += 250
            
        return dia_id, item_start