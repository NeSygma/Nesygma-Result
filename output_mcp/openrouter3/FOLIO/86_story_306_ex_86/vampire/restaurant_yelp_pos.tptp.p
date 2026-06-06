% Restaurant Yelp Problem - Positive Version
% Premises
fof(premise_1, axiom, ! [R] : (listed_in_yelp(R) => ~many_negative_reviews(R))).
fof(premise_2, axiom, ! [R] : (rating_gt_4(R) => listed_in_yelp(R))).
fof(premise_3, axiom, ? [R] : (~provides_take_out(R) & many_negative_reviews(R))).
fof(premise_4, axiom, ! [R] : (popular_among_locals(R) => rating_gt_4(R))).
fof(premise_5, axiom, rating_gt_4(hamden_plaza_subway) | popular_among_locals(hamden_plaza_subway)).

% Conclusion to evaluate
fof(conclusion, conjecture, ~provides_take_out(hamden_plaza_subway)).