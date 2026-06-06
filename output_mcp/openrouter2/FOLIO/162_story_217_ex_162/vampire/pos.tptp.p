fof(premise1, axiom, (likes_music(g) => wants_compose(g))).
fof(premise2, axiom, (has_program(g) => can_compose(g))).
fof(premise3, axiom, ((can_compose(g) & wants_compose(g)) => will_compose(g))).
fof(conjecture, conjecture, (~will_compose(g) => ~can_compose(g))).