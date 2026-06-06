fof(axiom_cost, axiom, cost(gre, c205).)
fof(axiom_cheaper, axiom, cheaper(c205, c300).)
fof(axiom_hardship_rule, axiom, ! [X] : (single_parent_family(X) | few_resources(X)) => prove_hardship(X)).
fof(axiom_aid_rule, axiom, ! [X] : (applicant_gre(X) & prove_hardship(X)) => provides_aid(X)).
fof(tom_single_parent, axiom, single_parent_family(tom)).
fof(tom_few_resources, axiom, few_resources(tom)).
fof(axiom_applying, axiom, applicant_gre(tom)).
fof(dad_out_of_work, axiom, out_of_work(dad)).
fof(distinct_constants, axiom, (tom != dad & tom != gre & dad != gre)).
fof(conjecture_pos, conjecture, cheaper(c205, c300).)