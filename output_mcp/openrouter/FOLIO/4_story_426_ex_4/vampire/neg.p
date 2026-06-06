% Negative version
fof(rule1, axiom, ![X] : (schedule_meeting(X) => go_to_building_today(X))).
fof(rule2, axiom, ![X] : (lunch_in_building(X) => schedule_meeting(X))).
fof(rule3, axiom, ![X] : (lunch_in_building(X) <=> ~lunch_at_home(X))).
fof(rule4, axiom, ![X] : (lunch_at_home(X) => working_remotely_from_home(X))).
fof(rule5, axiom, ![X] : (in_other_countries(X) => working_remotely_from_home(X))).
fof(rule6, axiom, ![X] : (manager(X) => ~working_remotely_from_home(X))).
fof(rule7, axiom, ![X] : (appear_in_company_today(X) <=> manager(X))).
fof(goal, conjecture, ~lunch_in_building(james)).