fof(heinrich_politician, axiom, politician(heinrich_schmidt)).
fof(heinrich_prussian, axiom, member_prussian_parliament(heinrich_schmidt)).
fof(heinrich_reichstag, axiom, member_nazi_reichstag(heinrich_schmidt)).
fof(goal, conjecture, ! [X] : (politician(X) => ~member_nazi_reichstag(X))).