% --- DATA ---
voter(v1;v2;v3;v4).
candidate(a;b;c).

% True preferences: pref(V, C, R) = voter V ranks candidate C at position R (1=best)
pref(v1,a,1). pref(v1,b,2). pref(v1,c,3).
pref(v2,a,1). pref(v2,c,2). pref(v2,b,3).
pref(v3,b,1). pref(v3,c,2). pref(v3,a,3).
pref(v4,c,1). pref(v4,b,2). pref(v4,a,3).

% Current (truthful) votes
cur_vote(v1,a). cur_vote(v2,a). cur_vote(v3,b). cur_vote(v4,c).

% Current winner: A has 2 votes, B has 1, C has 1. A is unique winner.
cur_winner(a).

% prefers(V, X, Y): V prefers X over Y (strictly)
prefers(V,X,Y) :- pref(V,X,RX), pref(V,Y,RY), RX < RY.

% --- MANIPULATION MODEL ---
% Some voters are manipulators
{ manip(V) } :- voter(V).

% Each voter casts exactly one new vote
1 { new_vote(V, C) : candidate(C) } 1 :- voter(V).

% Non-manipulators must vote truthfully (same as current vote)
:- not manip(V), new_vote(V, C), not cur_vote(V, C).

% Manipulators must vote differently from truthful
:- manip(V), new_vote(V, C), cur_vote(V, C).

% --- NEW WINNER DETERMINATION ---
new_count(C, N) :- N = #count{V : new_vote(V, C)}, candidate(C).
new_max(N) :- N = #max{M : new_count(_, M)}.

% Top candidates (tied for most votes)
new_top(C) :- new_count(C, N), new_max(N).
cur_top(C) :- cur_vote(C, _).  % Not needed

% --- CONSTRAINTS FOR SUCCESSFUL MANIPULATION ---
% 1. The new outcome must be different from current outcome (improvement)
%    The current winner (A) must not be a top candidate, OR there must be
%    at least one other top candidate that manipulators prefer
%    Actually: at least one top candidate that manipulators prefer over A

% Every manipulator must prefer at least one new_top candidate over A
:- manip(V), not benefited(V).

% A voter benefits if there exists a new_top candidate they prefer over current winner
benefited(V) :- manip(V), new_top(C), cur_winner(CW), prefers(V, C, CW).

% 3. At least one manipulator must exist
:- #count{V : manip(V)} < 1.

% The outcome must change: the current winner (A) must NOT be a unique winner
% (i.e., either A is not top, or there is another top candidate)
% Actually, we need the outcome to be strictly better. If A is still unique winner,
% the manipulators didn't achieve anything.
:- new_top(C), #count{C2 : new_top(C2)} = 1, new_top(a).

% --- COALITION SIZE ---
coalition_size(N) :- N = #count{V : manip(V)}.

% --- OUTPUT ---
#show manip/1.
#show new_vote/2.
#show new_top/1.
#show coalition_size/1.