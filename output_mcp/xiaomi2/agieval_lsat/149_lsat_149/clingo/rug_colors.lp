% Domains
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).
rug(r1). rug(r2). rug(r3).
option_name(a). option_name(b). option_name(c). option_name(d). option_name(e).

% Option A assignment
used_option(a, forest). used_option(a, turquoise). used_option(a, olive). used_option(a, peach). used_option(a, white).
in_rug_option(a, forest, r1). in_rug_option(a, turquoise, r2). in_rug_option(a, olive, r3). in_rug_option(a, peach, r3). in_rug_option(a, white, r3).

% Option B assignment
used_option(b, forest). used_option(b, turquoise). used_option(b, olive). used_option(b, peach). used_option(b, yellow).
in_rug_option(b, forest, r1). in_rug_option(b, turquoise, r2). in_rug_option(b, olive, r3). in_rug_option(b, peach, r3). in_rug_option(b, yellow, r3).

% Option C assignment
used_option(c, peach). used_option(c, turquoise). used_option(c, forest). used_option(c, olive). used_option(c, white).
in_rug_option(c, peach, r1). in_rug_option(c, turquoise, r2). in_rug_option(c, forest, r3). in_rug_option(c, olive, r3). in_rug_option(c, white, r3).

% Option D assignment
used_option(d, yellow). used_option(d, forest). used_option(d, turquoise). used_option(d, olive). used_option(d, peach).
in_rug_option(d, yellow, r1). in_rug_option(d, forest, r2). in_rug_option(d, turquoise, r2). in_rug_option(d, olive, r3). in_rug_option(d, peach, r3).

% Option E assignment
used_option(e, yellow). used_option(e, olive). used_option(e, peach). used_option(e, turquoise). used_option(e, white).
in_rug_option(e, yellow, r1). in_rug_option(e, olive, r2). in_rug_option(e, peach, r2). in_rug_option(e, turquoise, r3). in_rug_option(e, white, r3).

% Choose one option
{ select(X) } :- option_name(X).
:- not 1 { select(X) } 1.

% Derive selected assignment
selected_used(C) :- select(X), used_option(X, C).
selected_in_rug(C, R) :- select(X), in_rug_option(X, C, R).

% Exactly five colors are used
:- not 5 { selected_used(C) } 5.

% Each used color is in exactly one rug
:- selected_used(C), not 1 { selected_in_rug(C, R) : rug(R) } 1.

% Rule 1: If white is used in a rug, that rug must have at least two other colors
:- selected_in_rug(white, R), #count { C : selected_in_rug(C, R), C != white } < 2.

% Rule 2: If olive is used in a rug, peach must also be used in that rug
:- selected_in_rug(olive, R), not selected_in_rug(peach, R).

% Rule 3: Forest and turquoise cannot be together in a rug
:- selected_in_rug(forest, R), selected_in_rug(turquoise, R).

% Rule 4: Peach and turquoise cannot be together in a rug
:- selected_in_rug(peach, R), selected_in_rug(turquoise, R).

% Rule 5: Peach and yellow cannot be together in a rug
:- selected_in_rug(peach, R), selected_in_rug(yellow, R).

% Output the selected option
option(X) :- select(X).
#show option/1.