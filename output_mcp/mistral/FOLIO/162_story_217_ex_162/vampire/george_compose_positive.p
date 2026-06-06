fof(premise1, axiom, (likes(george, music) => wants_to_compose(george))).
fof(premise2, axiom, (has_access(george, program) => can_compose(george))).
fof(premise3, axiom, ((can_compose(george) & wants_to_compose(george)) => will_compose(george))).
fof(conclusion, conjecture, (~will_compose(george) => ~can_compose(george))).