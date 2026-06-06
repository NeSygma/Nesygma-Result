% Domain definitions
voter(v1). voter(v2). voter(v3). voter(v4). voter(v5). voter(v6).
candidate(a). candidate(b). candidate(c). candidate(d).

% Preference rankings (rank 1 = highest preference)
% V1: A > B > C > D
prefers(v1, a, 1). prefers(v1, b, 2). prefers(v1, c, 3). prefers(v1, d, 4).
% V2: A > C > B > D
prefers(v2, a, 1). prefers(v2, c, 2). prefers(v2, b, 3). prefers(v2, d, 4).
% V3: A > D > B > C
prefers(v3, a, 1). prefers(v3, d, 2). prefers(v3, b, 3). prefers(v3, c, 4).
% V4: B > C > D > A
prefers(v4, b, 1). prefers(v4, c, 2). prefers(v4, d, 3). prefers(v4, a, 4).
% V5: B > A > D > C
prefers(v5, b, 1). prefers(v5, a, 2). prefers(v5, d, 3). prefers(v5, c, 4).
% V6: B > D > A > C
prefers(v6, b, 1). prefers(v6, d, 2). prefers(v6, a, 3). prefers(v6, c, 4).

% Initial votes
initial_vote(v1, a).  % First preference
initial_vote(v2, b).  % Strategic vote (prefers A)
initial_vote(v3, b).  % Strategic vote (prefers A)
initial_vote(v4, b).  % First preference
initial_vote(v5, a).  % Strategic vote (prefers B)
initial_vote(v6, a).  % Strategic vote (prefers B)

% Dissatisfied voters (prefer B but currently vote A)
dissatisfied(v5).
dissatisfied(v6).

% Coalition formation: subset of dissatisfied voters
{in_coalition(V)} :- dissatisfied(V).

% Strategic voting rule: coalition members vote for Condorcet winner (B)
manipulated_vote(V, b) :- in_coalition(V).
% Non-coalition members keep their initial votes
manipulated_vote(V, C) :- voter(V), not in_coalition(V), initial_vote(V, C).

% Vote counts in manipulated election
vote_count(C, N) :- candidate(C), N = #count{V : manipulated_vote(V, C)}.

% Determine plurality winner with alphabetical tie-break
max_votes(N) :- N = #max{N2 : vote_count(_, N2)}.

% Winner is candidate with max votes, and in case of tie, smallest alphabetical order
winner(C) :- candidate(C), vote_count(C, N), max_votes(N),
             not exists_better(C).

exists_better(C) :- candidate(C), vote_count(C, N), max_votes(N),
                    candidate(C2), vote_count(C2, N), 
                    candidate_order(C2, O2), candidate_order(C, O), O2 < O.

% Define alphabetical order for tie-breaking
candidate_order(a, 1). candidate_order(b, 2). candidate_order(c, 3). candidate_order(d, 4).

% Check if manipulation is successful (B wins)
manipulation_successful :- winner(b).

% Check individual rationality: no coalition member worse off
% For each coalition member, B must be at least as good as A
better_or_equal(V, W1, W2) :- voter(V), candidate(W1), candidate(W2),
                               prefers(V, W1, R1), prefers(V, W2, R2), R1 <= R2.

no_member_worse_off :- in_coalition(V), better_or_equal(V, b, a).

% All coalition members must satisfy individual rationality
:- in_coalition(V), not better_or_equal(V, b, a).

% Constraints for successful manipulation
:- not manipulation_successful.

% Minimize coalition size
#minimize{1, V : in_coalition(V)}.

% Output definitions
#show in_coalition/1.
#show manipulation_successful/0.
#show no_member_worse_off/0.
#show winner/1.
#show vote_count/2.
#show coalition_size/1.

% Compute coalition size for output
coalition_size(N) :- N = #count{V : in_coalition(V)}.