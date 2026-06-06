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

% Show assignments
#show assigned/2.