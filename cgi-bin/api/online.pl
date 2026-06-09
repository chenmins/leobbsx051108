#####################################################
#  LeoBBS X REST API - Online Users Handler
#  GET api.cgi?endpoint=online  - Get online users
#####################################################

my $online_file = "${main::lbdir}data/onlinedata.cgi";

my @online_users;
my $total_guests = 0;
my $total_members = 0;

if (-e $online_file) {
    open(my $fh, '<', $online_file) or json_error(500, "Cannot read online data");
    while (my $line = <$fh>) {
        chomp $line;
        $line =~ s/\r//g;
        next if ($line eq '');
        
        # Online data format: username\tforumname\ttype\tdescription\ttimestamp\tip
        my ($user, $location, $type, $desc, $timestamp, $ip) = split(/\t/, $line);
        next unless $user;
        
        if ($user eq '' || $user =~ /^(����|guest)/i) {
            $total_guests++;
        } else {
            $total_members++;
            my $user_json = "{";
            $user_json .= "\"name\":" . json_str($user) . ",";
            $user_json .= "\"location\":" . json_str($location) . ",";
            $user_json .= "\"activity\":" . json_str($desc);
            $user_json .= "}";
            push @online_users, $user_json;
        }
    }
    close($fh);
}

my $total = $total_guests + $total_members;

my $result = "{";
$result .= "\"total\":$total,";
$result .= "\"members\":$total_members,";
$result .= "\"guests\":$total_guests,";
$result .= "\"users\":[" . join(",", @online_users) . "]";
$result .= "}";

json_success($result);

1;
