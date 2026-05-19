import sys

class PhysicalQuantity:
    """
    [ǝkǝn -> сформировать структуру базового элемента физического пространства]
    Класс описывает узел графа — физическую величину с её мультиязычными метаданными.
    """
    def __init__(self, key, ru_name, en_name, common_name):
        self.key = key          # Уникальный идентификатор (например, 'rho_e', 'v_e')
        self.ru_name = ru_name  # Ссылка на русскоязычный инвариант/вики
        self.en_name = en_name  # Ссылка на англоязычный инвариант
        self.name = common_name # Системное наименование величины

    def __repr__(self):
        return f"Quant({self.key}: '{self.name}')"


class OperatorEdge:
    """
    [ǝqqǝn -> связать два узла через оператор перехода]
    Описывает направленное ребро графа — физический закон или оператор (nabla, время, сдвиг).
    """
    def __init__(self, from_key, to_key, operator_symbol):
        self.from_key = from_key
        self.to_key = to_key
        self.operator = operator_symbol # Например, '^', 'nabla', 'l', 'T'

    def __repr__(self):
        return f"Edge({self.from_key} --[{self.operator}]--> {to_key})"


class PhysicalSpaceGraph:
    """
    [ǝkǝn -> развернуть многомерное координатное поле законов]
    Единое детерминированное хранилище величин и топологических связей между ними.
    """
    def __init__(self):
        # Хранилище узлов графа (физические величины из abcd_wiki.pl)
        self.quantities = {}
        # Хранилище связей и операторов перехода
        self.transitions = []
        
        # [ănt -> запуск наполнения ядра системы]
        self._populate_quantities()
        self._populate_operators()

    def _populate_quantities(self):
        """
        [ǝktǝb -> фиксация физических инвариантов в реестр]
        Парсинг и трансляция ассоциативного массива %wiki из abcd_wiki.pl
        """
        # Ниже приведены ключевые операторы и величины из вашего perl-модуля
        raw_wiki = {
            'v_e': {'ru': 'Скорость_передачи_энергии', 'en': 'Energy_transfer_speed', 'name': 'Скорость передачи энергии'},
            'T': {'ru': 'Время', 'en': 'Time_in_physics', 'name': 'Время'},
            'T_l': {'ru': 'Длительность_расстояния', 'en': '', 'name': 'Длительность расстояния'},
            'N_l': {'ru': 'Мощность', 'en': 'Power_(physics)', 'name': 'Мощность'},
            'l_1': {'ru': 'Теплопроводность', 'en': 'Heat conduction', 'name': 'Теплопроводность'},
            'S_l': {'ru': 'Вектор_Пойнтинга', 'en': 'Poynting_vector', 'name': 'Вектор Пойнтинга'},
            'rho_e': {'ru': 'Плотность_заряда', 'en': 'Charge_density', 'name': 'Плотность заряда'},
            '1_eps': {'ru': 'Угловое_ускорение', 'en': 'Angular_acceleration', 'name': 'Угловое ускорение'},
            'n_rho': {'ru': 'Уравнение непрерывности', 'en': 'Continuity equation', 'name': 'Градиент плотности'},
            'sig': {'ru': 'Удельная_проводимость', 'en': 'Electrical_conductivity', 'name': 'Удельная проводимость'},
            '1/r': {'ru': 'Адмиттанс', 'en': 'Admittance', 'name': 'Адмиттанс'},
            # Верхняя строчка неоткрытых законов и тонких полей времени аппроксимируется здесь ключевыми символами
            'nabla': {'ru': 'Набла', 'en': 'Del', 'name': 'Оператор Гамильтона / Градиент пространства'}
        }
        
        for key, data in raw_wiki.items():
            self.quantities[key] = PhysicalQuantity(key, data['ru'], data['en'], data['name'])

    def _populate_operators(self):
        """
        [măzzăy -> разметка координатных путей и законов без явного умножения]
        Трансляция матрицы смежности %data из abcd.pl. 
        Вместо умножения мы строим структуру чистых топологических сдвигов.
        """
        # Базовые правила переходов, извлеченные из шахматной структуры perl-скрипта
        # '0_4' -> Координатная строка/столбец в системе Кулакова-Бартини/Максвелла
        raw_matrix_edges = [
            # Исходный узел, Целевой узел, Оператор перехода
            ('T', 'T_l', 'l'),          # Время через пространственный сдвиг
            ('rho_e', 'n_rho', 'nabla'), # Плотность заряда под действием наблы (градиент)
            ('v_e', 'S_l', '^'),         # Скорость переноса энергии -> Вектор Пойнтинга
        ]
        
        for from_k, to_k, op in raw_matrix_edges:
            if from_k in self.quantities and :
                # [ǝqqǝn -> фиксация связи в контуре]
                self.transitions.append(OperatorEdge(from_k, to_k, op))

    def resolve_path(self, start_key, operator_sequence):
        """
        [răyrăy -> развернуть/вытянуть цепочку законов по графу]
        Прослеживает, в какую физическую величину перейдет стартовая точка 
        при последовательном применении операторов (без вычисления матриц).
        """
        current_node = start_key
        path = [current_node]
        
        for op in operator_sequence:
            # [ăɣăr -> инспекция локальных связей текущего узла]
            found = False
            for edge in self.transitions:
                if edge.from_key == current_node and edge.operator == op:
                    current_node = edge.to_key
                    path.append(current_node)
                    found = True
                    break
            if not found:
                # Столкновение с границей известной физики или разрывом графа
                break
                
        return path

# [sămdu -> сборка ядра завершена, запуск демонстрационного прогона]
if __name__ == "__main__":
    space = PhysicalSpaceGraph()
    print(f"Загружено физических операторов и величин: {len(space.quantities)}")
    
    # Пример детерминированного прохода: берем Время (T) и применяем оператор сдвига (l)
    trace = space.resolve_path('T', ['l'])
    print(f"Цепочка трансформации оператора: {trace}")
