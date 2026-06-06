fof(p1, axiom, likes_music(george) => wants_to_compose(george)).
fof(p2, axiom, has_access_to_program(george) => can_compose(george)).
fof(p3, axiom, (can_compose(george) & wants_to_compose(george)) => will_compose(george)).
fof(conclusion, conjecture, (likes_music(george) & has_access_to_program(george)) => will_compose(george)).