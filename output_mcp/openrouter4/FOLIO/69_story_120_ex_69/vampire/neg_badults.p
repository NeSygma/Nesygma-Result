fof(distinct_entities, axiom, (badults != secret_dude_society & badults != andrew_collins & secret_dude_society != andrew_collins)).
fof(premise1, axiom, british_sitcom(badults)).
fof(premise2, axiom, piloted_july_2013_bbc_three(badults)).
fof(premise3, axiom, working_title(badults, secret_dude_society)).
fof(premise4, axiom, script_editor(badults, andrew_collins)).
fof(goal_negated, conjecture, ~(? [X] : (script_editor(X, andrew_collins) & working_title(X, secret_dude_society)))).