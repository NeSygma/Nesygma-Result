% Positive version: Harding Pegmatite Mine is NOT located in a mountain range in New Mexico
fof(distinct_entities, axiom, (picuris_mountains != new_mexico & picuris_mountains != texas & picuris_mountains != harding_pegmatite_mine & new_mexico != texas & juan_de_onate != harding_pegmatite_mine)).

% Premise 1: Picuris Mountains are in New Mexico OR Texas
fof(premise_1, axiom, (mountain_range_in(picuris_mountains, new_mexico) | mountain_range_in(picuris_mountains, texas))).

% Premise 2: Juan de Onate visited Picuris Mountains
fof(premise_2, axiom, visited(juan_de_onate, picuris_mountains)).

% Premise 3: Harding Pegmatite Mine is located in Picuris Mountains AND was donated
fof(premise_3a, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(premise_3b, axiom, donated(harding_pegmatite_mine)).

% Premise 4: No mountain ranges in Texas have mines that have been donated
fof(premise_4, axiom, ! [M, Mine] : ((mountain_range_in(M, texas) & located_in(Mine, M) & donated(Mine)) => false)).

% Conclusion: Harding Pegmatite Mine is NOT located in a mountain range in New Mexico
fof(conclusion, conjecture, ~located_in(harding_pegmatite_mine, picuris_mountains) | ~mountain_range_in(picuris_mountains, new_mexico)).