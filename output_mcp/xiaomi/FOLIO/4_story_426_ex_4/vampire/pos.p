fof(p1, axiom, ! [X] : ((employee(X) & schedule_meeting(X)) => go_building(X))).
fof(p2, axiom, ! [X] : (lunch_building(X) => schedule_meeting(X))).
fof(p3, axiom, ! [X] : (employee(X) => (lunch_building(X) | lunch_home(X)))).
fof(p4, axiom, ! [X] : ((employee(X) & lunch_home(X)) => remote(X))).
fof(p5, axiom, ! [X] : ((employee(X) & other_country(X)) => remote(X))).
fof(p6, axiom, ! [X] : (manager(X) => ~remote(X))).
fof(p7, axiom, (appear_building(james) <=> manager(james))).
fof(p8, axiom, employee(james)).
fof(p9, axiom, ~other_country(james)).
fof(p10, axiom, appear_building(james)).
fof(goal, conjecture, lunch_building(james)).