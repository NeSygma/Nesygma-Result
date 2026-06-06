% --- Domain Definitions ---
strategy("COOP"). strategy("DEFECT"). strategy("TFT").
opponent_type("type_A"). opponent_type("type_B"). opponent_type("type_C").
round(1). round(2).

% --- Opponent Pool ---
opponent_count("type_A", 5).
opponent_count("type_B", 3).
opponent_count("type_C", 2).

% --- Payoff Matrix ---
payoff("C", "C", 3).
payoff("D", "C", 5).
payoff("C", "D", 0).
payoff("D", "D", 1).

% --- Strategy Logic ---
% Ego's move
ego_move("COOP", R, "C") :- round(R).
ego_move("DEFECT", R, "D") :- round(R).

% TFT: R1 'C', R2 copies opponent's R1 move
ego_move("TFT", 1, "C").
ego_move("TFT", 2, OppR1) :- opponent_move("TFT", "type_A", 1, OppR1).
ego_move("TFT", 2, OppR1) :- opponent_move("TFT", "type_B", 1, OppR1).
ego_move("TFT", 2, OppR1) :- opponent_move("TFT", "type_C", 1, OppR1).

% Opponent's move
% type_A: Always D
opponent_move(EgoS, "type_A", R, "D") :- strategy(EgoS), round(R).

% type_B: R1 'C', R2 copies Ego's R1 move
opponent_move(EgoS, "type_B", 1, "C") :- strategy(EgoS).
opponent_move(EgoS, "type_B", 2, EgoR1) :- strategy(EgoS), ego_move(EgoS, 1, EgoR1).

% type_C: Always C
opponent_move(EgoS, "type_C", R, "C") :- strategy(EgoS), round(R).

% --- Score Calculation ---
score(EgoS, OppT, R, P) :- strategy(EgoS), opponent_type(OppT), round(R),
                           ego_move(EgoS, R, EM), opponent_move(EgoS, OppT, R, OM),
                           payoff(EM, OM, P).

total_score_per_matchup(EgoS, OppT, TotalP) :- strategy(EgoS), opponent_type(OppT),
                                               TotalP = #sum { P, R : score(EgoS, OppT, R, P) }.

expected_total_score(EgoS, TotalExpected) :- strategy(EgoS),
                                             TotalExpected = #sum { P*Count, OppT : total_score_per_matchup(EgoS, OppT, P), opponent_count(OppT, Count) }.

% --- Objective ---
max_score(M) :- M = #max { S : expected_total_score(_, S) }.
best_strategy(EgoS) :- expected_total_score(EgoS, S), max_score(S).

% --- Output ---
option(EgoS) :- best_strategy(EgoS).
#show expected_total_score/2.
#show option/1.