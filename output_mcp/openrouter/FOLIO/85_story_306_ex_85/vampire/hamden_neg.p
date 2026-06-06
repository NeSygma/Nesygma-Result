% Negative version (negated conclusion)
fof(premise1, axiom, ![R] : (listed_in_yelp(R) => ~many_negative_reviews(R))).
fof(premise2, axiom, ![R] : (rating_gt4(R) => listed_in_yelp(R))).
fof(premise3, axiom, ?[R] : (~provides_takeout(R) & many_negative_reviews(R))).
fof(premise4, axiom, ![R] : (popular_local(R) => rating_gt4(R))).
fof(premise5, axiom, rating_gt4(hamden_plaza_subway) | popular_local(hamden_plaza_subway)).
fof(conjecture, conjecture, ~ (provides_takeout(hamden_plaza_subway) | ~many_negative_reviews(hamden_plaza_subway))).