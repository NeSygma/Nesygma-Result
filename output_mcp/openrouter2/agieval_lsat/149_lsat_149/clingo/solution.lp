% Define colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Define options
opt(a). opt(b). opt(c). opt(d). opt(e).

% Facts for used colors per option
used_color_fact(a, forest). used_color_fact(a, turquoise). used_color_fact(a, olive). used_color_fact(a, peach). used_color_fact(a, white).
used_color_fact(b, forest). used_color_fact(b, turquoise). used_color_fact(b, olive). used_color_fact(b, peach). used_color_fact(b, yellow).
used_color_fact(c, peach). used_color_fact(c, turquoise). used_color_fact(c, forest). used_color_fact(c, olive). used_color_fact(c, white).
used_color_fact(d, yellow). used_color_fact(d, forest). used_color_fact(d, turquoise). used_color_fact(d, olive). used_color_fact(d, peach).
used_color_fact(e, yellow). used_color_fact(e, olive). used_color_fact(e, peach). used_color_fact(e, turquoise). used_color_fact(e, white).

% Facts for rug membership per option
rug_fact(a,1,forest). rug_fact(a,2,turquoise). rug_fact(a,3,olive). rug_fact(a,3,peach). rug_fact(a,3,white).
rug_fact(b,1,forest). rug_fact(b,2,turquoise). rug_fact(b,3,olive). rug_fact(b,3,peach). rug_fact(b,3,yellow).
rug_fact(c,1,peach). rug_fact(c,2,turquoise). rug_fact(c,3,forest). rug_fact(c,3,olive). rug_fact(c,3,white).
rug_fact(d,1,yellow). rug_fact(d,2,forest). rug_fact(d,2,turquoise). rug_fact(d,3,olive). rug_fact(d,3,peach).
rug_fact(e,1,yellow). rug_fact(e,2,olive). rug_fact(e,2,peach). rug_fact(e,3,turquoise). rug_fact(e,3,white).

% Choose exactly one option
1 { chosen(a); chosen(b); chosen(c); chosen(d); chosen(e) } 1.

% Derived facts based on chosen option
used_color(Option, Color) :- chosen(Option), used_color_fact(Option, Color).
rug(Option, RugIndex, Color) :- chosen(Option), rug_fact(Option, RugIndex, Color).

% Constraints
% Exactly 5 colors used
:- chosen(Option), #count{C : used_color(Option, C)} != 5.
% Each used color appears only once across rugs
:- chosen(Option), color(C), #count{R : rug(Option, R, C)} > 1.
% White rule: if white used in a rug, that rug must have at least 3 colors
:- chosen(Option), rug(Option, R, white), #count{C : rug(Option, R, C)} < 3.
% Olive implies peach in same rug
:- chosen(Option), rug(Option, R, olive), not rug(Option, R, peach).
% Forest and turquoise not together in a rug
:- chosen(Option), rug(Option, R, forest), rug(Option, R, turquoise).
% Peach and turquoise not together in a rug
:- chosen(Option), rug(Option, R, peach), rug(Option, R, turquoise).
% Peach and yellow not together in a rug
:- chosen(Option), rug(Option, R, peach), rug(Option, R, yellow).

% Map the correct answer to option/1
option(a) :- chosen(a).
option(b) :- chosen(b).
option(c) :- chosen(c).
option(d) :- chosen(d).
option(e) :- chosen(e).

#show option/1.