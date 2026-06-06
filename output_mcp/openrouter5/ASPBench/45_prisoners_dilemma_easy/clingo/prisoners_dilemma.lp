%%% Prisoners' Dilemma Tournament Solver - Optimized for Grounding %%%

% ========== DOMAINS ==========
strategy(coop; defect; tft; gtft; rand).
round(0..99).

% ========== MATCHES ==========
match(S1, S2) :- strategy(S1), strategy(S2).

% ========== DETERMINISTIC STRATEGY MOVES ==========

% COOP: Always plays C
move(coop, S2, R, c) :- match(coop, S2), round(R).

% DEFECT: Always plays D
move(defect, S2, R, d) :- match(defect, S2), round(R).

% TFT: Round 0 -> C; Round R (R>0) -> copy opponent's last move
move(tft, S2, 0, c) :- match(tft, S2).
move(tft, S2, R, A) :- match(tft, S2), round(R), R > 0,
                        move(S2, tft, R-1, A).

% GTFT: Round 0 -> C
move(gtft, S2, 0, c) :- match(gtft, S2).
% For R>0: normally copy opponent's last move
move(gtft, S2, R, A) :- match(gtft, S2), round(R), R > 0,
                         move(S2, gtft, R-1, A),
                         not forgive(gtft, S2, R).
% Forgiveness: if opponent defected at R-1, GTFT may play C instead
{ forgive(gtft, S2, R) } :- match(gtft, S2), round(R), R > 0,
                             move(S2, gtft, R-1, d).
move(gtft, S2, R, c) :- match(gtft, S2), round(R), R > 0,
                         forgive(gtft, S2, R).

% RAND: each round, random choice (must pick exactly one)
{ move(rand, S2, R, c) } :- match(rand, S2), round(R).
{ move(rand, S2, R, d) } :- match(rand, S2), round(R).
:- match(rand, S2), round(R), not move(rand, S2, R, c), not move(rand, S2, R, d).
:- match(rand, S2), round(R), move(rand, S2, R, c), move(rand, S2, R, d).

% Each strategy must have exactly one action per round per match
:- match(S1, S2), round(R), not move(S1, S2, R, c), not move(S1, S2, R, d).
:- match(S1, S2), round(R), move(S1, S2, R, c), move(S1, S2, R, d).

% ========== PAYOFFS ==========
% Both cooperate: (3,3)
payoff(S1, S2, R, 3) :- match(S1, S2), round(R),
                         move(S1, S2, R, c),
                         move(S2, S1, R, c).
% Both defect: (1,1)
payoff(S1, S2, R, 1) :- match(S1, S2), round(R),
                         move(S1, S2, R, d),
                         move(S2, S1, R, d).
% S1 defects, S2 cooperates: (5,0)
payoff(S1, S2, R, 5) :- match(S1, S2), round(R),
                         move(S1, S2, R, d),
                         move(S2, S1, R, c).
% S1 cooperates, S2 defects: (0,5)
payoff(S1, S2, R, 0) :- match(S1, S2), round(R),
                         move(S1, S2, R, c),
                         move(S2, S1, R, d).

% ========== SCORE CALCULATION ==========
total_score(S, Total) :- strategy(S),
    Total = #sum { P, S2, R : payoff(S, S2, R, P) }.

% ========== WINNER ==========
winner(S) :- total_score(S, Total), 
             Total = #max { T : total_score(_, T) }.

% ========== OUTPUT ==========
#show total_score/2.
#show winner/1.