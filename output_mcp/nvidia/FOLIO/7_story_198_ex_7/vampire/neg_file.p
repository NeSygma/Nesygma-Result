fof(prem1, axiom, ! [X] : (human(X) => mammal(X))).
fof(prem2, axiom, ! [X] : (mammal(X) => animal(X))).
fof(prem3, axiom, ? [X] : (animal(X) & virus_can_occur(X))).
fof(neg_goal, conjecture, ! [X] : ~animal(X)).