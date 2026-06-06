% Negative file: negated conclusion as conjecture
fof(premise1, axiom, ! [X] : (born_multiple(X) => spends_time(X))).
fof(premise2, axiom, ! [X] : (has_siblings_together(X) => born_multiple(X))).
fof(premise3, axiom, ! [X] : (complains(X) => has_siblings_together(X))).
fof(premise4, axiom, ! [X] : (lives_home(X) => ~lives_strangers(X))).
fof(premise5, axiom, ! [X] : (spends_time(X) => lives_home(X))).

fof(premise6, axiom,
    ((born_multiple(luke) & lives_strangers(luke)) |
     (~born_multiple(luke) & ~lives_strangers(luke)))).

% Negated conclusion: ~(~born_multiple(luke) & ~complains(luke))
% which is equivalent to: born_multiple(luke) | complains(luke)
fof(negated_conclusion, conjecture,
    (born_multiple(luke) | complains(luke))).