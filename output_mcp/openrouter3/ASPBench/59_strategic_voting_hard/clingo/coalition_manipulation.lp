% Coalition Manipulation Problem

% Domain declarations
voter(v1). voter(v2). voter(v3). voter(v4). voter(v5). voter(v6).
candidate(a). candidate(b). candidate(c). candidate(d).

% Voter preferences (complete rankings)
% V1: A > B > C > D
prefers(v1, a, b). prefers(v1, a, c). prefers(v1, a, d).
prefers(v1, b, c). prefers(v1, b, d). prefers(v1, c, d).

% V2: A > C > B > D
prefers(v2, a, c). prefers(v2, a, b). prefers(v2, a, d).
prefers(v2, c, b). prefers(v2, c, d). prefers(v2, b, d).

% V3: A > D > B > C
prefers(v3, a, d). prefers(v3, a, b). prefers(v3, a, c).
prefers(v3, d, b). prefers(v3, d, c). prefers(v3, b, c).

% V4: B > C > D > A
prefers(v4, b, c). prefers(v4, b, d). prefers(v4, b, a).
prefers(v4, c, d). prefers(v4, c, a). prefers(v4, d, a).

% V5: B > A > D > C (dissatisfied)
prefers(v5, b, a). prefers(v5, b, d). prefers(v5, b, c).
prefers(v5, a, d). prefers(v5, a, c). prefers(v5, d, c).

% V6: B > D > A > C (dissatisfied)
prefers(v6, b, d). prefers(v6, b, a). prefers(v6, b, c).
prefers(v6, d, a). prefers(v6, d, c). prefers(v6, a, c).

% Current votes
current_vote(v1, a).
current_vote(v2, b).
current_vote(v3, b).
current_vote(v4, b).
current_vote(v5, a).
current_vote(v6, a).

% Dissatisfied voters (prefer B but currently vote A)
dissatisfied(v5). dissatisfied(v6).

% Condorcet winner is B
condorcet_winner(b).

% Coalition formation: only dissatisfied voters can be in coalition
% Choice rule to select coalition members
{ coalition_member(V) } :- dissatisfied(V).

% Coalition members must vote for B (Condorcet winner)
new_vote(V, b) :- coalition_member(V).

% Non-coalition members keep their current vote
new_vote(V, C) :- voter(V), not coalition_member(V), current_vote(V, C).

% Vote counting after manipulation
vote_count(C, N) :- candidate(C), N = #count{ V : new_vote(V, C) }.

% Determine winner: candidate with most votes
% If tie, use alphabetical order (A before B before C before D)
winner(a) :- vote_count(a, Na), vote_count(b, Nb), vote_count(c, Nc), vote_count(d, Nd),
             Na >= Nb, Na >= Nc, Na >= Nd.
winner(b) :- vote_count(b, Nb), vote_count(a, Na), vote_count(c, Nc), vote_count(d, Nd),
             Nb > Na, Nb >= Nc, Nb >= Nd.
winner(c) :- vote_count(c, Nc), vote_count(a, Na), vote_count(b, Nb), vote_count(d, Nd),
             Nc > Na, Nc > Nb, Nc >= Nd.
winner(d) :- vote_count(d, Nd), vote_count(a, Na), vote_count(b, Nb), vote_count(c, Nc),
             Nd > Na, Nd > Nb, Nd > Nc.

% Manipulation successful if winner is Condorcet winner (B)
manipulation_successful :- winner(b).

% Individual rationality: coalition members must not be worse off
% Since they prefer B over A, and they're voting for B, they're not worse off
% This is satisfied by definition since they're dissatisfied (prefer B over current A)

% Minimize coalition size
#minimize { 1, V : coalition_member(V) }.

% Show relevant information
#show coalition_member/1.
#show new_vote/2.
#show vote_count/2.
#show winner/1.
#show manipulation_successful/0.
#show condorcet_winner/1.

% Constraints
% Total votes must be 6
:- #count{ V : voter(V) } != 6.

% At least one coalition member needed for manipulation
:- not manipulation_successful.