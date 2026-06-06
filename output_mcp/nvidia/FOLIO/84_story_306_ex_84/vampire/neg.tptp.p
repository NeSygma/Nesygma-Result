fof(premise1, axiom, ! [X] : (listed_in_yelp(X) => ~many_negative_reviews(X))).
fof(premise2, axiom, ! [X] : (rating_gt_4(X) => listed_in_yelp(X))).
fof(premise3, axiom, ? [X] : (~provides_takeout(X) & many_negative_reviews(X))).
fof(premise4, axiom, ! [X] : (popular_local(X) => rating_gt_4(X))).
fof(premise5, axiom, rating_gt_4(hampden_plaza_subway) | popular_local(hampden_plaza_subway)).
fof(neg_conclusion, conjecture, (provides_takeout(hampden_plaza_subway) & many_negative_reviews(hampden_plaza_subway))).