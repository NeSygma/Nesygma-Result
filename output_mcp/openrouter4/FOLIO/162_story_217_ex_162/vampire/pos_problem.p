fof(premise1, axiom, (likes_music => wants_compose)).
fof(premise2, axiom, (has_access => can_compose)).
fof(premise3, axiom, ((can_compose & wants_compose) => will_compose)).
fof(conclusion, conjecture, (~will_compose => ~can_compose)).