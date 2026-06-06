% Domain definitions
species(grass). species(rabbits). species(foxes). species(hawks).
zone(forest). zone(meadow).
season(summer). season(winter).
level(0). level(1). level(2).

% Predator-prey relationships
prey(rabbits, grass).
prey(foxes, rabbits).
prey(hawks, foxes).

% Generate population levels for each species-zone-season combination
1 { population(S, Z, Se, L) : level(L) } 1 :- species(S), zone(Z), season(Se).

% Constraint 1: Carrying Capacity
% Grass max level 1 in Forest
:- population(grass, forest, _, 2).

% Foxes level 0 in Meadow
:- population(foxes, meadow, _, L), L != 0.

% Hawks max level 1 everywhere
:- population(hawks, _, _, 2).

% Constraint 2: Winter Scarcity
% Grass max level 1 in Winter
:- population(grass, _, winter, 2).

% Rabbits cannot have high (2) level in Winter
:- population(rabbits, _, winter, 2).

% Constraint 3: Predator-Prey Balance
% In any given location (zone, season), predator level <= prey level
:- population(Predator, Z, Se, PL), population(Prey, Z, Se, PreyL), 
   prey(Predator, Prey), PL > PreyL.

% Constraint 4: Biodiversity
% Total population for each species must be at least 1
total_species(S, T) :- species(S), T = #sum{L, Z, Se : population(S, Z, Se, L)}.
:- total_species(S, T), T < 1.

% Constraint 5: Hawk Population
% Total population level for Hawks must be exactly 2
total_species(hawks, 2).

% Show the population levels
#show population/4.
#show total_species/2.