fof(premise1, axiom, ![R] : (listed_in_yelp(R) => ~many_negative_reviews(R))).
fof(premise2, axiom, ![R] : (rating_gt_four(R) => listed_in_yelp(R))).
fof(premise3, axiom, ?[R] : (~take_out_service(R) & many_negative_reviews(R))).
fof(premise4, axiom, ![R] : (popular_local(R) => rating_gt_four(R))).
fof(premise5, axiom, rating_gt_four(hamden_plaza_subway) | popular_local(hamden_plaza_subway)).
fof(conjecture, conjecture, provides_takeout(hamden_plaza_subway) | ~many_negative_reviews(hamden_plaza_subway)).