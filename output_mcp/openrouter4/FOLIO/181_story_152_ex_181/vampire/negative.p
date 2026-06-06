% Negative file: negated claim as conjecture
% Premise 1: Susan flies to LGA airport
fof(premise1, axiom, flies_to(susan, lga)).
% Premise 2: The departure and arrival cannot be at the same airport
fof(premise2, axiom, ! [P, A] : ~(flies_from(P, A) & flies_to(P, A))).
% Premise 3: John flies from LGA airport
fof(premise3, axiom, flies_from(john, lga)).
% Negated Conclusion: John does NOT fly to LGA airport
fof(conclusion_neg, conjecture, ~flies_to(john, lga)).