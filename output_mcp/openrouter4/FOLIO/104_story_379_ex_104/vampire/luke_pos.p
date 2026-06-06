% Positive file: original conclusion as conjecture
% Predicates:
% born_multiple(x)     - x is born in a multiple birth
% spends_time(x)       - x spends a lot of time hanging out with and playing with siblings
% has_siblings_together(x) - x has siblings who were born together
% complains(x)         - x complains often about annoying siblings
% lives_home(x)        - x lives at home
% lives_strangers(x)   - x lives with strangers

fof(premise1, axiom, ! [X] : (born_multiple(X) => spends_time(X))).
fof(premise2, axiom, ! [X] : (has_siblings_together(X) => born_multiple(X))).
fof(premise3, axiom, ! [X] : (complains(X) => has_siblings_together(X))).
fof(premise4, axiom, ! [X] : (lives_home(X) => ~lives_strangers(X))).
fof(premise5, axiom, ! [X] : (spends_time(X) => lives_home(X))).

fof(premise6, axiom,
    ((born_multiple(luke) & lives_strangers(luke)) |
     (~born_multiple(luke) & ~lives_strangers(luke)))).

fof(conclusion, conjecture,
    (~born_multiple(luke) & ~complains(luke))).