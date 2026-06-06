% Negative version: negated conclusion as conjecture
% Barutin Cove is NOT named after all islands in Antarctica.

% Predicates:
% named_after(X, Y) - X is named after Y
% located_in(X, Y) - place X is located in place Y
% cove(X) - X is a cove
% island(X) - X is an island
% settlement(X) - X is a settlement

% Constants:
% barutin_cove, barutin_settlement, snow_island, greenwich_island, deception_island, south_shetland_islands, antarctica

fof(distinct, axiom, (
    barutin_cove != barutin_settlement &
    barutin_cove != snow_island &
    barutin_cove != greenwich_island &
    barutin_cove != deception_island &
    barutin_cove != south_shetland_islands &
    barutin_cove != antarctica &
    barutin_settlement != snow_island &
    barutin_settlement != greenwich_island &
    barutin_settlement != deception_island &
    barutin_settlement != south_shetland_islands &
    barutin_settlement != antarctica &
    snow_island != greenwich_island &
    snow_island != deception_island &
    snow_island != south_shetland_islands &
    snow_island != antarctica &
    greenwich_island != deception_island &
    greenwich_island != south_shetland_islands &
    greenwich_island != antarctica &
    deception_island != south_shetland_islands &
    deception_island != antarctica &
    south_shetland_islands != antarctica
)).

% Premise 1: Barutin Cove is a cove named after the Bulgarian settlement of Barutin.
fof(premise1a, axiom, cove(barutin_cove)).
fof(premise1b, axiom, settlement(barutin_settlement)).
fof(premise1c, axiom, named_after(barutin_cove, barutin_settlement)).

% Premise 2: Barutin Cove is on the southwest coast of Snow Island.
fof(premise2, axiom, located_in(barutin_cove, snow_island)).

% Premise 3: Snow Island, Greenwich Island, and Deception Island are located in the South Shetland Islands.
fof(premise3a, axiom, island(snow_island)).
fof(premise3b, axiom, island(greenwich_island)).
fof(premise3c, axiom, island(deception_island)).
fof(premise3d, axiom, located_in(snow_island, south_shetland_islands)).
fof(premise3e, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(premise3f, axiom, located_in(deception_island, south_shetland_islands)).

% Premise 4: Antarctica is located on the South Shetland Islands.
fof(premise4, axiom, located_in(antarctica, south_shetland_islands)).

% Premise 5: If place A is located in place B and place B is located in place C, then place A is located in place C.
fof(premise5, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).

% Negated conclusion: There exists an island X located in Antarctica such that barutin_cove is NOT named after X.
fof(goal, conjecture, ? [X] : (island(X) & located_in(X, antarctica) & ~named_after(barutin_cove, X))).