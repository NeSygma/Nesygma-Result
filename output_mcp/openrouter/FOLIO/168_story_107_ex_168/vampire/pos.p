% Positive version
fof(premise1, axiom, german_politician(heinrich_schmidt)).
fof(premise2, axiom, member_prussian_parliament(heinrich_schmidt)).
fof(premise3, axiom, member_nazi_reichstag(heinrich_schmidt)).
fof(goal, conjecture, ? [X] : (german_politician(X) & member_prussian_parliament(X) & member_nazi_reichstag(X))).