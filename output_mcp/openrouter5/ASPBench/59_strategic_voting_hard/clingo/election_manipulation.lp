%% Election Manipulation Problem
%% Find minimum coalition size to elect Condorcet winner B

%% --- Domain Definitions ---

% Voters
voter(v1; v2; v3; v4; v5; v6).

% Candidates
candidate(a; b; c; d).

% Dissatisfied voters (prefer B but currently vote A)
dissatisfied(v5; v6).

% Current plurality winner
current_winner(a).

% Condorcet winner
condorcet_winner(b).

% Original votes
original_vote(v1, a).
original_vote(v2, b).
original_vote(v3, b).
original_vote(v4, b).
original_vote(v5, a).
original_vote(v6, a).

% Voter preferences (complete rankings)
% rank(Voter, Candidate, Position) - lower position = higher preference
rank(v1, a, 1). rank(v1, b, 2). rank(v1, c, 3). rank(v1, d, 4).
rank(v2, a, 1). rank(v2, c, 2). rank(v2, b, 3). rank(v2, d, 4).
rank(v3, a, 1). rank(v3, d, 2). rank(v3, b, 3). rank(v3, c, 4).
rank(v4, b, 1). rank(v4, c, 2). rank(v4, d, 3). rank(v4, a, 4).
rank(v5, b, 1). rank(v5, a, 2). rank(v5, d, 3). rank(v5, c, 4).
rank(v6, b, 1). rank(v6, d, 2). rank(v6, a, 3). rank(v6, c, 4).

% Preference relation: prefers(V, X, Y) means V prefers X over Y
prefers(V, X, Y) :- rank(V, X, Px), rank(V, Y, Py), Px < Py.

%% --- Coalition Formation ---

% Coalition members are a subset of dissatisfied voters
{ coalition(V) } :- dissatisfied(V).

% Coalition size
coalition_size(S) :- S = #count { V : coalition(V) }.

%% --- Strategic Voting ---

% Coalition members vote for Condorcet winner (B)
strategic_vote(V, b) :- coalition(V).

% Non-coalition voters keep their original vote
strategic_vote(V, C) :- voter(V), not coalition(V), original_vote(V, C).

%% --- Manipulated Election Results ---

% Count votes for each candidate
vote_count(C, N) :- candidate(C), N = #count { V : strategic_vote(V, C) }.

% Determine winner: candidate with most votes
% Use tie-break: alphabetical order (a < b < c < d)

% Max vote count
max_votes(M) :- M = #max { N : vote_count(_, N) }.

% Candidates with max votes
top_candidate(C) :- vote_count(C, M), max_votes(M).

% Winner is alphabetically first among top candidates
% a < b < c < d
winner(a) :- top_candidate(a).
winner(b) :- top_candidate(b), not top_candidate(a).
winner(c) :- top_candidate(c), not top_candidate(a), not top_candidate(b).
winner(d) :- top_candidate(d), not top_candidate(a), not top_candidate(b), not top_candidate(c).

%% --- Constraints ---

% 1. Manipulation must succeed: Condorcet winner (B) must win
:- not winner(b).

% 2. Individual Rationality: No coalition member can be worse off
% A voter is worse off if their new vote is for a candidate they rank lower
% than the candidate they originally voted for
worse_off(V) :- coalition(V), original_vote(V, C_orig), strategic_vote(V, C_new),
                prefers(V, C_orig, C_new).
:- worse_off(V).

% 3. Vote conservation: total votes must equal number of voters
total_votes(N) :- N = #count { V : strategic_vote(V, _) }.
total_voters(N) :- N = #count { V : voter(V) }.
:- total_votes(N1), total_voters(N2), N1 != N2.

%% --- Optimization: Minimize coalition size ---

#minimize { 1, V : coalition(V) }.

%% --- Output ---

#show coalition/1.
#show coalition_size/1.
#show strategic_vote/2.
#show vote_count/2.
#show winner/1.