# Данную конструкцию нужно будет вставить внутрь цикла 'for idx, (b_name, b_code) in enumerate(branches):'
# Она создает горизонтальную стрелку от текущего шампура cx к следующему cx + step_x
if idx < num_branches - 1:
    self.cursor.execute(
        "INSERT INTO items (item_id, diagram_id, type, text, selected, x, y, w, h, a, b, aux_value, color, format, text2) "
        "VALUES (?, ?, 'arrow', '', 0, ?, ?, ?, 0, 0, 0, NULL, '', NULL, '');",
        (item_start, dia_id, cx, y_nodes_start + 200, step_x) # на уровне иконы Адрес
    )
    item_start += 1