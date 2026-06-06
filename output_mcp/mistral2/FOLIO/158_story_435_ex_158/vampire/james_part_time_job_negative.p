fof(premise1, axiom,
    ! [S] : (works_in_library(S) => ~from_department(S, computer_science))).

fof(premise2, axiom,
    ! [S] : (has_part_time_job(S) => works_in_library(S))).

fof(premise3, axiom,
    ! [S] : (taking_database_course(S) => from_department(S, computer_science))).

fof(premise4, axiom,
    ! [S] : (taking_class_with_professor_david(S) => taking_database_course(S))).

fof(premise5, axiom,
    ! [S] : (works_in_lab(S) => taking_class_with_professor_david(S))).

fof(premise6, axiom,
    works_in_lab(james)).

fof(premise7, axiom,
    ~has_part_time_job(james)).

fof(conclusion_negation, conjecture,
    has_part_time_job(james)).