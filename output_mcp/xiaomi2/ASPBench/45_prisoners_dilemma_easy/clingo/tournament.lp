% Prisoners' Dilemma Tournament in ASP

% Define strategies
strategy(coop).
strategy(defect).
strategy(tft).
strategy(gtft).
strategy(rand).

% Define rounds (1..100)
round(1..100).

% Define matches: each strategy plays against all others (including itself)
match(S1, S2) :- strategy(S1), strategy(S2).

% Define actions
action(c). % cooperate
action(d). % defect

% Define payoff matrix
payoff(c, c, 3, 3).
payoff(c, d, 0, 5).
payoff(d, c, 5, 0).
payoff(d, d, 1, 1).

% Helper: even and odd rounds
even(R) :- round(R), R2 = R / 2, R = R2 * 2.
odd(R) :- round(R), not even(R).

% Helper: forgiveness rounds for GTFT (every 10th round)
forgive(R) :- round(R), R10 = R / 10, R = R10 * 10.
not_forgive(R) :- round(R), not forgive(R).

% Strategy behaviors
% COOP: Always plays C
move(S1, S2, R, c) :- match(S1, S2), round(R), S1 = coop.

% DEFECT: Always plays D
move(S1, S2, R, d) :- match(S1, S2), round(R), S1 = defect.

% TFT: Plays C first, then copies opponent's last move
move(S1, S2, 1, c) :- match(S1, S2), S1 = tft.
move(S1, S2, R, A) :- match(S1, S2), round(R), R > 1, S1 = tft, 
                      R_prev = R - 1, move(S2, S1, R_prev, A).

% GTFT: Like TFT but forgives defection 10% of the time
move(S1, S2, 1, c) :- match(S1, S2), S1 = gtft.
% If opponent defected last round and we're not in a forgiveness round, defect
move(S1, S2, R, d) :- match(S1, S2), round(R), R > 1, S1 = gtft, 
                      R_prev = R - 1, move(S2, S1, R_prev, d), not_forgive(R).
% If opponent defected last round and we're in a forgiveness round, cooperate
move(S1, S2, R, c) :- match(S1, S2), round(R), R > 1, S1 = gtft, 
                      R_prev = R - 1, move(S2, S1, R_prev, d), forgive(R).
% If opponent cooperated last round, copy (like TFT)
move(S1, S2, R, c) :- match(S1, S2), round(R), R > 1, S1 = gtft, 
                      R_prev = R - 1, move(S2, S1, R_prev, c).

% RAND: Plays C or D with 50% probability each
% We'll model as alternating: odd rounds C, even rounds D
move(S1, S2, R, c) :- match(S1, S2), round(R), S1 = rand, odd(R).
move(S1, S2, R, d) :- match(S1, S2), round(R), S1 = rand, even(R).

% Calculate payoff for each round in each match
round_payoff(S1, S2, R, P1, P2) :- 
    match(S1, S2), round(R), 
    move(S1, S2, R, A1), move(S2, S1, R, A2),
    payoff(A1, A2, P1, P2).

% Calculate total score for each strategy across all matches
% First, calculate score in each match
match_score(S1, S2, Score1, Score2) :-
    match(S1, S2),
    Score1 = #sum { P1, R : round_payoff(S1, S2, R, P1, _) },
    Score2 = #sum { P2, R : round_payoff(S1, S2, R, _, P2) }.

% Then, calculate total score across all matches
total_score(S, Score) :-
    strategy(S),
    Score = #sum { Score1, S2 : match_score(S, S2, Score1, _) }.

% Find the winner (strategy with highest total score)
winner(S) :- 
    total_score(S, Score),
    Score = #max { Score2 : total_score(_, Score2) }.

% Output the results
#show total_score/2.
#show winner/1.