% --- Voters and Candidates ---
voter(v1;v2;v3;v4;v5;v6).
candidate(a;b;c;d).

% --- Voter Preferences (complete rankings) ---
pref(v1,a,1). pref(v1,b,2). pref(v1,c,3). pref(v1,d,4).
pref(v2,a,1). pref(v2,c,2). pref(v2,b,3). pref(v2,d,4).
pref(v3,a,1). pref(v3,d,2). pref(v3,b,3). pref(v3,c,4).
pref(v4,b,1). pref(v4,c,2). pref(v4,d,3). pref(v4,a,4).
pref(v5,b,1). pref(v5,a,2). pref(v5,d,3). pref(v5,c,4).
pref(v6,b,1). pref(v6,d,2). pref(v6,a,3). pref(v6,c,4).

% --- Initial Votes ---
initial_vote(v1,a).
initial_vote(v2,b).
initial_vote(v3,b).
initial_vote(v4,b).
initial_vote(v5,a).
initial_vote(v6,a).

% --- Dissatisfied voters (prefer B but currently vote A) ---
dissatisfied(v5). dissatisfied(v6).

% --- Condorcet winner and original winner ---
condorcet_winner(b).
original_winner(a).

% --- Alphabetical order for tie-breaking ---
alpha_order(a,1). alpha_order(b,2). alpha_order(c,3). alpha_order(d,4).

% --- Coalition Formation ---
% Coalition members are a subset of dissatisfied voters
{ coalition(V) : dissatisfied(V) }.

% --- New Votes ---
% Coalition members vote for the Condorcet winner (B)
new_vote(V, b) :- coalition(V).

% Non-coalition members keep their original vote
new_vote(V, C) :- voter(V), candidate(C), initial_vote(V, C), not coalition(V).

% Every voter casts exactly one vote
:- voter(V), not new_vote(V, _).

% --- Vote Counting ---
vote_count(C, N) :- candidate(C), N = #count{ V : new_vote(V, C) }.

% --- Determine Winner ---
% Max vote count among all candidates
max_votes(N) :- N = #max{ Cnt : vote_count(C, Cnt) }.

% Candidates with the max vote count (leading candidates)
leading(C) :- vote_count(C, N), max_votes(N).

% Winner is the alphabetically first among leading candidates (tie-break)
winner(C) :- leading(C), C = #min{ W : leading(W) }.

% Constraint: Manipulated election must elect Condorcet winner (B)
:- winner(C), C != b.

% --- Individual Rationality ---
% A coalition member is worse off if they prefer the original winner (A)
% over the new winner (B). Lower rank number = higher preference.
worse_off(V) :- coalition(V), pref(V, a, Ra), pref(V, b, Rb), Ra < Rb.

% No coalition member can be made worse off
:- worse_off(V).

% --- Optimization: Minimize coalition size ---
#minimize { 1, V : coalition(V) }.

% --- Output ---
#show coalition/1.
#show new_vote/2.
#show vote_count/2.
#show winner/1.