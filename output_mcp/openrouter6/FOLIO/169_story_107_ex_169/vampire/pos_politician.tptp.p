fof(premise1, axiom, politician(heinrich_schmidt)).
fof(premise2, axiom, member_of_nazi_reichstag(heinrich_schmidt)).
fof(conclusion, conjecture, ! [X] : (politician(X) => ~member_of_nazi_reichstag(X))).