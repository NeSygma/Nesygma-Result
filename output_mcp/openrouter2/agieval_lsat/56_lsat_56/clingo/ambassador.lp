% Domain facts
country(venezuela). country(yemen). country(zambia).
ambassador(jaramillo). ambassador(kayne). ambassador(landon). ambassador(novetzke). ambassador(ong).

% Exactly one ambassador per country
1 { assigned(C, A) : ambassador(A) } 1 :- country(C).

% At most one country per ambassador
0 { assigned(C, A) : country(C) } 1 :- ambassador(A).

% Exactly one of Kayne or Novetzke assigned
:- assigned(C, kayne), assigned(C2, novetzke).
:- not assigned(C, kayne), not assigned(C, novetzke).

% If Jaramillo assigned, then Kayne assigned
:- assigned(C, jaramillo), not assigned(C2, kayne).

% If Ong assigned to Venezuela, Kayne not assigned to Yemen
:- assigned(venezuela, ong), assigned(yemen, kayne).

% If Landon assigned, it is to Zambia
:- assigned(C, landon), C != zambia.

% Fact: Ong assigned to Venezuela
assigned(venezuela, ong).

% Option rules
option(a) :- assigned(yemen, jaramillo), assigned(zambia, landon).
option(a) :- assigned(yemen, landon), assigned(zambia, jaramillo).

option(b) :- assigned(yemen, jaramillo), assigned(zambia, novetzke).
option(b) :- assigned(yemen, novetzke), assigned(zambia, jaramillo).

option(c) :- assigned(yemen, kayne), assigned(zambia, landon).
option(c) :- assigned(yemen, landon), assigned(zambia, kayne).

option(d) :- assigned(yemen, kayne), assigned(zambia, novetzke).
option(d) :- assigned(yemen, novetzke), assigned(zambia, kayne).

option(e) :- assigned(yemen, landon), assigned(zambia, novetzke).
option(e) :- assigned(yemen, novetzke), assigned(zambia, landon).

% Uniqueness constraints
:- option(a), option(b).
:- option(a), option(c).
:- option(a), option(d).
:- option(a), option(e).
:- option(b), option(c).
:- option(b), option(d).
:- option(b), option(e).
:- option(c), option(d).
:- option(c), option(e).
:- option(d), option(e).

% At least one option
:- not option(a), not option(b), not option(c), not option(d), not option(e).

#show option/1.