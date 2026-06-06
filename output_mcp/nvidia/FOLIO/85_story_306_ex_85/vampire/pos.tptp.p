% Axioms
fof(premise_1, axiom, ! [X] : (listed(X) => ~many_negative_reviews(X))).
fof(premise_2, axiom, ! [X] : (rating_gt4(X) => listed(X))).
fof(premise_3, axiom, ? [X] : (~provides_takeout(X) & many_negative_reviews(X))).
fof(premise_4, axiom, ! [X] : (popular_local(X) => rating_gt4(X))).
fof(premise_5, axiom, rating_gt4(hamden_plaza_subway_store) | popular_local(hamden_plaza_subway_store)).
fof(goal, conjecture, provides_takeout(hamden_plaza_subway_store) | ~many_negative_reviews(hamden_plaza_subway_store)).