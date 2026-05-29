# === Цикл сборки поддиаграмм ===
        for d_name, shampurs in sub_diagrams:
            # Вызов изолированной функции
            dia_id, item_start = self._create_sub_diagram(d_name, shampurs, item_start)
            
            # Здесь вы можете использовать возвращенный dia_id 
            # для привязки поддиаграммы к основному Силуэту