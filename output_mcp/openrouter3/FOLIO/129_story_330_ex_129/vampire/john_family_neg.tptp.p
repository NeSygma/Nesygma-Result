% Negative version: John has a larger family (negation of conclusion)
fof(person_type, axiom, ! [X] : (person(X) => $true)). % Placeholder for person type
fof(premise_1, axiom, ! [X] : (wedding_plans(X) => engaged(X))).
fof(premise_2, axiom, ! [X] : (invites(X) => wedding_plans(X))).
fof(premise_3, axiom, ! [X] : (well_attended(X) => invites(X))).
fof(premise_4, axiom, ? [X] : (well_attended(X) & large_family(X))).
fof(premise_5, axiom, engaged(john) => (~invites_friends(john) & wedding_plans(john))).
fof(premise_6, axiom, large_family(john) => (well_attended(john) | invites_friends(john))).
fof(distinct_john, axiom, person(john)).
fof(goal, conjecture, large_family(john)).