#####################################################
#  LeoBBS X REST API - User Handler
#  GET api.cgi?endpoint=user&name=USERNAME  - Get user profile
#####################################################

my $username = $query->param('name') || '';

if ($username eq '') {
    json_error(400, "Missing name parameter");
}

# Normalize username for file lookup
my $nametocheck = $username;
$nametocheck =~ s/ /\_/g;
$nametocheck =~ tr/A-Z/a-z/;
$nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

my $namenumber = main::getnamenumber($nametocheck);
my ($memdir) = split(/\|/, main::getdir());
my $member_file = "${main::lbdir}${memdir}/${namenumber}/${nametocheck}.cgi";

unless (-e $member_file) {
    json_error(404, "User not found");
}

open(my $fh, '<', $member_file) or json_error(500, "Cannot read user data");
my $filedata = <$fh>;
close($fh);
chomp $filedata;

my ($membername, $password, $membertitle, $membercode, $numberofposts,
    $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber,
    $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference,
    $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar,
    $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04,
    $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born,
    $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime,
    $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);

# Only show email if user allows it
my $show_email = ($showemail eq 'yes') ? json_str($emailaddress) : 'null';

my $result = "{";
$result .= "\"name\":" . json_str($membername) . ",";
$result .= "\"title\":" . json_str($membertitle) . ",";
$result .= "\"role\":" . json_str($membercode) . ",";
$result .= "\"posts\":" . (int($numberofposts || 0)) . ",";
$result .= "\"email\":$show_email,";
$result .= "\"homepage\":" . json_str($homepage) . ",";
$result .= "\"qq\":" . json_str($oicqnumber) . ",";
$result .= "\"icq\":" . json_str($icqnumber) . ",";
$result .= "\"location\":" . json_str($location) . ",";
$result .= "\"interests\":" . json_str($interests) . ",";
$result .= "\"joined\":" . json_str($joineddate) . ",";
$result .= "\"last_post\":" . json_str($lastpostdate) . ",";
$result .= "\"avatar\":" . json_str($useravatar) . ",";
$result .= "\"personal_avatar\":" . json_str($personalavatar) . ",";
$result .= "\"rating\":" . (int($rating || 0)) . ",";
$result .= "\"visits\":" . (int($visitno || 0)) . ",";
$result .= "\"sex\":" . json_str($sex) . ",";
$result .= "\"signature\":" . json_str($signature) . ",";
$result .= "\"online_time\":" . (int($onlinetime || 0)) . ",";
$result .= "\"jifen\":" . (int($jifen || 0));
$result .= "}";

json_success($result);

1;
