fof(premise_1, axiom, ! [M, C] : (superhero_movie(M) & good_guy(C, M) => wins(C, M))).
fof(premise_2, axiom, superhero_movie(surprising_adventures)).
fof(premise_3a, axiom, ! [C1, C2, M] : (good_guy(C1, M) & ~good_guy(C2, M) => fights(C1, C2, M))).
fof(premise_3b, axiom, ! [C1, C2, M] : (~good_guy(C1, M) & good_guy(C2, M) => fights(C1, C2, M))).
fof(premise_4, axiom, fights(sir_digby, nemesis_of_digby, surprising_adventures)).
fof(premise_5, axiom, ! [M, C] : (superhero_movie(M) & named_after(M, C) => good_guy(C, M))).
fof(premise_6, axiom, named_after(surprising_adventures, sir_digby)).
fof(premise_7, axiom, ! [C1, C2, M] : (wins(C1, M) & fights(C1, C2, M) => ~wins(C2, M))).
fof(premise_8, axiom, ! [M, C] : (superhero_movie(M) & named_after(M, C) => in_movie(C, M))).
fof(distinct_chars, axiom, sir_digby != nemesis_of_digby).
fof(conclusion_negation, conjecture, wins(nemesis_of_digby, surprising_adventures)).