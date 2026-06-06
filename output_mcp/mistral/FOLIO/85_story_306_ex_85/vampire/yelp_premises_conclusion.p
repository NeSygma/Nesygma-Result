fof(yelp_recommended_implies_no_many_neg_reviews, axiom, 
    ! [R] : (yelp_recommended(R) => ~many_negative_reviews(R))).

fof(rating_gt4_implies_yelp_recommended, axiom, 
    ! [R] : (rating_greater_than_four(R) => yelp_recommended(R))).

fof(some_no_takeout_many_neg_reviews, axiom, 
    ? [R] : (~provides_takeout(R) & many_negative_reviews(R))).

fof(popular_implies_rating_gt4, axiom, 
    ! [R] : (popular_among_locals(R) => rating_greater_than_four(R))).

fof(hamden_plaza_subway_rating_or_popular, axiom, 
    rating_greater_than_four(hamden_plaza_subway) | popular_among_locals(hamden_plaza_subway)).

fof(conclusion, conjecture, 
    provides_takeout(hamden_plaza_subway) | ~many_negative_reviews(hamden_plaza_subway)).