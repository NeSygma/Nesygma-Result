% Positive version: original claim as conjecture
% Premises
fof(p1, axiom, ! [X] : ((zh(X) & adores(X)) => interesting(X))).
fof(p2, axiom, ! [X] : ((brutalist(X) & adores(X)) => ~interesting(X))).
fof(p3, axiom, ! [X] : (adores(X) => (zh(X) | kw(X)))).
fof(p4, axiom, ! [X] : ((kw(X) & adores(X)) => evocative(X))).
fof(p5, axiom, ! [X] : ((kw(X) & adores(X)) => dreamy(X))).
fof(p6, axiom, ! [X] : ((max_design(X) & adores(X) & interesting(X)) => (brutalist(X) & evocative(X)))).

% Conjecture: Every design by Max is either evocative or dreamy
fof(goal, conjecture, ! [X] : (max_design(X) => (evocative(X) | dreamy(X)))).