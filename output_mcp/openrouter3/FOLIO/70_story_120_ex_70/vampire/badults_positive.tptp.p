% Premises about Badults TV show
fof(premise_1, axiom, ? [X] : (pappy_member(X) & starred_in(X, badults))).
fof(premise_2, axiom, piloted_in(badults, july, 2013, bbc_three)).
fof(premise_3, axiom, working_title(badults, 'the_secret_dude_society')).
fof(premise_4, axiom, script_editor(andrew_collins, badults)).

% Distinctness axioms
fof(distinct_channels, axiom, (bbc_two != bbc_three)).

% Conclusion to evaluate: No members of Pappy's have starred in a show piloting on BBC Two or BBC Three
% This means: For all X, if X is a member of Pappy's and starred in some show Y, then Y was NOT piloted on BBC Two or BBC Three
fof(goal, conjecture, 
    ! [X, Y] : ((pappy_member(X) & starred_in(X, Y)) => 
                ~(piloted_in(Y, _, _, bbc_two) | piloted_in(Y, _, _, bbc_three))))).