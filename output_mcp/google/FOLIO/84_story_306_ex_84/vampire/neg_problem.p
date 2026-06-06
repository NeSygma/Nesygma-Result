fof(p1, axiom, ! [R] : (yelp_rec(R) => ~many_neg_reviews(R))).
fof(p2, axiom, ! [R] : (rating_gt_4(R) => yelp_rec(R))).
fof(p3, axiom, ? [R] : (~take_out(R) & many_neg_reviews(R))).
fof(p4, axiom, ! [R] : (popular(R) => rating_gt_4(R))).
fof(p5, axiom, (rating_gt_4(hamden_plaza_subway) | popular(hamden_plaza_subway))).
fof(goal, conjecture, ~((take_out(hamden_plaza_subway) & many_neg_reviews(hamden_plaza_subway)) => (rating_gt_4(hamden_plaza_subway) & ~take_out(hamden_plaza_subway)))).