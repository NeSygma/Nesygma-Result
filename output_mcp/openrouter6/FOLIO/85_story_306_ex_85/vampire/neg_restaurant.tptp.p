fof(premise1, axiom, ! [R] : (yelp_recommend(R) => ~many_negative_reviews(R))).
fof(premise2, axiom, ! [R] : (high_rating(R) => yelp_recommend(R))).
fof(premise3, axiom, ? [R] : (~take_out(R) & many_negative_reviews(R))).
fof(premise4, axiom, ! [R] : (popular(R) => high_rating(R))).
fof(premise5, axiom, high_rating(hamden) | popular(hamden)).
fof(neg_conclusion, conjecture, ~take_out(hamden) & many_negative_reviews(hamden)).