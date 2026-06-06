% Positive file: Conclude Space is a vampire
fof(premise_1, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(premise_2, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(premise_3, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(premise_4, axiom, vacuum(space)).
fof(premise_5, axiom, (household_appliance(duster) & ~sucks(duster))).
fof(goal, conjecture, vampire(space)).