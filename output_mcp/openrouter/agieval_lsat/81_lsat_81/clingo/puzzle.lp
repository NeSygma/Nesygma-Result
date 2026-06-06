% Domains
space(1..7).
business(opt). business(pharm). business(rest1). business(rest2). business(shoe). business(toy). business(vet).

% Assignment: bijection between businesses and spaces
1 { assign(B,S) : space(S) } 1 :- business(B).
1 { assign(B,S) : business(B) } 1 :- space(S).

% Helper predicates
end(1). end(7).
other_end(1,7). other_end(7,1).

neighbor(P,B) :- assign(B,S), S = P+1.
neighbor(P,B) :- assign(B,S), S = P-1.

% Base constraints (as a predicate)
base_ok :-
    assign(pharm,P), end(P),
    other_end(P,O), (assign(rest1,O); assign(rest2,O)),
    ( neighbor(P,opt) ; neighbor(P,vet) ),
    assign(toy,T), not neighbor(T,vet).

% Original restaurant separation (at least two businesses between)
separated_ok :- assign(rest1,X), assign(rest2,Y),
    X != Y+1, X != Y+2, Y != X+1, Y != X+2.

original_ok :- base_ok, separated_ok.

% Alternative A: a restaurant in space 3,4,5
altA_ok :- base_ok, (assign(rest1,S); assign(rest2,S)), S >= 3, S <= 5.

% Alternative B: a restaurant next to optometrist or veterinarian
altB_ok :- base_ok, (
    (assign(rest1,R), (neighbor(R,opt); neighbor(R,vet))) ;
    (assign(rest2,R), (neighbor(R,opt); neighbor(R,vet)))
).

% Helper for low/high between restaurants
low(L) :- assign(rest1,X), assign(rest2,Y), X < Y, L = X.
low(L) :- assign(rest1,X), assign(rest2,Y), Y < X, L = Y.
high(H) :- assign(rest1,X), assign(rest2,Y), X > Y, H = X.
high(H) :- assign(rest1,X), assign(rest2,Y), Y > X, H = Y.

% Alternative C: toy or vet somewhere between the two restaurants
altC_ok :- base_ok, low(L), high(H), (
    (assign(toy,S), S > L, S < H) ;
    (assign(vet,S), S > L, S < H)
).

% Alternative D: no more than two businesses separate pharmacy and nearest restaurant
altD_ok :- base_ok, assign(pharm,P), assign(rest1,R1), assign(rest2,R2), (
    P = R1+1 ; P = R1-1 ; P = R1+2 ; P = R1-2 ; P = R1+3 ; P = R1-3 ;
    P = R2+1 ; P = R2-1 ; P = R2+2 ; P = R2-2 ; P = R2+3 ; P = R2-3
).

% Alternative E: optometrist not next to shoe store
altE_ok :- base_ok, not neighbor(opt,shoe).

% Differences between original and each alternative
diffA1 :- original_ok, not altA_ok.
diffA2 :- altA_ok, not original_ok.

diffB1 :- original_ok, not altB_ok.
diffB2 :- altB_ok, not original_ok.

diffC1 :- original_ok, not altC_ok.
diffC2 :- altC_ok, not original_ok.

diffD1 :- original_ok, not altD_ok.
diffD2 :- altD_ok, not original_ok.

diffE1 :- original_ok, not altE_ok.
diffE2 :- altE_ok, not original_ok.

% Equivalence predicates
eqA :- not diffA1, not diffA2.
eqB :- not diffB1, not diffB2.
eqC :- not diffC1, not diffC2.
eqD :- not diffD1, not diffD2.
eqE :- not diffE1, not diffE2.

option(a) :- eqA.
option(b) :- eqB.
option(c) :- eqC.
option(d) :- eqD.
option(e) :- eqE.

% Ensure at least one option holds
:- not option(a), not option(b), not option(c), not option(d), not option(e).
% Ensure at most one option holds
:- option(a), option(b).
:- option(a), option(c).
:- option(a), option(d).
:- option(a), option(e).
:- option(b), option(c).
:- option(b), option(d).
:- option(b), option(e).
:- option(c), option(d).
:- option(c), option(e).
:- option(d), option(e).

#show option/1.