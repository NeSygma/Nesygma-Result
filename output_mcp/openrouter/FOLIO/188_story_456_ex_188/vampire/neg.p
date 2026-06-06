% Negative test: prove ~american(yuri)
fof(exist_non_american, axiom, (professional(p1) & ~american(p1))).
fof(distinct, axiom, p1 != yuri).
fof(all_pro_can_jump, axiom, ! [X] : (professional(X) => can_jump(X))).
fof(can_jump_leap, axiom, ! [X] : (can_jump(X) => leap(X))).
fof(leap_activate, axiom, ! [X] : (leap(X) => activate(X))).
fof(yuri_not_activate, axiom, ~activate(yuri)).
fof(goal, conjecture, ~american(yuri)).