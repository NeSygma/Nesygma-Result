fof(p1, axiom, ! [X] : (digital_media(X) => ~analog(X))).
fof(p2, axiom, ! [X] : (printed_text(X) => analog(X))).
fof(p3, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(p4, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(p5, axiom, (streaming_service(nineteen_eighty_four) => hardcover_book(nineteen_eighty_four))).
fof(goal, conjecture, ~printed_text(nineteen_eighty_four)).