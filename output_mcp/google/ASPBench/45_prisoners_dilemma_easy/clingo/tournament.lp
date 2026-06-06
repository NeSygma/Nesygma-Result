% Strategies
strategy(coop). strategy(defect). strategy(tft). strategy(gtft). strategy(rand).

% Rounds
round(1..100).

% Payoff Matrix
payoff(c, c, 3, 3).
payoff(d, d, 1, 1).
payoff(c, d, 0, 5).
payoff(d, c, 5, 0).

% Moves: move(Strategy, Round, Move, Opponent)
% COOP: Always C
move(coop, R, c, Opp) :- round(R), strategy(Opp).

% DEFECT: Always D
move(defect, R, d, Opp) :- round(R), strategy(Opp).

% TFT: First C, then copy opponent's last move
move(tft, 1, c, Opp) :- strategy(Opp).
move(tft, R, M, Opp) :- round(R), R > 1, strategy(Opp), move(Opp, R-1, M, tft).

% GTFT: Like TFT but forgives defection 10% of the time.
% Let's assume it forgives on rounds 10, 20, 30, ..., 100.
move(gtft, 1, c, Opp) :- strategy(Opp).
move(gtft, R, c, Opp) :- round(R), R > 1, R \ 10 == 0, strategy(Opp).
move(gtft, R, M, Opp) :- round(R), R > 1, R \ 10 != 0, strategy(Opp), move(Opp, R-1, M, gtft).

% RAND: Plays C or D with 50% probability.
% Let's assume it plays C on odd rounds, D on even rounds.
move(rand, R, c, Opp) :- round(R), R \ 2 != 0, strategy(Opp).
move(rand, R, d, Opp) :- round(R), R \ 2 == 0, strategy(Opp).

% Match Score
% match_score(S1, S2, Score1)
match_score(S1, S2, Total) :-
    strategy(S1), strategy(S2),
    Total = #sum { P1, R : round(R), move(S1, R, M1, S2), move(S2, R, M2, S1), payoff(M1, M2, P1, P2) }.

% Total Score
total_score(S1, Total) :-
    strategy(S1),
    Total = #sum { Score, S2 : strategy(S2), match_score(S1, S2, Score) }.

% Winner
max_score(M) :- M = #max { S : total_score(_, S) }.
winner(S) :- total_score(S, M), max_score(M).

% Results
tournament_results(S, Score) :- total_score(S, Score).

#show tournament_results/2.
#show winner/1.