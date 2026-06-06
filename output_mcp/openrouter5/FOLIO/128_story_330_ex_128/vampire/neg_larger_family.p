% Negative file: negated claim as conjecture
fof(premise1, axiom, ! [X] : (makes_wedding_plans(X) => engaged(X))).
fof(premise2, axiom, ! [X] : (invites_ceremony(X) => makes_wedding_plans(X))).
fof(premise3, axiom, ! [X] : (well_attended_wedding(X) => invites_ceremony(X))).
fof(premise4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(premise5, axiom, (engaged(john) => (~invites_friends_ceremony(john) & makes_wedding_plans(john)))).
fof(premise6, axiom, (larger_family(john) => (well_attended_wedding(john) | invites_friends_ceremony(john)))).

fof(goal, conjecture, ~larger_family(john)).