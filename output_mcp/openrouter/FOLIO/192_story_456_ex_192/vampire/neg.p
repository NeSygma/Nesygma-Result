% Negative version (negated conjecture)
fof(premise1, axiom, ? [X] : (pbp(X) & ~american(X))).
fof(premise2, axiom, ! [X] : (pbp(X) => can_jump(X))).
fof(premise3, axiom, ! [X] : (can_jump(X) => leaps(X))).
fof(premise4, axiom, ! [X] : (leaps(X) => activates(X))).
fof(premise5, axiom, ~activates(yuri)).
fof(goal_neg, conjecture, ~ ( ( ~ (american(yuri) & pbp(yuri)) ) => pbp(yuri) ) ).