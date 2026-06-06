% Employees
employee(myers; ortega; paine; schmidt; thomson; wong; yoder; zayre).

% Team selection: each employee is either selected or not
{ selected(E) } :- employee(E).

% At least 4 employees on the team
:- #count { E : selected(E) } < 4.

% Condition 1: If Myers is on the team, neither Ortega nor Paine can be.
:- selected(myers), selected(ortega).
:- selected(myers), selected(paine).

% Condition 2: If Schmidt is on the team, both Paine and Thomson must also be.
:- selected(schmidt), not selected(paine).
:- selected(schmidt), not selected(thomson).

% Condition 3: If Wong is on the team, both Myers and Yoder must also be.
:- selected(wong), not selected(myers).
:- selected(wong), not selected(yoder).

% Define the pairs
pair(a, myers, thomson).
pair(b, ortega, yoder).
pair(c, paine, zayre).
pair(d, schmidt, wong).
pair(e, wong, yoder).

% For each pair, check if they can be together.
% We'll use a choice rule to select a "test scenario" for each pair.
% For each pair PN, we create a test: if we force both members to be selected,
% is there a valid team?

% We'll use a different approach: for each pair, we check if there exists
% a valid team containing both. We'll use the solver to find all models
% and record which pairs appear together.

% Let's just compute all valid teams and see which pairs co-occur.
% We already saw some results. Let's look more systematically.

% Record which pairs are both selected
both_selected(PN) :- pair(PN, X, Y), selected(X), selected(Y).

% A pair is possible if both_selected appears in some model.
% A pair is impossible if both_selected never appears.

% Let's add constraints to force each pair and see which ones are SAT.

% Actually, let's just test each pair individually by adding a constraint
% that both are selected, and see which one makes it UNSAT.

% We'll use a single run with a choice over which pair to test.
% But we need to find the pair that CANNOT be together.

% Let's use a different encoding: 
% For each pair, we define a condition that says "if both are selected,
% then a contradiction arises" - meaning they cannot be together.

% We can derive: cannot_be_together(PN) if forcing both leads to UNSAT.
% But we can't directly express this in ASP.

% Let's just enumerate all possible teams systematically.
% We'll use #show to see all selected employees and both_selected pairs.

% Let's add more constraints to see more models.
% Actually, let's just test each pair one by one.

% Let's do it differently: we'll add a constraint that says
% "at least one pair cannot be together" and find which one.

% Actually, the simplest approach: test each pair by adding
% selected(X) and selected(Y) as facts, and see if SAT or UNSAT.

% Let's do 5 separate runs. But first, let's check which pairs
% appeared in the models we already got.

% From the output:
% both_selected(b) appears (ortega, yoder) - so B is possible
% both_selected(c) appears (paine, zayre) - so C is possible
% both_selected(a) never appears - Myers and Thomson never together?
% both_selected(d) never appears - Schmidt and Wong never together?
% both_selected(e) never appears - Wong and Yoder never together?

% Let's check more carefully. Let's run with more models.