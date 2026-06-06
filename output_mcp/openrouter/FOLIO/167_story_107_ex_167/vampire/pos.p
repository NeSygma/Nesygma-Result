% Positive test: conclusion should follow
fof(premise1, axiom, german(heinrich_schmidt)).
fof(premise2, axiom, politician(heinrich_schmidt)).
fof(premise3, axiom, member_of(heinrich_schmidt, prussian_state_parliament)).
fof(premise4, axiom, member_of(heinrich_schmidt, nazi_reichstag)).
fof(goal, conjecture, (german(heinrich_schmidt) | russian(heinrich_schmidt))).