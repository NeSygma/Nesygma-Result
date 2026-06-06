% Ecosystem Modeling in Clingo ASP

% ===== DOMAIN DEFINITIONS =====
species(grass).
species(rabbits).
species(foxes).
species(hawks).

% Carrying capacities
carrying_capacity(grass, 100).
carrying_capacity(rabbits, 30).
carrying_capacity(foxes, 10).
carrying_capacity(hawks, 5).

% ===== FEEDING RELATIONSHIPS =====
eats(rabbits, grass).
eats(foxes, rabbits).
eats(hawks, rabbits).
eats(hawks, foxes).

% ===== DECISION VARIABLES =====
% Population levels for each species (integer values from 1 to carrying capacity)
% Use choice rules with explicit domain
{ population(grass, P) } :- P = 1..100.
{ population(rabbits, P) } :- P = 1..30.
{ population(foxes, P) } :- P = 1..10.
{ population(hawks, P) } :- P = 1..5.

% Exactly one population value per species
1 { population(grass, P) : P = 1..100 } 1.
1 { population(rabbits, P) : P = 1..30 } 1.
1 { population(foxes, P) : P = 1..10 } 1.
1 { population(hawks, P) : P = 1..5 } 1.

% Consumption rates between predator and prey (0.1 to 0.5 in steps of 0.1)
{ consumption_rate(rabbits, grass, 0.1) }.
{ consumption_rate(rabbits, grass, 0.2) }.
{ consumption_rate(rabbits, grass, 0.3) }.
{ consumption_rate(rabbits, grass, 0.4) }.
{ consumption_rate(rabbits, grass, 0.5) }.

{ consumption_rate(foxes, rabbits, 0.1) }.
{ consumption_rate(foxes, rabbits, 0.2) }.
{ consumption_rate(foxes, rabbits, 0.3) }.
{ consumption_rate(foxes, rabbits, 0.4) }.
{ consumption_rate(foxes, rabbits, 0.5) }.

{ consumption_rate(hawks, rabbits, 0.1) }.
{ consumption_rate(hawks, rabbits, 0.2) }.
{ consumption_rate(hawks, rabbits, 0.3) }.
{ consumption_rate(hawks, rabbits, 0.4) }.
{ consumption_rate(hawks, rabbits, 0.5) }.

{ consumption_rate(hawks, foxes, 0.1) }.
{ consumption_rate(hawks, foxes, 0.2) }.
{ consumption_rate(hawks, foxes, 0.3) }.
{ consumption_rate(hawks, foxes, 0.4) }.
{ consumption_rate(hawks, foxes, 0.5) }.

% Exactly one consumption rate per relationship
1 { consumption_rate(rabbits, grass, R) : R = 0.1..0.5 } 1.
1 { consumption_rate(foxes, rabbits, R) : R = 0.1..0.5 } 1.
1 { consumption_rate(hawks, rabbits, R) : R = 0.1..0.5 } 1.
1 { consumption_rate(hawks, foxes, R) : R = 0.1..0.5 } 1.

% ===== CONSTRAINTS =====

% 3. Herbivore populations must be sustainable relative to primary producers
% Rabbits ≤ 0.5 × Grass
:- population(rabbits, R), population(grass, G), R > 0.5 * G.

% 4. Predator populations must be sustainable relative to prey
% Foxes ≤ 0.3 × Rabbits
:- population(foxes, F), population(rabbits, R), F > 0.3 * R.

% 5. No species can go extinct (all populations > 0) - already enforced by domain

% ===== OUTPUT PREDICATES =====
% Stable populations output
stable_populations(S, P) :- population(S, P).

% Food web relationships output - select one consumption rate per relationship
food_web(rabbits, grass, R) :- consumption_rate(rabbits, grass, R).
food_web(foxes, rabbits, R) :- consumption_rate(foxes, rabbits, R).
food_web(hawks, rabbits, R) :- consumption_rate(hawks, rabbits, R).
food_web(hawks, foxes, R) :- consumption_rate(hawks, foxes, R).

% ===== ECOSYSTEM HEALTH CALCULATIONS =====

% Biodiversity index: measure of species diversity (0-1)
% Simple calculation: number of species with positive population / total species
biodiversity_count(N) :- N = #count{S : population(S, P), P > 0}.
ecosystem_health.biodiversity_index(I) :- 
    biodiversity_count(N), 
    I = N / 4.0.  % 4 total species

% Stability score: measure of ecosystem stability (0-1)
% Based on how close populations are to carrying capacity
% Higher score when populations are well-distributed
stability_score_calc(Score) :-
    Score = #sum{1, S : population(S, P), carrying_capacity(S, C), P <= C, P > 0} / 4.0.
ecosystem_health.stability_score(S) :- stability_score_calc(S).

% Sustainability: whether the ecosystem is sustainable
% All constraints satisfied and populations positive
ecosystem_health.sustainability :-
    population(grass, G), G > 0,
    population(rabbits, R), R > 0,
    population(foxes, F), F > 0,
    population(hawks, H), H > 0,
    R <= 0.5 * G,
    F <= 0.3 * R.

% Balance achieved: whether ecological balance is achieved
% All species have positive populations and constraints are satisfied
balance_achieved :-
    ecosystem_health.sustainability,
    biodiversity_count(4).  % All 4 species present

% ===== SHOW DIRECTIVES =====
#show stable_populations/2.
#show food_web/3.
#show ecosystem_health.biodiversity_index/1.
#show ecosystem_health.stability_score/1.
#show ecosystem_health.sustainability/0.
#show balance_achieved/0.