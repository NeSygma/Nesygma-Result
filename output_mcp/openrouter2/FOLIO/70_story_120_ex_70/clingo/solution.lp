% Facts
show(badults).
member_of_pappys(pappy1).
star(badults, P) :- member_of_pappys(P).
pilot(badults, "BBC Three", july2013).
working_title(badults, "The Secret Dude Society").
script_editor(badults, "Andrew Collins").

% Counterexample existence
exists_counterexample :- member_of_pappys(P), star(S, P), pilot(S, "BBC Two", _).
exists_counterexample :- member_of_pappys(P), star(S, P), pilot(S, "BBC Three", _).

% Conclusion
conclusion_false :- exists_counterexample.
conclusion_true :- not exists_counterexample.

% Answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

#show answer/1.