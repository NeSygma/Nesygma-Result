fof(premise_1, axiom, ! [X] : ((employee(X) & schedules_meeting(X)) => goes_to_company(X))).
fof(premise_2, axiom, ! [X] : (has_lunch_company(X) => schedules_meeting(X))).
fof(premise_3, axiom, ! [X] : (employee(X) => (has_lunch_company(X) | has_lunch_home(X)))).
fof(premise_4, axiom, ! [X] : ((employee(X) & has_lunch_home(X)) => works_remotely(X))).
fof(premise_5, axiom, ! [X] : ((employee(X) & in_other_country(X)) => works_remotely(X))).
fof(premise_6, axiom, ! [X] : (manager(X) => ~works_remotely(X))).
fof(premise_7, axiom, (appears_company(james) <=> manager(james))).
fof(goal, conjecture, has_lunch_company(james)).