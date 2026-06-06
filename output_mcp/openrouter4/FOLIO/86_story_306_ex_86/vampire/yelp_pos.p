fof(premise1, axiom, ! [X] : (listed_in_yelp(X) => ~many_negative_reviews(X))).
fof(premise2, axiom, ! [X] : (rating_greater_than_four(X) => listed_in_yelp(X))).
fof(premise3, axiom, ? [X] : (~provides_takeout(X) & many_negative_reviews(X))).
fof(premise4, axiom, ! [X] : (popular_locally(X) => rating_greater_than_four(X))).
fof(premise5, axiom, rating_greater_than_four(hamden_plaza) | popular_locally(hamden_plaza)).

fof(conclusion, conjecture, ~provides_takeout(hamden_plaza)).