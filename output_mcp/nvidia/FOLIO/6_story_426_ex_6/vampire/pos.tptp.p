fof(prem1, axiom, ! [X] : (employee(X) & schedules_meeting_with_customers(X) => goes_to_company_building_today(X))).
fof(prem2, axiom, ! [X] : (has_lunch_in_company_building(X) => schedules_meeting_with_customers(X))).
fof(prem3, axiom, ! [X] : (employee(X) => (has_lunch_in_company_building(X) | has_lunch_at_home(X)))).
fof(prem4, axiom, ! [X] : (employee(X) & has_lunch_at_home(X) => working_remotely_from_home(X))).
fof(prem5, axiom, ! [X] : (employee(X) & in_other_countries(X) => working_remotely_from_home(X))).
fof(prem6, axiom, ! [X] : (manager(X) => ~working_remotely_from_home(X))).
fof(bicond_1, axiom, appears_today(james) => manager(james)).
fof(bicond_2, axiom, manager(james) => appears_today(james)).
fof(conclusion, conjecture, ((manager(james) | in_other_countries(james)) => ~(has_lunch_at_home(james) | working_remotely_from_home(james))) & ((has_lunch_at_home(james) | working_remotely_from_home(james)) => ~(manager(james) | in_other_countries(james)))).