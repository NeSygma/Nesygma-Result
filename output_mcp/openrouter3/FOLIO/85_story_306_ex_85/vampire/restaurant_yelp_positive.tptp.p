% Restaurant Yelp Problem - Positive Version
% Premises
fof(premise_1, axiom, ! [X] : (restaurant(X) & listed_in_yelp(X) => ~many_negative_reviews(X))).
fof(premise_2, axiom, ! [X] : (restaurant(X) & rating_gt_four(X) => listed_in_yelp(X))).
fof(premise_3, axiom, ? [X] : (restaurant(X) & ~take_out_service(X) & many_negative_reviews(X))).
fof(premise_4, axiom, ! [X] : (restaurant(X) & popular_local(X) => rating_gt_four(X))).
fof(premise_5, axiom, restaurant(hamden_plaza_subway) & (rating_gt_four(hamden_plaza_subway) | popular_local(hamden_plaza_subway))).

% Distinctness (only one constant, so not needed)
% Conclusion
fof(conclusion, conjecture, take_out_service(hamden_plaza_subway) | ~many_negative_reviews(hamden_plaza_subway)).