% Persons and countries
person(jaramillo). person(kayne). person(novetzke). person(landon). person(ong).
country(venezuela). country(yemen). country(zambia).

% Exactly one ambassador per country
1 { assign(P,C) : person(P) } 1 :- country(C).
% At most one country per person
:- assign(P,C1), assign(P,C2), C1 != C2.

% Constraint: exactly one of Kayne or Novetzke assigned
assigned_kayne :- assign(kayne,_).
assigned_novetzke :- assign(novetzke,_).
:- assigned_kayne, assigned_novetzke.
:- not assigned_kayne, not assigned_novetzke.

% If Jaramillo assigned then Kayne assigned
:- assign(jaramillo,_), not assigned_kayne.

% If Ong assigned to Venezuela then Kayne not assigned to Yemen
:- assign(ong,venezuela), assign(kayne,yemen).

% If Landon assigned, it must be to Zambia
:- assign(landon,C), C != zambia.

% Premise: Ong assigned to Venezuela
assign(ong,venezuela).

% Identify the other two ambassadors (excluding Ong)
other(P) :- assign(P,_), P != ong.

% Options mapping
option(a) :- other(jaramillo), other(landon), not other(kayne), not other(novetzke).
option(b) :- other(jaramillo), other(novetzke), not other(kayne), not other(landon).
option(c) :- other(kayne), other(landon), not other(jaramillo), not other(novetzke).
option(d) :- other(kayne), other(novetzke), not other(jaramillo), not other(landon).
option(e) :- other(landon), other(novetzke), not other(jaramillo), not other(kayne).

% Ensure exactly one option holds
:- option(X), option(Y), X != Y.

#show option/1.