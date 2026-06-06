% Positive file: original claim as conjecture
% Predicates:
% engaged(X) - X is engaged
% makes_wedding_plans(X) - X makes wedding plans
% invites_ceremony(X) - X invites others to come to their ceremony
% well_attended_wedding(X) - X has a well-attended wedding
% larger_family(X) - X has a larger family
% invites_friends_ceremony(X) - X invites friends to their ceremony

fof(premise1, axiom, ! [X] : (makes_wedding_plans(X) => engaged(X))).
fof(premise2, axiom, ! [X] : (invites_ceremony(X) => makes_wedding_plans(X))).
fof(premise3, axiom, ! [X] : (well_attended_wedding(X) => invites_ceremony(X))).
fof(premise4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(premise5, axiom, (engaged(john) => (~invites_friends_ceremony(john) & makes_wedding_plans(john)))).
fof(premise6, axiom, (larger_family(john) => (well_attended_wedding(john) | invites_friends_ceremony(john)))).

fof(goal, conjecture, larger_family(john)).