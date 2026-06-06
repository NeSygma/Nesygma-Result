% base facts
space(1).
space(2).
space(3).
space(4).
space(5).
space(6).

% employees
robertson.
souza.
togowa.
vaughn.
xu.
young.

% assignment constraints (exactly one space per employee)
1 { assign(robertson,S) : space(S) } 1.
1 { assign(souza,S) : space(S) } 1.
1 { assign(togowa,S) : space(S) } 1.
1 { assign(vaughn,S) : space(S) } 1.
1 { assign(xu,S) : space(S) } 1.
1 { assign(young,S) : space(S) } 1.

% all different
:- assign(E1,S), assign(E2,S), E1 != E2.

% ordering constraints
:- assign(young,Sy), assign(togowa,St), Sy <= St.
:- assign(xu,Sx), assign(souza,Ss), Sx <= Ss.
:- assign(robertson,Sr), assign(young,Sy), Sr <= Sy.

% Robertson cannot be 5 or 6
:- assign(robertson,5).
:- assign(robertson,6).

% option definitions
option(a) :- 0=1.
option(b) :- 0=1.
option(c) :- assign(vaughn,3).
option(d) :- 0=1.
option(e) :- 0=1.

#show option/1.