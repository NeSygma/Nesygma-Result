fof(premise1, axiom, ! [X] : (digital(X) => ~analog(X))).
fof(premise2, axiom, ! [X] : (printed_text(X) => analog(X))).
fof(premise3, axiom, ! [X] : (streaming(X) => digital(X))).
fof(premise4, axiom, ! [X] : (hardcover(X) => printed_text(X))).
fof(premise5, axiom, (streaming(book_1984) => hardcover(book_1984))).
fof(goal, conjecture, ~streaming(book_1984)).