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

% Assignment of houses to slots (bijection)
{ assign(H,S) : slot(S) } 1 :- house(H).
{ assign(H,S) : house(H) } 1 :- slot(S).

% Constraints
:- assign(j,S), not evening(S).   % J must be evening
:- assign(k,S), morning(S).      % K cannot be morning
:- assign(l,Sl), assign(k,Sk), Sl <= Sk.   % L after K
:- assign(l,Sl), assign(m,Sm), Sl >= Sm.   % L before M

% Options mapping
option(a) :- assign(k,S), evening(S).
option(b) :- assign(l,S), afternoon(S).
option(c) :- assign(l,S), evening(S).
option(d) :- assign(m,S), morning(S).
option(e) :- assign(m,S), afternoon(S).

% Enforce the must-be-true option and eliminate others
:- not option(b).   % must have option b true
:- option(a).
:- option(c).
:- option(d).
:- option(e).

#show option/1.