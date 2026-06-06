% Negative conjecture: Hamden Plaza provides take-out
fof(listed_not_negative, axiom, ![R] : (listed_in_yelp(R) => ~many_negative_reviews(R))).
fof(rating_implies_listed, axiom, ![R] : (rating_gt4(R) => listed_in_yelp(R))).
fof(some_not_takeout_negative, axiom, ?[R] : (~provides_takeout(R) & many_negative_reviews(R))).
fof(popular_implies_rating, axiom, ![R] : (popular_local(R) => rating_gt4(R))).
fof(hamden_info, axiom, rating_gt4(hamden_plaza) | popular_local(hamden_plaza)).
fof(goal, conjecture, provides_takeout(hamden_plaza)).