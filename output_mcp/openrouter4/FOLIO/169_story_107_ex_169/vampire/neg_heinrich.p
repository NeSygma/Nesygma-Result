% Negative file: negated claim as conjecture
fof(premise_1, axiom, politician(heinrich_schmidt)).
fof(premise_2, axiom, member_of_nazi_reichstag(heinrich_schmidt)).
fof(goal_neg, conjecture, ? [X] : (politician(X) & member_of_nazi_reichstag(X))).