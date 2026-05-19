#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
МОВА / БАЗИСНЫЙ ГЕОМЕТРИЧЕСКИЙ МОДУЛЬ (ЭКСТРАКЦИЯ ИЗ AUTODIA)
================================================================================
Цель: Предоставить плоский каркас (размеры и трассировку) для последующего
преобразования в многомерный тензор Ходжа-де Рама в вашем стиле.
"""

class AutodiaObjectBase:
    """
    Экстракция из Object.pm, Class.pm и Component.pm.
    Класс отвечает за абсолютные координаты на плоскости и динамический расчет границ.
    """
    def __init__(self, name, x=0.0, y=0.0):
        self.name = name
        self.left_x = float(x)
        self.top_y = float(y)
        
        # Начальные размеры ячейки по умолчанию (из _initialise в Object.pm)
        self.width = 1.0
        self.height = 1.0
        
        # Списки внутреннего контента (для демонстрации динамического масштабирования)
        self.attributes = []
        self.operations = []
        
        # Первичный расчет размера на основе имени
        self._update_dimensions(name)

    def _update_dimensions(self, last_string):
        """
        Математика масштабирования из Class.pm (_update):
        Ширина адаптируется под самую длинную строку, высота инкрементируется.
        """
        longest_allowed_len = (self.width - 1.0) / 0.5
        if len(last_string) > longest_allowed_len:
            # Формула AutoDia: width = (length * 0.5) + 1
            self.width = (len(last_string) * 0.5) + 1.0
            
    def add_attribute(self, attr_text):
        """ Добавление атрибута с каскадным расширением блока """
        self.attributes.append(attr_text)
        self.height += 0.8  # Шаг высоты из Class.pm
        self._update_dimensions(attr_text)
        
    def add_operation(self, oper_text):
        """ Добавление операции (глагола Тамашека или физического оператора) """
        self.operations.append(oper_text)
        self.height += 0.8
        self._update_dimensions(oper_text)

    @property
    def top_left_pos(self):
        """ Метод TopLeftPos из Object.pm (с фиксацией точности float) """
        return f"{self.left_x:.3f},{self.top_y:.3f}"

    @property
    def bottom_right_pos(self):
        """ Метод BottomRightPos из Object.pm """
        return f"{(self.left_x + self.width):.3f},{(self.top_y + self.height):.3f}"


class AutodiaDependancyBase:
    """
    Экстракция из Dependancy.pm и Diagram.pm.
    Расчет ортогональной трассировки линии между двумя объектами.
    """
    def __init__(self, child_obj, parent_obj):
        self.child = child_obj
        self.parent = parent_obj
        
        # Вычисляемые геометрические параметры линии
        self.left_x = 0.0
        self.right_x = 0.0
        self.mid_y = 0.0
        self.top_y = 0.0
        self.bottom_y = 0.0
        
        # Точки подключения (Handles)
        self.top_connection = ""
        self.bottom_connection = ""
        
        # Вызов оригинального алгоритма позиционирования связи
        self.reposition()

    def reposition(self):
        """
        Оригинальный метод Reposition из Dependancy.pm.
        Строит уступ по вертикали на 1.5 единицы и смещает ось X к центру.
        """
        # 1. Считывание позиции дочернего элемента
        child_tl = self.child.top_left_pos
        c_left_x, c_bottom_y = map(float, child_tl.split(","))
        
        # В AutoDia bottom_y для связи берется из top_left дочернего, 
        # так как шаг идет вертикально вверх к родителю
        self.bottom_y = c_bottom_y
        
        # 2. Формирование высоты ортогонального излома (уступы по 1.5 единицы)
        self.mid_y = self.bottom_y - 1.5
        self.top_y = self.mid_y - 1.5
        
        # 3. Смещение по оси X строго на центр грани объекта с базовым зазором 2
        # left_x += 2 + (Width / 2)
        self.left_x = c_left_x + 2.0 + (self.child.width / 2.0)
        self.right_x = self.left_x + 5.0  # Отвод вправо для разделения линий
        
        # 4. Фиксация векторов портов
        self.top_connection = f"{self.right_x:.3f},{self.top_y:.3f}"
        self.bottom_connection = f"{self.left_x:.3f},{self.bottom_y:.3f}"

    def export_dia_xml_connection(self):
        """
        Оригинальная концепция связывания из шаблона Diagram.pm.
        Фиксирует ребра за центральный автоматический порт 'connection="8"'.
        """
        return (
            f'<dia:connections>\n'
            f'  <dia:connection handle="0" to="{self.child.name}" connection="8"/>\n'
            f'  <dia:connection handle="1" to="{self.parent.name}" connection="8"/>\n'
            f'</dia:connections>'
        )


# ================================================================================
# ДЕМОНСТРАЦИЯ РАБОТЫ ДВУХМЕРНОГО ПРЕДКА
# ================================================================================
if __name__ == "__main__":
    print("# [Базис AutoDia загружен]: Проверка плоской геометрии...")
    
    # Создаем два объекта (Иконы ДРАКОН / Клетки)
    node_source = AutodiaObjectBase("măzzăy_921", x=10.0, y=20.0)
    node_target = AutodiaObjectBase("rho_e_923", x=30.0, y=5.0)
    
    # Наполняем контентом, чтобы сработал триггер расширения границ
    node_source.add_operation(" dL -> Шаг Вправо по де Раму ")
    node_source.add_attribute("pq_pos:921")
    
    # Рассчитываем связь между ними
    link = AutodiaDependancyBase(node_source, node_target)
    
    print(f"Объект Источник: TL={node_source.top_left_pos} | BR={node_source.bottom_right_pos} | Width={node_source.width}")
    print(f"Трассировка связи: Точка выхода={link.bottom_connection} -> Точка захода={link.top_connection}")
    print(f"XML-коннектор (Порт 8):\n{link.export_dia_xml_connection()}")