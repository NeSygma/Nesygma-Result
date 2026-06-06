% Negative version: negated conclusion as conjecture
% Negated conclusion: Some member of Pappy's has starred in a show piloting on BBC Two or BBC Three.
fof(distinct_channels, axiom, (bbc_two != bbc_three & bbc_two != bbc_three_alt & bbc_three != bbc_three_alt)).
fof(badults_is_show, axiom, badults = badults_show).

% Premise 1: Badults is a British Sitcom series starring members of Pappy's.
fof(premise1, axiom, ! [X] : (member_of_pappys(X) & stars_in(X, badults))).

% Premise 2: Badults was piloted in July 2013 on BBC Three.
fof(premise2, axiom, pilots_on(badults, bbc_three)).

% Negated conclusion: There exists a member of Pappy's who starred in a show piloting on BBC Two or BBC Three.
fof(neg_conclusion, conjecture, ? [X, Y, Z] : (member_of_pappys(X) & stars_in(X, Y) & pilots_on(Y, Z) & (Z = bbc_two | Z = bbc_three))).