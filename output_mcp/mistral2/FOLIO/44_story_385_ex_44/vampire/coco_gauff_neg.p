fof(axiom1, axiom,
    ! [X] : (lost_to_iga_rg2022(X) => is_highly_ranked_wta(X))).

fof(axiom2, axiom,
    ! [X] : (is_female_player_at_rg2022(X) => lost_to_iga_rg2022(X))).

fof(axiom3, axiom,
    ! [X] : (is_player_at_rg2022(X) =>
             (is_female_player_at_rg2022(X) | is_male_player_at_rg2022(X)))).

fof(axiom4, axiom,
    ! [X] : (is_male_player_at_rg2022(X) => lost_to_rafael_rg2022(X))).

fof(axiom5, axiom,
    (is_highly_ranked_wta(coco_gauff) | lost_to_rafael_rg2022(coco_gauff)) =>
    ~is_male_player_at_rg2022(coco_gauff)).

fof(axiom6, axiom,
    is_player_at_rg2022(coco_gauff)).

fof(goal_negation, conjecture,
    ~lost_to_rafael_rg2022(coco_gauff)).