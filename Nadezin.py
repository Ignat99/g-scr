import os

class Interval:
    """Интервальный тип по стандарту IEEE P1788 (Упрощенный Level 2 JInterval)"""
    def __init__(self, low, high=None):
        if high is None:
            high = low
        self.low = float(low)
        self.high = float(high)
        if self.low > self.high:
            raise ValueError(f"Нарушен инвариант интервала: [{self.low}, {self.high}]")

    def __repr__(self):
        return f"[{self.low:.2f}, {self.high:.2f}]"

    def __add__(self, other):
        if not isinstance(other, Interval): other = Interval(other)
        return Interval(self.low + other.low, self.high + other.high)

    def __mul__(self, other):
        if not isinstance(other, Interval): other = Interval(other)
        pts = [self.low * other.low, self.low * other.high, 
               self.high * other.low, self.high * other.high]
        return Interval(min(pts), max(pts))


class SparseIntervalMatrixNadezhin:
    """Разреженная интервальная матрица (схема COO) по заветам Д. Надёжина"""
    def __init__(self):
        self.data = {}  # Ключ: (row, col), Значение: Interval
        self.max_row = 0
        self.max_col = 0

    def set(self, r, c, val):
        if not isinstance(val, Interval):
            val = Interval(val)
        if val.low == 0.0 and val.high == 0.0:
            if (r, c) in self.data:
                del self.data[(r, c)]
        else:
            self.data[(r, c)] = val
            self.max_row = max(self.max_row, r)
            self.max_col = max(self.max_col, c)

    def get(self, r, c):
        return self.data.get((r, c), Interval(0.0, 0.0))

    def export_to_skill(self, filename="meander_sparse_matrix.md"):
        """Экспорт структуры в Skill-файл манифеста"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# ⵜⵙⴳⴱ\n## МАТРИЧНЫЙ ПАСПОРТ МЕАНДРА\n\n")
            f.write(f"* **Размерность:** Макс. узел матрицы = {self.max_row}x{self.max_col}\n")
            f.write(f"* **Количество активных связей Крона:** {len(self.data)}\n\n")
            f.write("### Сухие ненулевые интервальные коэффициенты соединений:\n")
            f.write("| Домен (Строка) | Домен (Столбец) | Интервальный коэффициент |\n")
            f.write("|---|---|---|\n")
            for (r, c), interval in sorted(self.data.items()):
                f.write(f"| {r} | {c} | {interval} |\n")
            f.write("\n# ⵜⵎⵔⵯⵜ\n~~~ignat99\n")


def parse_meander_to_nadezhin(file_content):
    """Кодировщик текстовой топологии в разреженную структуру"""
    matrix = SparseIntervalMatrixNadezhin()
    lines = file_content.strip().split('\n')
    
    parsing_table = False
    node_index = 1
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Обнаруживаем шапку таблицы связей окрестностей
        if "left" in line and "right" in line:
            parsing_table = True
            continue
        
        # Если пошли массивы траекторий (меандров) — останавливаем чтение таблицы
        if parsing_table and ("GNU Octave" in line or line.startswith("[")):
            parsing_table = False
            
        if parsing_table:
            parts = line.split()
            # Проверяем, что перед нами строка с 4 координатами направлений
            if len(parts) == 4:
                # Вводим неопределенность (шум контактов) в пределах 2% для интервального анализа
                weight_low = 0.98
                weight_high = 1.02
                
                for i, part in enumerate(parts):
                    if part != "Inf":
                        connected_node = int(part)
                        # Заколачиваем мостки в матрицу соединений C:
                        # строка = текущий узел, столбец = связанный узел
                        matrix.set(node_index, connected_node, Interval(weight_low, weight_high))
                node_index += 1
                
    return matrix


# === Исполнительный блок ===
if __name__ == "__main__":
    # Симулируем чтение поданного файла со старых носителей
    raw_data = """
left, right. above, below 
   Inf     2   Inf     6
     1     3   Inf     7
     2     4   Inf     8
     3     5   Inf     9
     4   Inf   Inf    10
   Inf     7     1    11
     6     8     2    12
    """
    
    print("Труд в сознании завершён. Начинаем мостить разреженную матрицу...")
    nadezhin_matrix = parse_meander_to_nadezhin(raw_data)
    
    # Экспортируем в канонический Skill-формат .md
    nadezhin_matrix.export_to_skill("meander_sparse_matrix.md")
    print("Мостки наведены! Файл 'meander_sparse_matrix.md' успешно загерметизирован.")