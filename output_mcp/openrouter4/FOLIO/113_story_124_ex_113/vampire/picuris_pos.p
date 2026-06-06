% Positive version: original conclusion as conjecture
% Juan de Onate visited a mountain range in Texas.

% Premise 1: Picuris Mountains are a mountain range in New Mexico or Texas.
fof(p1a, axiom, mountain_range(picuris_mountains)).
fof(p1b, axiom, (in(picuris_mountains, new_mexico) | in(picuris_mountains, texas))).

% Premise 2: Juan de Onate visited the Picuris Mountains.
fof(p2, axiom, visited(juan_de_onate, picuris_mountains)).

% Premise 3: Harding Pegmatite Mine is located in the Picuris Mountains and was donated.
fof(p3a, axiom, has_mine(picuris_mountains, harding_pegmatite_mine)).
fof(p3b, axiom, donated(harding_pegmatite_mine)).

% Premise 4: No mountain ranges in Texas have mines that have been donated.
fof(p4, axiom, ! [X, Y] : ((mountain_range(X) & in(X, texas) & has_mine(X, Y) & donated(Y)) => $false)).

% Distinct constants
fof(distinct, axiom, (picuris_mountains != harding_pegmatite_mine & juan_de_onate != picuris_mountains & juan_de_onate != harding_pegmatite_mine & new_mexico != texas & new_mexico != picuris_mountains & texas != picuris_mountains & new_mexico != harding_pegmatite_mine & texas != harding_pegmatite_mine & juan_de_onate != new_mexico & juan_de_onate != texas)).

% Conclusion: Juan de Onate visited a mountain range in Texas.
fof(conclusion, conjecture, ? [X] : (mountain_range(X) & in(X, texas) & visited(juan_de_onate, X))).