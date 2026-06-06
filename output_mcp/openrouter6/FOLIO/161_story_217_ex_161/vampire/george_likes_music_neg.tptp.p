fof(premise1, axiom, (likes_music(george) => wants_compose(george))).
fof(premise2, axiom, (has_program(george) => can_compose(george))).
fof(premise3, axiom, ((can_compose(george) & wants_compose(george)) => will_compose(george))).
fof(neg_conclusion, conjecture, (likes_music(george) & has_program(george) & ~will_compose(george))).