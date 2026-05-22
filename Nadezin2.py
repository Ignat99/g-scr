import os
import re

class Interval:
    """Интервальный тип по стандарту IEEE P1788 (JInterval Level 2)"""
    def __init__(self, low, high=None):
        if high is None: high = low
        self.low = float(low)
        self.high = float(high)
        if self.low > self.high:
            raise ValueError(f"Крах инварианта: [{self.low}, {self.high}]")

    def __repr__(self):
        return f"[{self.low:.3f}, {self.high:.3f}]"


class NadezhinSparseMatrix:
    """Разреженная матрица Крона по заветам Д. Надёжина"""
    def __init__(self):
        self.matrix_c = {}  # COO формат: {(строка, столбец): Interval}
        self.max_index = 0

    def add_link(self, from_node, to_node, weight_low=0.95, weight_high=1.05):
        """Заколачиваем гвоздь в мостки связи между доменами меандра"""
        if to_node == "Inf" or from_node == "Inf":
            return # Игнорируем бесконечность (нематериальные или пустые связи)
        
        r = int(from_node)
        c = int(to_node)
        # Каждую физическую связь оборачиваем в интервальный бокс (защита от шума контактов)
        self.matrix_c[(r, c)] = Interval(weight_low, weight_high)
        self.max_index = max(self.max_index, r, c)

    def save_to_skill_manifest(self, filename="meander_final_system.md"):
        """Экспорт в Skill-файл .md с каноническими буквами"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# ⵜⵙⴳⴱ\n\n")
            f.write("## ЦЕПНОЙ КОМПЛЕКС ОПЕРАТОРОВ: ГЕРБ ГРАФА МЕАНДРА\n")
            f.write(f"* **Индекс Рода в Ноосфере:** XVI, 151 (Игнатьевы)\n")
            f.write(f"* **Размерность координатной сетки:** {self.max_index} x {self.max_index}\n")
            f.write(f"* **Число активных мостков (связей):** {len(self.matrix_c)}\n\n")
            
            f.write("### Разреженные интервальные коэффициенты матрицы C:\n")
            f.write("| Узел (Строка) | Связанный Узел (Столбец) | Интервальный Инвариант |\n")
            f.write("|---|---|---|\n")
            for (r, c), interval in sorted(self.matrix_c.items()):
                f.write(f"| {r} | {c} | {interval} |\n")
                
            f.write("\n# ⵜⵎⵔⵯⵜ\n")
            f.write("### Криптографический коммит транзакции (ZenRoom):\n")
            f.write("С тугэрт а, Ignat99 ⵢⴻⵙⵄⴰ ⴷⴻⴳⵙ ⴰⴼⵓⵙ. ~~~ignat99\n")
            f.write("\nⴻⴳﮕ\n")


def smostit_matrix_from_file(file_path):
    """Функция-молоток: разбирает текстовый меандр и наводит мостки"""
    sparse_system = NadezhinSparseMatrix()
    
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден на материальном носителе.")
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.readlines()

    is_table_zone = False
    current_node = 1

    for line in content:
        line = line.strip()
        if not line:
            continue
        
        # Фиксируем шапку таблицы окрестностей
        if "left" in line and "right" in line and "above" in line:
            is_table_zone = True
            continue
            
        # Если таблица кончилась и пошли строки Octave или массивы [ - выходим
        if is_table_zone and ("GNU Octave" in line or line.startswith("[")):
            is_table_zone = False
            break

        if is_table_zone:
            # Разбиваем строку по пробелам или запятым, убирая перхоть
            tokens = re.split(r'[\s,]+', line)
            if len(tokens) >= 4:
                left, right, above, below = tokens[0], tokens[1], tokens[2], tokens[3]
                
                # Наводим мостки по всем 4 ортогональным направлениям Крона
                sparse_system.add_link(current_node, left)
                sparse_system.add_link(current_node, right)
                sparse_system.add_link(current_node, above)
                sparse_system.add_link(current_node, below)
                
                current_node += 1

    return sparse_system

# === ПРЯМОЙ ЗАПУСК МОЛОТКА В СРЕДЕ ===
if __name__ == "__main__":
    # Скрипт ищет ваш загруженный файл output_Meander.txt
    target_file = "output_Meander.txt"
    
    print(f"Работаем молотком по файлу: {target_file}...")
    system_matrix = smostit_matrix_from_file(target_file)
    
    if system_matrix:
        system_matrix.save_to_skill_manifest("skill_meander_nadezhin.md")
        print("Мостки успешно смощены! Манифест 'skill_meander_nadezhin.md' загерметизирован.")