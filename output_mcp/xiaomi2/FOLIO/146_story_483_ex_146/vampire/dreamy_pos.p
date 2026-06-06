fof(premise_1, axiom, ! [X] : (can_register_us(X) => can_participate_2024(X))).
fof(premise_2, axiom, ! [X] : (us_citizenship(X) => can_register_us(X))).
fof(premise_3, axiom, ! [X] : (us_citizenship(X) | korean_citizenship(X))).
fof(premise_4, axiom, ! [X] : (russian_official(X) => ~korean_citizenship(X))).
fof(premise_5, axiom, (~korean_citizenship(dreamy) & ~manager_gazprom(dreamy))).
fof(premise_6, axiom, (can_register_us(ekaterina) | russian_official(ekaterina))).
fof(distinct, axiom, dreamy != ekaterina).
fof(goal, conjecture, ~russian_official(dreamy)).