% Positive run: original claim as conjecture
% If something is a household appliance, it sucks.
fof(premise_1, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(premise_2, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(premise_3, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(premise_4, axiom, vacuum(space)).
fof(premise_5, axiom, ? [X] : (duster(X) & household_appliance(X) & ~sucks(X))).
fof(conclusion, conjecture, ! [X] : (household_appliance(X) => sucks(X))).