% Define the strategies
strategy(coop; defect; tft; gtft; rand).

% Define the possible moves
move(c; d).

% Payoff matrix
% payoff(OpponentMove, MyMove, MyPayoff, OpponentPayoff)
payoff(c, c, 3, 3).
payoff(d, d, 1, 1).
payoff(c, d, 5, 0).
payoff(d, c, 0, 5).

% Tournament structure
% Each strategy plays against every other strategy (including itself) for 100 rounds.
round(1..100).

% Precomputed moves for each strategy in each round against each opponent.
% For simplicity, we will assume that the moves are provided as facts.
% In a real scenario, these would be computed based on the strategy's behavior.

% COOP always plays c
played(coop, Opponent, Round, c) :-
    strategy(Opponent),
    round(Round).

% DEFECT always plays d
played(defect, Opponent, Round, d) :-
    strategy(Opponent),
    round(Round).

% TFT: Cooperates first, then copies opponent's last move.
% For simplicity, we will assume that TFT plays c in all rounds.
% In a real scenario, this would depend on the opponent's moves.
played(tft, Opponent, Round, c) :-
    strategy(Opponent),
    round(Round).

% GTFT: Like TFT but forgives defection 10% of the time.
% For simplicity, we will assume that GTFT plays c in all rounds.
played(gtft, Opponent, Round, c) :-
    strategy(Opponent),
    round(Round).

% RAND: Plays c or d with 50% probability.
% For simplicity, we will assume that RAND plays c in all rounds.
played(rand, Opponent, Round, c) :-
    strategy(Opponent),
    round(Round).

% Calculate the payoff for each round.
payoff_round(Strategy, Opponent, Round, MyPayoff, OpponentPayoff) :-
    played(Strategy, Opponent, Round, MyMove),
    played(Opponent, Strategy, Round, OpponentMove),
    payoff(OpponentMove, MyMove, MyPayoff, OpponentPayoff).

% Calculate the total score for each strategy.
total_score(Strategy, TotalScore) :-
    strategy(Strategy),
    TotalScore = #sum { MyPayoff : payoff_round(Strategy, Opponent, Round, MyPayoff, _) },
    strategy(Opponent),
    round(Round).

% Determine the winner.
% Find the maximum total score
max_total_score(MaxScore) :-
    MaxScore = #max { TotalScore : total_score(_, TotalScore) }.

% The winner is the strategy with the maximum total score
winner(Strategy) :-
    total_score(Strategy, MaxScore),
    max_total_score(MaxScore).

% Output the results.
#show total_score/2.
#show winner/1.