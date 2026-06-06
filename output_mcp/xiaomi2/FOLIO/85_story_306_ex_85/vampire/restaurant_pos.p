fof(p1, axiom, ! [X] : (listed_in_yelp(X) => ~negative_reviews(X))).
fof(p2, axiom, ! [X] : (rating_above_four(X) => listed_in_yelp(X))).
fof(p3, axiom, ? [X] : (~takeout(X) & negative_reviews(X))).
fof(p4, axiom, ! [X] : (popular_local(X) => rating_above_four(X))).
fof(p5, axiom, rating_above_four(hp_subway) | popular_local(hp_subway)).
fof(goal, conjecture, takeout(hp_subway) | ~negative_reviews(hp_subway)).