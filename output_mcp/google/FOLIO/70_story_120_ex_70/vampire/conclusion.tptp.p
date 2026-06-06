fof(premise_1, axiom, ? [X] : (is_member_of_pappys(X) & starred_in(X, badults))).
fof(premise_2, axiom, piloted_on(badults, bbc_three)).
fof(distinct_channels, axiom, bbc_two != bbc_three).
fof(conclusion, conjecture, ! [X, S, C] : ((is_member_of_pappys(X) & starred_in(X, S) & piloted_on(S, C)) => ~(C = bbc_two | C = bbc_three))).