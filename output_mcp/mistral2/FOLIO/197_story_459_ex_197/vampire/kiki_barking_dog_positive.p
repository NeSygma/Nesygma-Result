fof(premise_1, axiom, ! [A] : ((animal(A) & barks(A)) => ~likes(jane, A))).
fof(premise_2, axiom, ! [D] : (dog(D) => (animal(D) & barks(D)))).
fof(premise_3, axiom, ! [A] : ((animal(A) & jumps(A)) => likes(jane, A))).
fof(premise_4, axiom, ! [A] : ((animal(A) & has_legs(A)) => jumps(A))).
fof(premise_5, axiom, ! [A] : ((animal(A) & terricolous(A)) => has_legs(A))).
fof(premise_6, axiom, animal(kiki)).
fof(premise_7, axiom, (~jumps(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki))).

fof(conclusion, conjecture, (dog(kiki) & barks(kiki))).