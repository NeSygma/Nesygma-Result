fof(listed_implies_not_negative, axiom, ! [R] : (listed_in_yelp(R) => ~many_negative_reviews(R))).
fof(rating_gt_four_implies_listed, axiom, ! [R] : (rating_gt_four(R) => listed_in_yelp(R))).
fof(exist_negative, axiom, ? [R] : (~provides_takeout(R) & many_negative_reviews(R))).
fof(popular_local_implies_rating_gt_four, axiom, ! [R] : (popular_local(R) => rating_gt_four(R))).
fof(hamden_disj, axiom, (rating_gt_four(hamden_plaza_store) | popular_local(hamden_plaza_store))).
fof(conjecture, conjecture, provides_takeout(hamden_plaza_store)).