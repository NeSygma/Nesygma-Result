% Cities and States
city(billings).
city(butte).
city(helena).
city(missoula).
city(white_sulphur_springs).
city(st_pierre).

state(montana).
state(unknown_state). % For cities that might be in other states

% Premise 1: Billings is in Montana
in_state(billings, montana).

% Premise 2: Montana includes Butte, Helena, and Missoula
in_state(butte, montana).
in_state(helena, montana).
in_state(missoula, montana).

% Premise 3: White Sulphur Springs and Butte are in the same state
% We need to determine what state White Sulphur Springs is in
% Since Butte is in Montana, White Sulphur Springs must also be in Montana
in_state(white_sulphur_springs, montana).

% Premise 4: St Pierre is NOT in Montana
:- in_state(st_pierre, montana).

% Premise 5: Any city in Butte is not in St Pierre
% This means: if a city is in the same state as Butte, it cannot be in the same state as St Pierre
% Since Butte is in Montana, this means no city in Montana can be in the same state as St Pierre
% Therefore, St Pierre cannot be in Montana (already covered by premise 4)
% But more importantly, this implies St Pierre is in a different state than Montana

% Premise 6: A city can only be in one state except for special cities
% For simplicity, we'll assume all cities except the special ones are in exactly one state
% The special cities (Bristol, Texarkana, Texhoma, Union City) are not in our city list, so we ignore this for now

% For cities not explicitly assigned, we need to consider possibilities
% Let's define a choice rule for cities that might be in other states
{ in_state(C, S) } :- city(C), state(S).

% But we need to enforce the constraints:
% 1. Each city (except special ones) is in exactly one state
% 2. St Pierre is not in Montana
% 3. Butte is in Montana

% Constraint: St Pierre is not in Montana
:- in_state(st_pierre, montana).

% Constraint: Butte is in Montana (from premise 2)
:- not in_state(butte, montana).

% Constraint: White Sulphur Springs is in the same state as Butte (premise 3)
:- in_state(butte, S), not in_state(white_sulphur_springs, S).

% For the conclusion: Butte and St Pierre are in the same state
% We need to check if this can be true given the premises

% Let's derive the conclusion
conclusion_true :- in_state(butte, S), in_state(st_pierre, S).
conclusion_false :- in_state(butte, S1), in_state(st_pierre, S2), S1 != S2.

% Answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.

#show answer/1.
#show in_state/2.