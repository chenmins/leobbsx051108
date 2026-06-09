#####################################################
#  LeoBBS X REST API - Topics Handler
#  GET api.cgi?endpoint=topics&forum=N          - List topics in forum
#  GET api.cgi?endpoint=topics&forum=N&page=1   - Paginated list
#####################################################

my $forum_id = $query->param('forum') || '';
my $page = int($query->param('page') || 1);
my $per_page = int($query->param('per_page') || 20);

if ($forum_id eq '' || $forum_id !~ /^[0-9]+$/) {
    json_error(400, "Missing or invalid forum parameter");
}

$per_page = 50 if ($per_page > 50);
$per_page = 5 if ($per_page < 5);
$page = 1 if ($page < 1);

my $listno_file = "${main::lbdir}boarddata/listno${forum_id}.cgi";
unless (-e $listno_file) {
    json_error(404, "Forum not found or has no topics");
}

# Read topic list
open(my $fh, '<', $listno_file) or json_error(500, "Cannot read topic list");
my @all_topics = <$fh>;
close($fh);

my $total_topics = scalar(@all_topics);
my $total_pages = int(($total_topics + $per_page - 1) / $per_page);
$page = $total_pages if ($page > $total_pages && $total_pages > 0);

my $start = ($page - 1) * $per_page;
my $end = $start + $per_page - 1;
$end = $total_topics - 1 if ($end >= $total_topics);

my @topic_list;

for (my $i = $start; $i <= $end; $i++) {
    my $topic = $all_topics[$i];
    next unless $topic;
    chomp $topic;
    $topic =~ s/\r//g;
    next if ($topic eq '');
    
    my ($topicid, $forumid, $topictitle, $topicdescription, $threadstate, 
        $threadposts, $threadviews, $startedby, $startedpostdate, 
        $lastposter, $lastpostdate, $posticon, $posttemp, $addmetype) = split(/\t/, $topic);
    
    next unless ($topicid && $topicid =~ /^[0-9]+$/);
    
    # Clean title
    $topictitle =~ s/^[^>]*>// if $topictitle; # remove prefix like "无标题主题"
    $topictitle =~ s/^\x{65E0}\x{6807}\x{9898}\x{4E3B}\x{9898}//; # remove utf8 prefix
    $topictitle =~ s/^����������//; # remove GB prefix
    
    # Thread state interpretation
    my $is_locked = ($threadstate =~ /lock/i) ? 'true' : 'false';
    my $is_sticky = 'false'; # determined elsewhere via ontop data
    
    my $topic_json = "{";
    $topic_json .= "\"id\":$topicid,";
    $topic_json .= "\"forum_id\":$forumid,";
    $topic_json .= "\"title\":" . json_str($topictitle) . ",";
    $topic_json .= "\"description\":" . json_str($topicdescription) . ",";
    $topic_json .= "\"state\":" . json_str($threadstate) . ",";
    $topic_json .= "\"locked\":$is_locked,";
    $topic_json .= "\"replies\":" . (int($threadposts || 0)) . ",";
    $topic_json .= "\"views\":" . (int($threadviews || 0)) . ",";
    $topic_json .= "\"author\":" . json_str($startedby) . ",";
    $topic_json .= "\"created_at\":" . json_str($startedpostdate) . ",";
    $topic_json .= "\"last_poster\":" . json_str($lastposter) . ",";
    $topic_json .= "\"last_post_at\":" . json_str($lastpostdate);
    $topic_json .= "}";
    
    push @topic_list, $topic_json;
}

my $result = "{";
$result .= "\"forum_id\":$forum_id,";
$result .= "\"topics\":[" . join(",", @topic_list) . "],";
$result .= "\"pagination\":{";
$result .= "\"page\":$page,";
$result .= "\"per_page\":$per_page,";
$result .= "\"total\":$total_topics,";
$result .= "\"total_pages\":$total_pages";
$result .= "}}";

json_success($result);

1;
