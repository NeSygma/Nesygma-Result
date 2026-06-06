fof(rule1, axiom, ! [R] : (listed_in_yelp(R) => ~many_negative_reviews(R))).
fof(rule2, axiom, ! [R] : (high_rating(R) => listed_in_yelp(R))).
fof(rule3, axiom, ? [R] : (~take_out(R) & many_negative_reviews(R))).
fof(rule4, axiom, ! [R] : (popular(R) => high_rating(R))).
fof(rule5, axiom, (high_rating(hamden_plaza) | popular(hamden_plaza))).
fof(goal, conjecture, ~take_out(hamden_plaza)).