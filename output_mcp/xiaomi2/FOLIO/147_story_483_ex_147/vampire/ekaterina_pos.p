fof(p1, axiom, ! [X] : (can_register_us(X) => can_participate_2024(X))).
fof(p2, axiom, ! [X] : (us_citizenship(X) => can_register_us(X))).
fof(p3, axiom, ! [X] : (us_citizenship(X) | korean_citizenship(X))).
fof(p4, axiom, ! [X] : (russian_official(X) => ~korean_citizenship(X))).
fof(p5, axiom, (~korean_citizenship(dreamy) & ~gazprom_manager(dreamy))).
fof(p6, axiom, (can_register_us(ekaterina) | russian_official(ekaterina))).
fof(goal, conjecture, (can_participate_2024(ekaterina) | gazprom_manager(ekaterina))).