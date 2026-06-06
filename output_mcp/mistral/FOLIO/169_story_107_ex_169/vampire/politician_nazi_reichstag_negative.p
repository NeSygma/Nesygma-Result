fof(heinrich_is_german_politician, axiom, german_politician(heinrich_schmidt)).
fof(heinrich_is_politician, axiom, politician(heinrich_schmidt)).
fof(heinrich_member_prussian, axiom, member_of(heinrich_schmidt, prussian_state_parliament)).
fof(heinrich_member_nazi, axiom, member_of(heinrich_schmidt, nazi_reichstag)).
fof(some_politician_in_nazi_reichstag, conjecture, ? [X] : (politician(X) & member_of(X, nazi_reichstag))).