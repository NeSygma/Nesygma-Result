fof(prem1, axiom, likes(george, music) => wants_to_compose(george)).
fof(prem2, axiom, has_access_to_program(george) => can_compose(george)).
fof(prem3, axiom, (can_compose(george) & wants_to_compose(george)) => will_compose(george)).
fof(conclusion, conjecture, ~will_compose(george) => ~can_compose(george)).