% Premises about employees and lunch
fof(premise_1, axiom, ! [X] : (employee(X) & schedules_meeting(X) => goes_to_building(X))).
fof(premise_2, axiom, ! [X] : (has_lunch_in_building(X) => schedules_meeting(X))).
fof(premise_3, axiom, ! [X] : (employee(X) => (has_lunch_in_building(X) | has_lunch_at_home(X)))).
fof(premise_4, axiom, ! [X] : (employee(X) & has_lunch_at_home(X) => works_remotely(X))).
fof(premise_5, axiom, ! [X] : (employee(X) & in_other_country(X) => works_remotely(X))).
fof(premise_6, axiom, ! [X] : (manager(X) => ~works_remotely(X))).
fof(premise_7, axiom, ! [X] : (appears_in_company(X) <=> manager(X))).

% Facts about James
fof(james_employee, axiom, employee(james)).
fof(james_appears, axiom, appears_in_company(james)).

% Conclusion to evaluate
fof(goal, conjecture, ~has_lunch_in_building(james)).