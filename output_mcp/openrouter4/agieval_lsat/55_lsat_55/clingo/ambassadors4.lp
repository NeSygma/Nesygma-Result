% Facts
person(jaramillo; kayne; landon; novetzke; ong).
country(venezuela; yemen; zambia).

% Choice: assign a person to a country (one person per country, one country per person)
1 { assign(P, C) : person(P) } 1 :- country(C).
:- person(P), #count{ C : assign(P, C) } > 1.

% Derived: assigned/1
assigned(P) :- assign(P, _).
unassigned(P) :- person(P), not assigned(P).

% Constraint 1: Exactly one of Kayne or Novetzke is assigned
1 { assigned(kayne); assigned(novetzke) } 1.

% Constraint 2: If Jaramillo assigned then Kayne assigned
:- assigned(jaramillo), not assigned(kayne).

% Constraint 3: If Ong assigned to Venezuela then Kayne not assigned to Yemen
:- assign(ong, venezuela), assign(kayne, yemen).

% Constraint 4: If Landon assigned then it must be to Zambia
:- assigned(landon), not assign(landon, zambia).

% Show the full assignment and unassigned
#show assign/2.
#show unassigned/1.