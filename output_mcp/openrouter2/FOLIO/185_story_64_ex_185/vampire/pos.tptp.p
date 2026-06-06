fof(distinct, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & family_history != family_secrets & family_history != boston & family_secrets != boston)).
fof(rule_podcast_not_novel, axiom, ! [X] : (is_podcast(X) => ~is_novel(X))).
fof(rule_born_american, axiom, ! [P,C] : ((born_in(P,C) & is_american_city(C)) => is_american(P))).
fof(rule_novel_writer, axiom, ! [B,P] : ((is_book(B) & is_novel(B) & is_written_by(B,P)) => is_novel_writer(P))).
fof(fact_person, axiom, is_person(dani_shapiro)).
fof(fact_american, axiom, is_american(dani_shapiro)).
fof(fact_writer, axiom, is_writer(dani_shapiro)).
fof(fact_written_by, axiom, is_written_by(family_history, dani_shapiro)).
fof(fact_novel, axiom, is_novel(family_history)).
fof(fact_book, axiom, is_book(family_history)).
fof(fact_podcast, axiom, is_podcast(family_secrets)).
fof(fact_written_by_podcast, axiom, is_written_by(family_secrets, dani_shapiro)).
fof(fact_american_city, axiom, is_american_city(boston)).
fof(conjecture, conjecture, is_novel_writer(dani_shapiro)).