% Problem: du Maurier Classic - Negative (negated claim)
% Premises
fof(winner_is_steinhauer, axiom, winner(steinhauer, du_maurier_1992)).
fof(steinhauer_participated, axiom, participated(steinhauer, du_maurier_1992)).
fof(six_way_tie, axiom, tie_on_leaderboard(du_maurier_1992)).
fof(one_belgian_in_tie, axiom, ? [X] : (from_country(X, belgium) & on_leaderboard(X, du_maurier_1992))).
fof(descampe_belgian, axiom, from_country(descampe, belgium)).
fof(descampe_on_leaderboard, axiom, on_leaderboard(descampe, du_maurier_1992)).
fof(leaderboard_participation, axiom, ! [X] : (on_leaderboard(X, du_maurier_1992) => participated(X, du_maurier_1992))).

% Distinctness axioms
fof(distinct_people, axiom, (steinhauer != descampe)).

% Negated conclusion
fof(goal, conjecture, winner(steinhauer, du_maurier_1992)).