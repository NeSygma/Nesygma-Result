% Prisoners' Dilemma Tournament with deterministic RAND (alternating C/D)
% Strategies
strategy(coop).
strategy(defect).
strategy(tft).
strategy(gtft).
strategy(rand).

% Matches (round-robin, including self-play)
match(S1, S2) :- strategy(S1), strategy(S2).

% Rounds per match
round(1..100).

% Move definitions per strategy per round
% COOP: always C
move(coop, Opp, R, "C") :- match(coop, Opp), round(R).

% DEFECT: always D
move(defect, Opp, R, "D") :- match(defect, Opp), round(R).

% TFT: first round C, then copy opponent's last move
move(tft, Opp, 1, "C") :- match(tft, Opp).
move(tft, Opp, R, M) :- match(tft, Opp), round(R), R > 1, round(R-1),
    move(Opp, tft, R-1, M).  % copy opponent's previous move

% GTFT: like TFT but forgives defection 10% of the time
% Define when opponent defected in previous round
opponent_defeated(gtft, Opp, R) :- match(gtft, Opp), round(R), R > 1,
    move(Opp, gtft, R-1, "D").
% Allow forgiveness: up to 10 times per match (exactly 10% of rounds)
{ forgive(gtft, Opp, R) : opponent_defeated(gtft, Opp, R) } 10 :- match(gtft, Opp).
% GTFT move: if forgiven, cooperate; else copy opponent's last move
move(gtft, Opp, 1, "C") :- match(gtft, Opp).
move(gtft, Opp, R, "C") :- match(gtft, Opp), round(R), forgive(gtft, Opp, R).
move(gtft, Opp, R, M) :- match(gtft, Opp), round(R), R > 1, round(R-1),
    not forgive(gtft, Opp, R),
    move(Opp, gtft, R-1, M).

% RAND: deterministic alternating C/D (odd rounds C, even rounds D)
move(rand, Opp, R, "C") :- match(rand, Opp), round(R), R mod 2 = 1.
move(rand, Opp, R, "D") :- match(rand, Opp), round(R), R mod 2 = 0.

% Payoff matrix
payoff("C", "C", 3, 3).
payoff("D", "D", 1, 1).
payoff("C", "D", 0, 5).
payoff("D", "C", 5, 0).

% Compute payoff per round for each match
payoff(S1, S2, R, P1, P2) :-
    match(S1, S2), round(R),
    move(S1, S2, R, M1), move(S2, S1, R, M2),
    payoff(M1, M2, P1, P2).

% Total score per match per strategy
total_match_score(S1, S2, Score1) :-
    match(S1, S2),
    Score1 = #sum { P1, R : payoff(S1, S2, R, P1, _) }.

% Total score across all matches for each strategy
total_score(S, Score) :-
    strategy(S),
    Score = #sum { M_Score, Opp : total_match_score(S, Opp, M_Score) }.

% Find the strategy with maximum total score
max_score(Max) :- Max = #max { Score, S : total_score(S, Score) }.
winner(W) :- total_score(W, Max), max_score(Max).

% Tournament results: list of strategies with total scores sorted descending
#show total_score/2.
#show winner/1.