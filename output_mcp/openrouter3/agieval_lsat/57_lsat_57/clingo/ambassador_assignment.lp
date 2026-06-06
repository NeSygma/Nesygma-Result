% Domain declarations
country(venezuela). country(yemen). country(zambia).
candidate(jaramillo). candidate(kayne). candidate(landon). candidate(novetzke). candidate(ong).

% Assignment predicate: assigned(Candidate, Country)
{ assigned(C, Country) : country(Country) } 1 :- candidate(C).

% Constraint 1: Each country gets exactly one ambassador
1 { assigned(C, Country) : candidate(C) } 1 :- country(Country).

% Constraint 2: Either Kayne or Novetzke, but not both, is assigned
% Exactly one of them is assigned to some country
assigned_kayne_or_novetzke :- assigned(kayne, _).
assigned_kayne_or_novetzke :- assigned(novetzke, _).
:- assigned(kayne, _), assigned(novetzke, _).  % Not both
:- not assigned_kayne_or_novetzke.  % At least one

% Constraint 3: If Jaramillo is assigned, then Kayne is assigned
:- assigned(jaramillo, _), not assigned(kayne, _).

% Constraint 4: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
:- assigned(ong, venezuela), assigned(kayne, yemen).

% Constraint 5: If Landon is assigned, it is to Zambia
:- assigned(landon, Country), Country != zambia.

% Additional constraint: No ambassador assigned to more than one country
% This is already enforced by the choice rule (exactly one country per candidate)

% THE QUESTION CONDITION: Kayne is assigned to Yemen
:- not assigned(kayne, yemen).

% Answer choices evaluation
% (A) Jaramillo is assigned as ambassador to Venezuela
option(a) :- assigned(jaramillo, venezuela).

% (B) Landon is assigned as ambassador to Zambia
option(b) :- assigned(landon, zambia).

% (C) Ong is assigned as ambassador to Zambia
option(c) :- assigned(ong, zambia).

% (D) Jaramillo is not assigned to an ambassadorship
option(d) :- not assigned(jaramillo, _).

% (E) Ong is not assigned to an ambassadorship
option(e) :- not assigned(ong, _).

#show option/1.