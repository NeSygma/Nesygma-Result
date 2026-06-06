% Prisoners' Dilemma Tournament in ASP

% ===== STRATEGIES =====
strategy("COOP").
strategy("DEFECT").
strategy("TFT").
strategy("GTFT").
strategy("RAND").

% ===== ROUNDS =====
round(1..100).

% ===== MATCHES (Round-robin: each strategy plays against all others including itself) =====
match(S1, S2) :- strategy(S1), strategy(S2).

% ===== MOVE GENERATION =====
% For each match and each round, each strategy plays a move
{ move(S, R, M) : move_type(M) } 1 :- match(S, _), round(R).

% Move types
move_type("C").
move_type("D").

% ===== STRATEGY BEHAVIORS =====

% COOP: Always plays C
move("COOP", R, "C") :- round(R).

% DEFECT: Always plays D
move("DEFECT", R, "D") :- round(R).

% TFT: Plays C first, then copies opponent's last move
% For round 1: TFT plays C
move("TFT", 1, "C") :- round(1).
% For rounds > 1: TFT copies opponent's previous move
move("TFT", R, M) :- 
    round(R), R > 1,
    match("TFT", Opp),
    move(Opp, R-1, M).

% GTFT: Like TFT but forgives defection 10% of the time
% For round 1: GTFT plays C
move("GTFT", 1, "C") :- round(1).
% For rounds > 1: GTFT copies opponent's previous move with 10% forgiveness
% We model forgiveness as a choice: either forgive (play C) or copy opponent's move
forgive("GTFT", R) :- round(R), R > 1.
{ move("GTFT", R, "C") } :- forgive("GTFT", R).
move("GTFT", R, M) :- 
    round(R), R > 1,
    match("GTFT", Opp),
    move(Opp, R-1, M),
    not forgive("GTFT", R).

% RAND: Plays C or D with 50% probability each
% For each round, RAND randomly chooses C or D
{ move("RAND", R, "C") } 1 :- round(R).
{ move("RAND", R, "D") } 1 :- round(R).

% ===== PAYOFF CALCULATION =====
% Payoff matrix:
% Both cooperate: (3, 3)
% Both defect: (1, 1)
% One defects, other cooperates: (5, 0)

% Calculate payoff for each strategy in each round of each match
payoff(S1, R, P) :-
    match(S1, S2),
    round(R),
    move(S1, R, M1),
    move(S2, R, M2),
    P = #sum { 
        3 : M1 = "C", M2 = "C";
        1 : M1 = "D", M2 = "D";
        5 : M1 = "D", M2 = "C";
        0 : M1 = "C", M2 = "D"
    }.

% ===== TOTAL SCORE CALCULATION =====
% Sum payoffs across all matches and rounds
total_score(S, T) :-
    strategy(S),
    T = #sum { P, R, Opp : payoff(S, R, P), match(S, Opp) }.

% ===== WINNER DETERMINATION =====
% Find the strategy with the highest total score
max_score(Max) :- Max = #max { T : total_score(_, T) }.
winner(S) :- strategy(S), total_score(S, T), max_score(Max), T = Max.

% ===== OUTPUT =====
#show strategy/1.
#show total_score/2.
#show winner/1.
#show match/2.
#show payoff/3.