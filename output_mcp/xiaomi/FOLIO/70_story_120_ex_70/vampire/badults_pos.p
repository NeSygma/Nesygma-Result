fof(british_sitcom, axiom, british_sitcom(badults)).
fof(stars_pappys, axiom, stars_member_of(badults, pappys)).
fof(piloted_bbc3, axiom, piloted_on(badults, bbc_three)).
fof(working_title, axiom, working_title(badults, the_secret_dude_society)).
fof(script_editor, axiom, script_editor(badults, andrew_collins)).

% Conclusion: No members of Pappy's have starred in a show piloting on BBC Two or BBC Three.
% Formalization: For all X, if X stars a member of Pappy's, then X was not piloted on BBC Two and not piloted on BBC Three.
fof(goal, conjecture, ! [X] : (stars_member_of(X, pappys) => (~piloted_on(X, bbc_two) & ~piloted_on(X, bbc_three)))).