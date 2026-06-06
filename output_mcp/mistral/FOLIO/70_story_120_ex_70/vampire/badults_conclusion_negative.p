fof(badults_is_show, axiom, show(badults)).
fof(british_sitcom, axiom, sitcom(badults)).
fof(member_of_pappys_def, axiom, ! [X] : (member_of_pappys(X) <=> (X = member1 | X = member2 | X = member3))).
fof(starred_in_badults, axiom, ! [X] : (member_of_pappys(X) => starred_in(X, badults))).
fof(piloted_on_badults, axiom, piloted_on(badults, bbc_three)).
fof(working_title_badults, axiom, working_title(badults, "The Secret Dude Society")).
fof(script_editor_badults, axiom, script_editor(badults, andrew_collins)).
fof(bbc_two_three_channels, axiom, (channel(bbc_two) & channel(bbc_three))).
fof(negated_conclusion, conjecture, ? [X, S] : (member_of_pappys(X) & starred_in(X, S) & (piloted_on(S, bbc_two) | piloted_on(S, bbc_three)))).