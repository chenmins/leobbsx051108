#####################################################
#  LeoBBS X REST API - Auth Handler
#  POST api.cgi?endpoint=auth&action=login   - Login
#  POST api.cgi?endpoint=auth&action=verify  - Verify token
#####################################################

my $auth_action = $query->param('action') || 'login';

if ($auth_action eq 'login') {
    my $username = $query->param('username') || '';
    my $password = $query->param('password') || '';
    
    if ($username eq '' || $password eq '') {
        json_error(400, "Missing username or password");
    }
    
    # Hash the password the same way LeoBBS does
    my $hashed_password = '';
    eval {
        use Digest::MD5 qw(md5_hex);
        $hashed_password = "lEO" . md5_hex($password);
    };
    if ($@) {
        eval {
            require Digest::MD5;
            Digest::MD5->import('md5_hex');
            $hashed_password = "lEO" . md5_hex($password);
        };
    }
    
    if ($hashed_password eq '') {
        json_error(500, "Password hashing failed");
    }
    
    # Verify user exists and password matches
    my $nametocheck = $username;
    $nametocheck =~ s/ /\_/g;
    $nametocheck =~ tr/A-Z/a-z/;
    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    
    my $namenumber = main::getnamenumber($nametocheck);
    
    my ($memdir) = split(/\|/, main::getdir());
    my $member_file = "${main::lbdir}${memdir}/${namenumber}/${nametocheck}.cgi";
    
    unless (-e $member_file) {
        json_error(401, "User not found");
    }
    
    open(my $fh, '<', $member_file) or json_error(500, "Cannot read user data");
    my $filedata = <$fh>;
    close($fh);
    chomp $filedata;
    
    my ($membername, $stored_password, $membertitle, $membercode, $numberofposts,
        $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber,
        $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference,
        $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar,
        $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04,
        $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born,
        $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, 
        $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
    
    if ($hashed_password ne $stored_password) {
        json_error(401, "Invalid password");
    }
    
    # Generate a simple token (username:password_hash base64 encoded)
    my $token = '';
    eval {
        require MIME::Base64;
        $token = MIME::Base64::encode_base64("${username}:${hashed_password}", '');
    };
    if ($@ || $token eq '') {
        # Fallback: just concatenate
        $token = "${username}:${hashed_password}";
    }
    
    my $result = "{";
    $result .= "\"success\":true,";
    $result .= "\"token\":" . json_str($token) . ",";
    $result .= "\"user\":{";
    $result .= "\"name\":" . json_str($membername) . ",";
    $result .= "\"title\":" . json_str($membertitle) . ",";
    $result .= "\"role\":" . json_str($membercode) . ",";
    $result .= "\"posts\":" . (int($numberofposts || 0)) . ",";
    $result .= "\"email\":" . json_str($emailaddress) . ",";
    $result .= "\"avatar\":" . json_str($useravatar) . ",";
    $result .= "\"joined\":" . json_str($joineddate) . ",";
    $result .= "\"rating\":" . (int($rating || 0));
    $result .= "}}";
    
    json_success($result);
}
elsif ($auth_action eq 'verify') {
    my ($username, $passhash) = api_authenticate();
    
    if ($username eq '') {
        json_error(401, "No token provided or invalid token");
    }
    
    # Verify user
    my $nametocheck = $username;
    $nametocheck =~ s/ /\_/g;
    $nametocheck =~ tr/A-Z/a-z/;
    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    
    my $namenumber = main::getnamenumber($nametocheck);
    my ($memdir) = split(/\|/, main::getdir());
    my $member_file = "${main::lbdir}${memdir}/${namenumber}/${nametocheck}.cgi";
    
    unless (-e $member_file) {
        json_error(401, "User not found");
    }
    
    open(my $fh, '<', $member_file) or json_error(500, "Cannot read user data");
    my $filedata = <$fh>;
    close($fh);
    chomp $filedata;
    
    my ($membername, $stored_password) = split(/\t/, $filedata);
    
    if ($passhash ne $stored_password) {
        json_error(401, "Token expired or invalid");
    }
    
    json_success('{"valid":true,"username":' . json_str($membername) . '}');
}
else {
    json_error(400, "Unknown auth action: $auth_action");
}

1;
