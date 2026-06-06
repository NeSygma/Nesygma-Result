% Domains
country(venezuela; yemen; zambia).
candidate(jaramillo; kayne; landon; novetzke; ong).

% Assignment: assigned(Candidate, Country)
1 { assigned(C, V) : candidate(C) } 1 :- country(V).
:- assigned(C1, V1), assigned(C1, V2), V1 != V2.

% Constraint 1: Exactly one of Kayne or Novetzke is assigned (XOR)
1 { assigned(kayne, V) : country(V) ; assigned(novetzke, V) : country(V) } 1.

% Constraint 2: If Jaramillo is assigned, then Kayne must be assigned
:- assigned(jaramillo, _), not assigned(kayne, _).

% Constraint 3: If Ong is assigned to Venezuela, Kayne is not assigned to Yemen
:- assigned(ong, venezuela), assigned(kayne, yemen).

% Constraint 4: If Landon is assigned, it must be to Zambia
:- assigned(landon, V), V != zambia.

% Define unassigned candidates
unassigned(C) :- candidate(C), not assigned(C, _).

% Check which pair is unassigned
% A: jaramillo and novetzke
option(a) :- unassigned(jaramillo), unassigned(novetzke), 
             not unassigned(landon), not unassigned(kayne), not unassigned(ong).

% B: jaramillo and ong
option(b) :- unassigned(jaramillo), unassigned(ong), 
             not unassigned(landon), not unassigned(kayne), not unassigned(novetzke).

% C: kayne and landon
option(c) :- unassigned(kayne), unassigned(landon), 
             not unassigned(jaramillo), not unassigned(novetzke), not unassigned(ong).

% D: kayne and novetzke
option(d) :- unassigned(kayne), unassigned(novetzke), 
             not unassigned(jaramillo), not unassigned(landon), not unassigned(ong).

% E: landon and ong
option(e) :- unassigned(landon), unassigned(ong), 
             not unassigned(jaramillo), not unassigned(kayne), not unassigned(novetzke).

#show option/1.