fof(p1, axiom, ! [R] : (listed_in_yelp(R) => ~many_negative_reviews(R))).
fof(p2, axiom, ! [R] : (rating_gt_four(R) => listed_in_yelp(R))).
fof(p3, axiom, ? [R] : ( ~provides_takeout(R) & many_negative_reviews(R) )).
fof(p4, axiom, ! [R] : (popular_local(R) => rating_gt_four(R))).
fof(p5, axiom, rating_gt_four(hamden_plaza) | popular_local(hamden_plaza)).
fof(conclusion, conjecture, ~provides_takeout(hamden_plaza)).