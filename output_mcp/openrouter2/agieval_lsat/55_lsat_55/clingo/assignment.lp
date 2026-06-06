% Domain facts
country(v). country(y). country(z).
candidate(j). candidate(k). candidate(l). candidate(n). candidate(o).

% Assignment: each country gets exactly one candidate
{ assign(C, X) : candidate(X) } 1 :- country(C).

% Each candidate assigned at most once
:- assign(C1, X), assign(C2, X), C1 != C2.

% Exactly one of Kayne or Novetzke assigned
1 { assign(_, k); assign(_, n) } 1.

% If Jaramillo assigned, Kayne assigned
:- assign(_, j), not assign(_, k).

% If Ong assigned to Venezuela, Kayne not assigned to Yemen
:- assign(v, o), assign(y, k).

% If Landon assigned, Landon assigned to Zambia
:- assign(_, l), not assign(z, l).

% Derived atoms
assigned(X) :- assign(_, X).
not_assigned(X) :- candidate(X), not assigned(X).

% Options
option(a) :- not_assigned(j), not_assigned(n).
option(b) :- not_assigned(j), not_assigned(o).
option(c) :- not_assigned(k), not_assigned(l).
option(d) :- not_assigned(k), not_assigned(n).
option(e) :- not_assigned(l), not_assigned(o).

#show option/1.