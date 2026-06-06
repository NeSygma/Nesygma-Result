% Positive test: Is the conclusion "All events are sad" entailed?
fof(premise1, axiom, ! [E] : (event(E) => (happy(E) | sad(E)))).
fof(premise2, axiom, ? [E] : (event(E) & happy(E))).
fof(conclusion, conjecture, ! [E] : (event(E) => sad(E))).