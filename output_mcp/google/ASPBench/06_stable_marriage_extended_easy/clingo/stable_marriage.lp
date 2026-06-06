% --- Domain Definitions ---
man(m1; m2; m3; m4).
woman(w1; w2; w3; w4).

% --- Preferences ---
% pref_m(Man, Woman, Rank)
pref_m(m1, w1, 1). pref_m(m1, w2, 2). pref_m(m1, w3, 3).
pref_m(m2, w2, 1). pref_m(m2, w3, 2). pref_m(m2, w4, 3).
pref_m(m3, w3, 1). pref_m(m3, w4, 2). pref_m(m3, w1, 3).
pref_m(m4, w4, 1). pref_m(m4, w1, 2). pref_m(m4, w2, 3).

% pref_w(Woman, Man, Rank)
pref_w(w1, m4, 1). pref_w(w1, m1, 2). pref_w(w1, m3, 3).
pref_w(w2, m1, 1). pref_w(w2, m2, 2). pref_w(w2, m4, 3).
pref_w(w3, m2, 1). pref_w(w3, m3, 2). pref_w(w3, m1, 3).
pref_w(w4, m3, 1). pref_w(w4, m4, 2). pref_w(w4, m2, 3).

% --- Matching Constraints ---
% Each man is matched to exactly one woman
1 { match(M, W) : woman(W), pref_m(M, W, _) } 1 :- man(M).

% Each woman is matched to exactly one man
1 { match(M, W) : man(M), pref_w(W, M, _) } 1 :- woman(W).

% --- Stability Constraints ---
% A pair (M, W) is a blocking pair if:
% 1. They are not matched to each other
% 2. M prefers W over his current partner
% 3. W prefers M over her current partner

blocking(M, W) :- 
    man(M), woman(W), 
    not match(M, W),
    pref_m(M, W, RankM_W),
    pref_w(W, M, RankW_M),
    match(M, W_curr), pref_m(M, W_curr, RankM_curr), RankM_W < RankM_curr,
    match(M_curr, W), pref_w(W, M_curr, RankW_curr), RankW_M < RankW_curr.

:- blocking(M, W).

% --- Output ---
#show match/2.