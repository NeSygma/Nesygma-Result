% Negative: negated conclusion as conjecture
fof(premise1, axiom, ! [X] : (listed(X) => ~many_neg(X))).
fof(premise2, axiom, ! [X] : (rating_gt4(X) => listed(X))).
fof(premise3, axiom, ? [X] : (~takeout(X) & many_neg(X))).
fof(premise4, axiom, ! [X] : (popular(X) => rating_gt4(X))).
fof(premise5, axiom, (rating_gt4(h) | popular(h))).
fof(neg_conclusion, conjecture, ~((takeout(h) & many_neg(h)) => (rating_gt4(h) & ~takeout(h)))).