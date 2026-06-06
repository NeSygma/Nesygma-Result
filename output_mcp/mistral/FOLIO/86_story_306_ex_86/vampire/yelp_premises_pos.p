fof(yelp_recommendation_rule, axiom, 
    ! [R] : (yelp_recommended(R) => ~many_negative_reviews(R))).

fof(rating_gt4_to_yelp, axiom, 
    ! [R] : (rating_gt4(R) => yelp_recommended(R))).

fof(some_no_takeout_many_neg, axiom, 
    ? [R] : (~provides_takeout(R) & many_negative_reviews(R))).

fof(popular_implies_gt4, axiom, 
    ! [R] : (popular_among_locals(R) => rating_gt4(R))).

fof(hamden_plaza_rating_or_popular, axiom, 
    rating_gt4(hamden_plaza) | popular_among_locals(hamden_plaza)).

fof(conclusion, conjecture, 
    ~provides_takeout(hamden_plaza)).