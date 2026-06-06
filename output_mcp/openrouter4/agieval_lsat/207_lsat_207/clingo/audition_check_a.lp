%% Focus: Check if Option A has any counterexample
singer(kammer; lugo; trillo; waite; yoshida; zinn).
recorded(kammer; lugo).
nonrecorded(T) :- singer(T), not recorded(T).
position(1..6).

1 { at(S, P) : position(P) } 1 :- singer(S).
1 { at(S, P) : singer(S) } 1 :- position(P).

:- at(S, 4), recorded(S).
:- at(S, 5), nonrecorded(S).
:- at(kammer, PK), at(trillo, PT), PK >= PT.
:- at(zinn, PZ), at(yoshida, PY), PZ >= PY.

orig_holds :- at(waite, PW), at(kammer, PK), at(lugo, PL), PW < PK, PW < PL.

optA_holds :- #count{X : at(X, PX), at(waite, PW), PX < PW, X != zinn} = 0.

%% Type 1: orig but not optA
:- not ce_a1, orig_holds, not optA_holds.
ce_a1 :- orig_holds, not optA_holds.

%% Type 2: optA but not orig
:- not ce_a2, optA_holds, not orig_holds.
ce_a2 :- optA_holds, not orig_holds.

%% At least one counterexample must exist
:- not ce_a1, not ce_a2.

#show ce_a1/0.
#show ce_a2/0.
#show at/2.