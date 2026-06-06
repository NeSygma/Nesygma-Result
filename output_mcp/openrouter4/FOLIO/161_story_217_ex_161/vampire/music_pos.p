fof(premise1, axiom, (likes_music => wants_to_compose)).
fof(premise2, axiom, (has_access => can_compose)).
fof(premise3, axiom, ((can_compose & wants_to_compose) => will_compose)).
fof(conclusion, conjecture, ((likes_music & has_access) => will_compose)).