fof(yelp_recommendation_implies_few_neg_reviews, axiom, 
    ! [R] : (yelp_recommended(R) => ~many_negative_reviews(R))).

fof(rating_gt4_implies_yelp_recommended, axiom, 
    ! [R] : (rating_gt4(R) => yelp_recommended(R))).

fof(some_no_takeout_get_many_neg_reviews, axiom, 
    ? [R] : (~provides_takeout(R) & many_negative_reviews(R))).

fof(popular_implies_rating_gt4, axiom, 
    ! [R] : (popular_among_locals(R) => rating_gt4(R))).

fof(hamden_plaza_rating_or_popular, axiom, 
    rating_gt4(hamden_plaza_subway) | popular_among_locals(hamden_plaza_subway)).

fof(negated_conclusion, conjecture, 
    ~((provides_takeout(hamden_plaza_subway) & many_negative_reviews(hamden_plaza_subway)) =>
    (rating_gt4(hamden_plaza_subway) & ~provides_takeout(hamden_plaza_subway)))).