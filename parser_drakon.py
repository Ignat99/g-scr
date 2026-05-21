def parse_drakon_primitives(primitives):
    # Словари для классификации элементов
    icons = {}
    verticals = []
    horizontals = []
    branches = {}  # Имя ветки -> координата X
    
    # Шаг 1: Первичная сортировка и фильтрация мусора
    for p in primitives:
        p_id, _, p_type, p_text, _, x, y, w, h, _, _, _, _, _, _ = p
        
        if p_type in ['beginend', 'branch', 'action', 'select', 'case', 'if', 'loopstart', 'loopend', 'address']:
            icons[p_id] = {
                'id': p_id, 'type': p_type, 'text': p_text,
                'x': x, 'y': y, 'w': w, 'h': h,
                'next': None, 'branches': {} # для select и if
            }
            if p_type == 'branch':
                branches[p_text] = x
        elif p_type == 'vertical':
            verticals.append({'id': p_id, 'x': x, 'y': y, 'w': w, 'h': h})
        elif p_type == 'horizontal':
            horizontals.append({'id': p_id, 'x': x, 'y': y, 'w': w, 'h': h})

    # Находим координаты всех вертикальных осей (Шампуров) на основе заголовков веток
    shampurs_x = sorted(list(set([icon['x'] for icon in icons.values() if icon['type'] in ['branch', 'beginend']])))
    
    # Вспомогательная функция определения, к какому шампуру принадлежит координата X
    def get_shampur_x(x_coord):
        return min(shampurs_x, key=lambda s_x: abs(s_x - x_coord))

    # Шаг 2: Распределяем иконы по их родным Шампурам
    shampurs = {sx: [] for sx in shampurs_x}
    for icon in icons.values():
        sx = get_shampur_x(icon['x'])
        # Для 'case' и 'action', смещенных вправо, мы позже сделаем привязку, 
        # но базово упорядочиваем по их фактической вертикальной оси
        shampurs[sx].append(icon)
        
    # Сортируем иконы на каждом шампуре строго СВЕРХУ ВНИЗ по Y
    for sx in shampurs_x:
        shampurs[sx].sort(key=lambda item: item['y'])

    # Шаг 3: Линейная прошивка (Связывание последовательных элементов)
    for sx in shampurs_x:
        chain = shampurs[sx]
        for i in range(len(chain) - 1):
            curr_node = chain[i]
            next_node = chain[i+1]
            
            # Если текущий узел — терминальный адрес, у него нет линейного следующего на этом шампуре
            if curr_node['type'] == 'address':
                continue
                
            # Проверяем, есть ли физический разрыв связи (например, ветвление)
            # Если между ними есть вертикальная линия — связь прямая
            curr_node['next'] = next_node['id']

    # Шаг 4: Сборка структуры SWITCH-CASE (для икон 'select')
    for icon in icons.values():
        if icon['type'] == 'select':
            # Ищем горизонтальную шину выбора прямо под select
            bus = None
            for h in horizontals:
                if abs(h['y'] - (icon['y'] + 40)) <= 20 and h['x'] <= icon['x']:
                    bus = h
                    break
            
            if bus:
                # Находим все 'case', которые сидят на этой шине
                bus_end_x = bus['x'] + bus['w']
                for case_icon in icons.values():
                    if case_icon['type'] == 'case' and abs(case_icon['y'] - (bus['y'] + 40)) <= 30:
                        if bus['x'] <= case_icon['x'] <= bus_end_x:
                            icon['branches'][case_icon['text']] = case_icon['id']

    # Шаг 5: Сборка условных операторов IF (развилок)
    for icon in icons.values():
        if icon['type'] == 'if':
            # Находим, куда уходит правая ветка (обычно по горизонтальной линии)
            right_branch_y = icon['y']
            for h in horizontals:
                if abs(h['y'] - right_branch_y) <= 10 and abs(h['x'] - icon['x']) <= 20:
                    # Нашли горизонтальный вынос вправо
                    target_x = h['x'] + h['w']
                    # Ищем элемент, который стоит на этой координате X ниже по Y
                    for target_icon in icons.values():
                        if abs(target_icon['x'] - target_x) <= 20 and target_icon['y'] > icon['y']:
                            icon['branches']['Yes'] = target_icon['id']
                            break

    # Финальная сборка высокоуровневого дерева Силуэта
    silhouette_graph = {}
    for sx in shampurs_x:
        branch_icon = next((item for item in shampurs[sx] if item['type'] in ['branch', 'beginend']), None)
        if branch_icon:
            name = branch_icon['text']
            silhouette_graph[name] = {
                'shampur_x': sx,
                'entry_node_id': branch_icon['id'],
                'nodes': {node['id']: node for node in shampurs[sx]}
            }

    return silhouette_graph, branches

