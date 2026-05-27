# Поместить в метод _insert_silhouette_diagram1, ориентировочно после цикла отрисовки веток
self.cursor.execute(
    "INSERT INTO items (item_id, diagram_id, type, text, selected, x, y, w, h, a, b, aux_value, color, format, text2) "
    "VALUES (?, ?, 'horizontal', '', 0, ?, ?, ?, 0, 0, 0, NULL, '', NULL, '');",
    (item_start, dia_id, start_x, y_bottom_bus, num_branches * step_x)
)
item_start += 1