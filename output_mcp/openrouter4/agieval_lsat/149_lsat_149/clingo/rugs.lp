% Colors and rugs
color(forest; olive; peach; turquoise; white; yellow).
rug(1..3).
option_domain(a;b;c;d;e).

% --- Option definitions: used_in(Option, Color, Rug) ---

% Option A: rug1=forest, rug2=turquoise, rug3=olive,peach,white
used_in(a, forest, 1).
used_in(a, turquoise, 2).
used_in(a, olive, 3).
used_in(a, peach, 3).
used_in(a, white, 3).

% Option B: rug1=forest, rug2=turquoise, rug3=olive,peach,yellow
used_in(b, forest, 1).
used_in(b, turquoise, 2).
used_in(b, olive, 3).
used_in(b, peach, 3).
used_in(b, yellow, 3).

% Option C: rug1=peach, rug2=turquoise, rug3=forest,olive,white
used_in(c, peach, 1).
used_in(c, turquoise, 2).
used_in(c, forest, 3).
used_in(c, olive, 3).
used_in(c, white, 3).

% Option D: rug1=yellow, rug2=forest,turquoise, rug3=olive,peach
used_in(d, yellow, 1).
used_in(d, forest, 2).
used_in(d, turquoise, 2).
used_in(d, olive, 3).
used_in(d, peach, 3).

% Option E: rug1=yellow, rug2=olive,peach, rug3=turquoise,white
used_in(e, yellow, 1).
used_in(e, olive, 2).
used_in(e, peach, 2).
used_in(e, turquoise, 3).
used_in(e, white, 3).

% --- Derived counts ---
% Number of colors in a given rug for a given option
colors_in_rug(Opt, Rug, N) :- 
    N = #count{ C : used_in(Opt, C, Rug) },
    option_domain(Opt), rug(Rug).

% Total number of colors used in an option
colors_used(Opt, N) :- 
    N = #count{ C : used_in(Opt, C, _) },
    option_domain(Opt).

% --- Violation checks ---

% Rule 1: If white is used in a rug, that rug must have exactly 3 colors (white + 2 others)
violated_white(Opt) :- 
    used_in(Opt, white, Rug), 
    colors_in_rug(Opt, Rug, N), 
    N != 3.

% Rule 2: If olive is used in a rug, peach must also be in that rug
violated_olive(Opt) :- 
    used_in(Opt, olive, Rug), 
    not used_in(Opt, peach, Rug).

% Rule 3: Forest and turquoise cannot be in the same rug
violated_forest_turquoise(Opt) :- 
    used_in(Opt, forest, Rug), 
    used_in(Opt, turquoise, Rug).

% Rule 4: Peach and turquoise cannot be in the same rug
violated_peach_turquoise(Opt) :- 
    used_in(Opt, peach, Rug), 
    used_in(Opt, turquoise, Rug).

% Rule 5: Peach and yellow cannot be in the same rug
violated_peach_yellow(Opt) :- 
    used_in(Opt, peach, Rug), 
    used_in(Opt, yellow, Rug).

% Exactly 5 colors must be used
violated_count(Opt) :- 
    colors_used(Opt, N), 
    N != 5.

% Any violation makes the option invalid
violated(Opt) :- violated_white(Opt).
violated(Opt) :- violated_olive(Opt).
violated(Opt) :- violated_forest_turquoise(Opt).
violated(Opt) :- violated_peach_turquoise(Opt).
violated(Opt) :- violated_peach_yellow(Opt).
violated(Opt) :- violated_count(Opt).

% An option is valid if it is in the domain and not violated
valid_option(Opt) :- option_domain(Opt), not violated(Opt).

% Map to answer
option(a) :- valid_option(a).
option(b) :- valid_option(b).
option(c) :- valid_option(c).
option(d) :- valid_option(d).
option(e) :- valid_option(e).

#show option/1.