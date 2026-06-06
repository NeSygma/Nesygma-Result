fof(private, axiom, private(yale)).
fof(ivy_league, axiom, ivy_league(yale)).
fof(research_university, axiom, research_university(yale)).
fof(moved, axiom, moved(yale, new_haven)).
fof(conjecture, conjecture, ~? [U] : (private(U) & ivy_league(U) & research_university(U) & moved(U, new_haven))).