% Negative version: negated conclusion as conjecture
% Predicates:
% listed(X) - X is listed in Yelp's recommendations
% many_neg_reviews(X) - X has received many negative reviews
% rating_gt_four(X) - X has a rating greater than four
% takeout(X) - X provides take-out service
% popular(X) - X is popular among local residents

fof(premise1, axiom, ! [X] : (listed(X) => ~many_neg_reviews(X))).
fof(premise2, axiom, ! [X] : (rating_gt_four(X) => listed(X))).
fof(premise3, axiom, ? [X] : (~takeout(X) & many_neg_reviews(X))).
fof(premise4, axiom, ! [X] : (popular(X) => rating_gt_four(X))).
fof(premise5, axiom, rating_gt_four(hamden_plaza_subway) | popular(hamden_plaza_subway)).

% Negated conclusion: NOT (takeout(hamden_plaza_subway) | ~many_neg_reviews(hamden_plaza_subway))
% = ~takeout(hamden_plaza_subway) & many_neg_reviews(hamden_plaza_subway)
fof(negated_conclusion, conjecture, ~takeout(hamden_plaza_subway) & many_neg_reviews(hamden_plaza_subway)).