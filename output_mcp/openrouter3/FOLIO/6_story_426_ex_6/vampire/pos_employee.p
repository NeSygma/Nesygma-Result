fof(premise_1, axiom, ! [X] : (employee(X) & schedule_meeting(X) => go_to_building(X))).
fof(premise_2, axiom, ! [X] : (has_lunch_in_building(X) => schedule_meeting(X))).
fof(premise_3, axiom, ! [X] : (employee(X) => (has_lunch_in_building(X) | has_lunch_at_home(X)))).
fof(premise_4, axiom, ! [X] : (employee(X) & has_lunch_at_home(X) => works_remotely(X))).
fof(premise_5, axiom, ! [X] : (employee(X) & in_other_countries(X) => works_remotely(X))).
fof(premise_6, axiom, ! [X] : (manager(X) => ~works_remotely(X))).
fof(premise_7, axiom, go_to_building(james) <=> manager(james)).
fof(goal, conjecture, (has_lunch_at_home(james) | works_remotely(james)) => (~manager(james) & ~in_other_countries(james))).