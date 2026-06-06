fof(distinct, axiom, (
    dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston &
    dani_shapiro != year_2003 &
    family_history != family_secrets & family_history != boston & family_history != year_2003 &
    family_secrets != boston & family_secrets != year_2003 &
    boston != year_2003
)).
fof(premise1, axiom, ! [X] : (is_a_podcast(X) => ~is_a_novel(X))).
fof(premise2, axiom, ! [P, C] : ((born_in(P, C) & is_an_american_city(C)) => is_american(P))).
fof(premise3, axiom, ! [B, P] : ((is_a_novel(B) & written_by(B, P)) => is_novel_writer(P))).
fof(premise4, axiom, is_an_american_writer(dani_shapiro)).
fof(premise5, axiom, written_by(family_history, dani_shapiro)).
fof(premise6, axiom, (is_a_novel(family_history) & written_in(family_history, year_2003))).
fof(premise7, axiom, (created(dani_shapiro, family_secrets) & is_a_podcast(family_secrets))).
fof(premise8, axiom, is_an_american_city(boston)).
fof(conclusion, conjecture, ~is_a_novel(family_secrets)).