% Negative test: negation of the conclusion
fof(p1, axiom, politician(heinrich_schmidt)).
fof(p2, axiom, member_nazi_reichstag(heinrich_schmidt)).
fof(p3, axiom, member_prussian_state_parliament(heinrich_schmidt)).
fof(conj_neg, conjecture, ? [X] : (politician(X) & member_nazi_reichstag(X))).