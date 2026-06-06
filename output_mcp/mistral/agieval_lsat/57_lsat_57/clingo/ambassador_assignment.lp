% Countries and candidates
country(venezuela; yemen; zambia).
candidate(jaramillo; kayne; landon; novetzke; ong).

% Each country gets exactly one ambassador
1 { assigned(Candidate, Country) : candidate(Candidate) } 1 :- country(Country).

% No ambassador to multiple countries
:- candidate(C), { assigned(C, _) } 2.

% Constraint 2: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
kayne_assigned :- assigned(kayne, _).
novetzke_assigned :- assigned(novetzke, _).
:- kayne_assigned, novetzke_assigned.
:- not kayne_assigned, not novetzke_assigned.

% Constraint 3: If Jaramillo is assigned, then Kayne must be assigned
:- assigned(jaramillo, _), not assigned(kayne, _).

% Constraint 4: If Ong is ambassador to Venezuela, Kayne is not ambassador to Yemen
:- assigned(ong, venezuela), assigned(kayne, yemen).

% Constraint 5: If Landon is assigned to an ambassadorship, it is to Zambia
:- assigned(landon, Country), Country != zambia.

% Given condition: Kayne is assigned as ambassador to Yemen
assigned(kayne, yemen).

% Helper predicates for answer mapping
jaramillo_assigned_to_venezuela :- assigned(jaramillo, venezuela).
landon_assigned_to_zambia :- assigned(landon, zambia).
ong_assigned_to_zambia :- assigned(ong, zambia).
jaramillo_assigned :- assigned(jaramillo, _).
ong_assigned :- assigned(ong, _).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- jaramillo_assigned_to_venezuela.
option(b) :- landon_assigned_to_zambia.
option(c) :- ong_assigned_to_zambia.
option(d) :- not jaramillo_assigned.
option(e) :- not ong_assigned.

#show option/1.