% Negative: Is the negation of "Taylor eats salads regularly" entailed?
fof(distinct, axiom, $true).

% Premise 1
fof(p1, axiom, ! [X] : (eats_salads(X) => health_conscious(X))).

% Premise 2
fof(p2, axiom, ! [X] : (grew_up_healthy(X) => eats_salads(X))).

% Premise 3
fof(p3, axiom, ! [X] : (fulfills_nutrition(X) => grew_up_healthy(X))).

% Premise 4
fof(p4, axiom, ! [X] : (disregards_wellbeing(X) => ~health_conscious(X))).

% Premise 5
fof(p5, axiom, ! [X] : (visits_gym(X) => fulfills_nutrition(X))).

% Premise 6
fof(p6, axiom, 
    ( (grew_up_healthy(taylor) & disregards_wellbeing(taylor)) 
    | (~grew_up_healthy(taylor) & ~disregards_wellbeing(taylor)) )).

% Negated conclusion: Taylor does NOT eat salads regularly
fof(goal, conjecture, ~eats_salads(taylor)).