% Negative test: Is the negation of the conclusion entailed?
% Negated conclusion: ~(all events are sad) = exists event that is not sad
fof(premise1, axiom, ! [E] : (event(E) => (happy(E) | sad(E)))).
fof(premise2, axiom, ? [E] : (event(E) & happy(E))).
fof(conclusion_neg, conjecture, ~ ! [E] : (event(E) => sad(E))).