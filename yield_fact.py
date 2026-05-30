# База данных фактов (Пространство параметров)
# Допустим, у нас есть несколько вариантов технологических стандартов сетки
GEOMETRY_FACTS = [
    # (cx, w_all, h_be, h_act, h_dop, y_begin)
    (170, 110, 20, 100, 50, 60),  # Стандарт 1
    (200, 150, 30, 120, 60, 80)   # Стандарт 2 (более разреженный)
]

def primitive_geometry_fact():
    """Генератор-фактов (Поставляет альтернативы для перебора)"""
    for fact in GEOMETRY_FACTS:
        yield fact

def layout_primitive_rule(target_h_vert=None):
    """
    Декларативное правило. Ищет в пространстве фактов комбинацию, 
    удовлетворяющую топологическим ограничениям.
    """
    for cx, w_all, h_be, h_act, h_dop, y_begin in primitive_geometry_fact():
        # Математические зависимости топологии
        y_action = y_begin + h_be + h_dop
        y_end = y_action + h_act + h_dop
        y_vert = y_begin + h_be
        h_vert = y_end - y_vert
        
        # Защитное ограничение (Унификация / Фильтрация решения)
        # Если при запросе мы ищем конкретную высоту шампура, проверяем её
        if target_h_vert is not None and h_vert != target_h_vert:
            continue # Бэктрекинг: это решение не подошло, переходим к следующему факту
            
        # Если все ограничения выполнены, лениво отдаем сгенерированную топологию
        yield {
            'cx': cx, 'w_all': w_all, 'h_be': h_be, 
            'y_action': y_action, 'y_end': y_end, 
            'y_vert': y_vert, 'h_vert': h_vert
        }

# --- Использование (Query) ---

# Пример А: Хотим просто рассчитать все доступные варианты геометрии
print("Все варианты топологии:")
for solution in layout_primitive_rule():
    print(solution)

# Пример Б: Задаем жесткое целевое ограничение (Ищем схему, где чистая высота связи равна ровно 200)
print("\nПоиск схемы с высотой шампура 200:")
for solution in layout_primitive_rule(target_h_vert=200):
    print(f"Найдено! Координата оси X: {solution['cx']}, Старт Y: {solution['y_vert']}")