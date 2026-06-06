% Positive file: conclusion as conjecture
fof(distinct_constants, axiom, (michael != peter & michael != windy & peter != windy)).

fof(premise_1, axiom, 
    ! [X,Y] : (man(X) & man(Y) & taller(X,Y) => can_block(X,Y))).

fof(premise_2, axiom, 
    man(michael) & in_class(michael) & 
    ! [X] : (in_class(X) & X != michael => taller(michael,X))).

fof(premise_3, axiom, 
    ! [X,Y,Z] : (taller(X,Y) & taller(Y,Z) => taller(X,Z))).

fof(premise_4, axiom, 
    man(peter) & taller(peter,michael)).

fof(premise_5, axiom, 
    ! [X] : (person(X) & ~jump_when_shooting(X) => can_block(michael,X))).

fof(premise_6, axiom, 
    ~can_block(michael,windy)).

fof(premise_7, axiom, 
    ! [X] : (person(X) & jump_when_shooting(X) => great_shooter(X))).

% Additional assumptions: Michael and Peter are persons
fof(michael_is_person, axiom, person(michael)).
fof(peter_is_person, axiom, person(peter)).
fof(windy_is_person, axiom, person(windy)).

% Conclusion: Peter is shorter than a man in Michael's class
fof(conclusion, conjecture, 
    ? [X] : (man(X) & in_class(X) & taller(X,peter))).