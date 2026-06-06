% Positive version: original conclusion as conjecture
% Predicates:
% can_register(X) - X can register to vote in the US
% can_participate(X) - X can participate in the 2024 US presidential election
% us_citizen(X) - X has US citizenship
% taiwan_citizen(X) - X has Taiwanese citizenship
% russian_official(X) - X is a Russian Federation official
% manager_gazprom(X) - X is a manager at Gazprom

fof(distinct, axiom, (vladimir != ekaterina)).

% Premise 1: Everyone who can register to vote in the US can participate in the 2024 US presidential election
fof(premise1, axiom, ! [X] : (can_register(X) => can_participate(X))).

% Premise 2: If someone has US citizenship, then they can register to vote in the US
fof(premise2, axiom, ! [X] : (us_citizen(X) => can_register(X))).

% Premise 3: A person either has US citizenship or Taiwanese citizenship
fof(premise3, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).

% Premise 4: No Russian Federation officials hold Taiwanese citizenship
fof(premise4, axiom, ! [X] : (russian_official(X) => ~taiwan_citizen(X))).

% Premise 5: Vladimir neither holds Taiwanese citizenship nor is he a manager at Gazprom
fof(premise5, axiom, ~taiwan_citizen(vladimir)).
fof(premise5b, axiom, ~manager_gazprom(vladimir)).

% Premise 6: Ekaterina can register to vote in the US, or she is a Russian Federation official
fof(premise6, axiom, (can_register(ekaterina) | russian_official(ekaterina))).

% Conclusion: Ekaterina can participate in the 2024 US presidential election or Vladimir is a manager at Gazprom
fof(conclusion, conjecture, (can_participate(ekaterina) | manager_gazprom(vladimir))).