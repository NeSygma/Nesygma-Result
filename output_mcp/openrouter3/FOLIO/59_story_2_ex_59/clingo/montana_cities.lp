% Cities and States
city(billings). city(butte). city(helena). city(missoula).
city(white_sulphur_springs). city(st_pierre). city(bismarck).

state(montana). state(montana). % Montana is a state

% Special cities that can be in multiple states
special_city(bristol). special_city(texarkana). special_city(texhoma). special_city(union_city).

% Premise 1: Billings is in Montana
in_state(billings, montana).

% Premise 2: Montana includes Butte, Helena, Missoula
in_state(butte, montana).
in_state(helena, montana).
in_state(missoula, montana).

% Premise 3: White Sulphur Springs and Butte are in the same state
% We need to find what state White Sulphur Springs is in
% Since Butte is in Montana, White Sulphur Springs must also be in Montana
in_state(white_sulphur_springs, montana).

% Premise 4: St Pierre is not in Montana
% This means: not in_state(st_pierre, montana)

% Premise 5: Any city in Butte is not in St Pierre
% This means: any city in the same state as Butte (Montana) is not in St Pierre
% So St Pierre cannot be in Montana (already covered by premise 4)

% Premise 6: A city can only be in one state except for special cities
% For non-special cities: at most one state
% For special cities: can be in multiple states

% Helper: Determine if a city is special
is_special(C) :- special_city(C).
is_special(C) :- not special_city(C), false. % Default: not special

% Constraint: Non-special cities can be in at most one state
:- city(C), not is_special(C), in_state(C, S1), in_state(C, S2), S1 != S2.

% Choice rule for St Pierre's state (unknown)
{in_state(st_pierre, S) : state(S)} :- city(st_pierre), not is_special(st_pierre).

% Choice rule for Bismarck's state (unknown)
{in_state(bismarck, S) : state(S)} :- city(bismarck), not is_special(bismarck).

% Additional constraint from premise 5: Cities in Montana cannot be in St Pierre
% This means St Pierre cannot be in Montana (already covered)

% Evaluate conclusion: St Pierre and Bismarck are in the same state
conclusion_true :- in_state(st_pierre, S), in_state(bismarck, S).

% For conclusion to be false, they must be in different states
% But we need to consider all possibilities
conclusion_false :- in_state(st_pierre, S1), in_state(bismarck, S2), S1 != S2.

% If neither conclusion_true nor conclusion_false, it's uncertain
% (This could happen if one or both cities have no state assigned)

% Show relevant information
#show city/1.
#show state/1.
#show in_state/2.
#show conclusion_true.
#show conclusion_false.
#show answer/1.

% Final answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.