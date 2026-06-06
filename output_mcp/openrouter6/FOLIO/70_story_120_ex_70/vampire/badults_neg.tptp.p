% Premises
fof(premise1, axiom, ? [X] : (pappy_member(X) & stars_in(badults, X))).
fof(premise2, axiom, piloted_on(badults, bbc_three)).
fof(premise3, axiom, working_title(badults, the_secret_dude_society)).
fof(premise4, axiom, script_editor(badults, andrew_collins)).

% Distinctness axioms
fof(distinct1, axiom, badults != bbc_three).
fof(distinct2, axiom, badults != bbc_two).
fof(distinct3, axiom, bbc_two != bbc_three).

% Negated conclusion: There exists a member of Pappy's who starred in a show piloting on BBC Two or BBC Three.
fof(neg_conclusion, conjecture, ? [X, Y] : (pappy_member(X) & stars_in(Y, X) & (piloted_on(Y, bbc_two) | piloted_on(Y, bbc_three)))).

% Additional constants
fof(const_bbc_two, axiom, bbc_two = bbc_two).
fof(const_andrew, axiom, andrew_collins = andrew_collins).