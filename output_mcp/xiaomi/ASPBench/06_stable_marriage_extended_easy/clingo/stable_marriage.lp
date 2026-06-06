% ==================== DOMAIN ====================
man(m1). man(m2). man(m3). man(m4).
woman(w1). woman(w2). woman(w3). woman(w4).

% ==================== MEN'S PREFERENCES ====================
% m1: w1, w2, w3
pref_m(m1, w1, 1). pref_m(m1, w2, 2). pref_m(m1, w3, 3).
% m2: w2, w3, w4
pref_m(m2, w2, 1). pref_m(m2, w3, 2). pref_m(m2, w4, 3).
% m3: w3, w4, w1
pref_m(m3, w3, 1). pref_m(m3, w4, 2). pref_m(m3, w1, 3).
% m4: w4, w1, w2
pref_m(m4, w4, 1). pref_m(m4, w1, 2). pref_m(m4, w2, 3).

% ==================== WOMEN'S PREFERENCES ====================
% w1: m4, m1, m3
pref_w(w1, m4, 1). pref_w(w1, m1, 2). pref_w(w1, m3, 3).
% w2: m1, m2, m4
pref_w(w2, m1, 1). pref_w(w2, m2, 2). pref_w(w2, m4, 3).
% w3: m2, m3, m1
pref_w(w3, m2, 1). pref_w(w3, m3, 2). pref_w(w3, m1, 3).
% w4: m3, m4, m2
pref_w(w4, m3, 1). pref_w(w4, m4, 2). pref_w(w4, m2, 3).

% ==================== ACCEPTABILITY ====================
% A man finds a woman acceptable if she appears in his preference list
acceptable(M, W) :- pref_m(M, W, _).
% A woman finds a man acceptable if he appears in her preference list
acceptable_w(W, M) :- pref_w(W, M, _).

% ==================== MATCHING (CHOICE) ====================
% Each man is matched to at most one woman (among acceptable ones who also find him acceptable)
{ matched(M, W) : woman(W), acceptable(M, W), acceptable_w(W, M) } 1 :- man(M).

% Each woman is matched to at most one man
:- matched(M1, W), matched(M2, W), M1 != M2.

% ==================== STABILITY ====================
% A man prefers woman W2 over his current match W1 if W2 has a better (lower) rank
man_prefers(M, W2, W1) :- matched(M, W1), pref_m(M, W2, R2), pref_m(M, W1, R1), R2 < R1.

% A woman prefers man M2 over her current match M1 if M2 has a better (lower) rank
woman_prefers(W, M2, M1) :- matched(M1, W), pref_w(W, M2, R2), pref_w(W, M1, R1), R2 < R1.

% A blocking pair: both find each other acceptable, both prefer each other over current match
blocking_pair(M, W) :- man(M), woman(W), acceptable(M, W), acceptable_w(W, M),
                        not matched(M, W),
                        man_prefers(M, W, _),
                        woman_prefers(W, M, _).

% A matching is stable if there are no blocking pairs
:- blocking_pair(M, W).

% ==================== OUTPUT ====================
#show matched/2.