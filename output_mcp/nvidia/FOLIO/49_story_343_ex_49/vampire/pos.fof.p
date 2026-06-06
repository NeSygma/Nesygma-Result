fof(axiom1, axiom, ! [X] : (digital_media(X) => ~analog(X))).
fof(axiom2, axiom, ! [X] : (printed_text(X) => analog(X))).
fof(axiom3, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(axiom4, axiom, ! [X] : (hardcover(X) => printed_text(X))).
fof(axiom5, axiom, streaming_service(c1984) => hardcover(c1984)).
fof(conjecture, conjecture, printed_text(c1984)).