fof(premise1, axiom, ! [R] : (listed_in_yelp(R) => ~many_negative_reviews(R))).
fof(premise2, axiom, ! [R] : (rating_greater_than_four(R) => listed_in_yelp(R))).
fof(premise3, axiom, ? [R] : (~provides_take_out(R) & many_negative_reviews(R))).
fof(premise4, axiom, ! [R] : (popular_among_locals(R) => rating_greater_than_four(R))).
fof(premise5, axiom, rating_greater_than_four(hamden_plaza_subway) | popular_among_locals(hamden_plaza_subway)).
fof(conclusion, conjecture, (provides_take_out(hamden_plaza_subway) & many_negative_reviews(hamden_plaza_subway)) => (rating_greater_than_four(hamden_plaza_subway) & ~provides_take_out(hamden_plaza_subway))).