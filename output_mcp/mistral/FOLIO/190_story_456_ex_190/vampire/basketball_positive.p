fof(some_non_american_players, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).
fof(all_players_can_jump_shot, axiom, ! [X] : (professional_basketball_player(X) => can_jump_shot(X))).
fof(can_jump_shot_implies_leap, axiom, ! [X] : (can_jump_shot(X) => leaps_straight_into_air(X))).
fof(leap_implies_activate, axiom, ! [X] : (leaps_straight_into_air(X) => activates_leg_muscles(X))).
fof(yuri_does_not_activate, axiom, ~activates_leg_muscles(yuri)).
fof(conclusion, conjecture, professional_basketball_player(yuri) & american_national(yuri)).