#!/usr/bin/perl -w

my %locs = ();
my $gettingLocs = 0;
my @out = ();

foreach my $line (<>) {
    $line =~ s/^\s+|\s+$//g;
    if ($line =~ /^#define/) {
        my @parts = split / +/, $line;
        if ($parts[1] =~ /ADRIATIC/) {
            $gettingLocs = 1;
        }
        if ($gettingLocs) {
            $locs{$parts[1]} = $parts[2];
        }
        if ($parts[1] =~ /ZURICH/) {
            $gettingLocs = 0;
        }
    } elsif ($line =~ /^addLink/) {
        $line =~ s/^addLink\(|\);$//g;
        my @parts = split /, /, $line;
        foreach my $loc (keys %locs) {
            $parts[1] =~ s/$loc/$locs{$loc}/g;
            $parts[2] =~ s/$loc/$locs{$loc}/g;
        }
        $parts[3] =~ s/ROAD/1/g;
        $parts[3] =~ s/RAIL/2/g;
        $parts[3] =~ s/BOAT/3/g;
        push @out, "addlink(game, $parts[1], $parts[2], $parts[3])\n";
    }
}

foreach (sort @out) {
    print;
}