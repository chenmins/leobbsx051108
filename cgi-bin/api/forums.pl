#####################################################
#  LeoBBS X REST API - Forums Handler
#  GET api.cgi?endpoint=forums          - List all forums
#  GET api.cgi?endpoint=forums&id=N     - Get forum detail
#####################################################

my $forum_id = $query->param('id') || '';

if ($forum_id ne '') {
    # Get single forum info
    if ($forum_id !~ /^[0-9]+$/) {
        json_error(400, "Invalid forum ID");
    }
    
    my $foruminfo_file = "${main::lbdir}forum${forum_id}/foruminfo.cgi";
    unless (-e $foruminfo_file) {
        json_error(404, "Forum not found");
    }
    
    open(my $fh, '<', $foruminfo_file) or json_error(500, "Cannot read forum info");
    my $line = <$fh>;
    close($fh);
    chomp $line;
    
    my ($fid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator,
        $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter,
        $lastposttime, $threads, $posts, $forumgraphic, $tmp1, $tmp2, $forumpass,
        $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight,
        $miscad4, $todayforumpost, $miscad5) = split(/\t/, $line);
    
    # Get stats from boarddata
    my $stats_file = "${main::lbdir}boarddata/foruminfo${forum_id}.cgi";
    my ($stat_lastposttime, $stat_threads, $stat_posts, $stat_todaypost, $stat_lastposter) = ('', '0', '0', '0', '');
    if (open(my $sfh, '<', $stats_file)) {
        my $sline = <$sfh>;
        close($sfh);
        chomp $sline if $sline;
        ($stat_lastposttime, $stat_threads, $stat_posts, $stat_todaypost, $stat_lastposter) = split(/\t/, $sline || '');
    }
    
    # Parse lastposttime (contains %%% separated data)
    my ($real_lastposttime, $last_thread_number, $last_topic_title) = split(/\%\%\%/, $stat_lastposttime || '');
    $last_topic_title =~ s/^[^>]*>// if $last_topic_title; # strip prefix
    
    my $json = "{";
    $json .= "\"id\":$forum_id,";
    $json .= "\"name\":" . json_str($forumname) . ",";
    $json .= "\"description\":" . json_str($forumdescription) . ",";
    $json .= "\"moderator\":" . json_str($forummoderator) . ",";
    $json .= "\"category\":" . json_str($category) . ",";
    $json .= "\"private\":" . ($privateforum eq 'yes' ? 'true' : 'false') . ",";
    $json .= "\"hidden\":" . ($hiddenforum eq 'yes' ? 'true' : 'false') . ",";
    $json .= "\"threads\":" . (int($stat_threads || 0)) . ",";
    $json .= "\"posts\":" . (int($stat_posts || 0)) . ",";
    $json .= "\"today_posts\":" . (int($stat_todaypost || 0)) . ",";
    $json .= "\"last_poster\":" . json_str($stat_lastposter) . ",";
    $json .= "\"last_post_time\":" . json_str($real_lastposttime);
    $json .= "}";
    
    json_success($json);
}
else {
    # List all forums
    my $allforums_file = "${main::lbdir}data/allforums.cgi";
    unless (-e $allforums_file) {
        json_error(500, "Forum data file not found");
    }
    
    open(my $fh, '<', $allforums_file) or json_error(500, "Cannot read forums data");
    my @forums_data = <$fh>;
    close($fh);
    
    my @categories;
    my %cat_forums;
    my %cat_names;
    
    my @forum_list;
    
    foreach my $line (@forums_data) {
        chomp $line;
        $line =~ s/\r//g;
        next if (length($line) < 30);
        
        my ($forumid, $category, $categoryplace, $forumname, $forumdescription, 
            $forummoderator, $htmlstate, $idmbcodestate, $privateforum, 
            $startnewthreads, $lastposter, $lastposttime, $threadsno, $postsno,
            $forumgraphic, $tmp1, $tmp2, $forumpass, $hiddenforum, $indexforum,
            $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpostno, $miscad5) = split(/\t/, $line);
        
        next if ($forumid !~ /^[0-9]+$/ || $forumname eq '');
        next if ($hiddenforum eq 'yes'); # skip hidden forums
        
        # Get actual stats
        my ($stat_lastposttime, $stat_threads, $stat_posts, $stat_todaypost, $stat_lastposter) = ('', '0', '0', '0', '');
        my $stats_file = "${main::lbdir}boarddata/foruminfo${forumid}.cgi";
        if (open(my $sfh, '<', $stats_file)) {
            my $sline = <$sfh>;
            close($sfh);
            chomp $sline if $sline;
            ($stat_lastposttime, $stat_threads, $stat_posts, $stat_todaypost, $stat_lastposter) = split(/\t/, $sline || '');
        }
        
        my ($real_lastposttime) = split(/\%\%\%/, $stat_lastposttime || '');
        my ($today_count) = split(/\|/, $stat_todaypost || '0');
        
        my $is_child = ($category =~ /^childforum-(\d+)/) ? 1 : 0;
        my $parent_id = $is_child ? $1 : 0;
        
        my $forum_json = "{";
        $forum_json .= "\"id\":$forumid,";
        $forum_json .= "\"name\":" . json_str($forumname) . ",";
        $forum_json .= "\"description\":" . json_str($forumdescription) . ",";
        $forum_json .= "\"moderator\":" . json_str($forummoderator) . ",";
        $forum_json .= "\"category\":" . json_str($category) . ",";
        $forum_json .= "\"category_place\":" . json_str($categoryplace) . ",";
        $forum_json .= "\"is_child\":$is_child,";
        $forum_json .= "\"parent_id\":$parent_id,";
        $forum_json .= "\"private\":" . ($privateforum eq 'yes' ? 'true' : 'false') . ",";
        $forum_json .= "\"threads\":" . (int($stat_threads || 0)) . ",";
        $forum_json .= "\"posts\":" . (int($stat_posts || 0)) . ",";
        $forum_json .= "\"today_posts\":" . (int($today_count || 0)) . ",";
        $forum_json .= "\"last_poster\":" . json_str($stat_lastposter) . ",";
        $forum_json .= "\"last_post_time\":" . json_str($real_lastposttime);
        $forum_json .= "}";
        
        push @forum_list, $forum_json;
    }
    
    my $result = "{\"forums\":[" . join(",", @forum_list) . "],\"total\":" . scalar(@forum_list) . "}";
    json_success($result);
}

1;
