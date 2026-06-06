% Negative version: negated conclusion as conjecture
fof(premise_1, axiom, badults_is_british_sitcom).
fof(premise_2, axiom, starring_members_of_pappys(badults)).
fof(premise_3, axiom, piloted_july_2013_bbc_three(badults)).
fof(premise_4, axiom, working_title(badults, secret_dude_society)).
fof(premise_5, axiom, script_editor(badults, andrew_collins)).

% Negated conclusion: There does NOT exist a series S such that script_editor(S, andrew_collins) and working_title(S, secret_dude_society)
fof(goal_neg, conjecture, ~ ? [S] : (script_editor(S, andrew_collins) & working_title(S, secret_dude_society))).