# --- ТОЧКА ЗАПУСКА И ТЕСТИРОВАНИЕ НА ВАШЕМ МАССИВЕ ДАННЫХ ---
if __name__ == "__main__":
    raw_data = [
        (122, 8, 'beginend', 'quick_sort', 0, 110, 60, 50, 20, 0, 0, None, '', None, ''),
        (123, 8, 'beginend', 'End', 0, 2220, 510, 50, 20, 0, 0, None, '', None, ''),
        (124, 8, 'vertical', '', 0, 110, 80, 0, 710, 0, 0, None, '', None, ''),
        (125, 8, 'vertical', '', 0, 780, 120, 0, 670, 0, 0, None, '', None, ''),
        (126, 8, 'vertical', '', 0, 2220, 120, 0, 380, 0, 0, None, '', None, ''),
        (127, 8, 'horizontal', '', 0, 110, 120, 2110, 0, 0, 0, None, '', None, ''),
        (128, 8, 'arrow', '', 0, -20, 120, 130, 670, 1930, 1, None, '', None, ''),
        (129, 8, 'branch', 'analyze input', 0, 110, 170, 110, 30, 0, 0, None, '', None, ''),
        (130, 8, 'address', 'exit', 0, 110, 750, 110, 30, 0, 0, None, '', None, ''),
        (131, 8, 'branch', 'simple case', 0, 780, 170, 150, 30, 0, 0, None, '', None, ''),
        (132, 8, 'branch', 'partition', 0, 1450, 170, 160, 30, 0, 0, None, '', None, ''),
        (133, 8, 'address', 'exit', 0, 780, 750, 150, 30, 0, 0, None, '', None, ''),
        (134, 8, 'horizontal', '', 0, 150, 60, 120, 0, 0, 0, None, '', None, ''),
        (135, 8, 'action', '#method\n\nself\ncollection', 0, 310, 60, 50, 50, 0, 0, None, '', None, ''),
        (136, 8, 'action', 'length = len(collection)', 0, 110, 270, 110, 20, 0, 0, None, '', None, ''),
        (137, 8, 'select', 'length', 0, 110, 380, 110, 20, 0, 0, None, '', None, ''),
        (138, 8, 'case', '0', 0, 110, 460, 110, 20, 0, 0, None, '', None, ''),
        (139, 8, 'case', '1', 0, 280, 460, 50, 20, 60, 0, None, '', None, ''),
        (140, 8, 'case', '2', 0, 400, 460, 60, 20, 0, 0, None, '', None, ''),
        (141, 8, 'branch', 'exit', 0, 2220, 170, 70, 30, 0, 0, None, '', None, ''),
        (142, 8, 'horizontal', '', 0, 110, 420, 410, 0, 0, 0, None, '', None, ''),
        (143, 8, 'case', '', 0, 520, 460, 50, 20, 60, 0, None, '', None, ''),
        (144, 8, 'vertical', '', 0, 280, 420, 0, 80, 0, 0, None, '', None, ''),
        (145, 8, 'vertical', '', 0, 520, 420, 0, 370, 0, 0, None, '', None, ''),
        (146, 8, 'vertical', '', 0, 400, 420, 0, 370, 0, 0, None, '', None, ''),
        (147, 8, 'horizontal', '', 0, 110, 500, 170, 0, 0, 0, None, '', None, ''),
        (148, 8, 'action', 'result = collection', 0, 110, 610, 110, 20, 0, 0, None, '', None, ''),
        (149, 8, 'address', 'simple case', 0, 400, 750, 60, 30, 0, 0, None, '', None, ''),
        (150, 8, 'vertical', '', 0, 1450, 120, 0, 670, 0, 0, None, '', None, ''),
        (151, 8, 'address', 'recurse', 0, 1450, 750, 160, 30, 0, 0, None, '', None, ''),
        (152, 8, 'address', 'partition', 0, 520, 750, 50, 30, 60, 0, None, '', None, ''),
        (153, 8, 'action', 'first = collection[0]\nsecond = collection[1]', 0, 780, 290, 150, 30, 0, 0, None, '', None, ''),
        (154, 8, 'if', 'self.comparer(first, second) < 0', 0, 780, 360, 150, 20, 140, 1, None, '', None, ''),
        (155, 8, 'action', 'result = [ second, first ]', 0, 1070, 610, 120, 20, 0, 0, None, '', None, ''),
        (156, 8, 'vertical', '', 0, 1070, 360, 0, 300, 0, 0, None, '', None, ''),
        (157, 8, 'horizontal', '', 0, 780, 660, 290, 0, 0, 0, None, '', None, ''),
        (158, 8, 'action', 'half = int(length / 2)\nmedian = collection[half]\nleft = []\nright = []', 0, 1450, 270, 160, 50, 0, 0, None, '', None, ''),
        (159, 8, 'loopstart', 'i = 0; i < length; i += 1', 0, 1450, 360, 160, 20, 0, 0, None, '', None, ''),
        (160, 8, 'loopend', '', 0, 1450, 690, 160, 20, 0, 0, None, '', None, ''),
        (161, 8, 'action', 'current = collection[i]', 0, 1450, 480, 160, 20, 0, 0, None, '', None, ''),
        (162, 8, 'if', 'self.comparer(current, median) < 0', 0, 1450, 540, 160, 20, 120, 1, None, '', None, ''),
        (163, 8, 'action', 'left.append(current)', 0, 1450, 610, 160, 20, 0, 0, None, '', None, ''),
        (164, 8, 'action', 'right.append(current)', 0, 1730, 610, 100, 20, 0, 0, None, '', None, ''),
        (165, 8, 'horizontal', '', 0, 1450, 650, 390, 0, 0, 0, None, '', None, ''),
        (166, 8, 'vertical', '', 0, 1730, 540, 0, 110, 0, 0, None, '', None, ''),
        (167, 8, 'branch', 'recurse', 0, 1910, 170, 160, 30, 0, 0, None, '', None, ''),
        (168, 8, 'address', 'exit', 0, 1910, 750, 160, 30, 0, 0, None, '', None, ''),
        (169, 8, 'vertical', '', 0, 1910, 120, 0, 670, 0, 0, None, '', None, ''),
        (170, 8, 'action', 'left_sorted = self.quick_sort(left)\nright_sorted = self.quick_sort(right)', 0, 1910, 250, 160, 30, 0, 0, None, '', None, ''),
        (171, 8, 'action', 'result = []\nresult.extend(left_sorted)\nresult.append(median)\nresult.extend(right_sorted)', 0, 1910, 340, 160, 50, 0, 0, None, '', None, ''),
        (172, 8, 'if', 'i == half', 0, 1450, 410, 160, 20, 230, 0, None, '', None, ''),
        (173, 8, 'vertical', '', 0, 1840, 410, 0, 240, 0, 0, None, '', None, ''),
        (174, 8, 'action', 'result = collection', 0, 780, 610, 150, 20, 0, 0, None, '', None, ''),
        (175, 8, 'action', 'return result', 0, 2220, 420, 70, 20, 0, 0, None, '', None, '')
    ]

    graph, branches_map = parse_drakon_primitives(raw_data)
    
    # Выводим структуру одной из веток Силуэта для демонстрации связей
    print("--- СТРУКТУРА ВЕТКИ 'analyze input' (Шампур 1) ---")
    nodes = graph['analyze input']['nodes']
    for n_id in sorted(nodes.keys()):
        node = nodes[n_id]
        print(f"ID: {node['id']} | Тип: {node['type'].upper()} | Текст: {node['text'].replace('\n', ' ')} -> NEXT: {node['next']}")
        if node['branches']:
            print(f"   -> ВЕТВЛЕНИЯ КЕЙСОВ: {node['branches']}")