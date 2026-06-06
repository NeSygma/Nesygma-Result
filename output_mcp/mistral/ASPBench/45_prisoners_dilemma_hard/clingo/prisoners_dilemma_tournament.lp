% Domains
ego_strategy(COOP; DEFECT; TFT).
opponent_type(type_A; type_B; type_C).

% Opponent distribution (10 opponents total)
opponent_count(type_A, 5).
opponent_count(type_B, 3).
opponent_count(type_C, 2).

% Precomputed outcomes for each strategy pair (total score over 2 rounds)
% Format: outcome(EgoStrategy, OpponentType, TotalScore)
outcome(COOP, type_A, 0).   % COOP vs Always Defect: 0+0 = 0
outcome(DEFECT, type_A, 2). % DEFECT vs Always Defect: 1+1 = 2
outcome(TFT, type_A, 1).    % TFT vs Always Defect: 0+1 = 1

outcome(COOP, type_B, 6).   % COOP vs TFT: 3+3 = 6
outcome(DEFECT, type_B, 6). % DEFECT vs TFT: 5+1 = 6
outcome(TFT, type_B, 6).    % TFT vs TFT: 3+3 = 6

outcome(COOP, type_C, 6).   % COOP vs Forgiving TFT: 3+3 = 6
outcome(DEFECT, type_C, 10).% DEFECT vs Forgiving TFT: 5+5 = 10
outcome(TFT, type_C, 6).    % TFT vs Forgiving TFT: 3+3 = 6

% Calculate expected total score for each ego strategy
expected_score(Strategy, TotalScore) :-
    ego_strategy(Strategy),
    TotalScore = #sum { Count * Outcome : 
                        opponent_type(OppType), 
                        opponent_count(OppType, Count), 
                        outcome(Strategy, OppType, Outcome) }.

% Find the maximum score
max_score(MaxScore) :-
    expected_score(_, MaxScore),
    not (expected_score(_, OtherScore), OtherScore > MaxScore).

% Identify the best strategy
best_strategy(Strategy) :-
    max_score(MaxScore),
    expected_score(Strategy, MaxScore).

% Output the results
#show best_strategy/1.
#show expected_score/2.