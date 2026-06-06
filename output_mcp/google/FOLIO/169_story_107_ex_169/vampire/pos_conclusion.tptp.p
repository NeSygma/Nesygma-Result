fof(premise_1, axiom, politician(heinrich_schmidt)).
fof(premise_2, axiom, member_nazi_reichstag(heinrich_schmidt)).
fof(conclusion, conjecture, ! [X] : (politician(X) => ~member_nazi_reichstag(X))).