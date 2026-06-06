% Positive: conclusion "Steinhauer was not the winner"
fof(axiom1, axiom, winner(dmc1992, steinhauer)).
fof(axiom2, axiom, participant(steinhauer, dmc1992)).
fof(axiom3, axiom, on_leaderboard(descampe, dmc1992)).
fof(axiom4, axiom, from_country(descampe, belgium)).
fof(axiom5, axiom, ! [X] : (on_leaderboard(X, dmc1992) => participant(X, dmc1992))).

% Distinct tie members
fof(axiom6, axiom, (t1 != t2 & t1 != t3 & t1 != t4 & t1 != t5 & t1 != descampe &
                    t2 != t3 & t2 != t4 & t2 != t5 & t2 != descampe &
                    t3 != t4 & t3 != t5 & t3 != descampe &
                    t4 != t5 & t4 != descampe &
                    t5 != descampe)).

% Tie group membership
fof(axiom7, axiom, tie_group(t1)).
fof(axiom8, axiom, tie_group(t2)).
fof(axiom9, axiom, tie_group(t3)).
fof(axiom10, axiom, tie_group(t4)).
fof(axiom11, axiom, tie_group(t5)).
fof(axiom12, axiom, tie_group(descampe)).

% Tie members are on the leaderboard
fof(axiom13, axiom, ! [X] : (tie_group(X) => on_leaderboard(X, dmc1992))).

% Exactly these six are tied (no other tie members)
fof(axiom14, axiom, ! [X] : (tie_group(X) => (X = t1 | X = t2 | X = t3 | X = t4 | X = t5 | X = descampe))).

% Conclusion: Steinhauer was not the winner
fof(goal, conjecture, ~winner(dmc1992, steinhauer)).