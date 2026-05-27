self.cursor.execute(
    "INSERT INTO items (item_id, diagram_id, type, text, selected, x, y, w, h, a, b, aux_value, color, format, text2) "
    "VALUES (?, ?, 'vertical', '', 0, ?, ?, 0, ?, 0, 0, NULL, '', NULL, '');",
    (item_start, dia_id, exit_x, y_bottom_bus, 60)
)
item_start += 1