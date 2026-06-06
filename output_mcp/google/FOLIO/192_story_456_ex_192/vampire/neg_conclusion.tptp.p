fof(pro_bb_player, axiom, ! [X] : (pro_bb_player(X) => can_jump_shot(X))).
fof(can_jump_shot, axiom, ! [X] : (can_jump_shot(X) => leap_air(X))).
fof(leap_air, axiom, ! [X] : (leap_air(X) => activate_leg_muscles(X))).
fof(yuri_fact, axiom, ~activate_leg_muscles(yuri)).
fof(conclusion, conjecture, ~ (~(american(yuri) & pro_bb_player(yuri)) => pro_bb_player(yuri))).