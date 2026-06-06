% Candidates
candidate(jaramillo).
candidate(kayne).
candidate(landon).
candidate(novetzke).
candidate(ong).

% Countries
country(venezuela).
country(yemen).
country(zambia).

% Assignment: each candidate can be assigned to at most one country
{ assigned(C, Country) : country(Country) } 0..1 :- candidate(C).

% Each country must have exactly one ambassador
1 { assigned(C, Country) : candidate(C) } 1 :- country(Country).

% Define assigned_to_any(C) if candidate is assigned to some country
assigned_to_any(C) :- assigned(C, _).

% Constraint 2: Either Kayne or Novetzke, but not both, is assigned
1 { assigned_to_any(kayne), assigned_to_any(novetzke) } 1.

% Constraint 3: If Jaramillo is assigned, then Kayne is assigned
:- assigned_to_any(jaramillo), not assigned_to_any(kayne).

% Constraint 4: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
:- assigned(ong, venezuela), assigned(kayne, yemen).

% Constraint 5: If Landon is assigned, then to Zambia
:- assigned(landon, Country), Country != zambia.

% Define unassigned candidates
unassigned(C) :- candidate(C), not assigned_to_any(C).

% Ensure exactly two unassigned (since 3 assigned)
2 { unassigned(C) : candidate(C) } 2.

% Derive option atoms based on unassigned pair
option(a) :- unassigned(jaramillo), unassigned(novetzke).
option(b) :- unassigned(jaramillo), unassigned(ong).
option(c) :- unassigned(kayne), unassigned(landon).
option(d) :- unassigned(kayne), unassigned(novetzke).
option(e) :- unassigned(landon), unassigned(ong).

% Show only the option that is true in the model
#show option/1.