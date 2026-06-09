#####################################################
#  LeoBBS X REST API - Search Handler
#  GET api.cgi?endpoint=search&q=KEYWORD&forum=N  - Search topics
#####################################################

my $search_query = $query->param('q') || '';
my $search_forum = $query->param('forum') || '';
my $page = int($query->param('page') || 1);
my $per_page = int($query->param('per_page') || 20);

if ($search_query eq '') {
    json_error(400, "Missing search query parameter 'q'");
}

$per_page = 50 if ($per_page > 50);
$per_page = 5 if ($per_page < 5);

# Sanitize search query
$search_query =~ s/[\a\b\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\.\/\<\>\?]//isg;

# Read all forums list to get forum IDs
my $allforums_file = "${main::lbdir}data/allforums.cgi";
unless (-e $allforums_file) {
    json_error(500, "Forum data not found");
}

open(my $fh, '<', $allforums_file) or json_error(500, "Cannot read forums data");
my @forums_data = <$fh>;
close($fh);

my @forum_ids;
if ($search_forum ne '' && $search_forum =~ /^[0-9]+$/) {
    @forum_ids = ($search_forum);
} else {
    foreach my $line (@forums_data) {
        chomp $line;
        my ($fid) = split(/\t/, $line);
        push @forum_ids, $fid if ($fid =~ /^[0-9]+$/);
    }
}

# Search through topic lists
my @results;
my $max_results = 200; # limit total scan

foreach my $fid (@forum_ids) {
    last if (scalar(@results) >= $max_results);
    
    my $listno_file = "${main::lbdir}boarddata/listno${fid}.cgi";
    next unless (-e $listno_file);
    
    open(my $lfh, '<', $listno_file) or next;
    while (my $line = <$lfh>) {
        last if (scalar(@results) >= $max_results);
        chomp $line;
        $line =~ s/\r//g;
        next if ($line eq '');
        
        my ($topicid, $forumid, $topictitle, $topicdescription, $threadstate,
            $threadposts, $threadviews, $startedby, $startedpostdate,
            $lastposter, $lastpostdate) = split(/\t/, $line);
        
        next unless ($topicid && $topicid =~ /^[0-9]+$/);
        
        # Match against title, description, or author
        my $match = 0;
        $match = 1 if ($topictitle =~ /\Q$search_query\E/i);
        $match = 1 if ($topicdescription =~ /\Q$search_query\E/i);
        $match = 1 if ($startedby =~ /\Q$search_query\E/i);
        
        if ($match) {
            $topictitle =~ s/^����������//;
            
            my $item = "{";
            $item .= "\"id\":$topicid,";
            $item .= "\"forum_id\":$forumid,";
            $item .= "\"title\":" . json_str($topictitle) . ",";
            $item .= "\"description\":" . json_str($topicdescription) . ",";
            $item .= "\"replies\":" . (int($threadposts || 0)) . ",";
            $item .= "\"views\":" . (int($threadviews || 0)) . ",";
            $item .= "\"author\":" . json_str($startedby) . ",";
            $item .= "\"created_at\":" . json_str($startedpostdate) . ",";
            $item .= "\"last_poster\":" . json_str($lastposter) . ",";
            $item .= "\"last_post_at\":" . json_str($lastpostdate);
            $item .= "}";
            
            push @results, $item;
        }
    }
    close($lfh);
}

# Paginate results
my $total = scalar(@results);
my $total_pages = int(($total + $per_page - 1) / $per_page);
$page = $total_pages if ($page > $total_pages && $total_pages > 0);

my $start = ($page - 1) * $per_page;
my $end = $start + $per_page - 1;
$end = $total - 1 if ($end >= $total);

my @page_results;
for (my $i = $start; $i <= $end && $i < $total; $i++) {
    push @page_results, $results[$i];
}

my $result_json = "{";
$result_json .= "\"query\":" . json_str($search_query) . ",";
$result_json .= "\"results\":[" . join(",", @page_results) . "],";
$result_json .= "\"pagination\":{";
$result_json .= "\"page\":$page,";
$result_json .= "\"per_page\":$per_page,";
$result_json .= "\"total\":$total,";
$result_json .= "\"total_pages\":$total_pages";
$result_json .= "}}";

json_success($result_json);

1;
