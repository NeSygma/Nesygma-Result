fof(axiom_private, axiom, private(yale)).
fof(axiom_ivy, axiom, ivy_league(yale)).
fof(axiom_research, axiom, research_university(yale)).
fof(axiom_moved, axiom, moved_to(yale, new_haven)).
fof(conclusion, conjecture, ? [X] : (private(X) & ivy_league(X) & research_university(X) & moved_to(X, new_haven))).