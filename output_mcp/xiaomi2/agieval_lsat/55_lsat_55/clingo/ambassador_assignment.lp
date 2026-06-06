% Define countries and candidates
country(venezuela).
country(yemen).
country(zambia).

candidate(jaramillo).
candidate(kayne).
candidate(landon).
candidate(novetzke).
candidate(ong).

% Each country gets exactly one ambassador
1 { assigned(Candidate, Country) : candidate(Candidate) } 1 :- country(Country).

% Each candidate can be assigned to at most one country
0 { assigned(Candidate, Country) : country(Country) } 1 :- candidate(Candidate).

% Constraint 1: Exactly one of Kayne or Novetzke is assigned (but not both)
assigned(kayne, _) | assigned(novetzke, _).
:- assigned(kayne, _), assigned(novetzke, _).

% Constraint 2: If Jaramillo is assigned, then Kayne must be assigned
:- assigned(jaramillo, _), not assigned(kayne, _).

% Constraint 3: If Ong is assigned to Venezuela, then Kayne cannot be assigned to Yemen
:- assigned(ong, venezuela), assigned(kayne, yemen).

% Constraint 4: If Landon is assigned, it must be to Zambia
:- assigned(landon, Country), Country != zambia.

% Define unassigned candidates
unassigned(Candidate) :- candidate(Candidate), not assigned(Candidate, _).

% Count unassigned candidates
unassigned_count(N) :- N = #count{Candidate : unassigned(Candidate)}.

% We need exactly 2 unassigned candidates (since 5 candidates, 3 assignments)
:- unassigned_count(N), N != 2.

% Define pairs of unassigned candidates
unassigned_pair(C1, C2) :- unassigned(C1), unassigned(C2), C1 < C2.

% Check each option
option(a) :- unassigned_pair(jaramillo, novetzke).
option(b) :- unassigned_pair(jaramillo, ong).
option(c) :- unassigned_pair(kayne, landon).
option(d) :- unassigned_pair(kayne, novetzke).
option(e) :- unassigned_pair(landon, ong).

#show option/1.