% Domains
man(m1). man(m2). man(m3). man(m4).
woman(w1). woman(w2). woman(w3). woman(w4).

% Men's preference rankings (lower rank = more preferred)
man_pref(m1,w1,1). man_pref(m1,w2,2). man_pref(m1,w3,3).
man_pref(m2,w2,1). man_pref(m2,w3,2). man_pref(m2,w4,3).
man_pref(m3,w3,1). man_pref(m3,w4,2). man_pref(m3,w1,3).
man_pref(m4,w4,1). man_pref(m4,w1,2). man_pref(m4,w2,3).

% Women's preference rankings
woman_pref(w1,m4,1). woman_pref(w1,m1,2). woman_pref(w1,m3,3).
woman_pref(w2,m1,1). woman_pref(w2,m2,2). woman_pref(w2,m4,3).
woman_pref(w3,m2,1). woman_pref(w3,m3,2). woman_pref(w3,m1,3).
woman_pref(w4,m3,1). woman_pref(w4,m4,2). woman_pref(w4,m2,3).

% Acceptable pairs: both list each other
acceptable(M,W) :- man_pref(M,W,_), woman_pref(W,M,_).

% Rank predicates (aliases)
rank_m(M,W,R) :- man_pref(M,W,R).
rank_w(W,M,R) :- woman_pref(W,M,R).

% Choice of matches only over acceptable pairs
{ match(M,W) : acceptable(M,W) }.

% At most one partner per person
:- match(M,W1), match(M,W2), W1 != W2.
:- match(M1,W), match(M2,W), M1 != M2.

% Helper predicates for current partners
has_partner_m(M) :- match(M,_).
has_partner_w(W) :- match(_,W).

% Preference over current partner (or being single)
prefers_m_over_current(M,W) :- rank_m(M,W,RW), match(M,WM), rank_m(M,WM,RWM), RW < RWM.
prefers_m_over_current(M,W) :- rank_m(M,W,_), not has_partner_m(M).

prefers_w_over_current(W,M) :- rank_w(W,M,RW), match(MM,W), rank_w(W,MM,RWM), RW < RWM.
prefers_w_over_current(W,M) :- rank_w(W,M,_), not has_partner_w(W).

% Blocking pair definition
blocking(M,W) :- acceptable(M,W), not match(M,W), prefers_m_over_current(M,W), prefers_w_over_current(W,M).

% No blocking pairs allowed
:- blocking(M,W).

#show match/2.