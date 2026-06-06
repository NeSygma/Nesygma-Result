% Negative version: negated conclusion as conjecture
% Premises:
% Yale University is a private Ivy League research university.
% Yale University moved to New Haven in 1716.
% Yale university's endowment was valued at $42.3 billion.
% List of residential colleges at Yale (not needed for conclusion).

% Predicates:
% private_ivy_league_research_univ(X) - X is a private Ivy League research university
% moved_to(X, Y) - X moved to Y

fof(premise_1, axiom, private_ivy_league_research_univ(yale_university)).
fof(premise_2, axiom, moved_to(yale_university, new_haven)).
fof(distinct, axiom, yale_university != new_haven).

% Negated conclusion: There does NOT exist an X such that X is a private Ivy League research university and X moved to New Haven.
fof(goal_negated, conjecture, ~ ? [X] : (private_ivy_league_research_univ(X) & moved_to(X, new_haven))).