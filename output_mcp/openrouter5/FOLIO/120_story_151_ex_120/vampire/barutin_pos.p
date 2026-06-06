% Positive version: original conclusion as conjecture
% Conclusion: Barutin Cove is not located in Antarctica.
% So conjecture: ~located(barutin_cove, antarctica)

fof(distinct, axiom, (
    barutin_cove != snow_island &
    barutin_cove != greenwich_island &
    barutin_cove != deception_island &
    barutin_cove != antarctica &
    barutin_cove != south_shetland_islands &
    barutin_cove != barutin &
    snow_island != greenwich_island &
    snow_island != deception_island &
    snow_island != antarctica &
    snow_island != south_shetland_islands &
    snow_island != barutin &
    greenwich_island != deception_island &
    greenwich_island != antarctica &
    greenwich_island != south_shetland_islands &
    greenwich_island != barutin &
    deception_island != antarctica &
    deception_island != south_shetland_islands &
    deception_island != barutin &
    antarctica != south_shetland_islands &
    antarctica != barutin &
    south_shetland_islands != barutin
)).

% Premise 1: Barutin Cove is a cove named after the Bulgarian settlement of Barutin.
% This is just background info, no logical constraint needed.

% Premise 2: Barutin Cove is on the southwest coast of Snow Island.
% This means Barutin Cove is located in Snow Island.
fof(premise2, axiom, located(barutin_cove, snow_island)).

% Premise 3: Snow Island, Greenwich Island, and Deception Island are located in the South Shetland Islands.
fof(premise3a, axiom, located(snow_island, south_shetland_islands)).
fof(premise3b, axiom, located(greenwich_island, south_shetland_islands)).
fof(premise3c, axiom, located(deception_island, south_shetland_islands)).

% Premise 4: Antarctica is located on the South Shetland Islands.
fof(premise4, axiom, located(antarctica, south_shetland_islands)).

% Premise 5: If place A is located in place B and place B is located in place C, then place A is located in place C.
fof(premise5, axiom, ! [A, B, C] : ((located(A, B) & located(B, C)) => located(A, C))).

% Conclusion: Barutin Cove is not located in Antarctica.
fof(goal, conjecture, ~located(barutin_cove, antarctica)).