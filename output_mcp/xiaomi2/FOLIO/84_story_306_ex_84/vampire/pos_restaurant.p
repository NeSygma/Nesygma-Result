fof(p1, axiom, ! [X] : (listed_in_yelp(X) => ~many_negative_reviews(X))).
fof(p2, axiom, ! [X] : (rating_gt_four(X) => listed_in_yelp(X))).
fof(p3, axiom, ? [X] : (~provides_takeout(X) & many_negative_reviews(X))).
fof(p4, axiom, ! [X] : (popular_among_locals(X) => rating_gt_four(X))).
fof(p5, axiom, rating_gt_four(hp_subway) | popular_among_locals(hp_subway)).
fof(goal, conjecture,
    ((provides_takeout(hp_subway) & many_negative_reviews(hp_subway))
     => (rating_gt_four(hp_subway) & ~provides_takeout(hp_subway)))).