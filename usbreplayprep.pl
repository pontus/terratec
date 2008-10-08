#!/usr/bin/perl
# 
# usbreplayprep.pl
# This perl script reads an usbsnoop log file from STDIN and extracts
# commands and output data buffers, and prints them out like this:
# 
# w1 39
#     00000000: 01 00 00 00 00 00 00 4c 00 00 00 00 00 00 4d 00
#     00000010: 00 00 00 00 00 4e 00 00 00 00 00 00 4f 00 00 00
#     00000020: 00 00 00 50 00 00 00 00 00 00 51 00 00 00 00 00
#     00000030: 00 52 00 00 00 00 00 00 53
# 
# r81 40
# 
# The "w1 39" section means write a buffer of size 0x39 to Endpoint 1,
# and "r81 40" means read 0x40 bytes from Endpoint 0x81.
#
# I have only tried this program with logs from usbsnoop-1.8 and
# Windows XP. It probably needs adjustments for other cases.

my ($line,$urb);

sub print_bufstuff {
    my $text = shift;
    if ($text =~ m/TransferBufferMDL.*\n((    [0-9a-f]{8}:( [0-9a-f]{2})+\n)+)  UrbLink/) {
        print $1;
    }
}

sub process_urb {
    my $text = shift;
    if (defined($text)) {
        if ($text =~ m/URB (\d+) (going down|coming back)/) {
            my $urbno = $1;
            my $dirtext = $2;
            if ($text =~ m/PipeHandle.*endpoint 0x([0-9a-f]+)/) {
                my $endpoint = hex($1);
                if ($text =~ m/TransferBufferLength\s+=\s+([0-9a-f]+)/) {
                    my $bufsize = hex($1);
                    if ($dirtext eq 'going down') {
                        if ($text =~ m/TransferFlags.*_TRANSFER_DIRECTION_IN/) {
                            printf "r%x %x\n", $endpoint, $bufsize;
                        } elsif ($text =~ m/TransferFlags.*_TRANSFER_DIRECTION_OUT/) {
                            printf "w%x %x\n", $endpoint, $bufsize;
                            &print_bufstuff($text);
                        }
                    }
                }
            }
        }
    }
}

while (defined($line = <STDIN>)) {
    if ($line =~ m/ URB (\d+) (going down|coming back)/) {
        &process_urb($urb);
        $urb = $line;
    } elsif (defined($urb)) {
        $urb .= $line;
    }
}

&process_urb($urb);
