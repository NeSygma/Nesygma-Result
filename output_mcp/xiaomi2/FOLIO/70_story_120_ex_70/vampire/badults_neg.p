fof(show_badults, axiom, show(badults)).
fof(stars_pappys, axiom, stars_members_of_pappys(badults)).
fof(piloted_bbc_three, axiom, piloted_on(badults, bbc_three)).
fof(neg_conclusion, conjecture,
    ? [X] : (show(X) & stars_members_of_pappys(X) & (piloted_on(X, bbc_two) | piloted_on(X, bbc_three)))).