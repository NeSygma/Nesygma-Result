fof(ranked_highly_implies_active, axiom, 
    ! [X] : (ranked_highly_by_wta(X) => most_active_major_tennis_player(X))).

fof(lost_to_iga_implies_ranked_highly, axiom, 
    ! [X] : (lost_to_iga_swiatek_at_roland_garros_2022(X) => ranked_highly_by_wta(X))).

fof(female_implies_lost_to_iga, axiom, 
    ! [X] : (female_tennis_player_at_roland_garros_2022(X) => lost_to_iga_swiatek_at_roland_garros_2022(X))).

fof(all_players_are_female_or_male, axiom, 
    ! [X] : (at_roland_garros_2022(X) => 
             (female_tennis_player_at_roland_garros_2022(X) | male_tennis_player_at_roland_garros_2022(X)))).

fof(male_implies_lost_to_rafael, axiom, 
    ! [X] : (male_tennis_player_at_roland_garros_2022(X) => lost_to_rafael_nadal_at_roland_garros_2022(X))).

fof(ranked_or_lost_implies_not_male, axiom, 
    (ranked_highly_by_wta(coco_gauff) | lost_to_rafael_nadal_at_roland_garros_2022(coco_gauff)) 
    => ~male_tennis_player_at_roland_garros_2022(coco_gauff)).

fof(coco_at_roland_garros, axiom, 
    at_roland_garros_2022(coco_gauff)).

fof(conclusion, conjecture, 
    most_active_major_tennis_player(coco_gauff)).