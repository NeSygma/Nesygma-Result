fof(likes_music, axiom, likes_music(george) => wants_compose(george)).
fof(has_program, axiom, has_program(george) => can_compose(george)).
fof(compose_conditions, axiom, (can_compose(george) & wants_compose(george)) => will_compose(george)).
fof(goal_negation, conjecture, ~(~will_compose(george) => ~can_compose(george))).