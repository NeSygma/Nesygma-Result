% Men and Women
man(m1). man(m2). man(m3). man(m4).
woman(w1). woman(w2). woman(w3). woman(w4).

% Acceptable pairs (both find each other acceptable)
accept(m1,w1). accept(m1,w2). accept(m1,w3).
accept(m2,w2). accept(m2,w3). accept(m2,w4).
accept(m3,w3). accept(m3,w4). accept(m3,w1).
accept(m4,w4). accept(m4,w1). accept(m4,w2).

% Men's preference ranks (lower is better)
rank_m(m1,w1,1). rank_m(m1,w2,2). rank_m(m1,w3,3).
rank_m(m2,w2,1). rank_m(m2,w3,2). rank_m(m2,w4,3).
rank_m(m3,w3,1). rank_m(m3,w4,2). rank_m(m3,w1,3).
rank_m(m4,w4,1). rank_m(m4,w1,2). rank_m(m4,w2,3).

% Women's preference ranks (lower is better)
rank_w(w1,m4,1). rank_w(w1,m1,2). rank_w(w1,m3,3).
rank_w(w2,m1,1). rank_w(w2,m2,2). rank_w(w2,m4,3).
rank_w(w3,m2,1). rank_w(w3,m3,2). rank_w(w3,m1,3).
rank_w(w4,m3,1). rank_w(w4,m4,2). rank_w(w4,m2,3).

% Choice of matches (only acceptable pairs can be matched)
{match(M,W)} :- man(M), woman(W), accept(M,W).

% Matching constraints: at most one partner per person
:- match(M,W1), match(M,W2), W1 != W2.
:- match(M1,W), match(M2,W), M1 != M2.

% Current partner of each person (none if unmatched)
partner_m(M,PM) :- match(M,PM).
partner_w(W,PM) :- match(PM,W).
partner_m(M,none) :- man(M), not match(M,_).
partner_w(W,none) :- woman(W), not match(_,W).

% Preference: a person prefers X over Y if rank of X is lower than rank of Y
pref_m(M,W,PM) :- accept(M,W), accept(M,PM), rank_m(M,W,R1), rank_m(M,PM,R2), R1 < R2.
pref_w(W,M,PM) :- accept(W,M), accept(W,PM), rank_w(W,M,R1), rank_w(W,PM,R2), R1 < R2.
% Any acceptable partner is preferred over being unmatched
pref_m(M,W,none) :- accept(M,W).
pref_w(W,M,none) :- accept(W,M).

% Stability: no blocking pair
:- accept(M,W), not match(M,W), pref_m(M,W,PM), pref_w(W,M,PW).

#show match/2.