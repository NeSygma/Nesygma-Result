% Negative version: negated conclusion as conjecture
% Predicates:
% listed(X) - X is listed in Yelp's recommendations
% many_neg_reviews(X) - X has received many negative reviews
% rating_gt_four(X) - X has a rating greater than four
% takeout(X) - X provides take-out service
% popular_local(X) - X is popular among local residents

% Constants:
% hamden_subway - The Hamden Plaza Subway store

fof(distinct, axiom, $true).

fof(premise1, axiom, ! [X] : (listed(X) => ~many_neg_reviews(X))).
fof(premise2, axiom, ! [X] : (rating_gt_four(X) => listed(X))).
fof(premise3, axiom, ? [X] : (~takeout(X) & many_neg_reviews(X))).
fof(premise4, axiom, ! [X] : (popular_local(X) => rating_gt_four(X))).
fof(premise5, axiom, rating_gt_four(hamden_subway) | popular_local(hamden_subway)).

% Negated conclusion: ~((takeout(hamden_subway) & many_neg_reviews(hamden_subway)) => (rating_gt_four(hamden_subway) & ~takeout(hamden_subway)))
% Which is equivalent to: (takeout(hamden_subway) & many_neg_reviews(hamden_subway)) & ~(rating_gt_four(hamden_subway) & ~takeout(hamden_subway))
% Which simplifies to: takeout(hamden_subway) & many_neg_reviews(hamden_subway) & (~rating_gt_four(hamden_subway) | takeout(hamden_subway))
% Since takeout is true, the second part is trivially satisfied, so: takeout(hamden_subway) & many_neg_reviews(hamden_subway)
fof(negated_conclusion, conjecture, takeout(hamden_subway) & many_neg_reviews(hamden_subway)).