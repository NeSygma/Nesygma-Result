% Positive version
fof(distinct, axiom, (badults != andrew_collins & badults != secret_dude_society & andrew_collins != secret_dude_society)).
fof(premise1, axiom, working_title(badults, secret_dude_society)).
fof(premise2, axiom, script_editor(andrew_collins, badults)).
fof(goal, conjecture, ? [S] : (script_editor(andrew_collins, S) & working_title(S, secret_dude_society))).