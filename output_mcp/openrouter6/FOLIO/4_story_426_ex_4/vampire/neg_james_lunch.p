fof(premise1, axiom, ! [X] : (employee(X) & schedules_meeting(X) => goes_to_company_building_today(X))).
fof(premise2, axiom, ! [X] : (has_lunch_in_company_building(X) => schedules_meeting(X))).
fof(premise3, axiom, ! [X] : (employee(X) => (has_lunch_in_company_building(X) | has_lunch_at_home(X)))).
fof(premise3_exclusive, axiom, ! [X] : (employee(X) => ~(has_lunch_in_company_building(X) & has_lunch_at_home(X)))).
fof(premise4, axiom, ! [X] : (employee(X) & has_lunch_at_home(X) => works_remotely_from_home(X))).
fof(premise5, axiom, ! [X] : (employee(X) & in_other_countries(X) => works_remotely_from_home(X))).
fof(premise6, axiom, ! [X] : (manager(X) => ~works_remotely_from_home(X))).
fof(premise7, axiom, appears_in_company_today(james) <=> manager(james)).
fof(james_is_employee, axiom, employee(james)). % We need to assume James is an employee? Not given. Let's add as an assumption? Actually we should not assume. Let's not add this.
fof(goal_neg, conjecture, ~has_lunch_in_company_building(james)).