% Negative test: negated conclusion as conjecture
fof(distinct1, axiom, pappy_member1 != badults).
fof(distinct2, axiom, pappy_member1 != bbc_two).
fof(distinct3, axiom, pappy_member1 != bbc_three).
fof(distinct4, axiom, badults != bbc_two).
fof(distinct5, axiom, badults != bbc_three).
fof(distinct6, axiom, bbc_two != bbc_three).

% Premise: member of Pappy's starred in Badults
fof(premise1, axiom, member_of_pappys(pappy_member1)).
fof(premise2, axiom, starred_in(pappy_member1, badults)).
% Premise: Badults piloted on BBC Three
fof(premise3, axiom, piloted_on(badults, bbc_three)).

% Negated conclusion: there exists a member of Pappy's who starred in a show piloting on BBC Two or BBC Three
fof(neg_conclusion, conjecture, ? [X] : (member_of_pappys(X) & ? [S] : (starred_in(X,S) & (piloted_on(S, bbc_two) | piloted_on(S, bbc_three))))).