fof(premise1, axiom, ! [A] : ((animal(A) & barks(A)) => ~likes(jane, A))).
fof(premise2, axiom, ! [D] : (dog(D) => (animal(D) & barks(D)))).
fof(premise3, axiom, ! [A] : ((animal(A) & jumps(A)) => likes(jane, A))).
fof(premise4, axiom, ! [A] : ((animal(A) & has_legs(A)) => jumps(A))).
fof(premise5, axiom, ! [A] : ((animal(A) & terricolous(A)) => has_legs(A))).
fof(premise6, axiom, animal(kiki)).
fof(premise7, axiom, (~jumps(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki))).
fof(conclusion_negation, conjecture, ~terricolous(kiki)).