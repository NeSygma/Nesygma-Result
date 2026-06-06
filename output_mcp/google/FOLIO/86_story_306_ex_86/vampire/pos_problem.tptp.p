fof(p1, axiom, ! [R] : (yelp_recommended(R) => ~many_negative_reviews(R))).
fof(p2, axiom, ! [R] : (rating_gt_four(R) => yelp_recommended(R))).
fof(p3, axiom, ? [R] : (~take_out(R) & many_negative_reviews(R))).
fof(p4, axiom, ! [R] : (popular_local(R) => rating_gt_four(R))).
fof(p5, axiom, (rating_gt_four(hamden_plaza_subway) | popular_local(hamden_plaza_subway))).
fof(goal, conjecture, ~take_out(hamden_plaza_subway)).