% Domains
species(grass; rabbits; foxes; hawks).
zones(forest; meadow).
seasons(summer; winter).
levels(0; 1; 2).

% Predator-prey relationships
predator_prey(rabbits, grass).
predator_prey(foxes, rabbits).
predator_prey(hawks, foxes).

% Choice rule: Assign population levels
{ population(S, Z, Se, L) : levels(L) } = 1 :- species(S), zones(Z), seasons(Se).

% Carrying capacity constraints
% Grass in forest has max level 1
:- population(grass, forest, _, L), L > 1.
% Foxes in meadow have level 0
:- population(foxes, meadow, _, L), L > 0.
% Hawks have max level 1 everywhere
:- population(hawks, _, _, L), L > 1.

% Winter scarcity constraints
% Grass in winter has max level 1
:- population(grass, _, winter, L), L > 1.
% Rabbits cannot have level 2 in winter
:- population(rabbits, _, winter, 2).

% Predator-prey balance constraints
% For each predator-prey pair, ensure predator level <= prey level in the same zone and season
:- predator_prey(Predator, Prey),
   zones(Z), seasons(Se),
   population(Predator, Z, Se, PL),
   population(Prey, Z, Se, PrL),
   PL > PrL.

% Biodiversity: Total population for each species must be at least 1
:- species(S),
   #sum { L, Z, Se : population(S, Z, Se, L) } = 0.

% Hawk population must be exactly 2
:- #sum { L, Z, Se : population(hawks, Z, Se, L) } != 2.

% Derive balance_achieved if all constraints are satisfied
balance_achieved :- not exception.

% Show the population levels and balance_achieved
#show population/4.
#show balance_achieved/0.