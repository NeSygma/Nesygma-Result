% Positive file: original claim as conjecture
fof(premise_1, axiom, politician(heinrich_schmidt)).
fof(premise_2, axiom, member_of_nazi_reichstag(heinrich_schmidt)).
fof(goal, conjecture, ! [X] : (politician(X) => ~member_of_nazi_reichstag(X))).