fof(premise1, axiom, ! [X] : (can_register_us(X) => can_participate_2024(X))).
fof(premise2, axiom, ! [X] : (us_citizenship(X) => can_register_us(X))).
fof(premise3, axiom, ! [X] : (us_citizenship(X) | korean_citizenship(X))).
fof(premise4, axiom, ! [X] : (russian_official(X) => ~korean_citizenship(X))).
fof(premise5, axiom, (~korean_citizenship(dreamy) & ~manager_gazprom(dreamy))).
fof(premise6, axiom, (can_register_us(ekaterina) | russian_official(ekaterina))).
fof(goal, conjecture, ~russian_official(dreamy)).