% Distinct constants
fof(distinct_constants, axiom, (picuris != new_mexico & picuris != texas & picuris != juan_de_onate & picuris != harding_pegmatite & new_mexico != texas & new_mexico != juan_de_onate & new_mexico != harding_pegmatite & texas != juan_de_onate & texas != harding_pegmatite & juan_de_onate != harding_pegmatite)).

% Premise 1: Picuris is in New Mexico or Texas
fof(premise_1, axiom, mountain_range_in(picuris, new_mexico) | mountain_range_in(picuris, texas)).

% Premise 2: Juan visited Picuris
fof(premise_2, axiom, visited(juan_de_onate, picuris)).

% Premise 3: Harding Pegmatite Mine is in Picuris and donated
fof(premise_3, axiom, mine_in(harding_pegmatite, picuris) & donated(harding_pegmatite)).

% Premise 4: No mountain range in Texas has a donated mine
fof(premise_4, axiom, ! [M] : (mountain_range_in(M, texas) => ! [X] : ~(mine_in(X, M) & donated(X)))).

% Conclusion: Juan visited a mountain range in Texas
fof(conclusion, conjecture, ? [M] : (mountain_range_in(M, texas) & visited(juan_de_onate, M))).