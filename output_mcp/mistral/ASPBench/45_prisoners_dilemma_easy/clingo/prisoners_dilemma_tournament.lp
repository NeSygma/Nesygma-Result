% ===== DOMAINS =====

% Define all strategies explicitly
strategy("COOP").
strategy("DEFECT").
strategy("TFT").
strategy("GTFT").
strategy("RAND").

% Time steps: 0 to 99 (100 rounds)
time(0..99).

% ===== MATCH STRUCTURE =====

% Round-robin: each ordered pair (S1, S2) plays a match
% This includes self-matches (e.g., COOP vs COOP)
match(S1, S2) :- strategy(S1), strategy(S2).

% ===== PAYOFF MATRIX =====

% payoff(Move1, Move2, Score1, Score2)
% Both cooperate
payoff("C", "C", 3, 3).

% Both defect
payoff("D", "D", 1, 1).

% One defects, other cooperates
payoff("D", "C", 5, 0).  % Defector gets 5, cooperator gets 0
payoff("C", "D", 0, 5).  % Cooperator gets 0, defector gets 5

% ===== STRATEGY BEHAVIORS =====

% --- COOP: Always Cooperate ---
move("COOP", S2, T, "C") :- match("COOP", S2), time(T).

% --- DEFECT: Always Defect ---
move("DEFECT", S2, T, "D") :- match("DEFECT", S2), time(T).

% --- TFT: Tit-for-Tat ---
% First move is cooperate
move("TFT", S2, 0, "C") :- match("TFT", S2).

% Subsequent moves copy opponent's last move
move("TFT", S2, T, M) :- match("TFT", S2), time(T), T > 0,
                      move(S2, "TFT", T-1, M).

% --- GTFT: Generous Tit-for-Tat ---
% First move is cooperate
move("GTFT", S2, 0, "C") :- match("GTFT", S2).

% Allow GTFT to forgive opponent's defection with 10% probability over 100 rounds
% We model forgiveness as a choice with constraints to enforce at most 10 forgiveness events
{ forgive("GTFT", S2, T) } :- match("GTFT", S2), strategy(S2), time(T), T > 0,
                           move(S2, "GTFT", T-1, "D").

% Constraint: GTFT can forgive at most 10 times over 100 rounds
:- match("GTFT", S2), strategy(S2), #count{T : forgive("GTFT", S2, T)} > 10.

% GTFT's move: if opponent defected last round and forgiveness is chosen this round, play C; otherwise copy opponent's move
move("GTFT", S2, T, "C") :- match("GTFT", S2), strategy(S2), time(T), T > 0,
                           move(S2, "GTFT", T-1, "D"),
                           forgive("GTFT", S2, T).

move("GTFT", S2, T, M) :- match("GTFT", S2), strategy(S2), time(T), T > 0,
                       move(S2, "GTFT", T-1, M),
                       not (move(S2, "GTFT", T-1, "D"), forgive("GTFT", S2, T)).

% --- RAND: Random Strategy ---
% Allow both choices to be made
{ rand_choice("RAND", S2, T, "C") ; rand_choice("RAND", S2, T, "D") } :- match("RAND", S2), time(T).

% RAND's actual move based on the random choice
move("RAND", S2, T, "C") :- match("RAND", S2), time(T), rand_choice("RAND", S2, T, "C").
move("RAND", S2, T, "D") :- match("RAND", S2), time(T), rand_choice("RAND", S2, T, "D").

% ===== SYMMETRIC MOVES =====

% The opponent's move in the same match is needed to calculate payoffs correctly
% This ensures move(S2,S1,T,M) is derived for every match(S1,S2)
move(S2, S1, T, M) :- move(S1, S2, T, M), match(S1, S2), time(T).

% ===== ROUND SCORE CALCULATION =====

% Score for S1 in match against S2 in round T
% Use payoff matrix to derive scores
round_score(S1, S2, T, Score1, Score2) :-
    move(S1, S2, T, M1),
    move(S2, S1, T, M2),
    payoff(M1, M2, Score1, Score2).

% ===== TOTAL SCORE CALCULATION =====

% Total score for a strategy across all matches
% Each strategy plays against all 5 strategies (including itself) for 100 rounds
% So total rounds per strategy = 5 * 100 = 500
total_score(S, Total) :-
    Total = #sum { Score1 : match(S, O), strategy(O), time(T),
                   round_score(S, O, T, Score1, _) }.

% ===== OUTPUT =====

% Show tournament results: strategies with their total scores
% This will list all strategies and their computed total scores
tournament_results(S, Total) :- total_score(S, Total).

#show tournament_results/2.

% ===== OPTIMIZATION =====

% Find the strategy that maximizes total score
#maximize { Score : total_score(S, Score) }.

% ===== WINNER IDENTIFICATION =====

% Compute the maximum total score
max_total_score(Max) :- tournament_results(_, Max), not tournament_results(_, Larger), Larger > Max.

% Identify the winner(s) as the strategy(ies) with the maximum total score
winner(S) :- total_score(S, Max), max_total_score(Max).

% Show the winner(s)
#show winner/1.

% Show the total score for the winner(s)
winner_score(S, Score) :- winner(S), total_score(S, Score).

#show winner_score/2.

% Show the total number of strategies for verification
num_strategies(N) :- N = #count { S : strategy(S) }.

#show num_strategies/1.