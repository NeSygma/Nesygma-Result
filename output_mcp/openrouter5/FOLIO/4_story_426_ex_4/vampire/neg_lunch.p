% Negative version: conjecture is "James does NOT have lunch in the company"
fof(distinct, axiom, (james != manager_generic)).

% All employees who schedule a meeting with their customers will go to the company building today.
fof(rule1, axiom, ! [X] : ((employee(X) & schedules_meeting(X)) => goes_to_building(X))).

% Everyone who has lunch in the company building schedules meetings with their customers.
fof(rule2, axiom, ! [X] : (lunch_in_building(X) => schedules_meeting(X))).

% Employees have lunch either in the company building or at home.
fof(rule3, axiom, ! [X] : (employee(X) => (lunch_in_building(X) | lunch_at_home(X)))).

% If an employee has lunch at home, they are working remotely from home.
fof(rule4, axiom, ! [X] : ((employee(X) & lunch_at_home(X)) => works_remotely(X))).

% All employees who are in other countries work remotely from home.
fof(rule5, axiom, ! [X] : ((employee(X) & in_other_country(X)) => works_remotely(X))).

% No managers work remotely from home.
fof(rule6, axiom, ! [X] : (manager(X) => ~works_remotely(X))).

% James will appear in the company today if and only if he is a manager.
fof(rule7, axiom, (appears_in_company(james) <=> manager(james))).

% James is an employee.
fof(fact1, axiom, employee(james)).

% Negated conclusion: James does NOT have lunch in the company.
fof(goal, conjecture, ~lunch_in_building(james)).