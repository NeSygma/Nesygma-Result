% Premise 1: If people at Mary's school work in student jobs on campus, then they need to earn money
fof(premise1, axiom, ! [X] : (at_marys_school(X) => (works_student_job(X) => needs_money(X)))).

% Premise 2: If people at Mary's school order takeout frequently, then they work in student jobs
fof(premise2, axiom, ! [X] : (at_marys_school(X) => (orders_takeout(X) => works_student_job(X)))).

% Premise 3: People at Mary's school order takeout or enjoy dining hall
fof(premise3, axiom, ! [X] : (at_marys_school(X) => (orders_takeout(X) | enjoys_dining(X)))).

% Premise 4: If people at Mary's school enjoy dining hall, then they are not picky eaters
fof(premise4, axiom, ! [X] : (at_marys_school(X) => (enjoys_dining(X) => ~picky_eater(X)))).

% Premise 5: If people at Mary's school enjoy dining hall, then they spend time eating with friends
fof(premise5, axiom, ! [X] : (at_marys_school(X) => (enjoys_dining(X) => time_eating_friends(X)))).

% Premise 6: Hannah is at Mary's school
fof(premise6, axiom, at_marys_school(hannah)).

% Premise 7: Hannah works in student jobs and if she needs money then she is neither picky nor needs money
fof(premise7, axiom, works_student_job(hannah) & (needs_money(hannah) => (~picky_eater(hannah) & ~needs_money(hannah)))).

% Conclusion: Hannah is at Mary's school, not a picky eater, and spends time eating with friends
fof(goal, conjecture, at_marys_school(hannah) & ~picky_eater(hannah) & time_eating_friends(hannah)).