% Voters and Candidates
voter(v1; v2; v3; v4).
candidate(a; b; c).

% Preferences (Rank 1 is best)
pref(v1, 1, a). pref(v1, 2, b). pref(v1, 3, c).
pref(v2, 1, a). pref(v2, 2, c). pref(v2, 3, b).
pref(v3, 1, b). pref(v3, 2, c). pref(v3, 3, a).
pref(v4, 1, c). pref(v4, 2, b). pref(v4, 3, a).

% Truthful votes
truthful_vote(v1, a).
truthful_vote(v2, a).
truthful_vote(v3, b).
truthful_vote(v4, c).

% --- Truthful Outcome ---
% Define truthful votes as a separate predicate to avoid conflict
current_vote(V, C) :- truthful_vote(V, C).
vote_count_truthful(C, N) :- candidate(C), N = #count { V : current_vote(V, C) }.
max_votes_truthful(M) :- M = #max { N : vote_count_truthful(C, N) }.
truthful_winner(W) :- candidate(W), vote_count_truthful(W, M), max_votes_truthful(M).

% --- Strategic Outcome ---
{ strategic_vote(V, C) : candidate(C) } = 1 :- voter(V).

% Winner determination
vote_count_strategic(C, N) :- candidate(C), N = #count { V : strategic_vote(V, C) }.
max_votes_strategic(M) :- M = #max { N : vote_count_strategic(C, N) }.
strategic_winner(W) :- candidate(W), vote_count_strategic(W, M), max_votes_strategic(M).

% Coalition definition
is_coalition_member(V) :- voter(V), strategic_vote(V, C), truthful_vote(V, CV), C != CV.
coalition_size(N) :- N = #count { V : is_coalition_member(V) }.

% Better outcome condition
better(V, New, Old) :- voter(V), pref(V, R1, New), pref(V, R2, Old), R1 < R2.

% Successful manipulation:
% 1. New winner is different from truthful winner
% 2. Every coalition member prefers the new winner over the truthful winner
successful_manipulation :- 
    strategic_winner(New), truthful_winner(Old), New != Old,
    is_coalition_member(_),
    not worse_for_any_member(New, Old).

worse_for_any_member(New, Old) :- 
    is_coalition_member(V), 
    pref(V, R1, New), pref(V, R2, Old), R1 > R2.

% Optimization
#minimize { N : coalition_size(N), successful_manipulation }.

#show successful_manipulation/0.
#show coalition_size/1.