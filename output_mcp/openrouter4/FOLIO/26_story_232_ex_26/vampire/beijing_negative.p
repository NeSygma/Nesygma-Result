% Negative run: negated claim that Beijing is located in southern China
fof(premise_1, axiom, capital_of_prc(beijing)).
fof(premise_2, axiom, capital_of_most_populous_nation(beijing)).
fof(premise_3, axiom, located_in_northern_china(beijing)).
fof(premise_4, axiom, hosted_2008_games(beijing)).
fof(premise_5, axiom, hosted_all_four_games(beijing)).
fof(premise_6, axiom, has_good_universities(beijing)).
% Northern China and southern China are mutually exclusive
fof(mutual_exclusivity, axiom, ! [X] : (located_in_northern_china(X) => ~located_in_southern_china(X))).
% Negated conclusion: Beijing is NOT located in southern China
fof(negated_conclusion, conjecture, ~located_in_southern_china(beijing)).