fof(ranked_highly_implies_active, axiom,
    ! [X] : (ranked_highly_by_wta(X) => most_active_player_in_major_tennis(X))).

fof(lost_to_iga_implies_ranked_highly, axiom,
    ! [X] : (lost_to(X, iga_swiatek) & player_at_rg2022(X) => ranked_highly_by_wta(X))).

fof(all_female_lost_to_iga, axiom,
    ! [X] : (female_player_at_rg2022(X) => lost_to(X, iga_swiatek))).

fof(player_is_female_or_male, axiom,
    ! [X] : (player_at_rg2022(X) <=> (female_player_at_rg2022(X) | male_player_at_rg2022(X)))).

fof(all_male_lost_to_rafael, axiom,
    ! [X] : (male_player_at_rg2022(X) => lost_to(X, rafael_nadal))).

fof(coco_gauff_condition, axiom,
    (ranked_highly_by_wta(coco_gauff) | lost_to(coco_gauff, rafael_nadal)) =>
    ~male_player_at_rg2022(coco_gauff)).

fof(coco_gauff_at_rg2022, axiom,
    player_at_rg2022(coco_gauff)).

fof(negated_conclusion, conjecture,
    lost_to(coco_gauff, iga_swiatek) & most_active_player_in_major_tennis(coco_gauff)).