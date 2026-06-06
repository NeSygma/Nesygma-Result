fof(working_title_badults, axiom, working_title(badults, secret_dude_society)).
fof(script_editor_badults, axiom, script_editor(badults, andrew_collins)).
fof(distinct1, axiom, badults != andrew_collins).
fof(distinct2, axiom, badults != secret_dude_society).
fof(distinct3, axiom, andrew_collins != secret_dude_society).
fof(conjecture, conjecture, ~? [S] : (script_editor(S, andrew_collins) & working_title(S, secret_dude_society))).