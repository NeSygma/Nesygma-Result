fof(p1, axiom, ! [X] : ((employee(X) & schedule_meeting(X)) => go_to_building(X))).
fof(p2, axiom, ! [X] : (lunch_building(X) => schedule_meeting(X))).
fof(p3, axiom, ! [X] : (employee(X) => (lunch_building(X) | lunch_home(X)))).
fof(p4, axiom, ! [X] : ((employee(X) & lunch_home(X)) => work_remote(X))).
fof(p5, axiom, ! [X] : ((employee(X) & in_other_countries(X)) => work_remote(X))).
fof(p6, axiom, ! [X] : (manager(X) => ~work_remote(X))).
fof(p7, axiom, appear_today(james) <=> manager(james)).
fof(p8, axiom, employee(james)).
fof(goal, conjecture, ((manager(james) | in_other_countries(james)) => (~lunch_home(james) & ~work_remote(james)))).