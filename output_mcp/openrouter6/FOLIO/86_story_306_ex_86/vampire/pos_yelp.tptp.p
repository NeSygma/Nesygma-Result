tff(restaurant_type, type, restaurant: $tType).
tff(rating_type, type, rating: restaurant > $int).
tff(listed_in_yelp_type, type, listed_in_yelp: restaurant > $o).
tff(many_negative_reviews_type, type, many_negative_reviews: restaurant > $o).
tff(take_out_type, type, take_out: restaurant > $o).
tff(popular_type, type, popular: restaurant > $o).
tff(hamden_plaza_decl, type, hamden_plaza: restaurant).

tff(rule1, axiom, ! [R: restaurant] : (listed_in_yelp(R) => ~many_negative_reviews(R))).
tff(rule2, axiom, ! [R: restaurant] : ($greater(rating(R), 4) => listed_in_yelp(R))).
tff(rule3, axiom, ? [R: restaurant] : (~take_out(R) & many_negative_reviews(R))).
tff(rule4, axiom, ! [R: restaurant] : (popular(R) => $greater(rating(R), 4))).
tff(rule5, axiom, ($greater(rating(hamden_plaza), 4) | popular(hamden_plaza))).

tff(conclusion, conjecture, ~take_out(hamden_plaza)).