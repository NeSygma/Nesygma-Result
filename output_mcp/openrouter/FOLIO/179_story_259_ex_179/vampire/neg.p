fof(ax1, axiom, ! [X] : (horse(X) => hooves(X))).
fof(ax2, axiom, ! [X] : (human(X) => ~hooves(X))).
fof(goal, conjecture, ! [X] : ~ (human(X) & horse(X))).