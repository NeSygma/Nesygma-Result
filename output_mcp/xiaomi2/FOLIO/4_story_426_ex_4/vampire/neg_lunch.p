fof(p1, axiom, ! [X] : ((employee(X) & schedule_meeting(X)) => go_to_building(X))).
fof(p2, axiom, ! [X] : (lunch_in_building(X) => schedule_meeting(X))).
fof(p3, axiom, ! [X] : (employee(X) => (lunch_in_building(X) | lunch_at_home(X)))).
fof(p4, axiom, ! [X] : ((employee(X) & lunch_at_home(X)) => work_remote(X))).
fof(p5, axiom, ! [X] : ((employee(X) & in_other_country(X)) => work_remote(X))).
fof(p6, axiom, ! [X] : (manager(X) => ~work_remote(X))).
fof(p7, axiom, appear_in_company(james) <=> manager(james)).
fof(james_employee, axiom, employee(james)).
fof(goal, conjecture, ~lunch_in_building(james)).