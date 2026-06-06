% Negative file: negated claim as conjecture
% Premise 1: People who are born in a multiple birth with siblings spend a lot of time hanging out with and playing with their siblings.
fof(p1, axiom, ! [X] : (born_in_multiple_birth(X) => spends_time_with_siblings(X))).

% Premise 2: If people have siblings who were born together, then they were born in a multiple birth.
fof(p2, axiom, ! [X] : (has_siblings_born_together(X) => born_in_multiple_birth(X))).

% Premise 3: If people complain often about annoying siblings, then they have siblings who were born together.
fof(p3, axiom, ! [X] : (complains_about_siblings(X) => has_siblings_born_together(X))).

% Premise 4: If people live at home, then they do not live with strangers.
fof(p4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).

% Premise 5: If people spend a lot of time hanging out with and playing with their siblings, then they often live at home.
fof(p5, axiom, ! [X] : (spends_time_with_siblings(X) => lives_at_home(X))).

% Premise 6: Luke either is a baby born in a multiple birth and live with strangers, or is not a baby born in a multiple birth and does not live with strangers
fof(p6, axiom, (born_in_multiple_birth(luke) <=> lives_with_strangers(luke))).

% Negated conclusion: Luke does NOT complain often about annoying siblings.
fof(goal_negated, conjecture, ~complains_about_siblings(luke)).