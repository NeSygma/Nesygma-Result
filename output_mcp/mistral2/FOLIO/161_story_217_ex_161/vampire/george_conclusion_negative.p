fof(premise1, axiom, likes_music(george) => wants_to_compose(george)).
fof(premise2, axiom, has_access_to_program(george) => can_compose(george)).
fof(premise3, axiom, (can_compose(george) & wants_to_compose(george)) => will_compose(george)).
fof(conclusion_negation, conjecture, ~((likes_music(george) & has_access_to_program(george)) => will_compose(george))).