% Axioms
fof(winner_steinhauer, axiom, winner(steinhauer)).
fof(unique_winner, axiom, ! [X] : (winner(X) => X = steinhauer)).
fof(steinhauer_participated, axiom, participated(steinhauer)).
fof(six_way_tie_exists, axiom, ? [X] : (in_six_way_tie(X) & from_belgium(X))).
fof(six_way_tie_on_leaderboard, axiom, ! [X] : (in_six_way_tie(X) => on_leaderboard(X))).
fof(all_leaderboard_participated, axiom, ! [X] : (on_leaderboard(X) => participated(X))).
fof(descampe_from_belgium, axiom, from_belgium(descampe)).
fof(descampe_on_leaderboard, axiom, on_leaderboard(descampe)).
fof(conclusion, conjecture, ~in_six_way_tie(descampe)).