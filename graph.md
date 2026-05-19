graph TD
    %% Определение узлов главного шампура
    Start([backward])
    Init[topo = [] <br> visited = set()]
    CallBuild[Вызов функции: build_topo self]
    InitGrad[self.grad = 1]
    LoopTopo{Для каждого v <br> в reversed topo}
    End([Конец])

    %% Связи главного шампура
    Start --> Init
    Init --> CallBuild
    CallBuild --> InitGrad
    InitGrad --> LoopTopo
    LoopTopo -- Конец обхода графа --> End

    %% Определение узлов подграфа рекурсии
    CondVisited{v не в visited?}
    MarkVisited[Добавить v в visited]
    LoopChildren{Для каждого child <br> в v._children}
    CallRec[Рекурсия: build_topo child]
    AppendTopo[Добавить v в topo]
    EndSub([Выход из рекурсии])

    %% Связи подграфа
    CallBuild -.-> CondVisited
    CondVisited -- Да --> MarkVisited
    MarkVisited --> LoopChildren
    LoopChildren -- Итерация --> CallRec
    CallRec --> LoopChildren
    LoopChildren -- Конец цикла --> AppendTopo
    AppendTopo --> EndSub
    CondVisited -- Нет --> EndSub

    %% Связи внутри цикла расчета градиентов
    LoopGrads{Для каждого child, local_grad <br> в zip}
    Calc[child.grad += local_grad * v.grad]

    LoopTopo -- Итерация --> LoopGrads
    LoopGrads -- Расчет --> Calc
    Calc --> LoopGrads
    LoopGrads -- Конец вложенного цикла --> LoopTopo

    %% Применение стилей (вынесено отдельно от стрелок)
    classDef beginend fill:#f9f,stroke:#333,stroke-width:2px;
    classDef action fill:#fff,stroke:#333,stroke-width:1px;
    classDef condition fill:#ff9,stroke:#333,stroke-width:1px;

    class Start,End,EndSub beginend;
    class Init,CallBuild,InitGrad,MarkVisited,CallRec,AppendTopo,Calc action;
    class LoopTopo,CondVisited,LoopChildren,LoopGrads condition;
