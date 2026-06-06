% Barutin Cove Problem - Positive Version
% Conclusion: Barutin Cove is not located in Antarctica

% Distinct entities
fof(distinct_entities, axiom, 
    (barutin_cove != snow_island & barutin_cove != greenwich_island & 
     barutin_cove != deception_island & barutin_cove != antarctica &
     barutin_cove != south_shetland_islands &
     snow_island != greenwich_island & snow_island != deception_island &
     snow_island != antarctica & snow_island != south_shetland_islands &
     greenwich_island != deception_island & greenwich_island != antarctica &
     greenwich_island != south_shetland_islands &
     deception_island != antarctica & deception_island != south_shetland_islands &
     antarctica != south_shetland_islands)).

% Premise 1: Barutin Cove is a cove named after Barutin settlement
fof(premise_1, axiom, cove(barutin_cove)).

% Premise 2: Barutin Cove is on the southwest coast of Snow Island
% This implies Barutin Cove is located in Snow Island
fof(premise_2, axiom, located_in(barutin_cove, snow_island)).

% Premise 3: Snow Island, Greenwich Island, and Deception Island are in South Shetland Islands
fof(premise_3a, axiom, located_in(snow_island, south_shetland_islands)).
fof(premise_3b, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(premise_3c, axiom, located_in(deception_island, south_shetland_islands)).

% Premise 4: Antarctica is located on the South Shetland Islands
fof(premise_4, axiom, located_in(antarctica, south_shetland_islands)).

% Premise 5: Transitivity of location
fof(premise_5, axiom, 
    ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).

% Conclusion: Barutin Cove is not located in Antarctica
fof(goal, conjecture, ~located_in(barutin_cove, antarctica)).