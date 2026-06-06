%% Problem: Find which option has the same effect as condition 3 when substituted

singer(kammer; lugo; trillo; waite; yoshida; zinn).
recorded(kammer; lugo).
nonrecorded(T) :- singer(T), not recorded(T).
position(1..6).

%% Generate all possible orderings (permutations)
1 { at(S, P) : position(P) } 1 :- singer(S).
1 { at(S, P) : singer(S) } 1 :- position(P).

%% Base constraints (shared by all versions)
% Condition 1: fourth not recorded
:- at(S, 4), recorded(S).
% Condition 2: fifth recorded
:- at(S, 5), nonrecorded(S).
% Condition 4: Kammer before Trillo
:- at(kammer, PK), at(trillo, PT), PK >= PT.
% Condition 5: Zinn before Yoshida
:- at(zinn, PZ), at(yoshida, PY), PZ >= PY.

%% Original Condition 3: Waite before both recorded auditions
orig_cond3 :- at(waite, PW), at(kammer, PK), at(lugo, PL), PW < PK, PW < PL.

%% Option A: Zinn is the only one that can take place earlier than Waite
% No singer other than Zinn is before Waite
option_a_cond :- #count{X : at(X, PX), at(waite, PW), PX < PW, X != zinn} = 0.

%% Option B: Waite immediately before or after Zinn
option_b_cond :- at(waite, PW), at(zinn, PZ), |PW - PZ| = 1.

%% Option C: Waite before Lugo
option_c_cond :- at(waite, PW), at(lugo, PL), PW < PL.

%% Option D: Waite first or second
option_d_cond :- at(waite, PW), PW <= 2.

%% Option E: First audition cannot be recorded
option_e_cond :- #count{S : at(S, 1), recorded(S)} = 0.

%% Now check equivalence
% Valid under original (base + orig_cond3)
valid_orig :- orig_cond3.

% Valid under each option (base + option_X_cond)
valid_a :- option_a_cond.
valid_b :- option_b_cond.
valid_c :- option_c_cond.
valid_d :- option_d_cond.
valid_e :- option_e_cond.

%% An option is equivalent iff:
%% 1. Every ordering valid under orig is valid under the option, AND
%% 2. Every ordering valid under the option is valid under orig.

%% Check violations of (1): valid_orig but not option
viol_a1 :- valid_orig, not option_a_cond.
viol_b1 :- valid_orig, not option_b_cond.
viol_c1 :- valid_orig, not option_c_cond.
viol_d1 :- valid_orig, not option_d_cond.
viol_e1 :- valid_orig, not option_e_cond.

%% Check violations of (2): option but not orig (valid under option but not orig)
viol_a2 :- option_a_cond, not orig_cond3.
viol_b2 :- option_b_cond, not orig_cond3.
viol_c2 :- option_c_cond, not orig_cond3.
viol_d2 :- option_d_cond, not orig_cond3.
viol_e2 :- option_e_cond, not orig_cond3.

%% A correct option has NO violations of either type
option(a) :- not viol_a1, not viol_a2.
option(b) :- not viol_b1, not viol_b2.
option(c) :- not viol_c1, not viol_c2.
option(d) :- not viol_d1, not viol_d2.
option(e) :- not viol_e1, not viol_e2.

#show option/1.
#show at/2.