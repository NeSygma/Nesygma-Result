fof(nvp_rule, axiom, ! [B] : (published_by(B, nvp) => in_english(B))).
fof(nc_published, axiom, published_by(nc, nvp)).
fof(pf_published, axiom, published_by(pf, nvp)).
fof(distinct_books, axiom, nc != pf).
fof(goal, conjecture, ~in_english(nc)).