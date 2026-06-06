fof(no_digital_analog, axiom, ! [X] : (digital_media(X) => ~analog(X))).
fof(printed_is_analog, axiom, ! [X] : (printed_text(X) => analog(X))).
fof(streaming_is_digital, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(hardcover_is_printed, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(nineteen_eighty_four_rule, axiom, (streaming_service(nineteen_eighty_four) => hardcover_book(nineteen_eighty_four))).
fof(goal, conjecture, streaming_service(nineteen_eighty_four)).