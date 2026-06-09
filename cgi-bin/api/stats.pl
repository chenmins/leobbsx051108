#####################################################
#  LeoBBS X REST API - Stats Handler
#  GET api.cgi?endpoint=stats  - Get board statistics
#####################################################

# Read board stats
my $stats_file = "${main::lbdir}data/boardstats.cgi";
my ($total_members, $total_posts, $total_topics, $latest_member) = (0, 0, 0, '');

if (-e $stats_file) {
    eval { require $stats_file; };
    # boardstats.cgi typically defines $totalmembers, $totalposts, $totalthreads, $latestmember
    $total_members = $main::totalmembers || 0;
    $total_posts = $main::totalposts || 0;
    $total_topics = $main::totalthreads || 0;
    $latest_member = $main::latestmember || '';
}

# Count forums
my $total_forums = 0;
my $allforums_file = "${main::lbdir}data/allforums.cgi";
if (-e $allforums_file) {
    open(my $fh, '<', $allforums_file) or json_error(500, "Cannot read forums");
    while (<$fh>) { $total_forums++ if length($_) > 30; }
    close($fh);
}

my $result = "{";
$result .= "\"board_name\":" . json_str($main::boardname) . ",";
$result .= "\"board_description\":" . json_str($main::boarddescription) . ",";
$result .= "\"board_url\":" . json_str($main::boardurl) . ",";
$result .= "\"total_members\":$total_members,";
$result .= "\"total_posts\":$total_posts,";
$result .= "\"total_topics\":$total_topics,";
$result .= "\"total_forums\":$total_forums,";
$result .= "\"latest_member\":" . json_str($latest_member) . ",";
$result .= "\"version\":" . json_str("LeoBBS X Build051108");
$result .= "}";

json_success($result);

1;
