fof(yelp_implies_not_many_negative, axiom, ! [R] : (yelp_recommended(R) => not_many_negative_reviews(R))).
fof(rating_gt4_implies_yelp, axiom, ! [R] : (rating_gt4(R) => yelp_recommended(R))).
fof(exists_restaurant, axiom, ~take_out(x_restaurant) & many_negative_reviews(x_restaurant)).
fof(popular_local_implies_rating_gt4, axiom, ! [R] : (popular_local(R) => rating_gt4(R))).
fof(hamden_plaza_disjunction, axiom, rating_gt4(hamden_plaza_subway) | popular_local(hamden_plaza_subway)).
fof(distinct_restaurants, axiom, hamden_plaza_subway != x_restaurant).
fof(conjecture, conjecture, (take_out(hamden_plaza_subway) & many_negative_reviews(hamden_plaza_subway)) => (rating_gt4(hamden_plaza_subway) & ~take_out(hamden_plaza_subway))).