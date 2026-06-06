% --- Instance Data ---
species(grass).
species(rabbit).
species(fox).
species(hawk).

capacity(grass, 100).
capacity(rabbit, 30).
capacity(fox, 10).
capacity(hawk, 5).

% Feeding relationships (predator, prey)
eats(rabbit, grass).
eats(fox, rabbit).
eats(hawk, rabbit).
eats(hawk, fox).

% --- Choice Rules ---
% Select consumption rates between 1/10 and 5/10 (0.1 to 0.5)
{eats_rate(Predator, Prey, RateNumerator, 10) : RateNumerator=1..5} 1 :- eats(Predator, Prey).

% Select populations for each species (bounded by carrying capacity and > 0)
{population(Species, Pop) : Pop=1..Capacity} 1 :- species(Species), capacity(Species, Capacity).

% --- Helper Predicates ---
% Convert fraction to float for readability in constraints
consumption_rate(Predator, Prey, Rate) :-
    eats_rate(Predator, Prey, Num, Den),
    Rate = Num / Den.

% --- Constraints ---
% No extinction (population > 0)
:- population(S, 0).

% Carrying capacity constraint
:- population(S, P), capacity(S, C), P > C.

% Herbivore sustainability: Rabbits <= 0.5 * Grass
:- population(rabbit, PR), population(grass, PG), PR > (5 * PG) / 10.

% Predator sustainability: Foxes <= 0.3 * Rabbits
:- population(fox, PF), population(rabbit, PR), PF > (3 * PR) / 10.

% Predator sustainability: Hawks <= 0.3 * (Rabbits + Foxes)
:- population(hawk, PH), population(rabbit, PR), population(fox, PF), PH > (3 * (PR + PF)) / 10.

% Consumption balance: Prey population must be >= total consumption
% Rabbits eat Grass: PG >= Rate * PR
:- consumption_rate(rabbit, grass, Rate), population(rabbit, PR), population(grass, PG), PG * 10 < Rate * PR * 10.

% Foxes eat Rabbits: PR >= Rate * PF
:- consumption_rate(fox, rabbit, Rate), population(fox, PF), population(rabbit, PR), PR * 10 < Rate * PF * 10.

% Hawks eat Rabbits: PR >= Rate * PH
:- consumption_rate(hawk, rabbit, Rate), population(hawk, PH), population(rabbit, PR), PR * 10 < Rate * PH * 10.

% Hawks eat Foxes: PF >= Rate * PH
:- consumption_rate(hawk, fox, Rate), population(hawk, PH), population(fox, PF), PF * 10 < Rate * PH * 10.

% --- Ecosystem Health ---
% Biodiversity Index: Number of species with population > 0 divided by total species
num_species(4).
biodiversity_index(BI) :-
    num_species(N),
    #count{S : population(S, P), P > 0} = Count,
    BI = Count / N.

% Stability Score: Based on balance of populations and consumption rates
% This is a simplified heuristic: higher stability if populations are balanced and consumption rates are moderate
stability_score(SS) :-
    population(grass, PG),
    population(rabbit, PR),
    population(fox, PF),
    population(hawk, PH),
    % Heuristic: stability is higher if populations are closer to carrying capacity and consumption rates are moderate
    % We use a simple weighted sum for demonstration
    SS = (PG/100 + PR/30 + PF/10 + PH/5) / 4.

% Sustainability: All constraints are satisfied
sustainability :-
    not #count{_: #false} = 0.

% Balance achieved: All constraints are satisfied
balance_achieved :-
    not #count{_: #false} = 0.

% --- Objective ---
% Maximize sustainability and stability (simplified as a single objective)
#maximize {1@1 : sustainability}.
#maximize {1@1 : balance_achieved}.
#maximize {SS@2 : stability_score(SS)}.

% --- Output ---
#show population/2.
#show eats_rate/4.
#show consumption_rate/3.
#show biodiversity_index/1.
#show stability_score/1.
#show sustainability/0.
#show balance_achieved/0.