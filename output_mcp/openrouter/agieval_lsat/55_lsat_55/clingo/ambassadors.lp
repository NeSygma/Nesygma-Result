% Candidates
cand(jaramillo). cand(kayne). cand(landon). cand(novetzke). cand(ong).
% Countries
country(venezuela). country(yemen). country(zambia).

% Assignment choice: each candidate may be assigned to at most one country
{ assign(C,Co) : country(Co) } 1 :- cand(C).

% Exactly three assignments total
:- #count{ C,Co : assign(C,Co) } != 3.

% Each country assigned to exactly one candidate
:- country(Co), not assigned_one(Co).
assigned_one(Co) :- assign(_,Co).

% No two candidates to same country
:- assign(C1,Co), assign(C2,Co), C1 != C2.

% Helper: assigned predicate
assigned(C) :- assign(C,_).

% Constraint 1: exactly one of Kayne or Novetzke assigned
:- assigned(kayne), assigned(novetzke).
:- not assigned(kayne), not assigned(novetzke).

% Constraint 2: Jaramillo implies Kayne
:- assigned(jaramillo), not assigned(kayne).

% Constraint 3: Ong to Venezuela implies Kayne not to Yemen
:- assign(ong,venezuela), assign(kayne,yemen).

% Constraint 4: Landon only to Zambia
:- assign(landon,Co), Co != zambia.

% Options: which two are not assigned
option(a) :- not assigned(jaramillo), not assigned(novetzke).
option(b) :- not assigned(jaramillo), not assigned(ong).
option(c) :- not assigned(kayne), not assigned(landon).
option(d) :- not assigned(kayne), not assigned(novetzke).
option(e) :- not assigned(landon), not assigned(ong).

% Exactly one option must hold
:- #count{ X : option(X) } != 1.

#show option/1.