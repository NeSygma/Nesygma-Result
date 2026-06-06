fof(axiom_wild_tom, axiom, wild_turkey(tom)).
fof(axiom_not_eastern, axiom, ~eastern_wild_turkey(tom)).
fof(axiom_not_osceola, axiom, ~osceola_wild_turkey(tom)).
fof(axiom_not_goulds, axiom, ~goulds_wild_turkey(tom)).
fof(axiom_not_merriams, axiom, ~merriams_wild_turkey(tom)).
fof(axiom_not_rio_grande, axiom, ~rio_grande_wild_turkey(tom)).
fof(domain_axiom, axiom, ! [X] : (wild_turkey(X) => (eastern_wild_turkey(X) | osceola_wild_turkey(X) | goulds_wild_turkey(X) | merriams_wild_turkey(X) | rio_grande_wild_turkey(X) | ocellated_wild_turkey(X)))).
fof(goal, conjecture, ~eastern_wild_turkey(tom)).