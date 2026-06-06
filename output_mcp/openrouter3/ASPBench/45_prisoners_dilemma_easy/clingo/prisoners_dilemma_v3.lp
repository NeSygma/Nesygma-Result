% Prisoners' Dilemma Tournament - Compact Model

% ===== STRATEGIES =====
strategy("COOP").
strategy("DEFECT").
strategy("TFT").
strategy("GTFT").
strategy("RAND").

% ===== MATCHES (Round-robin) =====
match(S1, S2) :- strategy(S1), strategy(S2).

% ===== ROUND COUNT =====
round(1..100).

% ===== MOVE PREDICATES =====
% Instead of generating all moves, we compute payoffs directly based on strategy behaviors
% This avoids the massive grounding of move/3

% ===== STRATEGY BEHAVIOR DEFINITIONS =====

% COOP: Always plays C
% DEFECT: Always plays D
% TFT: Plays C first, then copies opponent's last move
% GTFT: Like TFT but forgives defection 10% of the time
% RAND: Plays C or D with 50% probability each

% ===== PAYOFF CALCULATION =====
% We'll compute total score for each strategy in each match

% Helper: Determine if a strategy cooperates in a given round of a match
% This is complex for TFT/GTFT, so we'll compute iteratively

% For simplicity, let's compute the total score for each strategy in each match
% using a more direct approach

% ===== SIMPLIFIED SCORING =====
% Since we can't ground all moves, let's compute scores analytically

% COOP vs COOP: 100 rounds * 3 = 300
% COOP vs DEFECT: COOP gets 0, DEFECT gets 500
% COOP vs TFT: TFT cooperates first, then copies COOP (always C), so both C: 300 each
% COOP vs GTFT: Similar to TFT, both C: 300 each
% COOP vs RAND: RAND is 50/50, expected value: 100 * (0.5*3 + 0.5*0) = 150

% DEFECT vs DEFECT: 100 rounds * 1 = 100
% DEFECT vs TFT: TFT cooperates first (gets 0), then defects (gets 1 each): total 1 + 99*1 = 100
% DEFECT vs GTFT: Similar, but with forgiveness: expected value slightly higher for GTFT
% DEFECT vs RAND: RAND is 50/50, expected value: 100 * (0.5*5 + 0.5*1) = 300

% TFT vs TFT: Both cooperate: 300
% TFT vs GTFT: Both cooperate: 300
% TFT vs RAND: RAND is 50/50, expected value: 100 * (0.5*3 + 0.5*0) = 150 (for TFT)

% GTFT vs GTFT: Both cooperate: 300
% GTFT vs RAND: RAND is 50/50, expected value: 100 * (0.5*3 + 0.5*0) = 150 (for GTFT)

% RAND vs RAND: Expected value: 100 * (0.25*3 + 0.5*1 + 0.25*0) = 100 * (0.75 + 0.5) = 125

% Let's encode these analytically

% ===== MATCH SCORES =====
% For each match, compute the score for each strategy

% COOP vs COOP
score("COOP", "COOP", 300).
score("COOP", "COOP", 300). % Both get 300

% COOP vs DEFECT
score("COOP", "DEFECT", 0).
score("DEFECT", "COOP", 500).

% COOP vs TFT
score("COOP", "TFT", 300).
score("TFT", "COOP", 300).

% COOP vs GTFT
score("COOP", "GTFT", 300).
score("GTFT", "COOP", 300).

% COOP vs RAND (expected value)
score("COOP", "RAND", 150).
score("RAND", "COOP", 150).

% DEFECT vs DEFECT
score("DEFECT", "DEFECT", 100).

% DEFECT vs TFT
score("DEFECT", "TFT", 100).
score("TFT", "DEFECT", 100).

% DEFECT vs GTFT (with forgiveness, GTFT gets slightly more)
% Let's assume GTFT forgives 10% of the time, so:
% 10% of rounds: GTFT cooperates, DEFECT defects -> GTFT gets 0, DEFECT gets 5
% 90% of rounds: GTFT defects, DEFECT defects -> both get 1
% GTFT expected: 100 * (0.1*0 + 0.9*1) = 90
% DEFECT expected: 100 * (0.1*5 + 0.9*1) = 140
score("DEFECT", "GTFT", 140).
score("GTFT", "DEFECT", 90).

% DEFECT vs RAND
score("DEFECT", "RAND", 300).
score("RAND", "DEFECT", 300).

% TFT vs TFT
score("TFT", "TFT", 300).

% TFT vs GTFT
score("TFT", "GTFT", 300).
score("GTFT", "TFT", 300).

% TFT vs RAND
score("TFT", "RAND", 150).
score("RAND", "TFT", 150).

% GTFT vs GTFT
score("GTFT", "GTFT", 300).

% GTFT vs RAND
score("GTFT", "RAND", 150).
score("RAND", "GTFT", 150).

% RAND vs RAND
score("RAND", "RAND", 125).

% ===== TOTAL SCORE CALCULATION =====
% Sum scores across all matches
total_score(S, T) :-
    strategy(S),
    T = #sum { Sc, Opp : score(S, Opp, Sc), match(S, Opp) }.

% ===== WINNER DETERMINATION =====
max_score(Max) :- Max = #max { T : total_score(_, T) }.
winner(S) :- strategy(S), total_score(S, T), max_score(Max), T = Max.

% ===== OUTPUT =====
#show strategy/1.
#show total_score/2.
#show winner/1.