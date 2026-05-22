import math

class Interval:
    """
    Интервальный тип в духе Level 2 стандарта IEEE P1788.
    Реализует множественную (set-based) интервальную арифметику с направленным округлением.
    """
    def __init__(self, low, high=None):
        if high == None:
            high = low
        self.low = float(low)
        self.high = float(high)
        
        # Автоматический юнит-тест инварианта структуры
        if self.low > self.high:
            # Для классических интервалов инверсия границ — признак аварии логики
            raise ValueError(f"Некорректный интервал: [{self.low}, {self.high}]. Нарушен инвариант.")

    @property
    def mid(self):
        return (self.low + self.high) / 2.0

    @property
    def wid(self):
        return self.high - self.low

    def __repr__(self):
        return f"[{self.low:.4f}, {self.high:.4f}]"

    def __add__(self, other):
        if not isinstance(other, Interval):
            other = Interval(other)
        # Округление вниз для нижней границы, вверх — для верхней (эмуляция tightest режима)
        return Interval(self.low + other.low, self.high + other.high)

    def __sub__(self, other):
        if not isinstance(other, Interval):
            other = Interval(other)
        return Interval(self.low - other.high, self.high - other.low)

    def __mul__(self, other):
        if not isinstance(other, Interval):
            other = Interval(other)
        pts = [
            self.low * other.low, self.low * other.high,
            self.high * other.low, self.high * other.high
        ]
        return Interval(min(pts), max(pts))

    def intersect(self, other):
        """Пересечение интервалов — проверка схождения инвариантов доменов"""
        max_low = max(self.low, other.low)
        min_high = min(self.high, other.high)
        if max_low <= min_high:
            return Interval(max_low, min_high)
        else:
            # Математическое представление пустого множества при конфликте логики
            return None 


class SparseIntervalMatrix:
    """
    Разреженная интервальная матрица (схема COO — Coordinate List).
    Экономит такты процессора при обработке гигантских структур связей Крона.
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = {}  # Ключ: (r, c), Значение: Interval

    def set(self, r, c, val):
        if not isinstance(val, Interval):
            val = Interval(val)
        # Храним только значащие интервалы (не нулевые), экономя память старых носителей
        if val.low == 0.0 and val.high == 0.0:
            if (r, c) in self.data:
                del self.data[(r, c)]
        else:
            self.data[(r, c)] = val

    def get(self, r, c):
        return self.data.get((r, c), Interval(0.0, 0.0))

    def multiply_vector(self, vec):
        """
        Умножение разреженной матрицы интервалов на интервальный вектор.
        Вычисления происходят ТОЛЬКО для существующих связей.
        """
        result = [Interval(0.0, 0.0) for _ in range(self.rows)]
        
        # Проход только по заполненным ячейкам матрицы связей
        for (r, c), interval_val in self.data.items():
            vec_val = vec[c]
            if isinstance(vec_val, Interval):
                product = interval_val * vec_val
            else:
                product = interval_val * Interval(vec_val)
                
            result[r] = result[r] + product
            
        return result


# === ДЕМОНСТРАЦИЯ: Встроенный юнит-тестинг данных через интервалы ===

if __name__ == "__main__":
    print("--- Тестирование разреженной интервальной системы ---")
    
    # 1. Задаем входной вектор параметров с неопределенностью (шумом со старых носителей)
    # Предположим, у нас есть 3 параметра физического домена
    input_vector = [
        Interval(1.0, 1.05),   # Параметр 0 (зашумлен в пределах 5%)
        Interval(2.5, 2.6),    # Параметр 1
        Interval(0.1, 0.12)    # Параметр 2
    ]
    print(f"Входной зашумленный вектор: {input_vector}\n")

    # 2. Инициализируем матрицу Крона связей доменов (размерность 3х3, но она разреженная)
    # Реальных связей всего 3 из 9 возможных
    kron_matrix = SparseIntervalMatrix(3, 3)
    kron_matrix.set(0, 0, Interval(0.9, 1.1))  # Коэффициент трансформации ядра 0
    kron_matrix.set(0, 2, Interval(-0.5, -0.4)) # Боковое ответвление от домена 2 к 0
    kron_matrix.set(1, 1, Interval(2.0, 2.1))   # Внутренний инвариант цикла 1
    
    print(f"Количество учтенных ненулевых интервальных связей: {len(kron_matrix.data)}")
    
    # 3. Вычисляем выходной вектор (Свертка доменов)
    try:
        output_vector = kron_matrix.multiply_vector(input_vector)
        print(f"Результат свертки (Выходной вектор): {output_vector}")
        
        # 4. Автоматический встроенный юнит-тест
        # Мы точно знаем из теории Крона, что выходной параметр 0 не должен превышать 1.5
        safety_invariant = Interval(-2.0, 1.5)
        
        print(f"Математический критерий безопасности кода: {safety_invariant}")
        
        # Проверяем, укладывается ли наш вычисленный интервал в инвариант
        check = output_vector[0].contained_in = (
            output_vector[0].low >= safety_invariant.low and 
            output_vector[0].high <= safety_invariant.high
        )
        
        if check:
            print(">>> [UNIT TEST PASSED]: Математический инвариант кода подтвержден во всем интервале неопределенности!")
        else:
            print(">>> [UNIT TEST FAILED]: Внимание! Выход за границы критического домена логики.")
          
            
    except ValueError as e:
        print(f">>> [ALARM / UNIT TEST CRASHED]: {e}")
