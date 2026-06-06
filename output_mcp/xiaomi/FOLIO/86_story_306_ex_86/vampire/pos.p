fof(p1, axiom, ! [R] : (listed_in_yelp(R) => ~many_negative_reviews(R))).
fof(p2, axiom, ! [R] : (rating_greater_than_four(R) => listed_in_yelp(R))).
fof(p3, axiom, ? [R] : (~provides_takeout(R) & many_negative_reviews(R))).
fof(p4, axiom, ! [R] : (popular_among_locals(R) => rating_greater_than_four(R))).
fof(p5, axiom, rating_greater_than_four(hamden_plaza_subway) | popular_among_locals(hamden_plaza_subway)).
fof(goal, conjecture, ~provides_takeout(hamden_plaza_subway)).