fof(event_domain, axiom, ! [X] : (event(X) => (happy(X) | sad(X)))).
fof(at_least_one_happy, axiom, ? [X] : (event(X) & happy(X))).
fof(conclusion, conjecture, ! [X] : (event(X) => sad(X))).