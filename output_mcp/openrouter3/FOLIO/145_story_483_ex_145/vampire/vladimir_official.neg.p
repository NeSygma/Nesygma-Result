% Premises about citizenship and voting
fof(rule_1, axiom, ! [X] : (can_register(X) => can_participate(X))).
fof(rule_2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(rule_3, axiom, ! [X] : (us_citizen(X) | tw_citizen(X))).
fof(rule_4, axiom, ! [X] : (russian_official(X) => ~tw_citizen(X))).

% Facts about Vladimir
fof(vladimir_citizenship, axiom, ~tw_citizen(vladimir)).
fof(vladimir_position, axiom, ~manager_gazprom(vladimir)).

% Facts about Ekaterina
fof(ekaterina_fact, axiom, can_register(ekaterina) | russian_official(ekaterina)).

% Distinctness of individuals
fof(distinct_people, axiom, (vladimir != ekaterina)).

% Negated conclusion to evaluate
fof(goal_negation, conjecture, ~russian_official(vladimir)).