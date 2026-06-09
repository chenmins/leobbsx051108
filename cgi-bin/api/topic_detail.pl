#####################################################
#  LeoBBS X REST API - Topic Detail Handler
#  GET api.cgi?endpoint=topic&forum=N&id=M        - Get topic with posts
#  GET api.cgi?endpoint=topic&forum=N&id=M&page=1 - Paginated posts
#####################################################

my $forum_id = $query->param('forum') || '';
my $topic_id = $query->param('id') || '';
my $page = int($query->param('page') || 1);
my $per_page = int($query->param('per_page') || 20);

if ($forum_id eq '' || $forum_id !~ /^[0-9]+$/) {
    json_error(400, "Missing or invalid forum parameter");
}
if ($topic_id eq '' || $topic_id !~ /^[0-9]+$/) {
    json_error(400, "Missing or invalid topic id parameter");
}

$per_page = 50 if ($per_page > 50);
$per_page = 5 if ($per_page < 5);
$page = 1 if ($page < 1);

# Topic messages are stored in messages directory
# Path: messages/{forum_id}/{topic_id}.cgi or similar structure
my ($memdir, $msgdir, $usrdir, $saledir) = split(/\|/, main::getdir());

my $topic_file = "${main::lbdir}${msgdir}/${forum_id}/${topic_id}.cgi";
unless (-e $topic_file) {
    json_error(404, "Topic not found");
}

# Read topic file - contains all posts separated by specific delimiter
open(my $fh, '<', $topic_file) or json_error(500, "Cannot read topic");
my $file_content = '';
{
    local $/;
    $file_content = <$fh>;
}
close($fh);

# Posts in LeoBBS are separated by the record separator
# Each post format: poster\tdate\tip\ttitle\tpost_content\tsignature\temail\thomepage\ticq\toicq\ticon\tattachment...
my @raw_posts = split(/\n/, $file_content);

# First line is the topic header/first post
my @posts;
my $post_index = 0;

foreach my $line (@raw_posts) {
    chomp $line;
    $line =~ s/\r//g;
    next if ($line eq '');
    
    my ($poster, $postdate, $ip, $posttitle, $postcontent, $signature, 
        $email, $homepage, $icq, $oicq, $posticon, @rest) = split(/\t/, $line);
    
    next unless ($poster);
    
    # Clean content - basic HTML entities decode
    $postcontent =~ s/\[br\]/\n/ig if $postcontent;
    
    my $post_json = "{";
    $post_json .= "\"index\":$post_index,";
    $post_json .= "\"author\":" . json_str($poster) . ",";
    $post_json .= "\"date\":" . json_str($postdate) . ",";
    $post_json .= "\"title\":" . json_str($posttitle) . ",";
    $post_json .= "\"content\":" . json_str($postcontent) . ",";
    $post_json .= "\"signature\":" . json_str($signature) . ",";
    $post_json .= "\"icon\":" . json_str($posticon);
    $post_json .= "}";
    
    push @posts, $post_json;
    $post_index++;
}

my $total_posts = scalar(@posts);
my $total_pages = int(($total_posts + $per_page - 1) / $per_page);
$page = $total_pages if ($page > $total_pages && $total_pages > 0);

my $start = ($page - 1) * $per_page;
my $end = $start + $per_page - 1;
$end = $total_posts - 1 if ($end >= $total_posts);

my @page_posts;
for (my $i = $start; $i <= $end && $i < $total_posts; $i++) {
    push @page_posts, $posts[$i];
}

my $result = "{";
$result .= "\"forum_id\":$forum_id,";
$result .= "\"topic_id\":$topic_id,";
$result .= "\"posts\":[" . join(",", @page_posts) . "],";
$result .= "\"pagination\":{";
$result .= "\"page\":$page,";
$result .= "\"per_page\":$per_page,";
$result .= "\"total\":$total_posts,";
$result .= "\"total_pages\":$total_pages";
$result .= "}}";

json_success($result);

1;
