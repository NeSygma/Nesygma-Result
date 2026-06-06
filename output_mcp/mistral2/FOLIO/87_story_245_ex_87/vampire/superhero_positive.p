fof(superhero_movie_def, axiom, superhero_movie(surprising_adventures_of_sir_digby_chicken_caesar)).

fof(good_guys_win, axiom,
    ! [M, C] :
      (superhero_movie(M) &
       in_movie(C, M) &
       good_guy(C)
       => wins(C))).

fof(good_vs_bad_fight, axiom,
    ! [C1, C2] :
      ((good_guy(C1) & bad_guy(C2)) => fights(C1, C2))).

fof(bad_vs_good_fight, axiom,
    ! [C1, C2] :
      ((bad_guy(C1) & good_guy(C2)) => fights(C1, C2))).

fof(sir_digby_fights_nemesis, axiom,
    ? [N] : (nemesis(sir_digby, N) & fights(sir_digby, N))).

fof(named_after_good_guy, axiom,
    ! [M, C] :
      (superhero_movie(M) &
       named_after(M, C)
       => good_guy(C))).

fof(movie_named_after_sir_digby, axiom,
    named_after(surprising_adventures_of_sir_digby_chicken_caesar, sir_digby)).

fof(named_after_in_movie, axiom,
    ! [M, C] :
      (superhero_movie(M) &
       named_after(M, C)
       => in_movie(C, M))).

fof(winner_loser, axiom,
    ! [C1, C2] :
      (fights(C1, C2) &
       wins(C1)
       => ~wins(C2))).

fof(goal, conjecture,
    ? [N] : (nemesis(sir_digby, N) & ~wins(N))).