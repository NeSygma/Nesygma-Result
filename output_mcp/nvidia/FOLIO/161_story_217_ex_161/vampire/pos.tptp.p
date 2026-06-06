% Axioms
fof(premise1, axiom, likes(george, music) => wants_to_compose(george)).
fof(premise2, axiom, has_program(george) => can_compose(george)).
fof(premise3, axiom, (can_compose(george) & wants_to_compose(george)) => will_compose(george)).
fof(conclusion, conjecture, (likes(george, music) & has_program(george)) => will_compose(george)).