% Positive file: original conclusion as conjecture
% Conclusion: James does not have lunch in the company.

% Predicates:
% employee(X) - X is an employee
% schedules_meeting(X) - X schedules a meeting with their customers
% goes_to_building(X) - X goes to the company building today
% has_lunch_building(X) - X has lunch in the company building
% has_lunch_home(X) - X has lunch at home
% works_remote(X) - X works remotely from home
% in_other_country(X) - X is in other countries
% manager(X) - X is a manager
% appears_today(X) - X will appear in the company today

fof(distinct, axiom, (james != other_employee)).

% All employees who schedule a meeting with their customers will go to the company building today.
fof(rule1, axiom, ! [X] : ((employee(X) & schedules_meeting(X)) => goes_to_building(X))).

% Everyone who has lunch in the company building schedules meetings with their customers.
fof(rule2, axiom, ! [X] : (has_lunch_building(X) => schedules_meeting(X))).

% Employees have lunch either in the company building or at home.
fof(rule3, axiom, ! [X] : (employee(X) => (has_lunch_building(X) | has_lunch_home(X)))).

% If an employee has lunch at home, they are working remotely from home.
fof(rule4, axiom, ! [X] : ((employee(X) & has_lunch_home(X)) => works_remote(X))).

% All employees who are in other countries work remotely from home.
fof(rule5, axiom, ! [X] : ((employee(X) & in_other_country(X)) => works_remote(X))).

% No managers work remotely from home.
fof(rule6, axiom, ! [X] : (manager(X) => ~works_remote(X))).

% James will appear in the company today if and only if he is a manager.
fof(rule7, axiom, (appears_today(james) <=> manager(james))).

% James is an employee (implicitly from context)
fof(fact_james_employee, axiom, employee(james)).

% Conclusion: James does not have lunch in the company.
fof(goal, conjecture, ~has_lunch_building(james)).