% Negative version: negated conclusion as conjecture
% Predicates:
% can_register(X) - X can register to vote in the US
% can_participate(X) - X can participate in the 2024 US presidential election
% us_citizen(X) - X has US citizenship
% taiwan_citizen(X) - X has Taiwanese citizenship
% russian_official(X) - X is a Russian Federation official
% manager_gazprom(X) - X is a manager at Gazprom

fof(distinct, axiom, (vladimir != ekaterina)).

% Premise 1: Everyone who can register to vote in the US can participate in the 2024 US presidential election
fof(premise_1, axiom, ! [X] : (can_register(X) => can_participate(X))).

% Premise 2: If someone has US citizenship, then they can register to vote in the US
fof(premise_2, axiom, ! [X] : (us_citizen(X) => can_register(X))).

% Premise 3: A person either has US citizenship or Taiwanese citizenship
fof(premise_3, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).

% Premise 4: No Russian Federation officials hold Taiwanese citizenship
fof(premise_4, axiom, ! [X] : (russian_official(X) => ~taiwan_citizen(X))).

% Premise 5: Vladimir neither holds Taiwanese citizenship nor is he a manager at Gazprom
fof(premise_5, axiom, ~taiwan_citizen(vladimir)).
fof(premise_5b, axiom, ~manager_gazprom(vladimir)).

% Premise 6: Ekaterina can register to vote in the US, or she is a Russian Federation official
fof(premise_6, axiom, (can_register(ekaterina) | russian_official(ekaterina))).

% Negated conclusion: It is NOT the case that (Ekaterina can participate OR is a manager at Gazprom)
% i.e., Ekaterina cannot participate AND is not a manager at Gazprom
fof(negated_conclusion, conjecture, (~can_participate(ekaterina) & ~manager_gazprom(ekaterina))).