fof(premise1, axiom, ! [X] : (schedules_with_customer(X) => appear_today(X))).
fof(premise2, axiom, ! [X] : (lunch_in_company(X) => schedules_with_customer(X))).
fof(premise3, axiom, ! [X] : (lunch_in_company(X) | lunch_at_home(X))).
fof(premise4, axiom, ! [X] : (lunch_at_home(X) => remote_home(X))).
fof(premise5, axiom, ! [X] : (foreign(X) => remote_home(X))).
fof(premise6, axiom, ! [X] : (manager(X) => ~remote_home(X))).
fof(iff_james, axiom, appear_today(james) <=> manager(james)).
fof(goal, conjecture, lunch_in_company(james)).