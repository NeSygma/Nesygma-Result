% Same premises as positive file.
fof(p1, axiom, ! [X] : ((employee(X) & schedules_meeting(X)) => goes_to_building(X))).

fof(p2, axiom, ! [X] : (has_lunch_building(X) => schedules_meeting(X))).

fof(p3a, axiom, ! [X] : (employee(X) => (has_lunch_building(X) | has_lunch_home(X)))).

fof(p3b, axiom, ! [X] : (employee(X) => ~(has_lunch_building(X) & has_lunch_home(X)))).

fof(p4, axiom, ! [X] : ((employee(X) & has_lunch_home(X)) => works_remote(X))).

fof(p5, axiom, ! [X] : ((employee(X) & in_other_countries(X)) => works_remote(X))).

fof(p6, axiom, ! [X] : (manager(X) => ~works_remote(X))).

fof(p7, axiom, appears_in_company(james) <=> manager(james)).

% Negated conclusion: (manager(james) | in_other_countries(james)) & (has_lunch_home(james) | works_remote(james))
fof(neg_conclusion, conjecture, (manager(james) | in_other_countries(james)) & (has_lunch_home(james) | works_remote(james))).