fof(podcast_not_novel, axiom, ! [X] : (is_podcast(X) => ~is_novel(X))).
fof(born_in_american_city_implies_american, axiom,
    ! [P, C] : (born_in(P, C) & american_city(C) => is_american(P))).
fof(novel_and_written_by_implies_writer, axiom,
    ! [B, P] : (is_novel(B) & written_by(B, P) => is_novel_writer(P))).
fof(dani_shapiro_american_writer, axiom,
    is_american(dani_shapiro) & is_novel_writer(dani_shapiro)).
fof(family_history_written_by_dani, axiom,
    written_by(family_history, dani_shapiro)).
fof(family_history_is_novel, axiom,
    is_novel(family_history)).
fof(family_history_written_in_2003, axiom,
    written_in(family_history, 2003)).
fof(dani_shapiro_created_family_secrets, axiom,
    created(dani_shapiro, family_secrets)).
fof(boston_is_american_city, axiom,
    american_city(boston)).
fof(distinct_entities, axiom,
    dani_shapiro != family_history &
    dani_shapiro != family_secrets &
    dani_shapiro != boston &
    family_history != family_secrets &
    family_history != boston &
    family_secrets != boston).
fof(conclusion_negation, conjecture,
    ~is_novel_writer(dani_shapiro)).