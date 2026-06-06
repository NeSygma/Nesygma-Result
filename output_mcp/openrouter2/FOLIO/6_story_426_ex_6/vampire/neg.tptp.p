fof(employee_j, axiom, employee(j)).
fof(manager_equiv, axiom, (go_to_company_building_today(j) <=> manager(j))).
fof(no_manager_remote, axiom, ! [X] : (manager(X) => ~works_remotely_from_home(X))).
fof(in_other_remote, axiom, ! [X] : (in_other_countries(X) => works_remotely_from_home(X))).
fof(has_lunch_home_remote, axiom, ! [X] : (has_lunch_at_home(X) => works_remotely_from_home(X))).
fof(employee_lunch, axiom, ! [X] : (employee(X) => (has_lunch_in_company_building(X) | has_lunch_at_home(X)))).
fof(lunch_in_meeting, axiom, ! [X] : (has_lunch_in_company_building(X) => schedule_meeting_with_customer(X))).
fof(meeting_go, axiom, ! [X] : (schedule_meeting_with_customer(X) => go_to_company_building_today(X))).
fof(conjecture, conjecture, ~(((manager(j) | in_other_countries(j)) => ~((has_lunch_at_home(j) | works_remotely_from_home(j)))) & ((has_lunch_at_home(j) | works_remotely_from_home(j)) => ~((manager(j) | in_other_countries(j)))))).