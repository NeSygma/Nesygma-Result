tff(premise_piloted, axiom, piloted_on(badu, bbc_three)).
tff(premise_member, axiom, member_of_pappy(p1)).
tff(premise_starred, axiom, starred_in(p1, badu)).
tff(premise_rule, axiom, ! [X] : (starred_in(X, badu) & piloted_on(badu, bbc_three) => starred_in_show_piloting_on(X, bbc_three))).
tff(neg_conclusion, conjecture, ? [X] : (member_of_pappy(X) & (starred_in_show_piloting_on(X, bbc_two) | starred_in_show_piloting_on(X, bbc_three)))).