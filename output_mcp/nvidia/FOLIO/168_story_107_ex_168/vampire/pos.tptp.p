fof(premise1, axiom, german(heinrich_schmidt)).
fof(premise2, axiom, politician(heinrich_schmidt)).
fof(premise3, axiom, member_of(heinrich_schmidt, prussian)).
fof(premise4, axiom, member_of(heinrich_schmidt, nazi)).
fof(conjecture, conjecture, ? [X] : (german(X) & politician(X) & member_of(X, prussian) & member_of(X, nazi))).