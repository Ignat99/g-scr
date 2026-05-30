from pylog import Symbols, Value, Variable, Fact, Rule, Prolog

# 1. Объявляем переменные и предикаты как символы
Cx, WAll, HBe, HAct, HDop, YBegin = Variable(), Variable(), Variable(), Variable(), Variable(), Variable()
YAction, YEnd, YVert, HVert = Variable(), Variable(), Variable(), Variable()

primitive_geometry = Symbols('primitive_geometry')
layout_primitive = Symbols('layout_primitive')

pl = Prolog()

# 2. Декларируем факты базы знаний (аналог primitive_geometry(170, 110, 20, 100, 50, 60).)
pl = Fact(primitive_geometry(170, 110, 20, 100, 50, 60))

# 3. Декларируем правила (Отношения между переменными)
# В логических библиотеках Python арифметические ограничения часто задаются функциями-предикатами
pl += Rule(layout_primitive(YAction, YEnd, YVert, HVert, Cx, WAll, HBe),
           primitive_geometry(Cx, WAll, HBe, HAct, HDop, YBegin),
           Value(YAction) == (Value(YBegin) + Value(HBe) + Value(HDop)),
           Value(YEnd) == (Value(YAction) + Value(HAct) + Value(HDop)),
           Value(YVert) == (Value(YBegin) + Value(HBe)),
           Value(HVert) == (Value(YEnd) - Value(YVert)))

# 4. Запрос к базе знаний (Query)
result = pl.query(layout_primitive(YAction, YEnd, YVert, HVert, Cx, WAll, HBe))

for solution in result:
    print(f"Решение: YAction={solution[YAction]}, YEnd={solution[YEnd]}, HVert={solution[HVert]}")