% Domains
man(m1). man(m2). man(m3). man(m4).
woman(w1). woman(w2). woman(w3). woman(w4).

% Men's preferences: mpref(man, woman, rank) - lower rank = more preferred
mpref(m1, w1, 1). mpref(m1, w2, 2). mpref(m1, w3, 3).
mpref(m2, w2, 1). mpref(m2, w3, 2). mpref(m2, w4, 3).
mpref(m3, w3, 1). mpref(m3, w4, 2). mpref(m3, w1, 3).
mpref(m4, w4, 1). mpref(m4, w1, 2). mpref(m4, w2, 3).

% Women's preferences: wpref(woman, man, rank) - lower rank = more preferred
wpref(w1, m4, 1). wpref(w1, m1, 2). wpref(w1, m3, 3).
wpref(w2, m1, 1). wpref(w2, m2, 2). wpref(w2, m4, 3).
wpref(w3, m2, 1). wpref(w3, m3, 2). wpref(w3, m1, 3).
wpref(w4, m3, 1). wpref(w4, m4, 2). wpref(w4, m2, 3).

% Acceptability: both find each other acceptable
acceptable(M, W) :- mpref(M, W, _).
acceptable(M, W) :- wpref(W, M, _).
% A pair is mutually acceptable only if both list each other
mutual(M, W) :- mpref(M, W, _), wpref(W, M, _).

% Choice: each man can be matched to at most one mutually acceptable woman
{ matched(M, W) : mutual(M, W) } 1 :- man(M).

% Each woman matched to at most one mutually acceptable man
{ matched(M, W) : mutual(M, W) } 1 :- woman(W).

% Helper: man M prefers woman W1 over W2 (W1 has lower rank)
mprefers_over(M, W1, W2) :- mpref(M, W1, R1), mpref(M, W2, R2), R1 < R2.

% Helper: woman W prefers man M1 over M2
wprefers_over(W, M1, M2) :- wpref(W, M1, R1), wpref(W, M2, R2), R1 < R2.

% A man is unmatched if he has no match
unmatched_man(M) :- man(M), not matched(M, _).

% A woman is unmatched if she has no match
unmatched_woman(W) :- woman(W), not matched(_, W).

% Blocking pair definition:
% (M, W) is a blocking pair if:
% 1. They are not matched to each other
% 2. They find each other mutually acceptable
% 3. M prefers W to his current partner (or M is unmatched)
% 4. W prefers M to her current partner (or W is unmatched)

% M would rather be with W than current partner (or unmatched)
m_would_switch(M, W) :- mutual(M, W), unmatched_man(M), man(M), woman(W).
m_would_switch(M, W) :- mutual(M, W), matched(M, W2), W != W2, mprefers_over(M, W, W2).

% W would rather be with M than current partner (or unmatched)
w_would_switch(W, M) :- mutual(M, W), unmatched_woman(W), man(M), woman(W).
w_would_switch(W, M) :- mutual(M, W), matched(M2, W), M != M2, wprefers_over(W, M, M2).

% A blocking pair exists
blocking_pair(M, W) :- m_would_switch(M, W), w_would_switch(W, M), not matched(M, W).

% Stability constraint: no blocking pairs allowed
:- blocking_pair(M, W).

% Show the matchings
#show matched/2.