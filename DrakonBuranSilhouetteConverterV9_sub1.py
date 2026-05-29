def _create_sub_diagram(self, d_name, shampurs, item_start):
        """
        Создает изолированную поддиаграмму (Примитив) для простых функций и методов.
        Строки без 'For' группируются в укрупненные блоки Action. Строки с 'For' 
        выделяются в индивидуальные блоки Action.
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
            
            # Буфер для накопления линейных строк кода текущего блока
            current_block = []
            
            # Внутренняя функция для сброса накопленного буфера в базу
            def flush_current_block(block_lines, current_y, current_item_id):
                if block_lines:
                    # Объединяем накопленные строки в один многострочный текст
                    combined_text = "\n".join(block_lines)
                    self.cursor.execute(
                        "INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 180, 40, 0, 0, NULL, '', NULL, '');",
                        (current_item_id, dia_id, combined_text, x, current_y)
                    )
                    current_item_id += 1
                    current_y += 100
                return current_y, current_item_id

            for line in lines:
                # Проверяем наличие управляющего слова 'For' в строке
                if "For " in line or "for " in line:
                    # 1. Перед записью For сбрасываем все, что накопили до него
                    y, item_start = flush_current_block(current_block, y, item_start)
                    current_block = []
                    
                    # 2. Записываем сам For в отдельную изолированную икону
                    self.cursor.execute(
                        "INSERT INTO items VALUES (?, ?, 'action', ?, 0, ?, ?, 180, 40, 0, 0, NULL, '', NULL, '');",
                        (item_start, dia_id, line, x, y)
                    )
                    item_start += 1
                    y += 100
                else:
                    # Обычная линейная строка — накапливаем в буфер
                    current_block.append(line)
            
            # Сбрасываем оставшийся хвост линейного кода в конце шампура (если он есть)
            y, item_start = flush_current_block(current_block, y, item_start)
                
            # Сдвиг оси X для следующего шампура (инвариантный шаг сетки)
            x += 250
            
        return dia_id, item_start
        
