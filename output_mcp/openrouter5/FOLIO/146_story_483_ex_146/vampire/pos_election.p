% Positive file: original conclusion as conjecture
% Conclusion: Vladimir is not a Russian federation official

% Predicates:
% can_register(X) - X can register to vote in the United States
% can_participate(X) - X can participate in the 2024 US presidential election
% us_citizen(X) - X has United States citizenship
% taiwan_citizen(X) - X has Taiwanese citizenship
% russian_official(X) - X is a Russian Federation official
% manager_gazprom(X) - X is a manager at Gazprom

fof(premise_1, axiom, ! [X] : (can_register(X) => can_participate(X))).
fof(premise_2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(premise_3, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).
fof(premise_4, axiom, ! [X] : (russian_official(X) => ~taiwan_citizen(X))).
fof(premise_5, axiom, (~taiwan_citizen(vladimir) & ~manager_gazprom(vladimir))).
fof(premise_6, axiom, (can_register(ekaterina) | russian_official(ekaterina))).

fof(conclusion, conjecture, ~russian_official(vladimir)).