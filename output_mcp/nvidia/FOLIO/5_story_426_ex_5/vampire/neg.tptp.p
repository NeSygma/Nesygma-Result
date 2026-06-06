% Axioms
fof(axiom1, axiom, ! [X] : ((employee(X) & schedules_meeting_with_customers(X)) => go_to_company_building_today(X))).
fof(axiom2, axiom, ! [X] : ((employee(X) & has_lunch_in_company_building(X)) => schedules_meeting_with_customers(X))).
fof(axiom3, axiom, ! [X] : (employee(X) => (has_lunch_in_company_building(X) | has_lunch_at_home(X)))).
fof(axiom4, axiom, ! [X] : ((employee(X) & has_lunch_at_home(X)) => works_remotely_from_home(X))).
fof(axiom5, axiom, ! [X] : ((employee(X) & in_other_country(X)) => works_remotely_from_home(X))).
fof(axiom6, axiom, ! [X] : (manager(X) => ~works_remotely_from_home(X))).
fof(axiom7, axiom, go_to_company_building_today(james) <=> manager(james)).
fof(conclusion, conjecture, has_lunch_in_company_building(james)).