fof(club_member, axiom, cm(bonnie)).
fof(premise_1, axiom, ! [X] : (cm(X) & po(X) => ae(X))).
fof(premise_2, axiom, ! [X] : (cm(X) => (po(X) | id(X)))).
fof(premise_3, axiom, ! [X] : (cm(X) & cd(X) => ~sa(X))).
fof(premise_4, axiom, ! [X] : (cm(X) & id(X) => cd(X))).
fof(premise_5, axiom, ! [X] : (cm(X) & ycwa(X) => sa(X))).
fof(premise_6, axiom, cm(bonnie) & (ae(bonnie) <=> sa(bonnie))).
fof(conclusion, conjecture, (cd(bonnie) | po(bonnie)) => (ycwa(bonnie) & id(bonnie))).