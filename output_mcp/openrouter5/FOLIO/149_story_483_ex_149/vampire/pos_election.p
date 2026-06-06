% Positive file: original conclusion as conjecture
% Conclusion: It is not true that (Ekaterina can register to vote AND Vladimir can participate)
% i.e., ~(can_register(ekaterina) & can_participate(vladimir))

fof(distinct, axiom, (vladimir != ekaterina)).

% Premise 1: Everyone who can register to vote in the US can participate in the 2024 US presidential election.
fof(premise1, axiom, ! [X] : (can_register(X) => can_participate(X))).

% Premise 2: If someone has US citizenship, then they can register to vote in the US.
fof(premise2, axiom, ! [X] : (us_citizen(X) => can_register(X))).

% Premise 3: A person either has US citizenship or Taiwanese citizenship.
fof(premise3, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).

% Premise 4: No Russian Federation officials hold Taiwanese citizenship.
fof(premise4, axiom, ! [X] : (russian_official(X) => ~taiwan_citizen(X))).

% Premise 5: Vladimir neither holds Taiwanese citizenship nor is he a manager at Gazprom.
fof(premise5, axiom, ~taiwan_citizen(vladimir)).
fof(premise5b, axiom, ~gazprom_manager(vladimir)).

% Premise 6: Ekaterina can register to vote in the US, or she is a Russian Federation official.
fof(premise6, axiom, (can_register(ekaterina) | russian_official(ekaterina))).

% Conclusion: It is not true that Ekaterina can register and Vladimir can participate.
% i.e., ~(can_register(ekaterina) & can_participate(vladimir))
fof(conclusion, conjecture, ~(can_register(ekaterina) & can_participate(vladimir))).