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

% --- Now evaluate each pair option ---

% For each pair (X,Y), we want to know if they CAN be together.
% We'll define a predicate cannot_be_together(X,Y) if selecting both leads to contradiction.
% Actually, we need to check: is there ANY valid team that includes both?
% We'll use a choice rule to test each pair.

% Option A: Myers and Thomson
% Can they be together? Check if there exists a team with both.
% We'll derive a fact if they CAN be together.
% Use a helper: test_pair(PairName, X, Y)
test_pair(a, myers, thomson).
test_pair(b, ortega, yoder).
test_pair(c, paine, zayre).
test_pair(d, schmidt, wong).
test_pair(e, wong, yoder).

% For each pair, we check if there is a valid selection containing both.
% We'll use a choice rule to allow selecting additional members.
% But we need to check existence. Let's use a different approach:
% We'll define a predicate possible_pair(PairName) that holds if there exists
% a valid team containing both members of the pair.

% Since we can't directly express existence in ASP without multiple models,
% we'll use the following trick: for each pair, we add a constraint that
% FORBIDS the pair from being together, and see if the problem becomes UNSAT.
% Actually, we need the opposite: we want to know which pair CANNOT be together.
% So we test each pair by adding a constraint that they ARE together,
% and see if the problem is SAT (they can be together) or UNSAT (they cannot).

% Let's use a different approach: enumerate all possible teams and check.

% First, let's just find all valid teams and see which pairs appear together.
% We'll use a helper to record which pairs appear together in a valid team.

% For each pair, we can check if there exists a valid team containing both.
% We'll use a choice rule to select a "scenario" for each pair.

% Actually, simpler: we can just check each pair individually by adding
% the constraint that both are selected, and see if SAT or UNSAT.

% Let's do it in one shot using a meta-approach:
% We'll define a predicate pair(PN, X, Y) for each option.
pair(a, myers, thomson).
pair(b, ortega, yoder).
pair(c, paine, zayre).
pair(d, schmidt, wong).
pair(e, wong, yoder).

% For each pair, we want to know if they CAN be together.
% We'll use a choice rule to select which pair we're testing.
% But we need to test each independently.

% Better approach: use #show to output all selected employees,
% then manually check which pairs appear together.
% But we need the answer to be derived automatically.

% Let's use the following method:
% For each pair, we create a separate "test" by adding the constraint
% that both are selected. If the problem is SAT, they can be together.
% If UNSAT, they cannot.

% We'll use a choice rule to pick exactly one pair to test.
1 { test_pair_option(PN) : pair(PN, _, _) } 1.

% If we're testing pair PN, then both members must be selected.
selected(X) :- test_pair_option(PN), pair(PN, X, Y).
selected(Y) :- test_pair_option(PN), pair(PN, X, Y).

% Now, if the problem is SAT, the pair CAN be together.
% If UNSAT, the pair CANNOT be together.
% But we need to find which pair CANNOT be together.
% Since the question asks for the pair that CANNOT be together,
% we need to find the pair for which adding both leads to UNSAT.

% Actually, this approach tests one pair at a time per model.
% We need to test all pairs and find the one that's impossible.

% Let's rethink: we can use a different encoding.
% For each pair, define a condition that checks if they can be together.
% We'll use the fact that if selecting both leads to a contradiction,
% then they cannot be together.

% Let's define: cannot(PN) if selecting both members of pair PN
% leads to an unavoidable contradiction.

% We can encode this by saying: for each pair, if we assume both are selected,
% then we must be able to complete the team. If not, the pair is impossible.

% Let's use a simpler approach: just enumerate all valid teams
% and check which pairs appear together in at least one valid team.

% We'll use a helper to record pair occurrences.
% For each valid team, record which pairs are both selected.
both_selected(PN) :- pair(PN, X, Y), selected(X), selected(Y).

% Now, a pair CAN be together if both_selected(PN) is true in some model.
% A pair CANNOT be together if both_selected(PN) is never true.

% Since we want the pair that CANNOT be together, we need to find
% the pair that is never both_selected in any valid model.

% Let's just run the problem and look at all answer sets.
% We'll show selected employees and both_selected pairs.

#show selected/1.
#show both_selected/1.