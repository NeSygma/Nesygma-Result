% Define the countries and candidates
country(venezuela).
country(yemen).
country(zambia).

candidate(jaramillo).
candidate(kayne).
candidate(landon).
candidate(novetzke).
candidate(ong).

% Assign exactly one ambassador to each country
1 { assignment(Country, Candidate) : candidate(Candidate) } 1 :- country(Country).

% No ambassador is assigned to more than one country
:- candidate(Candidate), 2 { assignment(Country, Candidate) : country(Country) }.

% Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
:- 2 { assignment(Country, kayne) : country(Country) }.
:- 2 { assignment(Country, novetzke) : country(Country) }.
:- not (1 { assignment(Country, kayne) : country(Country) } + 1 { assignment(Country, novetzke) : country(Country) } = 1).

% Constraint 2: If Jaramillo is assigned to one of the ambassadorships, then so is Kayne
:- assignment(Country, jaramillo), not 1 { assignment(Country, kayne) : country(Country) }.

% Constraint 3: If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen
:- assignment(venezuela, ong), assignment(yemen, kayne).

% Constraint 4: If Landon is assigned to an ambassadorship, it is to Zambia
:- assignment(Country, landon), Country != zambia.

% Given condition: Kayne is assigned as ambassador to Yemen
assignment(yemen, kayne).

% Map the correct answer to option/1
% (A) Jaramillo is assigned as ambassador to Venezuela
option(a) :- assignment(venezuela, jaramillo).

% (B) Landon is assigned as ambassador to Zambia
option(b) :- assignment(zambia, landon).

% (C) Ong is assigned as ambassador to Zambia
option(c) :- assignment(zambia, ong).

% (D) Jaramillo is not assigned to an ambassadorship
option(d) :- not assignment(_, jaramillo).

% (E) Ong is not assigned to an ambassadorship
option(e) :- not assignment(_, ong).

#show option/1.