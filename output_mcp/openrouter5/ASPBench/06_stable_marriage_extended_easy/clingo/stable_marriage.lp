%%% Stable Marriage Problem
%%% 4 men, 4 women with preference rankings

%%% DOMAIN DECLARATIONS %%%
man(m1; m2; m3; m4).
woman(w1; w2; w3; w4).

%%% PREFERENCE RANKINGS %%%
%%% Men's preferences: rank(man, woman, rank) where lower rank = more preferred
rank(m1, w1, 1). rank(m1, w2, 2). rank(m1, w3, 3).
rank(m2, w2, 1). rank(m2, w3, 2). rank(m2, w4, 3).
rank(m3, w3, 1). rank(m3, w4, 2). rank(m3, w1, 3).
rank(m4, w4, 1). rank(m4, w1, 2). rank(m4, w2, 3).

%%% Women's preferences: rank(woman, man, rank)
rank(w1, m4, 1). rank(w1, m1, 2). rank(w1, m3, 3).
rank(w2, m1, 1). rank(w2, m2, 2). rank(w2, m4, 3).
rank(w3, m2, 1). rank(w3, m3, 2). rank(w3, m1, 3).
rank(w4, m3, 1). rank(w4, m4, 2). rank(w4, m2, 3).

%%% Acceptability: a pair is acceptable if both have ranked each other
acceptable(M, W) :- man(M), woman(W), rank(M, W, _), rank(W, M, _).

%%% CHOICE RULES: Matching %%%
%%% Each man is matched to at most one woman (or unmatched)
{ matched(M, W) : acceptable(M, W) } 1 :- man(M).

%%% Each woman is matched to at most one man (or unmatched)
{ matched(M, W) : acceptable(M, W) } 1 :- woman(W).

%%% A woman cannot be matched to more than one man
:- matched(M1, W), matched(M2, W), M1 != M2.

%%% A man cannot be matched to more than one woman
:- matched(M, W1), matched(M, W2), W1 != W2.

%%% STABILITY CONSTRAINTS %%%

%%% A blocking pair (M, W) exists if:
%%% 1. M and W are not matched to each other
%%% 2. Both find each other acceptable
%%% 3. M prefers W over his current partner (or is unmatched)
%%% 4. W prefers M over her current partner (or is unmatched)

%%% Helper: man is matched to someone
man_matched(M) :- matched(M, _).

%%% Helper: woman is matched to someone
woman_matched(W) :- matched(_, W).

%%% Helper: man's current partner (if any)
current_partner(M, W) :- matched(M, W).

%%% Helper: woman's current partner (if any)
current_partner_w(W, M) :- matched(M, W).

%%% Condition: M prefers W over his current partner
%%% M is unmatched -> prefers anyone acceptable
prefers_man(M, W) :- man(M), woman(W), acceptable(M, W), not man_matched(M).
%%% M is matched to W_cur and prefers W over W_cur
prefers_man(M, W) :- man(M), woman(W), acceptable(M, W), man_matched(M),
                     current_partner(M, W_cur), W != W_cur,
                     rank(M, W, R1), rank(M, W_cur, R2), R1 < R2.

%%% Condition: W prefers M over her current partner
%%% W is unmatched -> prefers anyone acceptable
prefers_woman(W, M) :- woman(W), man(M), acceptable(M, W), not woman_matched(W).
%%% W is matched to M_cur and prefers M over M_cur
prefers_woman(W, M) :- woman(W), man(M), acceptable(M, W), woman_matched(W),
                       current_partner_w(W, M_cur), M != M_cur,
                       rank(W, M, R1), rank(W, M_cur, R2), R1 < R2.

%%% Blocking pair: both prefer each other over current partners
blocking_pair(M, W) :- man(M), woman(W), acceptable(M, W),
                       not matched(M, W),
                       prefers_man(M, W),
                       prefers_woman(W, M).

%%% No blocking pairs allowed
:- blocking_pair(M, W).

%%% OUTPUT %%%
%%% Enumerate each matching as a set of pairs
%%% Use a matching ID to enumerate all solutions

%%% We need to enumerate all stable matchings.
%%% Clingo's default enumeration with #show will give us each answer set.
%%% Let's format the output nicely.

#show matched/2.