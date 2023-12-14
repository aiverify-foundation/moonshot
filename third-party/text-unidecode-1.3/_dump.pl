#!/usr/bin/env perl
use Text::Unidecode;
use Encode;

for ($c=1; $c<65535; $c++){ # limit ourselves to narrow python builds
    $trans = unidecode(chr($c));
    print encode("utf8", "$trans\x00");
}

# usage: perl _dump.pl > src/text_unidecode/data.bin
