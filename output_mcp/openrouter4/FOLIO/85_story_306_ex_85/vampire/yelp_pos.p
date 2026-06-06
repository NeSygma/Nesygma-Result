fof(premise1, axiom, ! [X] : (listed_in_yelp(X) => ~many_negative_reviews(X))).
fof(premise2, axiom, ! [X] : (rating_greater_than_four(X) => listed_in_yelp(X))).
fof(premise3, axiom, ? [X] : (~provides_takeout(X) & many_negative_reviews(X))).
fof(premise4, axiom, ! [X] : (popular_among_locals(X) => rating_greater_than_four(X))).
fof(premise5, axiom, (rating_greater_than_four(hamden_subway) | popular_among_locals(hamden_subway))).
fof(conclusion, conjecture, (provides_takeout(hamden_subway) | ~many_negative_reviews(hamden_subway))).