% persons and countries
person(j). person(k). person(l). person(n). person(o).
country(vene). country(yemen). country(zambia).

% assignment choice
1 { assign(P,C) : person(P) } 1 :- country(C).
% at most one country per person
:- assign(P,C1), assign(P,C2), C1 != C2.
% helper assigned predicate
assigned(P) :- assign(P,_).

% exactly one of Kayne or Novetzke assigned
:- assigned(k), assigned(n).
:- not assigned(k), not assigned(n).

% original J -> K
:- assigned(j), not assigned(k).

% Ong to Venezuela implies Kayne not Yemen
:- assign(o,vene), assign(k,yemen).

% Landon only to Zambia
:- assign(l,C), C != zambia.

#show assign/2.