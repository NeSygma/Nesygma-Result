% Negative version (negated conjecture)
fof(premise1, axiom, ! [R] : (listed(R) => ~many_negative(R))).
fof(premise2, axiom, ! [R] : (rating_gt4(R) => listed(R))).
fof(premise3, axiom, ? [X] : (~provides_takeout(X) & many_negative(X))).
fof(premise4, axiom, ! [R] : (popular(R) => rating_gt4(R))).
fof(premise5, axiom, rating_gt4(hamden_subway) | popular(hamden_subway)).

fof(conjecture, conjecture, ~(((provides_takeout(hamden_subway) & many_negative(hamden_subway)) => (rating_gt4(hamden_subway) & ~provides_takeout(hamden_subway))))).