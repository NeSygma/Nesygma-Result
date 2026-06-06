% Positive: all events are sad
fof(premise_exclusive1, axiom, ! [E] : (happy(E) => ~sad(E))).
fof(premise_exclusive2, axiom, ! [E] : (sad(E) => ~happy(E))).
fof(premise_exhaustive, axiom, ! [E] : (happy(E) | sad(E))).
fof(premise_some_happy, axiom, ? [E] : happy(E)).
fof(goal_all_sad, conjecture, ! [E] : sad(E)).