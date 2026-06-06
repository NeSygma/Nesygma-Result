fof(premise1, axiom, ~(? [A] : (likes(jane, A) & bark(A)))).
fof(premise2, axiom, ! [A] : (dog(A) => bark(A))).
fof(premise3, axiom, ! [A] : (jump(A) => likes(jane, A))).
fof(premise4, axiom, ! [A] : (has_legs(A) => jump(A))).
fof(premise5, axiom, ! [A] : (terricolous(A) => has_legs(A))).
fof(premise6, axiom, animal(kiki)).
fof(premise7, axiom, ((~jump(kiki) & ~has_legs(kiki)) => (terricolous(kiki) | has_legs(kiki)))).
fof(conclusion, conjecture, (dog(kiki) & bark(kiki))).