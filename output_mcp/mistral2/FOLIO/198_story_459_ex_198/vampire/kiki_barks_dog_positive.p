fof(premise_1, axiom, ! [A] : (barks(A) => ~likes(jane, A))).
fof(premise_2, axiom, ! [A] : (dog(A) => barks(A))).
fof(premise_3, axiom, ! [A] : (jumps(A) => likes(jane, A))).
fof(premise_4, axiom, ! [A] : (has_legs(A) => jumps(A))).
fof(premise_5, axiom, ! [A] : (terricolous(A) => has_legs(A))).
fof(premise_6, axiom, animal(kiki)).
fof(premise_7, axiom, (~jumps(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki))).

fof(conclusion, conjecture, (~barks(kiki) & ~dog(kiki))).