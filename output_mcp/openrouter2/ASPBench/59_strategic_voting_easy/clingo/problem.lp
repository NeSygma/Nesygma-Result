% Voters
voter(v1). voter(v2). voter(v3). voter(v4).

% Candidates
candidate(a). candidate(b). candidate(c).

% Current votes
cur(v1,a). cur(v2,a). cur(v3,b). cur(v4,c).

% Preferences: lower number = higher preference
pref(v1,a,1). pref(v1,b,2). pref(v1,c,3).
pref(v2,a,1). pref(v2,c,2). pref(v2,b,3).
pref(v3,b,1). pref(v3,c,2). pref(v3,a,3).
pref(v4,c,1). pref(v4,b,2). pref(v4,a,3).

% Coalition size choice
{coalition_size(K)} :- K = 1..4.
% Exactly K voters in the coalition
K { in_coalition(V) : voter(V) } 1 :- coalition_size(K).

% New vote assignment: each voter votes for exactly one candidate
1 { new_vote(V,C) : candidate(C) } 1 :- voter(V).

% Non-coalition voters must keep their current vote
:- not in_coalition(V), new_vote(V,C), cur(V,C2), C != C2.

% Winner determination for current votes
winner_cur(C) :- #count{V : cur(V,C)} > #count{V : cur(V,C2) : C2 != C}.

% Winner determination for new votes
winner_new(C) :- #count{V : new_vote(V,C)} > #count{V : new_vote(V,C2) : C2 != C}.

% Ensure a unique winner in each scenario
:- winner_cur(C1), winner_cur(C2), C1 != C2.
:- winner_new(C1), winner_new(C2), C1 != C2.

% A coalition member benefits if the new winner is more preferred than the current winner
better(V) :- in_coalition(V), winner_new(W), winner_cur(CurW), pref(V,W,Rw), pref(V,CurW,Rc), Rw < Rc.

% At least one coalition member benefits
:- coalition_size(K), not better(_).

% Optimize for minimal coalition size
#minimize {1@1, K : coalition_size(K)}.

% Show results
#show coalition_size/1.
#show winner_new/1.
#show better/1.