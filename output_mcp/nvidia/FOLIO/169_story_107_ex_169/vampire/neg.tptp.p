fof(prem1, axiom, german(heinrich_schmidt)).
fof(prem2, axiom, politician(heinrich_schmidt)).
fof(prem3, axiom, member_of(heinrich_schmidt, prussian_state_parliament)).
fof(prem4, axiom, member_of(heinrich_schmidt, nazi_reichstag)).
fof(conclusion, conjecture, ? [X] : (politician(X) & member_of(X, nazi_reichstag))).