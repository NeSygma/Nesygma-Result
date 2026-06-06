fof(p1, axiom, ! [X] : ((employee(X) & schedules_meeting(X)) => goes_to_building(X))).
fof(p2, axiom, ! [X] : ((employee(X) & has_lunch_in_building(X)) => schedules_meeting(X))).
fof(p3, axiom, ! [X] : (employee(X) => (has_lunch_in_building(X) | has_lunch_at_home(X)))).
fof(p4, axiom, ! [X] : ((employee(X) & has_lunch_at_home(X)) => works_remotely(X))).
fof(p6, axiom, ! [X] : (manager(X) => ~works_remotely(X))).
fof(p7, axiom, (goes_to_building(james) <=> manager(james))).
fof(p_james_is_employee, axiom, employee(james)).
fof(goal, conjecture, has_lunch_in_building(james)).