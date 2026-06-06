% Prisoners' Dilemma Tournament
% Strategies: COOP, DEFECT, TFT, GTFT, RAND

% Domain definitions
strategy(coop).
strategy(defect).
strategy(tft).
strategy(gtft).
strategy(rand).

% Rounds 1..100
round(1..100).

% Match pairs (including self-play)
match(S1, S2) :- strategy(S1), strategy(S2).

% First round moves (deterministic for most strategies)
% COOP always cooperates
move(coop, S, 1, coop_move) :- match(coop, S).
% DEFECT always defects
move(defect, S, 1, defect_move) :- match(defect, S).
% TFT cooperates first
move(tft, S, 1, coop_move) :- match(tft, S).
% GTFT cooperates first
move(gtft, S, 1, coop_move) :- match(gtft, S).
% RAND: choice for first round
{ move(rand, S, 1, coop_move) } :- match(rand, S).
{ move(rand, S, 1, defect_move) } :- match(rand, S).
% RAND must make exactly one move in round 1
:- move(rand, S, 1, M1), move(rand, S, 1, M2), M1 != M2.
% RAND must make some move
:- match(rand, S), round(1), not move(rand, S, 1, coop_move), not move(rand, S, 1, defect_move).

% Subsequent rounds (R > 1)
% COOP always cooperates
move(coop, S, R, coop_move) :- match(coop, S), round(R), R > 1.
% DEFECT always defects
move(defect, S, R, defect_move) :- match(defect, S), round(R), R > 1.

% TFT: copies opponent's last move
move(tft, S, R, M) :- match(tft, S), round(R), R > 1, move(S, tft, R-1, M).

% GTFT: like TFT but forgives defection 10% of the time
% We model forgiveness as a choice for each round where opponent defected
{ forgive(S, R) } :- match(gtft, S), round(R), R > 1, move(S, gtft, R-1, defect_move).
% If opponent cooperated, copy it
move(gtft, S, R, coop_move) :- match(gtft, S), round(R), R > 1, move(S, gtft, R-1, coop_move).
% If opponent defected and we forgive, cooperate
move(gtft, S, R, coop_move) :- match(gtft, S), round(R), R > 1, forgive(S, R).
% If opponent defected and we don't forgive, defect
move(gtft, S, R, defect_move) :- match(gtft, S), round(R), R > 1, move(S, gtft, R-1, defect_move), not forgive(S, R).

% RAND: choice for each round
{ move(rand, S, R, coop_move) } :- match(rand, S), round(R), R > 1.
{ move(rand, S, R, defect_move) } :- match(rand, S), round(R), R > 1.
% RAND must make exactly one move per round
:- move(rand, S, R, M1), move(rand, S, R, M2), M1 != M2.
:- match(rand, S), round(R), not move(rand, S, R, coop_move), not move(rand, S, R, defect_move).

% Payoff calculation
% Both cooperate: (3, 3)
payoff(S1, S2, R, 3) :- match(S1, S2), round(R), move(S1, S2, R, coop_move), move(S2, S1, R, coop_move).
% Both defect: (1, 1)
payoff(S1, S2, R, 1) :- match(S1, S2), round(R), move(S1, S2, R, defect_move), move(S2, S1, R, defect_move).
% S1 defects, S2 cooperates: (5, 0)
payoff(S1, S2, R, 5) :- match(S1, S2), round(R), move(S1, S2, R, defect_move), move(S2, S1, R, coop_move).
% S1 cooperates, S2 defects: (0, 5)
payoff(S1, S2, R, 0) :- match(S1, S2), round(R), move(S1, S2, R, coop_move), move(S2, S1, R, defect_move).

% Total score for each strategy across all matches and rounds
total_score(S, T) :- strategy(S), T = #sum { P, S2, R : payoff(S, S2, R, P) }.

% Find the winner (strategy with highest total score)
winner(S) :- total_score(S, T), T = #max { T2 : total_score(_, T2) }.

% Output
#show total_score/2.
#show winner/1.