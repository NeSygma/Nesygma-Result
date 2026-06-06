% domain facts
space(1).
space(2).
space(3).
space(4).
space(5).
space(6).

% employee facts
emp(robertson).
emp(souza).
emp(togowa).
emp(vaughn).
emp(xu).
emp(young).

% assignment predicate
assign(E,S) :- emp(E), space(S).

% exactly one space per employee
1 { assign(E,S) : space(S) } 1 :- emp(E).

% all different
:- assign(E1,S), assign(E2,S), E1 != E2.

% ordering constraints
:- assign(young,Sy), assign(togowa,St), Sy <= St.
:- assign(xu,Sx), assign(souza,Ss), Sx <= Ss.
:- assign(robertson,Sr), assign(young,Sy), Sr <= Sy.

% Robertson must be 1-4
:- assign(robertson,5).
:- assign(robertson,6).

% Force Vaughn to space 3 (the condition that yields uniqueness)
assign(vaughn,3).

% Option definitions
option(a) :- 0=1.
option(b) :- 0=1.
option(c) :- assign(vaughn,3).
option(d) :- 0=1.
option(e) :- 0=1.

#show option/1.