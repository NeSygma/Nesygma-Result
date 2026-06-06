fof(politician_hs, axiom, politician(heinnrich_schmidt)).
fof(member_prussian_hs, axiom, member_of_prussian_state_parliament(heinnrich_schmidt)).
fof(member_nazi_hs, axiom, member_of_nazi_reichstag(heinnrich_schmidt)).
fof(conjecture, conjecture, ! [X] : (politician(X) => ~member_of_nazi_reichstag(X))).