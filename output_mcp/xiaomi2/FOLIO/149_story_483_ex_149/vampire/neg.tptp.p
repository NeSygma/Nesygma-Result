% Premise 1: Everyone who can register to vote in the US can participate in the 2024 election
fof(premise1, axiom, ! [X] : (can_register_us(X) => can_participate_2024(X))).

% Premise 2: US citizenship implies can register to vote
fof(premise2, axiom, ! [X] : (us_citizenship(X) => can_register_us(X))).

% Premise 3: Everyone has either US or Korean citizenship
fof(premise3, axiom, ! [X] : (us_citizenship(X) | korean_citizenship(X))).

% Premise 4: No Russian officials hold Korean citizenship
fof(premise4, axiom, ! [X] : (russian_official(X) => ~korean_citizenship(X))).

% Premise 5: Dreamy neither holds Korean citizenship nor is a manager at Gazprom
fof(premise5, axiom, (~korean_citizenship(dreamy) & ~manager_gazprom(dreamy))).

% Premise 6: Ekaterina can register to vote in the US, or she is a Russian official
fof(premise6, axiom, (can_register_us(ekaterina) | russian_official(ekaterina))).

% Negated conclusion: Ekaterina CAN register AND Dreamy CAN participate
fof(goal, conjecture, (can_register_us(ekaterina) & can_participate_2024(dreamy))).