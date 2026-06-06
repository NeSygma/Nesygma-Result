% Houses and slots
house(j). house(k). house(l). house(m). house(n). house(o). house(p).
slot(1..7).

morning(S) :- S=1.
morning(S) :- S=2.
afternoon(S) :- S=3.
afternoon(S) :- S=4.
afternoon(S) :- S=5.
evening(S) :- S=6.
evening(S) :- S=7.

% Assignment of houses to slots
{ assign(H,S) : slot(S) } 1 :- house(H).
{ assign(H,S) : house(H) } 1 :- slot(S).

% Constraints
:- assign(j,S), not evening(S).
:- assign(k,S), morning(S).
:- assign(l,Sl), assign(k,Sk), Sl <= Sk.
:- assign(l,Sl), assign(m,Sm), Sl >= Sm.

% Options mapping
option(a) :- assign(k,S), evening(S).
option(b) :- assign(l,S), afternoon(S).
option(c) :- assign(l,S), evening(S).
option(d) :- assign(m,S), morning(S).
option(e) :- assign(m,S), afternoon(S).

#show option/1.