#!/usr/bin/perl
#####################################################
#  LeoBBS X REST API Gateway
#  Provides JSON REST API for LeoBBS forum data
#####################################################

BEGIN {
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
        my $LBPATH = $_;
        next if ($LBPATH eq '');
        $LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use strict;
use warnings;
use LBCGI;

$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;

# Load board configuration
eval { require "data/boardinfo.cgi"; };
if ($@) {
    print "Content-Type: application/json; charset=utf-8\n";
    print "Access-Control-Allow-Origin: *\n\n";
    print '{"error":"Board configuration not found"}';
    exit;
}

require "bbs.lib.pl";

my $query = new LBCGI;

# Handle CORS preflight
if ($ENV{'REQUEST_METHOD'} eq 'OPTIONS') {
    print "Content-Type: application/json; charset=utf-8\n";
    print "Access-Control-Allow-Origin: *\n";
    print "Access-Control-Allow-Methods: GET, POST, OPTIONS\n";
    print "Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Token\n";
    print "Access-Control-Max-Age: 86400\n\n";
    exit;
}

# Common API headers
sub api_headers {
    print "Content-Type: application/json; charset=utf-8\n";
    print "Access-Control-Allow-Origin: *\n";
    print "Access-Control-Allow-Methods: GET, POST, OPTIONS\n";
    print "Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Token\n\n";
}

# JSON encoding helpers (minimal implementation without external modules)
sub json_encode_string {
    my $str = shift;
    return 'null' unless defined $str;
    $str =~ s/\\/\\\\/g;
    $str =~ s/"/\\"/g;
    $str =~ s/\n/\\n/g;
    $str =~ s/\r/\\r/g;
    $str =~ s/\t/\\t/g;
    $str =~ s/[\x00-\x1f]/sprintf("\\u%04x", ord($&))/ge;
    return "\"$str\"";
}

sub json_error {
    my ($code, $message) = @_;
    api_headers();
    print "{\"error\":" . json_encode_string($message) . ",\"code\":$code}";
    exit;
}

sub json_success {
    my ($data) = @_;
    api_headers();
    print $data;
    exit;
}

# Try to encode GB2312/GBK to UTF-8 if Encode module is available
my $has_encode = 0;
eval {
    require Encode;
    $has_encode = 1;
};

sub to_utf8 {
    my $str = shift;
    return '' unless defined $str;
    if ($has_encode) {
        eval {
            $str = Encode::decode('gbk', $str) unless Encode::is_utf8($str);
            $str = Encode::encode('utf-8', $str);
        };
    }
    return $str;
}

sub json_str {
    my $str = shift;
    return json_encode_string(to_utf8($str));
}

# Authentication helper
sub api_authenticate {
    my $token = $ENV{'HTTP_X_API_TOKEN'} || $query->param('token') || '';
    return ('', '') if ($token eq '');
    
    # Token format: base64(username:md5password)
    my $decoded = '';
    eval {
        require MIME::Base64;
        $decoded = MIME::Base64::decode_base64($token);
    };
    if ($@ || $decoded eq '') {
        # Simple decode without MIME::Base64
        $decoded = $token; # fallback: token is "username:password_hash"
    }
    
    my ($username, $passhash) = split(/:/, $decoded, 2);
    return ($username || '', $passhash || '');
}

# Route the request
my $endpoint = $query->param('endpoint') || '';
my $action = $query->param('action') || 'list';

if ($endpoint eq 'forums') {
    require "api/forums.pl";
}
elsif ($endpoint eq 'topics') {
    require "api/topics.pl";
}
elsif ($endpoint eq 'topic') {
    require "api/topic_detail.pl";
}
elsif ($endpoint eq 'auth') {
    require "api/auth.pl";
}
elsif ($endpoint eq 'user') {
    require "api/user.pl";
}
elsif ($endpoint eq 'search') {
    require "api/search.pl";
}
elsif ($endpoint eq 'stats') {
    require "api/stats.pl";
}
elsif ($endpoint eq 'online') {
    require "api/online.pl";
}
elsif ($endpoint eq '') {
    # API info/welcome
    api_headers();
    print '{"name":"LeoBBS X REST API","version":"1.0.0","endpoints":["forums","topics","topic","auth","user","search","stats","online"]}';
}
else {
    json_error(404, "Unknown endpoint: $endpoint");
}
