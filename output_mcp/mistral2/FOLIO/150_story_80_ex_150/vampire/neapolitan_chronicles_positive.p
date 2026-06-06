fof(publisher_specialization, axiom,
    ! [B] : (publishes(new_vessel_press, B) => is_in_english(B))).

fof(neapolitan_published, axiom,
    publishes(new_vessel_press, neapolitan_chronicles)).

fof(neapolitan_translated, axiom,
    translated_from(neapolitan_chronicles, italian)).

fof(palace_published, axiom,
    publishes(new_vessel_press, palace_of_flies)).

fof(distinct_entities, axiom,
    (new_vessel_press != neapolitan_chronicles &
     new_vessel_press != palace_of_flies &
     neapolitan_chronicles != palace_of_flies &
     neapolitan_chronicles != italian &
     palace_of_flies != italian &
     new_vessel_press != italian)).

fof(conclusion, conjecture,
    is_in_english(neapolitan_chronicles)).