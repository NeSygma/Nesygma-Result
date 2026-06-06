% Domain facts
country(venezuela). country(yemen). country(zambia).
ambassador(jaramillo). ambassador(kayne). ambassador(landon). ambassador(novetzke). ambassador(ong).

% Exactly one ambassador per country
1 { assignment(C, A) : ambassador(A) } 1 :- country(C).

% At most one country per ambassador
:- assignment(C1, A), assignment(C2, A), C1 != C2.

% Option facts
option(b).

% Assignment facts based on option
assignment(venezuela, jaramillo) :- option(a).
assignment(yemen, ong) :- option(a).
assignment(zambia, novetzke) :- option(a).

assignment(venezuela, kayne) :- option(b).
assignment(yemen, jaramillo) :- option(b).
assignment(zambia, landon) :- option(b).

assignment(venezuela, landon) :- option(c).
assignment(yemen, novetzke) :- option(c).
assignment(zambia, ong) :- option(c).

assignment(venezuela, novetzke) :- option(d).
assignment(yemen, jaramillo) :- option(d).
assignment(zambia, kayne) :- option(d).

assignment(venezuela, ong) :- option(e).
assignment(yemen, kayne) :- option(e).
assignment(zambia, landon) :- option(e).

% Derived predicates for assigned ambassadors
assigned_kayne :- assignment(C, kayne).
assigned_novetzke :- assignment(C, novetzke).
assigned_jaramillo :- assignment(C, jaramillo).
assigned_landon :- assignment(C, landon).
assigned_ong :- assignment(C, ong).

% Constraints
:- not assigned_kayne, not assigned_novetzke.
:- assigned_kayne, assigned_novetzke.
:- assigned_jaramillo, not assigned_kayne.
:- assignment(venezuela, ong), assignment(yemen, kayne).
:- assignment(C, landon), C != zambia.

#show option/1.