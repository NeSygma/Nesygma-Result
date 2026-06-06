% Negative file: conjecture is "Descampe is NOT in the six-way tie"
fof(distinct, axiom, steinhauer != descampe).

fof(premise_1, axiom, winner_of_1992_du_maurier(steinhauer)).
fof(premise_2, axiom, participated_in_1992_du_maurier(steinhauer)).

% There exists a six-way tie on the leaderboard, and one person in it is from Belgium
fof(premise_3a, axiom, ? [X] : in_six_way_tie(X)).
fof(premise_3b, axiom, ? [X] : (in_six_way_tie(X) & from_belgium(X))).

% Descampe is from Belgium and on the leaderboard
fof(premise_4a, axiom, from_belgium(descampe)).
fof(premise_4b, axiom, on_leaderboard_of_1992_du_maurier(descampe)).

% All people on the leaderboard participated
fof(premise_5, axiom, ! [X] : (on_leaderboard_of_1992_du_maurier(X) => participated_in_1992_du_maurier(X))).

% Negated conclusion: Descampe is NOT in the six-way tie
fof(negated_conclusion, conjecture, ~in_six_way_tie(descampe)).