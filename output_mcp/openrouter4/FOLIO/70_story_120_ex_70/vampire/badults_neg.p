% Negated claim: Some member of Pappy's has starred in a show piloting on BBC Two or BBC Three
fof(distinct_channels, axiom, bbc_two != bbc_three).

fof(premise1, axiom,
    (british(badults) & sitcom(badults) & ? [X] : (member_of_pappys(X) & starred_in(X, badults)))).

fof(premise2, axiom, piloted_on(badults, bbc_three)).

fof(premise3, axiom, working_title(badults, the_secret_dude_society)).

fof(premise4, axiom, script_editor(andrew_collins, badults)).

% Negation of the original conclusion:
% It is NOT the case that no members of Pappy's have starred in a show piloting on BBC Two or BBC Three.
% Equivalently: There exists a member of Pappy's who starred in a show piloting on BBC Two or BBC Three.
fof(goal_neg, conjecture,
    ? [X, Y] : (member_of_pappys(X) & starred_in(X, Y) & (piloted_on(Y, bbc_two) | piloted_on(Y, bbc_three)))).