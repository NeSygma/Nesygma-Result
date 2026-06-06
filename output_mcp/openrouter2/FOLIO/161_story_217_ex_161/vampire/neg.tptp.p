fof(p1, axiom, likes_music(george) => wants_compose(george)).
fof(p2, axiom, has_program(george) => can_compose(george)).
fof(p3, axiom, (can_compose(george) & wants_compose(george)) => will_compose(george)).
fof(conj, conjecture, ~((likes_music(george) & has_program(george)) => will_compose(george))).