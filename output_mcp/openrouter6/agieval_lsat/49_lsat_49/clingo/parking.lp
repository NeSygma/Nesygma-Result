% Employees and spaces
employee(robertson). employee(souza). employee(togowa). employee(vaughn). employee(xu). employee(young).
space(1..6).

% Assign each employee exactly one space
1 { assign(E, S) : space(S) } 1 :- employee(E).

% No two employees get the same space
:- assign(E1, S), assign(E2, S), E1 != E2.

% Ordering constraints
:- assign(young, Sy), assign(togowa, St), Sy <= St.
:- assign(xu, Sx), assign(souza, Ss), Sx <= Ss.
:- assign(robertson, Sr), assign(young, Sy), Sr <= Sy.

% Robertson's space constraint (1-4)
:- assign(robertson, Sr), Sr > 4.

% Extra condition: Togowa > Souza
:- assign(togowa, St), assign(souza, Ss), St <= Ss.

% Force Vaughn to be 5 to demonstrate that option B could be true
% (This is one of the two possible assignments)
assign(vaughn, 5).

% Derive option conditions
option(a) :- assign(young, 2).
option(b) :- assign(vaughn, 5).
option(c) :- assign(togowa, 3).
option(d) :- assign(souza, 2).
option(e) :- assign(robertson, 3).

#show option/1.