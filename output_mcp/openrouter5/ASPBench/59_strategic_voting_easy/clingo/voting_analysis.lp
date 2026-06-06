%%% Voting Scenario Analysis
%%% 4 voters, 3 candidates, plurality voting

% --- Domain Definitions ---
voter(v1; v2; v3; v4).
candidate(a; b; c).

% --- True Preferences (rankings) ---
% rank(Voter, Candidate, Position) - lower position = more preferred
rank(v1, a, 1). rank(v1, b, 2). rank(v1, c, 3).
rank(v2, a, 1). rank(v2, c, 2). rank(v2, b, 3).
rank(v3, b, 1). rank(v3, c, 2). rank(v3, a, 3).
rank(v4, c, 1). rank(v4, b, 2). rank(v4, a, 3).

% --- Truthful Votes (baseline) ---
truthful_vote(v1, a).
truthful_vote(v2, a).
truthful_vote(v3, b).
truthful_vote(v4, c).

% --- Strategic Votes (choice: each voter can vote for any candidate) ---
{ strategic_vote(V, C) : candidate(C) } 1 :- voter(V).

% --- Vote Counting ---
% Count votes for each candidate under strategic voting
vote_count(C, N) :- N = #count { V : strategic_vote(V, C) }, candidate(C).

% --- Winner Determination ---
% A candidate wins if they have strictly more votes than all others
winner(C) :- vote_count(C, N), candidate(C),
             N > #max { M : vote_count(C2, M), candidate(C2), C2 != C }.

% --- Baseline (truthful) outcome ---
truthful_vote_count(C, N) :- N = #count { V : truthful_vote(V, C) }, candidate(C).

truthful_winner(C) :- truthful_vote_count(C, N), candidate(C),
                      N > #max { M : truthful_vote_count(C2, M), candidate(C2), C2 != C }.

% --- Preference Comparison ---
% prefers(V, X, Y) means voter V prefers candidate X over Y
prefers(V, X, Y) :- rank(V, X, Px), rank(V, Y, Py), Px < Py.

% --- Strategic Benefit ---
% Truthful winner exists
truthful_winner_exists :- truthful_winner(_).

% Strategic winner exists
strategic_winner_exists :- winner(_).

% Voter benefits if they prefer the strategic winner over truthful winner
% and they actually changed their vote
benefits(V) :- voter(V),
               truthful_winner(Wt),
               winner(Ws),
               Ws != Wt,
               prefers(V, Ws, Wt),
               strategic_vote(V, Cv),
               not truthful_vote(V, Cv).

% Also benefit if truthful had no winner (tie) and strategic has a winner they prefer
benefits(V) :- voter(V),
               not truthful_winner_exists,
               winner(Ws),
               strategic_vote(V, Cv),
               not truthful_vote(V, Cv).

% --- Coalition Size ---
% Count how many voters deviate from truthful voting
deviates(V) :- voter(V), strategic_vote(V, Cv), not truthful_vote(V, Cv).
coalition_size(S) :- S = #count { V : deviates(V) }.

% --- Manipulation Success ---
% Manipulation is successful if at least one voter benefits
manipulation_successful :- benefits(_).

% --- Minimum Coalition Size for Successful Manipulation ---
% We want the minimum S such that manipulation_successful holds
% Use #minimize to find smallest coalition
#minimize { S@1, S : coalition_size(S), manipulation_successful }.

% --- Condorcet Winner ---
% A candidate is a Condorcet winner if they beat every other candidate in pairwise comparisons
% Pairwise: count voters who prefer X over Y
pairwise_win(X, Y) :- candidate(X), candidate(Y), X != Y,
                      #count{ V : prefers(V, X, Y) } > #count{ V : prefers(V, Y, X) }.

condorcet_winner(X) :- candidate(X),
                       pairwise_win(X, Y) : candidate(Y), Y != X.

% --- Output ---
#show truthful_winner/1.
#show winner/1.
#show benefits/1.
#show deviates/1.
#show coalition_size/1.
#show manipulation_successful/0.
#show condorcet_winner/1.
#show strategic_vote/2.