fof(heinrich_politician, axiom, politician(heinrich_schmidt)).
fof(heinrich_reichstag, axiom, member_of_nazi_reichstag(heinrich_schmidt)).
fof(conclusion, conjecture, ! [X] : (politician(X) => ~member_of_nazi_reichstag(X))).