% Colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Rugs
rug(1). rug(2). rug(3).

% Exactly 5 colors are used (one color is not used)
1 { used(C) : color(C) } 5.

% Each used color appears in exactly one rug
1 { in_rug(C, R) : rug(R) } 1 :- used(C).

% Rug types: solid (1 color) or multicolored (2+ colors)
% We'll derive rug type from color count
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

% Additional constraint: Exactly one rug is solid peach (since each color appears once)
% Actually, if peach is used and solid, it must be in exactly one rug as solid
% We need to ensure that if peach is used, it's either solid or multicolored
% But the problem states "one of the rugs is solid peach", so we enforce that

% Now let's check the answer choices
% (A) One of the rugs is solid forest
solid_forest_exists :- solid(R), in_rug(forest, R).

% (B) One of the rugs is solid turquoise
solid_turquoise_exists :- solid(R), in_rug(turquoise, R).

% (C) One of the rugs is solid yellow
solid_yellow_exists :- solid(R), in_rug(yellow, R).

% (D) Forest and white are used together in a rug
forest_white_together :- in_rug(forest, R), in_rug(white, R).

% (E) White and yellow are used together in a rug
white_yellow_together :- in_rug(white, R), in_rug(yellow, R).

% Map the correct answer to option/1 (MANDATORY)
% We need to find which must be true in ALL models where one rug is solid peach
% We'll check each option by seeing if its negation is impossible

% For option A: If we assume NO solid forest, can we still satisfy all constraints?
% We'll add a constraint that forbids solid forest and see if it's satisfiable
% But we need to do this in a single program. Let's use a different approach.

% Actually, let's just run the program and see what models we get
% Then we'll see which condition is true in all models

% For now, let's output the models and see what we get
#show used/1.
#show in_rug/2.
#show solid/1.
#show multicolored/1.
#show solid_peach_exists/0.
#show solid_forest_exists/0.
#show solid_turquoise_exists/0.
#show solid_yellow_exists/0.
#show forest_white_together/0.
#show white_yellow_together/0.