fof(p1, axiom, ! [X] : (listed_in_yelp(X) => ~many_negative_reviews(X))).
fof(p2, axiom, ! [X] : (rating_gt_four(X) => listed_in_yelp(X))).
fof(p3, axiom, ? [X] : (~provides_takeout(X) & many_negative_reviews(X))).
fof(p4, axiom, ! [X] : (popular_among_locals(X) => rating_gt_four(X))).
fof(p5, axiom, (rating_gt_four(hamden_plaza_subway) | popular_among_locals(hamden_plaza_subway))).
fof(goal, conjecture, provides_takeout(hamden_plaza_subway)).