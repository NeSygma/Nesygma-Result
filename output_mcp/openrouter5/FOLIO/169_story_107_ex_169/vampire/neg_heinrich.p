% Negative version: negated conclusion as conjecture
% Negation of "No politicians are part of the Nazi Reichstag"
% i.e., ~(! [X] : (politician(X) => ~member_of_nazi_reichstag(X)))
% which is equivalent to ? [X] : (politician(X) & member_of_nazi_reichstag(X))

fof(premise_1, axiom, german_politician(heinrich_schmidt)).
fof(premise_2, axiom, member_of_prussian_parliament(heinrich_schmidt)).
fof(premise_3, axiom, member_of_nazi_reichstag(heinrich_schmidt)).

fof(politician_def, axiom, ! [X] : (german_politician(X) => politician(X))).

% Negated conclusion: There exists a politician who is a member of the Nazi Reichstag
fof(goal_neg, conjecture, ? [X] : (politician(X) & member_of_nazi_reichstag(X))).