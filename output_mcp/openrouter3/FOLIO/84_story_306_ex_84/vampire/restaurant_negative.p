% Restaurant Yelp Problem - Negative Version
fof(distinct_entities, axiom, hamden_plaza_subway != other_restaurant).
fof(premise_1, axiom, ! [X] : (listed_in_yelp(X) => ~many_negative_reviews(X))).
fof(premise_2, axiom, ! [X] : (rating_greater_than_four(X) => listed_in_yelp(X))).
fof(premise_3, axiom, ? [X] : (~provides_take_out(X) & many_negative_reviews(X))).
fof(premise_4, axiom, ! [X] : (popular_among_locals(X) => rating_greater_than_four(X))).
fof(premise_5, axiom, rating_greater_than_four(hamden_plaza_subway) | popular_among_locals(hamden_plaza_subway)).
fof(conclusion_negation, conjecture, ~( (provides_take_out(hamden_plaza_subway) & many_negative_reviews(hamden_plaza_subway)) => (rating_greater_than_four(hamden_plaza_subway) & ~provides_take_out(hamden_plaza_subway)) )).