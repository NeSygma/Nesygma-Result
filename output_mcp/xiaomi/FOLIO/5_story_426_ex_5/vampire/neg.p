% Premises
fof(p1, axiom, ! [X] : ((employee(X) & schedule_meeting(X)) => go_to_building(X))).
fof(p2, axiom, ! [X] : (lunch_building(X) => schedule_meeting(X))).
fof(p3, axiom, ! [X] : (employee(X) => (lunch_building(X) | lunch_home(X)))).
fof(p4, axiom, ! [X] : (lunch_home(X) => remote(X))).
fof(p5, axiom, ! [X] : (in_other_country(X) => remote(X))).
fof(p6, axiom, ! [X] : (manager(X) => ~remote(X))).
fof(p7, axiom, appear_today(james) <=> manager(james)).

% James is an employee
fof(james_employee, axiom, employee(james)).

% Negated conclusion: James DOES have lunch in the company building
fof(goal, conjecture, lunch_building(james)).