%% Approach: Check if for any option, the set of valid orderings under 
%% (base + option) equals the set under (base + original condition 3)
%%
%% We'll check for counterexamples in both directions.

singer(kammer; lugo; trillo; waite; yoshida; zinn).
recorded(kammer; lugo).
nonrecorded(T) :- singer(T), not recorded(T).
position(1..6).

%% Generate all possible orderings (permutations)
1 { at(S, P) : position(P) } 1 :- singer(S).
1 { at(S, P) : singer(S) } 1 :- position(P).

%% Base constraints
:- at(S, 4), recorded(S).
:- at(S, 5), nonrecorded(S).
:- at(kammer, PK), at(trillo, PT), PK >= PT.
:- at(zinn, PZ), at(yoshida, PY), PZ >= PY.

%% Original Condition 3: Waite before Kammer and Lugo
orig_holds :- at(waite, PW), at(kammer, PK), at(lugo, PL), PW < PK, PW < PL.

%% Option A: No singer other than Zinn before Waite
optA_holds :- #count{X : at(X, PX), at(waite, PW), PX < PW, X != zinn} = 0.

%% Option B: Waite immediately before or after Zinn
optB_holds :- at(waite, PW), at(zinn, PZ), |PW - PZ| = 1.

%% Option C: Waite before Lugo
optC_holds :- at(waite, PW), at(lugo, PL), PW < PL.

%% Option D: Waite first or second
optD_holds :- at(waite, PW), PW <= 2.

%% Option E: First audition cannot be recorded
optE_holds :- #count{S : at(S, 1), recorded(S)} = 0.

%% Identify counterexamples
%% Type 1: satisfies base + orig but NOT option
ce_a1 :- orig_holds, not optA_holds.
ce_b1 :- orig_holds, not optB_holds.
ce_c1 :- orig_holds, not optC_holds.
ce_d1 :- orig_holds, not optD_holds.
ce_e1 :- orig_holds, not optE_holds.

%% Type 2: satisfies base + option but NOT orig
ce_a2 :- optA_holds, not orig_holds.
ce_b2 :- optB_holds, not orig_holds.
ce_c2 :- optC_holds, not orig_holds.
ce_d2 :- optD_holds, not orig_holds.
ce_e2 :- optE_holds, not orig_holds.

%% Show counterexamples if they exist
#show ce_a1/0.
#show ce_a2/0.
#show ce_b1/0.
#show ce_b2/0.
#show ce_c1/0.
#show ce_c2/0.
#show ce_d1/0.
#show ce_d2/0.
#show ce_e1/0.
#show ce_e2/0.
#show at/2.