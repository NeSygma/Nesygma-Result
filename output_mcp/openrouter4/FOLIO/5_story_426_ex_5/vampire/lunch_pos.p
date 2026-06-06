% Positive file: original conclusion as conjecture
fof(premise1, axiom, ! [X] : ((employee(X) & schedules_meeting(X)) => goes_to_company(X))).
fof(premise2, axiom, ! [X] : (has_lunch_company(X) => schedules_meeting(X))).
fof(premise3, axiom, ! [X] : (employee(X) => (has_lunch_company(X) | has_lunch_home(X)))).
fof(premise4, axiom, ! [X] : ((employee(X) & has_lunch_home(X)) => works_remotely(X))).
fof(premise5, axiom, ! [X] : ((employee(X) & in_other_country(X)) => works_remotely(X))).
fof(premise6, axiom, ! [X] : (manager(X) => ~works_remotely(X))).
fof(premise7, axiom, goes_to_company(james) <=> manager(james)).
fof(conclusion, conjecture, ~has_lunch_company(james)).