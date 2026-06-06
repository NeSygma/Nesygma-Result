% Domain: countries and candidates
country(venezuela; yemen; zambia).
candidate(jaramillo; kayne; landon; novetzke; ong).

% Each country gets exactly one ambassador
1 { assigned(Co, C) : candidate(C) } 1 :- country(Co).
% Each candidate can be assigned to at most one country
:- candidate(C), #count{Co : assigned(Co, C)} > 1.

% Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships.
assigned_kayne :- assigned(_, kayne).
assigned_novetzke :- assigned(_, novetzke).
:- assigned_kayne, assigned_novetzke.  % not both
:- not assigned_kayne, not assigned_novetzke.  % at least one

% Constraint 2: If Jaramillo is assigned to one of the ambassadorships, then so is Kayne.
assigned_jaramillo :- assigned(_, jaramillo).
:- assigned_jaramillo, not assigned_kayne.

% Constraint 3: If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen.
:- assigned(venezuela, ong), assigned(yemen, kayne).

% Constraint 4: If Landon is assigned to an ambassadorship, it is to Zambia.
assigned_landon :- assigned(_, landon).
:- assigned_landon, not assigned(zambia, landon).

#show assigned/2.