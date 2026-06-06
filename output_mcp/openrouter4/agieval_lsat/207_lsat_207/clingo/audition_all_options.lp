%% Domain
singer(kammer; lugo; trillo; waite; yoshida; zinn).
recorded(kammer; lugo).
position(1..6).

%% Exactly one singer per position, each singer at exactly one position
1 { at(S, P) : position(P) } 1 :- singer(S).
1 { at(S, P) : singer(S) } 1 :- position(P).

%% Fixed constraints (always apply)
:- at(S, 4), recorded(S).              %% 4th cannot be recorded
:- at(S, 5), not recorded(S).          %% 5th must be recorded
:- at(kammer, PK), at(trillo, PT), PK >= PT.  %% Kammer before Trillo
:- at(zinn, PZ), at(yoshida, PY), PZ >= PY.   %% Zinn before Yoshida

%% Original condition: Waite before both recorded (Kammer and Lugo)
orig_holds :- at(waite, PW), at(kammer, PK), at(lugo, PL), PW < PK, PW < PL.

%% Option A: Zinn is the only one that can take place earlier than Waite
%% i.e., no singer X (X != zinn) can be before Waite
optA_holds :- at(waite, PW), 
              #count{X : at(X, PX), PX < PW, X != zinn} = 0.

%% Option B: Waite immediately before or after Zinn
optB_holds :- at(waite, PW), at(zinn, PZ), (PW = PZ + 1; PZ = PW + 1).

%% Option C: Waite before Lugo
optC_holds :- at(waite, PW), at(lugo, PL), PW < PL.

%% Option D: Waite is 1st or 2nd
optD_holds :- at(waite, 1).
optD_holds :- at(waite, 2).

%% Option E: The first audition cannot be recorded
optE_holds :- not at(S, 1) : recorded(S).

%% Counterexample for each option
%% Type 1: orig holds but optX does not hold
%% Type 2: optX holds but orig does not hold

%% Option A
ce_a1 :- orig_holds, not optA_holds.
ce_a2 :- optA_holds, not orig_holds.

%% Option B
ce_b1 :- orig_holds, not optB_holds.
ce_b2 :- optB_holds, not orig_holds.

%% Option C
ce_c1 :- orig_holds, not optC_holds.
ce_c2 :- optC_holds, not orig_holds.

%% Option D
ce_d1 :- orig_holds, not optD_holds.
ce_d2 :- optD_holds, not orig_holds.

%% Option E
ce_e1 :- orig_holds, not optE_holds.
ce_e2 :- optE_holds, not orig_holds.

%% Helper: show which options have counterexamples
bad_option(A) :- ce_a1.
bad_option(A) :- ce_a2.
bad_option(B) :- ce_b1.
bad_option(B) :- ce_b2.
bad_option(C) :- ce_c1.
bad_option(C) :- ce_c2.
bad_option(D) :- ce_d1.
bad_option(D) :- ce_d2.
bad_option(E) :- ce_e1.
bad_option(E) :- ce_e2.

good_option(X) :- singer(X), not bad_option(X).  %% not used this way

#show orig_holds/0.
#show optA_holds/0.
#show optB_holds/0.
#show optC_holds/0.
#show optD_holds/0.
#show optE_holds/0.
#show ce_a1/0. #show ce_a2/0.
#show ce_b1/0. #show ce_b2/0.
#show ce_c1/0. #show ce_c2/0.
#show ce_d1/0. #show ce_d2/0.
#show ce_e1/0. #show ce_e2/0.
#show at/2.