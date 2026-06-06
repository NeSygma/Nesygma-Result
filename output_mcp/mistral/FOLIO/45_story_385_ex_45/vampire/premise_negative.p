fof(ranked_implies_active, axiom, 
    ! [X] : (ranked_highly_by_wta(X) => most_active_player(X))).

fof(lost_to_iga_implies_ranked, axiom, 
    ! [X] : (lost_to(X, iga_swiatek, roland_garros_2022) => ranked_highly_by_wta(X))).

fof(female_implies_lost_to_iga, axiom, 
    ! [X] : (female_tennis_player(X, roland_garros_2022) => lost_to(X, iga_swiatek, roland_garros_2022))).

fof(players_are_female_or_male, axiom, 
    ! [X] : (tennis_player(X, roland_garros_2022) => 
             (female_tennis_player(X, roland_garros_2022) | male_tennis_player(X, roland_garros_2022)))).

fof(male_implies_lost_to_rafael, axiom, 
    ! [X] : (male_tennis_player(X, roland_garros_2022) => lost_to(X, rafael_nadal, roland_garros_2022))).

fof(ranked_or_lost_implies_not_male, axiom, 
    (ranked_highly_by_wta(coco_gauff) | lost_to(coco_gauff, rafael_nadal, roland_garros_2022)) => 
    ~male_tennis_player(coco_gauff, roland_garros_2022)).

fof(coco_at_roland_garros, axiom, 
    tennis_player(coco_gauff, roland_garros_2022)).

fof(conclusion_negation, conjecture, 
    lost_to(coco_gauff, iga_swiatek, roland_garros_2022) & most_active_player(coco_gauff)).