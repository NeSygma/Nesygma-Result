% Positive version: original claim as conjecture
% Premises

% The winner of the 1992 du Maurier Classic was Steinhauer.
fof(winner, axiom, winner_of(du_maurier_1992) = steinhauer).

% Steinhauer participated in the 1992 du Maurier Classic.
fof(steinhauer_participated, axiom, participated(steinhauer, du_maurier_1992)).

% One six-way tie was on the leaderboard, and one person in the six-way tie was from Belgium.
fof(six_way_tie_exists, axiom, ? [T] : (six_way_tie(T) & on_leaderboard(T, du_maurier_1992) & ? [P] : (person_in_tie(P, T) & from(P, belgium)))).

% Descampe is from Belgium and is on the leaderboard of the 1992 du Maurier Classic.
fof(descampe_belgium, axiom, from(descampe, belgium)).
fof(descampe_on_leaderboard, axiom, on_leaderboard_person(descampe, du_maurier_1992)).

% All people on the leaderboard of the 1992 du Maurier Classic participated in the 1992 du Maurier Classic.
fof(leaderboard_participate, axiom, ! [P] : (on_leaderboard_person(P, du_maurier_1992) => participated(P, du_maurier_1992))).

% Distinctness
fof(distinct, axiom, (descampe != steinhauer)).

% Conclusion: Descampe is in the six-way tie in the leaderboard of the 1992 du Maurier Classic.
fof(goal, conjecture, ? [T] : (six_way_tie(T) & on_leaderboard(T, du_maurier_1992) & person_in_tie(descampe, T))).