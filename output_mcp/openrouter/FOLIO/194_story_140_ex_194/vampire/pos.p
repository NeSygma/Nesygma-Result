% Positive version: claim that Steinhauer was not the winner
fof(a1, axiom, winner(steinhauer)).
fof(a2, axiom, participated(steinhauer)).
fof(a3, axiom, ? [X] : (tie6(X) & from_belgium(X))).
fof(a4, axiom, from_belgium(descampe)).
fof(a5, axiom, on_leaderboard(descampe)).
fof(a6, axiom, ! [X] : (on_leaderboard(X) => participated(X))).
fof(goal_pos, conjecture, ~winner(steinhauer)).