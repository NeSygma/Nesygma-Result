% Species, zones, seasons, and levels
species(grass; rabbit; fox; hawk).
zone(forest; meadow).
season(summer; winter).
level(0; 1; 2).

% Predator-prey relationships
predator_prey(rabbit, grass).
predator_prey(fox, rabbit).
predator_prey(hawk, fox).

% Choice rule: each (species, zone, season) has a population level
{ population(S, Z, Sn, L) : level(L) } = 1 :-
    species(S), zone(Z), season(Sn).

% Carrying capacity constraints
% Grass max level 1 in Forest
:- population(grass, forest, _, L), L > 1.

% Foxes level 0 in Meadow
:- population(fox, meadow, _, L), L > 0.

% Hawks max level 1 everywhere
:- population(hawk, _, _, L), L > 1.

% Winter scarcity constraints
% Grass max level 1 in Winter
:- population(grass, _, winter, L), L > 1.

% Rabbits cannot have high (2) level in Winter
:- population(rabbit, _, winter, L), L > 1.

% Predator-Prey balance constraints
% For each (zone, season) and each predator-prey pair,
% the predator's level must be <= prey's level
:- population(Pred, Z, Sn, L_pred),
   population(Prey, Z, Sn, L_prey),
   predator_prey(Pred, Prey),
   L_pred > L_prey.

% Biodiversity: each species must have total population >= 1
:- species(S), #sum { L, Z, Sn : population(S, Z, Sn, L) } = 0.

% Hawk population must be exactly 2
:- #sum { L, Z, Sn : population(hawk, Z, Sn, L) } != 2.

% Balance achieved if all constraints are satisfied
balance_achieved.

% Show the relevant predicates
#show population/4.
#show balance_achieved.