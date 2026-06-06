% Colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Rugs
rug(1). rug(2). rug(3).

% Exactly 5 colors are used (one color is not used)
1 { used(C) : color(C) } 5.

% Each used color appears in exactly one rug
1 { in_rug(C, R) : rug(R) } 1 :- used(C).

% Rug types: solid (1 color) or multicolored (2+ colors)
solid(R) :- rug(R), #count{C : in_rug(C, R)} = 1.
multicolored(R) :- rug(R), #count{C : in_rug(C, R)} >= 2.

% RULE 1: If white is used in a rug, that rug must have exactly 3 colors
:- in_rug(white, R), #count{C : in_rug(C, R)} != 3.

% RULE 2: If olive is used in a rug, peach must also be used in that rug
:- in_rug(olive, R), not in_rug(peach, R).

% RULE 3: Forest and turquoise cannot be together
:- in_rug(forest, R), in_rug(turquoise, R).

% RULE 4: Peach and turquoise cannot be together
:- in_rug(peach, R), in_rug(turquoise, R).

% RULE 5: Peach and yellow cannot be together
:- in_rug(peach, R), in_rug(yellow, R).

% CONSTRAINT: One rug is solid peach
solid_peach_exists :- solid(R), in_rug(peach, R).
:- not solid_peach_exists.

% Define helper predicates for the options
solid_forest_exists :- solid(R), in_rug(forest, R).
solid_turquoise_exists :- solid(R), in_rug(turquoise, R).
solid_yellow_exists :- solid(R), in_rug(yellow, R).
forest_white_together :- in_rug(forest, R), in_rug(white, R).
white_yellow_together :- in_rug(white, R), in_rug(yellow, R).

% Now we need to determine which conclusion is necessarily true
% We'll check each option by seeing if its negation is impossible
% We'll add constraints to forbid each option and see which ones lead to unsat

% For option A: Check if we can have a model where solid_forest_exists is false
% We'll add a constraint to forbid solid forest and see if it's satisfiable
% But we need to do this in a single program. Let's use a different approach.

% Actually, let's just run the program and see what models we get
% Then we'll see which condition is true in all models

% For now, let's output the models and see what we get
#show used/1.
#show in_rug/2.
#show solid/1.
#show solid_peach_exists/0.
#show solid_forest_exists/0.
#show solid_turquoise_exists/0.
#show solid_yellow_exists/0.
#show forest_white_together/0.
#show white_yellow_together/0.