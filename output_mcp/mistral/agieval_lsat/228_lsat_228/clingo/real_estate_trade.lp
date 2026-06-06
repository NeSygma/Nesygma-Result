% Buildings and their classes (class doesn't change)
building_class(garza_tower, 1).
building_class(yates_house, 3).
building_class(zimmer_house, 3).
building_class(flores_tower, 1).
building_class(lynch_building, 2).
building_class(king_building, 2).
building_class(meyer_building, 2).
building_class(ortiz_building, 2).

% Companies
company(realprop; southco; trustcorp).

% Buildings
building(B) :- building_class(B, _).

% In the final state, each building is owned by exactly one company
{final_owner(B, C) : company(C)} = 1 :- building(B).

% The class of a building doesn't change
final_class(B, Cl) :- building_class(B, Cl).

% Constraint: RealProp owns only class 2 buildings
% This means: if RealProp owns a building, it must be class 2
:- final_owner(B, realprop), final_class(B, Cl), Cl != 2.

% Answer choice conditions:

% (A) Trustcorp owns a class 1 building
option(a) :- final_owner(B, trustcorp), final_class(B, 1).

% (B) Trustcorp owns the Meyer Building
option(b) :- final_owner(meyer_building, trustcorp).

% (C) Southco owns a class 2 building
option(c) :- final_owner(B, southco), final_class(B, 2).

% (D) Southco owns both of the class 3 buildings
option(d) :- final_owner(yates_house, southco), final_owner(zimmer_house, southco).

% (E) Southco owns the Flores Tower
option(e) :- final_owner(flores_tower, southco).

% Show the options
#show option/1.