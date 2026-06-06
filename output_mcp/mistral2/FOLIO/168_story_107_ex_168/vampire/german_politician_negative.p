fof(heinrich_is_german_politician, axiom, german_politician(heinrich_schmidt)).
fof(heinrich_in_prussian_parliament, axiom, member_of_prussian_parliament(heinrich_schmidt)).
fof(heinrich_in_nazi_reichstag, axiom, member_of_nazi_reichstag(heinrich_schmidt)).
fof(conclusion_negation, conjecture, ~(? [X] : (german_politician(X) & member_of_prussian_parliament(X) & member_of_nazi_reichstag(X)))).