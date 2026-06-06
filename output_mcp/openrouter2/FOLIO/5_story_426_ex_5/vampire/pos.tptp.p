fof(rule_1, axiom, ! [X] : ((employee(X) & schedule_meeting_with_customer(X)) => go_to_company_today(X))).
fof(rule_2, axiom, ! [X] : ((employee(X) & lunch_in_company(X)) => schedule_meeting_with_customer(X))).
fof(rule_3, axiom, ! [X] : (employee(X) => (lunch_in_company(X) | lunch_at_home(X)))).
fof(rule_4, axiom, ! [X] : ((employee(X) & lunch_at_home(X)) => remote_home(X))).
fof(rule_5, axiom, ! [X] : ((employee(X) & in_other_country(X)) => remote_home(X))).
fof(rule_6, axiom, ! [X] : (manager(X) => ~remote_home(X))).
fof(rule_7, axiom, (go_to_company_today(james) <=> manager(james))).
fof(employee_james, axiom, employee(james)).
fof(conjecture, conjecture, ~lunch_in_company(james)).