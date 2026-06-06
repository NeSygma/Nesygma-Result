fof(badults_is_show, axiom, is_a(badults, british_sitcom_series)).
fof(pappys_members_star_in_badults, axiom, ! [M] : (member_of_pappys(M) => stars_in(M, badults))).
fof(badults_piloted_on_bbc_three, axiom, piloted_in(badults, bbc_three)).
fof(working_title, axiom, working_title_of(the_secret_dude_society, badults)).
fof(script_editor, axiom, script_editor_of(andrew_collins, badults)).

fof(badults_is_a_show, axiom, show(badults)).
fof(bbc_three_is_channel, axiom, channel(bbc_three)).
fof(bbc_two_is_channel, axiom, channel(bbc_two)).

fof(exists_show_starred_in_def, axiom, ! [P, C] : (exists_show_starred_in(P, C) <=> ? [S] : (stars_in(P, S) & piloted_in(S, C)))).

fof(conclusion, conjecture, ! [M] : (member_of_pappys(M) => ~(exists_show_starred_in(M, bbc_two) | exists_show_starred_in(M, bbc_three)))).