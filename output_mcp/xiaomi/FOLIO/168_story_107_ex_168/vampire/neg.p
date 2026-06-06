fof(heinrich_german_politician, axiom, german_politician(heinrich_schmidt)).
fof(heinrich_prussian, axiom, member_of(heinrich_schmidt, prussian_state_parliament)).
fof(heinrich_nazi, axiom, member_of(heinrich_schmidt, nazi_reichstag)).
fof(goal_negation, conjecture, ~? [X] : (german_politician(X) & member_of(X, prussian_state_parliament) & member_of(X, nazi_reichstag))).