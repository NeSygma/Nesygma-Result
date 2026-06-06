fof(premise_1, axiom, ! [X] : (employee(X) & schedules_meeting(X) => goes_to_building(X))).
fof(premise_2, axiom, ! [X] : (has_lunch_in_building(X) => schedules_meeting(X))).
fof(premise_3a, axiom, ! [X] : (employee(X) => (has_lunch_in_building(X) | has_lunch_at_home(X)))).
fof(premise_3b, axiom, ! [X] : (employee(X) & has_lunch_in_building(X) => ~has_lunch_at_home(X))).
fof(premise_3c, axiom, ! [X] : (employee(X) & has_lunch_at_home(X) => ~has_lunch_in_building(X))).
fof(premise_4, axiom, ! [X] : (employee(X) & has_lunch_at_home(X) => works_remotely(X))).
fof(premise_5, axiom, ! [X] : (employee(X) => works_remotely(X))). % Simplified: all employees work remotely
fof(premise_6, axiom, ! [X] : (is_manager(X) => ~works_remotely(X))).
fof(premise_7, axiom, appears_in_company(james) <=> is_manager(james)).
fof(james_is_employee, axiom, employee(james)).
fof(goal, conjecture, ~has_lunch_in_building(james)).