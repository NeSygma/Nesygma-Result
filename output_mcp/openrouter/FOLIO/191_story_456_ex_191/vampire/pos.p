% Positive run: check if conclusion follows
fof(distinct_yuri, axiom, yuri != yuri).  % trivial but ensures name
fof(premise1, axiom, ? [X] : (pbp(X) & ~american(X))).
fof(premise2, axiom, ! [X] : (pbp(X) => can_jump(X))).
fof(premise3, axiom, ! [X] : (can_jump(X) => leap(X))).
fof(premise4, axiom, ! [X] : (leap(X) => activate(X))).
fof(premise5, axiom, ~activate(yuri)).
fof(goal, conjecture, (~leap(yuri) => (american(yuri) & pbp(yuri)))).