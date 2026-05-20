#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
DMM МЕТА-КОМПИЛЯТОР ПО ТУРЧИНУ (ОПЕРАТОР UP / DN И ДЕТЕРМИНИРОВАННЫЙ DAG)
================================================================================
"""

import os
import collections

class MetaTurchinCompiler:
    """
    Эмулятор Рефал-машины для свертки Call-графов и активных классов в DAG.
    Использует концепцию 'поле зрения' для деструктуризации объектных выражений.
    """
    def __init__(self, project_name="DMM_Output"):
        self.project_name = project_name
        self.call_graph = collections.defaultdict(set)
        self.active_classes = {}  # Имя класса -> Состояния Конечного Автомата
        
    # ⴰⵏⵟⵓ -> Функция UP: Упрятывание сырых метаданных в поле зрения компилятора
    def register_call(self, caller, callee):
        """ Запись ребра в Call-граф зависимостей функций """
        self.call_graph[caller].add(callee)
        
    def register_active_class(self, class_name, states, transitions):
        """ Регистрация активного класса с внутренним конечным автоматом """
        self.active_classes[class_name] = {
            "states": states,
            "transitions": transitions
        }

    # ⵎⴰⵣⵣⴰⵢ -> Анализ и генерация правильного DAG (Топологическая сортировка)
    def build_dag(self):
        """
        Преобразует объединенный граф вызовов и классов в ациклический контур.
        Выбрасывает исключение при обнаружении взаимных петель (нарушение каузальности).
        """
        dependencies = collections.defaultdict(set)
        
        # Сшиваем вызовы функций и структуры классов в единую матрицу зависимостей
        for caller, callees in self.call_graph.items():
            for callee in callees:
                dependencies[caller].add(callee)
                
        # Находим порядок сборки модулей (Алгоритм Кана для DAG)
        in_degree = {u: 0 for u in dependencies}
        for u in dependencies:
            for v in dependencies[u]:
                if v not in in_degree:
                    in_degree[v] = 0
                in_degree[v] += 1
                
        queue = collections.deque([u for u in in_degree if in_degree[u] == 0])
        dag_order = []
        
        while queue:
            u = queue.popleft()
            dag_order.append(u)
            for v in dependencies.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
                    
        if len(dag_order) < len(in_degree):
            # ⵯⵔⵏ -> Обнаружен циклический тупик в мета-структуре
            raise ValueError("ⵯⵔⵏ -> Ошибка: Нарушение DAG. Обнаружена циклическая зависимость вызовов!")
            
        return dag_order[::-1]  # Возвращаем порядок сборки (от независимых к зависимым)

    # ⴰⴽⴻⵏ -> Функция DN: Выковыривание структуры из мета-поля и запись на диск
    def generate_project_structure(self):
        """ Разворачивает вычисленный DAG в физические папки и модули """
        order = self.build_dag()
        print(f"# [ⵇⵇⴻⵏ]: Топологический порядок сборки модулей: {order}")
        
        base_dir = self.project_name
        os.makedirs(base_dir, exist_ok=True)
        
        # Создаем корневой пакет инициализации
        with open(os.path.join(base_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write(f'# ⴰⵏⵟⵓ -> Корневой пакет DMM для {self.project_name}\n')
            
        # Генерируем изолированные модули на основе DAG
        for module in order:
            module_path = os.path.join(base_dir, f"{module}.py")
            with open(module_path, "w", encoding="utf-8") as f:
                f.write(f'# -*- coding: utf-8 -*-\n# ⴰⴽⴻⵏ -> Автоматическая генерация модуля: {module}\n\n')
                
                # Если модуль является активным классом с КА — внедряем матрицу состояний
                if module in self.active_classes:
                    ka = self.active_classes[module]
                    f.write(f'class {module.capitalize()}:\n')
                    f.write(f'    """ Активный класс. Конечный автомат. """\n')
                    f.write(f'    STATES = {ka["states"]}\n\n')
                    f.write(f'    def __init__(self):\n')
                    f.write(f'        self.current_state = "{ka["states"][0]}"\n\n')
                    f.write(f'    def transition(self, event):\n')
                    f.write(f'        # ⵎⴰⵣⵣⴰⵢ -> Логика переключения состояний\n')
                    f.write(f'        transitions = {ka["transitions"]}\n')
                    f.write(f'        if (self.current_state, event) in transitions:\n')
                    f.write(f'            self.current_state = transitions[(self.current_state, event)]\n')
        
        print(f"# [ⵇⵇⴻⵏ -> ⴰⴽⴻ็น]: Проект успешно развернут в каталоге: '{base_dir}/'")


# ================================================================================
# ДЕМОНСТРАЦИЯ СБОРКИ АКТИВНОГО КА-ГРАФА
# ================================================================================
if __name__ == "__main__":
    # Инициализируем компилятор
    compiler = MetaTurchinCompiler("IncaIonosphereProject")
    
    # 1. Загружаем Call-граф (кто кого вызывает в подсистемах)
    compiler.register_call("ionosphere_core", "maxwell_solver")
    compiler.register_call("maxwell_solver", "hodge_dual_operator")
    
    # 2. Регистрируем активный класс (Конечный автомат управления фильтром Варни)
    compiler.register_active_class(
        class_name="hodge_dual_operator",
        states=["STATE_IDLE", "STATE_COMPUTING", "STATE_WARN_REJECTION"],
        transitions={
            ("STATE_IDLE", "START"): "STATE_COMPUTING",
            ("STATE_COMPUTING", "ERROR"): "STATE_WARN_REJECTION"
        }
    )
    
    # 3. Запуск транслятора (Сборка DAG -> Файловая структура)
    compiler.generate_project_structure()