% Employees and spaces
employee(robertson). employee(souza). employee(togowa). employee(vaughn). employee(xu). employee(young).
space(1..6).

% Each employee gets exactly one space, each space exactly one employee
1 { assign(E, S) : space(S) } 1 :- employee(E).
1 { assign(E, S) : employee(E) } 1 :- space(S).

% Ordering constraints
:- assign(young, Sy), assign(togowa, St), Sy <= St.
:- assign(xu, Sx), assign(souza, Ss), Sx <= Ss.
:- assign(robertson, Sr), assign(young, Sy), Sr <= Sy.
:- assign(robertson, Sr), Sr > 4.

% Additional condition: Togowa > Souza
:- assign(togowa, St), assign(souza, Ss), St <= Ss.

% Option definitions
option(a) :- assign(young, 2).
option(b) :- assign(vaughn, 5).
option(c) :- assign(togowa, 3).
option(d) :- assign(souza, 2).
option(e) :- assign(robertson, 3).

#show option/1.
#show assign/2.