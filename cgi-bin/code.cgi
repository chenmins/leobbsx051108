#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

sub lbnocode {
    my $post = shift;
    study($$post);

    $$post =~ s/javascript/\&\#106\;avascript/isg;
    $$post =~ s/value/\&\#118\;alue/isg;
    $$post =~ s/FORM/\&\#102\;orm/isg;
    $$post =~ s/about:/about\&\#58\;/isg;
    $$post =~ s/document.cookie/documents\&\#46\;cookie/isg;
    $$post =~ s/apasswordcookie/a\&\#112\;asswordcookies/isg;
    $$post =~ s/adminpass/admin\&\#112\;ass/isg;
    $$post =~ s/file:/file\&\#58\;/isg;
    $$post =~ s/on(mouse|exit|error|click|key)/\&\#111\;n$1/isg;
    $$post =~ s/title/\&\#116\;itle/isg;
    $$post =~ s/membercode/memberc\&\#111\;de/isg;
    $$post =~ s/setmembers.cgi/setmembers\&\#46\;cgi/isg;
    $$post =~ s/\[DISABLELBCODE\]//isg;

    if ($$post =~ /\[ADMINOPE=(.+?)\]/) {
	while ($$post =~ /\[ADMINOPE=(.+?)\]/g) {
	    my ($inmembername1,$editmembername1,$ratingname1,$reason1,$thistime1) = split(/\|/,$1);
	    $thistime1 = $thistime1 + ($timedifferencevalue*3600) + ($timezone*3600);
	    $thistime1 = &dateformatshort($thistime1);
	    $$post =~ s/\[ADMINOPE=(.+?)\]/<font color=$fonthighlight>-------------------------------------------------------------------<br>$inmembername1 在 $thistime1 由于此帖对 $editmembername1　进行如下操作：<BR>$ratingname1<BR>理由： $reason1<br>-------------------------------------------------------------------<\/font><br><br>/is;
	}
    }

    if ($$post =~ /\[POSTISDELETE=(.+?)\]/) {
    	$postdelete = 1;
    	if ($1 ne " ") { $presult = "<BR>屏蔽理由：$1<BR>"; } else { $presult = "<BR>"; }
    	if (($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes")) {
    	    $$post =~ s/\[POSTISDELETE=(.+?)\]//;
            $$post = "--------------------------<br><font color=$posternamecolor>此帖子内容已经被单独屏蔽！$presult内容如下（只有管理员可视）：</font><br>--------------------------<br><br>" . $$post;
    	} else {
            $$post = qq(<br>--------------------------<br><font color=$posternamecolor>此帖子内容已经被单独屏蔽！$presult如有疑问，请联系管理员！</font><br>--------------------------<BR>);
            return;
        }
    }
   if ($$post =~ /\[UploadFile.{0,6}=.+?\]/) {
        
        if (($nodispphoto ne 'yes' && $arrawpostpic eq 'on') || $membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo') {
            if ($imgslt eq "Disp") {
            	$defaultsltwidth = 60 if ($defaultsltwidth eq "");
            	$defaultsltheight = 60 if ($defaultsltheight eq "");
            	$sltnoperline = 5 if ($sltnoperline eq "");
            	my $jsq = 0;
            	while ($$post =~ /\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/i) {
            	    $jsq ++;
            	    if (($jsq eq $sltnoperline)&&($sltnoperline ne 0)) {
                        $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a><BR><BR>/i;
                        $jsq = 0;
                    } else {
                        $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a>　/i;
                    }
                }
            } else {
                $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a>/isg;
            }
            if ($thisprog eq "post.cgi") {
                $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><BR>/isg;
            } else {
                $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><span style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')><img id=followImg$1 src=$imagesurl\/images\/cat.gif width=9 loaded=no nofollow="cat.gif" valign=absmiddle> 按此查看图片详细信息<table cellpadding=0 class=ts1 cellspacing=0 width=50% id=follow$1 style=DISPLAY:none><tr><td id=followTd$1><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')>正在读取此图片的详细信息，请稍候 ...<\/DIV><\/td><\/tr><\/table><\/span><BR><BR>/isg;
            }
	} else{
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=$imagesurl\/icon\/$2.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank>点击显示此主题相关图片<\/a><br>/isg;
	}
	
	if (($arrawpostflash eq "on") ||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	    $$post =~ s/\[UploadFileDisp=([^\]]+?)\.swf\]/<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf quality=high width=$defaultflashwidth height=$defaultflashheight pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>/isg;
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.swf\]/<br><img src=$imagesurl\/icon\/swf.gif border=0 width=16> 该主题有一个 swf 格式 Flash 动画<br><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf quality=high width=$defaultflashwidth height=$defaultflashheight pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed><br>&nbsp;<img src=$imagesurl\/images\/fav.gif width=16> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf target=_blank>全屏观看<\/a> (按右键下载)<br><BR>/isg;
	} else {
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.swf\]/<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf target=_blank><img src=$imagesurl\/icon\/swf.gif border=0 width=16 height=16>点击欣赏 Flash 动画<\/a><BR>/isg;
	}

	if ($$post =~ /\[UploadFile.{0,6}=([^\\\]]+?)\.torrent\]/) {
	    require "newbt.pl" if ($loadnewbt ne 1);
	    $loadnewbt = 1;
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.torrent\]/<BR><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank><img src=$imagesurl\/icon\/torrent.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank>该主题有一个 BitTorrent 格式的文件，按此可直接下载<\/a><br>btfileinfolist/i;
            newbt();
	    $$post =~ s/<br>btfileinfolist/<br>$addme/i;
	    $addme = "";
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.torrent\]/<BR><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank><img src=$imagesurl\/icon\/torrent.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank>这个是上传的 BitTorrent 文件，按此可直接下载<\/a><br>/isg;
	}

	while ($$post =~ /\[UploadFile.{0,6}=([^\\\]]+?)(\.(.*?))\]/i) {
   	    $file_type = (-e "${imagesdir}icon/$3.gif") ? $3 : "unknow";
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)(\.(.*?))\]/<br><img src=$imagesurl\/icon\/$file_type.gif border=0 width=16> 这个是上传的 $3 格式文件 [<a href=$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=$2 target=_blank><B>点击查看<\/b><\/a>]<br>/isg;
	}
    }
    return;
}

sub lbcode {
    my $post = shift;
    study($$post);
    
    $arrawautoplay = 1 if ($arrawautoplay eq "");

    $$post =~ s/javascript/\&\#106\;avascript/isg;
    $$post =~ s/value/\&\#118\;alue/isg;
    $$post =~ s/FORM/\&\#102\;orm/isg;
    $$post =~ s/about:/about\&\#58\;/isg;
    $$post =~ s/document.cookie/documents\&\#46\;cookie/isg;
    $$post =~ s/apasswordcookie/a\&\#112\;asswordcookies/isg;
    $$post =~ s/adminpass/admin\&\#112\;ass/isg;
    $$post =~ s/file:/file\&\#58\;/isg;
    $$post =~ s/on(mouse|exit|error|click|key)/\&\#111\;n$1/isg;
    $$post =~ s/title/\&\#116\;itle/isg;
    $$post =~ s/membercode/memberc\&\#111\;de/isg;
    $$post =~ s/setmembers.cgi/setmembers\&\#46\;cgi/isg;

    if ($$post =~ /\[ADMINOPE=(.+?)\]/) {
	while ($$post =~ /\[ADMINOPE=(.+?)\]/g) {
	    my ($inmembername1,$editmembername1,$ratingname1,$reason1,$thistime1) = split(/\|/,$1);
	    $thistime1 = $thistime1 + ($timedifferencevalue*3600) + ($timezone*3600);
	    $thistime1 = &dateformatshort($thistime1);
	    $$post =~ s/\[ADMINOPE=(.+?)\]/<font color=$fonthighlight>-------------------------------------------------------------------<br>$inmembername1 在 $thistime1 由于此帖对 $editmembername1　进行如下操作：<BR>$ratingname1<BR>理由： $reason1<br>-------------------------------------------------------------------<\/font><br><br>/is;
	}
    }

    if ($$post =~ /\[POSTISDELETE=(.+?)\]/) {
    	$postdelete = 1;
    	if ($1 ne " ") { $presult = "<BR>屏蔽理由：$1<BR>"; } else { $presult = "<BR>"; }
    	if (($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes")) {
    	    $$post =~ s/\[POSTISDELETE=(.+?)\]//;
            $$post = "--------------------------<br><font color=$posternamecolor>此帖子内容已经被单独屏蔽！$presult内容如下（只有管理员可视）：</font><br>--------------------------<br><br>" . $$post;
    	} else {
            $$post = qq(<br>--------------------------<br><font color=$posternamecolor>此帖子内容已经被单独屏蔽！$presult如有疑问，请联系管理员！</font><br>--------------------------<BR>);
            return;
        }
    }

    if ($$post =~ /\[UploadFile.{0,6}=.+?\]/) {
        if (($nodispphoto ne 'yes' && $arrawpostpic eq 'on') || $membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo') {
            if ($imgslt eq "Disp") {
            	$defaultsltwidth = 60 if ($defaultsltwidth eq "");
            	$defaultsltheight = 60 if ($defaultsltheight eq "");
            	$sltnoperline = 5 if ($sltnoperline eq "");

            	my $jsq = 0;
            	while ($$post =~ /\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/i) {
            	    $jsq ++;
            	    if (($jsq eq $sltnoperline)&&($sltnoperline ne 0)) {
                        $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a><BR><BR>/i;
                        $jsq = 0;
                    } else {
                        $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 width=$defaultsltwidth height=$defaultsltheight onmousewheel="return bbimg(this)"><\/a>　/i;
                    }
                }
            } else {
                $$post =~ s/\[UploadFileDisp=([^\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a>/isg;
            }
            if ($thisprog eq "post.cgi") {
                $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><BR>/isg;
            } else {
                $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><img src=$imagesurl\/icon\/$2.gif border=0 width=16> 此主题相关图片如下：<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0 alt=按此在新窗口浏览图片 onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"><\/a><br><img src=$imagesurl\/images\/none.gif whidth=0 height=5><BR><span style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')><img id=followImg$1 src=$imagesurl\/images\/cat.gif width=9 loaded=no nofollow="cat.gif" valign=absmiddle> 按此查看图片详细信息<table cellpadding=0 class=ts1 cellspacing=0 width=50% id=follow$1 style=DISPLAY:none><tr><td id=followTd$1><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,'','$2','$1')>正在读取此图片的详细信息，请稍候 ...<\/DIV><\/td><\/tr><\/table><\/span><BR><BR>/isg;
            }
	} else{
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(gif|jpg|png|bmp|jpeg)\]/<BR><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank><img src=$imagesurl\/icon\/$2.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 target=_blank>点击显示此主题相关图片<\/a><br>/isg;
	}
	
	if (($arrawpostflash eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	    $$post =~ s/\[UploadFileDisp=([^\]]+?)\.swf\]/<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf quality=high width=$defaultflashwidth height=$defaultflashheight pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>/isg;
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.swf\]/<br><img src=$imagesurl\/icon\/swf.gif border=0 width=16> 该主题有一个 swf 格式 Flash 动画<br><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf quality=high width=$defaultflashwidth height=$defaultflashheight pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed><br>&nbsp;<img src=$imagesurl\/images\/fav.gif width=16> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf target=_blank>全屏观看<\/a> (按右键下载)<br><BR>/isg;
	} else {
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.swf\]/<br><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.swf target=_blank><img src=$imagesurl\/icon\/swf.gif border=0 width=16 height=16>点击欣赏 Flash 动画<\/a><BR>/isg;
	}

	if (($arrawpostsound eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.wav\]/<br><img src=$imagesurl\/icon\/wav.gif border=0 width=16> 该主题有一个 wave 格式音乐<br><bgsound src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.wav border=0><img src=$imagesurl\/images\/wave.gif width=16 height=16 alt=WAVE音乐>/isg;
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(mid|midi)\]/<br><img src=$imagesurl\/icon\/mid.gif border=0 width=16> 该主题有一个 MIDI 格式音效<br><bgsound src=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2 border=0><img src=$imagesurl\/images\/mid.gif width=16 height=16 alt=MIDI音乐>/isg;
	}

	if (($arrawpostreal eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(mp3|mp2)\]/<br><img src=$imagesurl\/icon\/mp3.gif border=0 width=16> 该主题有一个 MP3 格式音乐<br><embed type="application\/x-mplayer2" pluginspage="http:\/\/www.microsoft.com\/Windows\/Downloads\/Contents\/Products\/MediaPlayer\/" src="$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2" name="realradio" showcontrols=1 ShowDisplay=0 ShowStatusBar=1 width=480 height=70 autostart=$arrawautoplay><\/embed><BR>/isg;
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(ra)\]/<br><img src=$imagesurl\/icon\/ra.gif border=0 width=16> 该主题有一个 RealPlayer 格式音乐<br><object classid="clsid:CFCDAA03-8BE4-11CF-B84B-0020AFBBCCFA" id="RAOCX" width="480" height="70"><param name="_ExtentX" value="6694"><param name="_ExtentY" value="1588"><param name="AUTOSTART" value=$arrawautoplay><param name="SHUFFLE" value="0"><param name="PREFETCH" value="0"><param name="NOLABELS" value="0"><param name="SRC" value="$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2"><param name="CONTROLS" value="StatusBar,ControlPanel"><param name="LOOP" value="0"><param name="NUMLOOP" value="0"><param name="CENTER" value="0"><param name="MAINTAINASPECT" value="0"><param name="BACKGROUNDCOLOR" value="#000000"><embed src="$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2" width="320" autostart=$arrawautoplay height="70"><\/object><BR>/isg;
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(ram|rmm|rm|rmvb|mpg|mpv|mpeg|dat|avi|mpga)\]/<br><img src=$imagesurl\/icon\/ra.gif border=0 width=16> 该主题有一个 RealPlayer 格式影片<br><object classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" HEIGHT=300 ID=Player WIDTH=480 VIEWASTEXT><param NAME="_ExtentX" VALUE="12726"><param NAME="_ExtentY" VALUE="8520"><param NAME="AUTOSTART" VALUE=$arrawautoplay><param NAME="SHUFFLE" VALUE="0"><param NAME="PREFETCH" VALUE="0"><param NAME="NOLABELS" VALUE="0"><param NAME="CONTROLS" VALUE="ImageWindow"><param NAME="CONSOLE" VALUE="_master"><param NAME="LOOP" VALUE="0"><param NAME="NUMLOOP" VALUE="0"><param NAME="CENTER" VALUE="0"><param NAME="MAINTAINASPECT" VALUE="$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2"><param NAME="BACKGROUNDCOLOR" VALUE="#000000"><\/object><br><object CLASSID=clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA HEIGHT=32 ID=Player WIDTH=480 VIEWASTEXT><param NAME="_ExtentX" VALUE="18256"><param NAME="_ExtentY" VALUE="794"><param NAME="AUTOSTART" VALUE=$arrawautoplay><param NAME="SHUFFLE" VALUE="0"><param NAME="PREFETCH" VALUE="0"><param NAME="NOLABELS" VALUE="0"><param NAME="CONTROLS" VALUE="controlpanel"><param NAME="CONSOLE" VALUE="_master"><param NAME="LOOP" VALUE="0"><param NAME="NUMLOOP" VALUE="0"><param NAME="CENTER" VALUE="0"><param NAME="MAINTAINASPECT" VALUE="0"><param NAME="BACKGROUNDCOLOR" VALUE="#000000"><param NAME="SRC" VALUE="$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2"><\/object><BR>/isg;
	}

	if (($arrawpostmedia eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(mp3|mp2)\]/<br><img src=$imagesurl\/icon\/mp3.gif border=0 width=16> 该主题有一个 MP3 格式音乐<br><embed type="application\/x-mplayer2" pluginspage="http:\/\/www.microsoft.com\/Windows\/Downloads\/Contents\/Products\/MediaPlayer\/" src="$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2" name="realradio" showcontrols=1 ShowDisplay=0 ShowStatusBar=1 width=480 height=70 autostart=$arrawautoplay><\/embed><BR>/isg;
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(wma|wm|mpa|mpga)\]/<br><img src=$imagesurl\/icon\/movie.gif border=0 width=16> 该主题有一个 Windows Media Player 格式音乐<br><embed type="application\/x-mplayer2" pluginspage="http:\/\/www.microsoft.com\/Windows\/Downloads\/Contents\/Products\/MediaPlayer\/" src="$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2" name="realradio" showcontrols=1 ShowDisplay=0 ShowStatusBar=1 width=480 height=70 autostart=$arrawautoplay><\/embed><BR>/isg;
	    $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.(asf|asx|avi|wmv|mpg|mpeg|dat|mpv)\]/<br><img src=$imagesurl\/icon\/movie.gif border=0 width=16> 该主题有一个 Windows Media Player 格式影片<br><object id="videowindow1" width="480" height="330" classid="CLSID:22d6f312-b0f6-11d0-94ab-0080c74c7e95"><param NAME="Filename" value="$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.$2"><param name="AUTOSTART" value=$arrawautoplay><\/object><BR>/isg;
	}

	if ($$post =~ /\[UploadFile.{0,6}=([^\\\]]+?)\.torrent\]/) {
	    require "newbt.pl" if ($loadnewbt ne 1);
	    $loadnewbt = 1;
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.torrent\]/<BR><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank><img src=$imagesurl\/icon\/torrent.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank>该主题有一个 BitTorrent 格式的文件，按此可直接下载<\/a><br>btfileinfolist/i;
            newbt();
	    $$post =~ s/<br>btfileinfolist/<br>$addme/i;
	    $addme = "";
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)\.torrent\]/<BR><a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank><img src=$imagesurl\/icon\/torrent.gif border=0 width=16><\/a> <a href=attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=.torrent target=_blank>这个是上传的 BitTorrent 文件，按此可直接下载<\/a><br>/isg;
	}

	while ($$post =~ /\[UploadFile.{0,6}=([^\\\]]+?)(\.(.*?))\]/i) {
   	    $file_type = (-e "${imagesdir}icon/$3.gif") ? $3 : "unknow";
            $$post =~ s/\[UploadFile.{0,6}=([^\\\]]+?)(\.(.*?))\]/<br><img src=$imagesurl\/icon\/$file_type.gif border=0 width=16> 这个是上传的 $3 格式文件 [<a href=$boardurl\/attachment.cgi?forum=$inforum&topic=$intopic&postno=$editpostnumber&name=$1&type=$2 target=_blank><B>点击查看<\/b><\/a>]<br>/isg;
	}
    }
    if ($wwjf ne "no") {
	if ($$post=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg) {
    	    if ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes")|| ($myrating >= $1) ){
	    } else {
		$$post=qq~<FONT COLOR=$fonthighlight><B>[Hidden Post: Rating $1]</B></FONT> <BR>  <BR> <FONT COLOR=$posternamecolor>（您没有权限看这个帖子，您的威望至少需要 <B>$1<\/B>）</FONT><BR>  <BR> ~;
		$addme="附件保密!<br><br>" if ($addme);
	    }
	    $$post=~s/LBHIDDEN\[(.*?)\]LBHIDDEN/<font color=$fonthighlight>（此贴只有威望大于等于 <B>$1<\/B> 的才能查看）<\/font><br>/sg;   
	}
    }
    else { $$post=~s/LBHIDDEN\[(.*?)\]LBHIDDEN//; }

    if ($cansale ne "no") {
	if ($$post=~/LBSALE\[(.*?)\]LBSALE/sg) {
	    require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
    	    my $postno = $rn;
            my $isbuyer = "";
            my $allbuyer = "";
            my $allbuyerno = "";
            undef @allbuyer;
            if (open(FILE, "${lbdir}$saledir/$inforum\_$intopic\_$postno.cgi")) {
                my $allbuyer = <FILE>;
                close(FILE);
                chomp $allbuyer;
		$allbuyer =~ s/\t\t/\t/isg;
                $allbuyer =~ s/\t$//gi;
                $allbuyer =~ s/^\t//gi;
		@allbuyer = split(/\t/, $allbuyer);
		$allbuyerno = @allbuyer;
	        $allbuyer = "\t$allbuyer\t";
		$isbuyer="yes" if ($allbuyer =~ /\t$inmembername\t/i);
            }
            $allbuyerno = 0 if (($allbuyerno < 0)||($allbuyerno eq ""));
            { @allexege = ($$post =~ /\[buyexege\].*?\[\/buyexege\]/ig); }
            unless ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad")||($mymembercode eq 'smo')||($myinmembmod eq "yes")||($isbuyer eq "yes")) {
                $$post=qq~<FONT COLOR=$fonthighlight><B>[Sale Post: Money $1]</B></FONT><BR>  <BR><FONT COLOR=$posternamecolor>[查看这个帖子需要 <b>$1</b> $moneyname，目前已有 <B>$allbuyerno</B> 人购买]</FONT><BR><br><script>function salesubmitonce(theform){if (document.all||document.getElementById){for (i=0;i<theform.length;i++){ var tempobj=theform.elements[i]; if(tempobj.type.toLowerCase()=="submit"||tempobj.type.toLowerCase()=="reset") { tempobj.disabled=true; }}}}</script>
                <FORM action=buypost.cgi method=post onSubmit="salesubmitonce(this)"><input name=inforum type=hidden value=$inforum><input name=intopic type=hidden value=$intopic><input name=postnumber type=hidden value=$postno><input name=salemembername type=hidden value="$membername"><input name=moneynumber type=hidden value=$1><INPUT name=B1 type=submit value="算你狠。。我买，我付钱"></form><BR> ~;
                $$post .= join ('<BR>', @allexege);
                $addme="附件保密!<br><br>" if ($addme);
	    } else {
	    	$buyeroutput = "";
	    	if ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad")||($mymembercode eq 'smo')||($myinmembmod eq "yes")) {
                    if ($allbuyerno > 0 ) {
	                $buyeroutput = qq~<SCRIPT LANGUAGE="JavaScript">function surfto(list) { var myindex1  = list.selectedIndex; if (myindex1 != 0 & myindex1 != 1) { var newwindow = list.options[myindex1].value; var msgwindow = window.open("profile.cgi?action=show&member=" + newwindow,"",""); } }</SCRIPT><img src=$imagesurl/images/team2.gif width=19 height=19 align=absmiddle><select onchange="surfto(this)">
<option>购买名单：</option><option>------------</option>
~;
	                foreach (@allbuyer) {
	                    chomp $_;
	                    next if ($_ eq "");
	                    my $cleanedmodname = $_;
	                    $cleanedmodname =~ s/ /\_/g;
	                    $cleanedmodname =~ tr/A-Z/a-z/;
	                    $cleanedmodname = uri_escape($cleanedmodname);
    	                    $buyeroutput .= qq~<option value="$cleanedmodname">$_</option>~;
	                }
	                $buyeroutput .= qq~</select></form><BR>\n~;
                    }
                }
	        $$post=~s/LBSALE\[(.*?)\]LBSALE/$buyeroutput<font color=$fonthighlight>（此贴售价 <B>$1<\/B> $moneyname，目前已有 <B>$allbuyerno<\/B> 人购买）<\/font><br><br>/sg;   
	    }
	    $$post =~ s/\[buyexege\](.*?)\[\/buyexege\]/<blockquote><font color=$posternamecolor>买卖文章注解内容： <hr noshade size=1>$1<hr noshade size=1><\/blockquote><\/font>/g;
	} else { $$post=~s/\[buyexege\](.*?)\[\/buyexege\]/$1/isg; }
    }
    else { $$post=~s/LBSALE\[(.*?)\]LBSALE//; $$post=~s/\[buyexege\](.*?)\[\/buyexege\]/$1/isg; }

    if ($$post =~/\[DISABLELBCODE\]/) {
	$$post =~ s/\[DISABLELBCODE\]//isg;
	return;
    }

    $$post =~ s/(^|\s|\>|\\|\;)(ed2k:\/\/\|file\|)(\S+?)\|(\S+?)(\s|$|\<)/$1 eMule 下载： <a href=$2$3\|$4 target=_blank>$3<\/a><BR>$5/isg;
    $$post =~ s/(^|\s|\>|\\|\;)(exeem:\/\/)(\S+?)\/(\S+?)\/(\S+?)(\s|$|\<)/$1 eXeem 下载： <a href=$2$3\/$4\/$5$6 target=_blank>$5<\/a><BR>$6/isg;

    $$post =~ s/(^|\s|\>|\\|\;)(http|https|ftp|ed2k|exeem):\/\/(\S+?)(\s|$|\<|\[)/$1<a href=$2:\/\/$3\ target=_blank>$2\:\/\/$3<\/a>$4/isg;

    if (($arrawpostpic eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	$$post =~ s/\[url.+?\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]\[\/url\]/<a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333\"><\/a>/isg;
	$$post =~ s/\[img\]\s*(http|https|ftp):\/\/(\S+?)\s*\[\/img\]/<a href=$1:\/\/$2 target=_blank title=开新窗口浏览><img src=$1:\/\/$2 border=0 onload=\"javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333\"><\/a>/isg;
	$$post =~ s/(^|\s|\>|\\|\;)(http|https|ftp):\/\/(\S+?\.)(png|bmp|gif|jpg|jpeg)(\s|$|\<|\[)/$1<a href=$2:\/\/$3$4 target=_blank title=开新窗口浏览><img src=$2:\/\/$3$4 border=0 onload=\"javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333\"><\/a>$5/isg;
    }
    if (($arrawpostflash eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	$$post =~ s/(\[swf\])\s*(http|https|ftp):\/\/(\S+?\.swf)\s*(\[\/swf\])/<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$2:\/\/$3 quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash" WIDTH=$defaultflashwidth height=$defaultflashheight><\/embed>/isg;
	$$post =~ s/(\[FLASH=)(\S+?)(\,)(\S+?)(\])\s*(http|https|ftp):\/\/(\S+?\.swf)\s*(\[\/FLASH\])/<OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$2 HEIGHT=$4><PARAM NAME=MOVIE VALUE=$6:\/\/$7><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$6:\/\/$7 WIDTH=$2 HEIGHT=$4 PLAY=TRUE LOOP=TRUE QUALITY=HIGH><\/EMBED><\/OBJECT>/isg;
        $$post =~ s/(^|\s|\>)(http|https|ftp):\/\/(\S+?\.swf)(\s|$|\<)/$1<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$2:\/\/$3 quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash" WIDTH=$defaultflashwidth height=$defaultflashheight><\/embed>$4/isg;
    }

    $$post =~ s/(^|\s|\>|\\|\;)www\.(\S+?)(\s|$|\<|\[)/$1<a href=http:\/\/www.$2 target=_blank>www.$2<\/a>$3/isg;
    $$post =~ s/(^|\s|\>|\\|\;)(\w+\@\w+\.\w+)(\s|$|\<|\[)/$1<A HREF=mailto:$2>$2<\/A>$3/isg;
    $$post =~ s/\<p>/<br><br>/isg;
    $$post =~ s/\[br\]/<br>/isg;
    $$post =~ s/(<br>){10,}/<br><br><br>/ig;

    if (($$post =~/\[curl=(http|https|ftp):\/\/(.*?)\]/i)&&($usecurl ne "no")) {
        my $clinkcount=0;my $clinkcode;
        $postcountnumber=($thisprog eq "view.cgi")?$rn:$postcountnumber;
        $$post =~ s/\[curl=(http|https|ftp):\/\/(.*?)\]/
        $clinkcode=sprintf("%.3d%.5d%.5d%.2d",$inforum,$intopic,$postcountnumber,$clinkcount);
        my $return = '<form action="decrypt.cgi" name="decrypt'.$clinkcode.'" method=POST><input type=hidden name=clno value="'.$clinkcount.'"><input type=hidden name=forum value="'.$inforum.'"><input type=hidden name=topic value="'.$intopic.'"><input type="hidden" name="postno" value="'.$postcountnumber.'"><\/form> ［<span style=cursor:hand onClick="decrypt'.$clinkcode.'.submit()">加密链接，点击进入<\/span>］ ';
        $clinkcount++;
        $return;
        /ige;
    }

    unless ($$post =~ /\[\/.{1,12}]/) {
        $$post =~ s/\{br\}/<br>/sg;
	return;
    }

    $$post =~ s/\[url\](\[\S+\])(\S+?)(\[\S+\])\[\/url\]/<a href=$2 target=_blank>$1$2$3<\/a>/isg;
    $$post =~ s/\[url=\s*(.*?)\s*\]\s*(.*?)\s*\[\/url\]/<a href=$1 target=_blank>$2<\/a>/isg;
    $$post =~ s/\[url\]\s*(.*?)\s*\[\/url\]/<a href=$1 target=_blank>$1<\/a>/isg;
    $$post =~ s/(\[email\])(\S+?\@\S+?)(\[\/email\])/<A HREF="mailto:$2">$2<\/A>/isg;
    $$post =~ s/\[email=(\S+?\@\S+?)\]\s*(.*?)\s*\[\/email\]/<a href=mailto:$1>$2<\/a>/isg;

    $$post =~ s/\[emule\](\S+?)\[\/emule\]/eMule 下载： <a href=$1 target=_blank>$1<\/a>/isg;
    $$post =~ s/\[emule=\s*(.*?)\s*\]\s*(.*?)\s*\[\/emule\]/eMule 下载： <a href=$1 target=_blank>$2<\/a>/isg;

    $$post =~ s/\[exeem\](\S+?)\[\/exeem\]/eXeem 下载： <a href=$1 target=_blank>$1<\/a>/isg;
    $$post =~ s/\[exeem=\s*(.*?)\s*\]\s*(.*?)\s*\[\/exeem\]/eXeem 下载： <a href=$1 target=_blank>$2<\/a>/isg;

    if ($hidejf eq "yes" ) {
      if ($$post =~m/(\[hide\])(.*)(\[\/hide\])/isg){ 
        if ($viewhide ne "1") { 
            $$post =~ s/(\[hide\])(.*)(\[\/hide\])/<blockquote><font color=$posternamecolor>隐藏： <hr noshade size=1><font color=$fonthighlight>本部分内容已经隐藏，必须回复后，才能查看<\/font><hr noshade size=1><\/blockquote><\/font><\/blockquote>/isg;
            $addme="附件保密!<br><br>" if (($addme)&&($1 eq "[hide]"));
	} else { 
            $$post =~ s/\[hide\](.*)\[hide\](.*)\[\/quote](.*)\[\/hide\]/<blockquote><font color=$posternamecolor>隐藏： <hr noshade>$1<blockquote><hr noshade size=1>$2<hr noshade size=1><\/blockquote>$3<\/font><hr noshade><\/blockquote>/isg; 
     	    $$post =~ s/\[hide\]\s*(.*?)\s*\[\/hide\]/<blockquote><font color=$posternamecolor>隐藏： <hr noshade size=1>$1<hr noshade size=1><\/blockquote><\/font>/isg; 
  	}
      }
    }

    if ($postjf eq "yes") {
	if ($$post =~m/\[post=(\d+?)\](.+?)\[\/post\]/isg){ 
	    $viewusepost=$1; 
	    if ($StartCheck >= $viewusepost) { $Checkpost='ok'; } else { $Checkpost='not'; }

	    if (($Checkpost eq 'ok')||($mymembercode eq "ad")||($mymembercode eq "smo")||($myinmembmod eq "yes")||(lc($membername) eq lc($inmembername))){ 
	   	$$post =~s/\[post=(\d+?)\](.*)\[\/post\]/<blockquote><font color=$posternamecolor>文章内容：（发言总数须有 <B>$viewusepost<\/B> 才能查看本贴） <hr noshade size=1>$2<hr noshade size=1><\/font><\/blockquote>/isg; 
	    } else { 
   		$$post =~s/(\[post=(\d+?)\])(.*)(\[\/post\])/<blockquote><font color=$posternamecolor>文章内容： <hr noshade size=1><font color=$fonthighlight>本内容已被隐藏 , 发言总数须有 <B>$viewusepost<\/B> 才能查看<\/font><hr noshade size=1><\/font><\/blockquote>/isg; 
                $addme="附件保密!<br><br>" if (($addme)&&($1 =~ m/^\[post/));
   	    }
   	}
    }

    if ($jfmark eq "yes") {
	if ($$post =~m/\[jf=(\d+?)\](.+?)\[\/jf\]/isg){ 
	    $jfpost=$1;
	    if (($jfpost <= $jifen)||($mymembercode eq "ad")||($mymembercode eq "smo")||($myinmembmod eq "yes")||(lc($membername) eq lc($inmembername))){ 
	   	$$post =~s/\[jf=(\d+?)\](.*)\[\/jf\]/<blockquote><font color=$posternamecolor>文章内容：（积分必须达到 <B>$jfpost<\/B> 才能查看本内容） <hr noshade size=1>$2<hr noshade size=1><\/font><\/blockquote>/isg; 
	    } else { 
	        &error("有问题&积分必须达到 $jfpost 才能查看，你目前的积分是 $jifen ！") if (($editpostnumber eq "1")&&($noviewjf eq "yes"));
   		$$post =~s/(\[jf=(\d+?)\])(.*)(\[\/jf\])/<blockquote><font color=$posternamecolor>文章内容： <hr noshade size=1><font color=$fonthighlight>本内容已被隐藏 , 积分必须达到 <B>$jfpost<\/B> 才能查看<\/font><hr noshade size=1><\/font><\/blockquote>/isg; 
                $addme="附件保密!<br><br>" if (($addme)&&($1 =~ m/^\[jf/));
   	    }
   	}
    }

    if ($$post =~/\[HTML\](.+?)\[\/HTML\]/is) {
      while ($$post =~/\[HTML\](.+?)\[\/HTML\]/is) {
	my $post1=$$post;

	$post1 =~ s/\[HTML\](.+?)\[\/HTML\]//is;
	$post1=$1;
	$post1 =~ s/\&\#106\;avascript/javascript/isg;
	$post1 =~ s/\&\#118\;alue/value/isg;
	$post1 =~ s/\&\#111\;nmouse/onmouse/isg;
	$post1 =~ s/<br>/\n/isg;
	$post1 =~ s/<p>/\n\n/isg;
	$post1 =  &HTML($post1);
    	$post1 =~ s/</\&lt;/g;
    	$post1 =~ s/>/\&gt;/g;
    	$post1 =~ s/"/\&quot;/g;
	$$post =~ s/(\[HTML\])(.+?)(\[\/HTML\])/<br><SPAN><IMG src=$imagesurl\/images\/code.gif align=absBottom> HTML 代码片段如下:<BR><TEXTAREA style=\"WIDTH: 94%; BACKGROUND-COLOR: #f7f7f7\" name=textfield rows=10>$post1<\/TEXTAREA><BR><INPUT onclick=runEx() type=button value=运行此代码> <input type=button value=另存代码 onclick=saveCode()> [Ctrl+A 全部选择   提示:你可先修改部分代码，再按运行]<\/SPAN><BR>/is;
      }
      return;
    }

	if ($openiframe eq "yes") {
	    $$post =~ s/(\[iframe\])(.+?)(\[\/iframe\])/<IFRAME SRC='$2' FRAMEBORDER=0 ALLOWTRANSPARENCY="true" SCROLLING="YES" WIDTH="100%" HEIGHT=340><\/IFRAME><br><br><a href="$2" target="_blank">Netscape 用户点这儿查看<\/a><BR>/isg;
	}

	$postbackcolor = "#ffffff" unless ($postbackcolor);
	while ($$post =~ /\[watermark\](.+?)\[\/watermark\]/is) {
	    my $post1 = $1;
	    $post1 =~ s/<p>/<br><br>/isg;
	    my @lines = split(/<br>/i, $post1);
	    $post1 = "";
	    foreach (@lines) {
		my $addline = "";
		for (0 .. int(myrand(6))) {
		    $addline .= chr(32 + int(myrand(95)));
		}
		$addline =~ s/"/\&quot;/sg;
		$addline =~ s/</\&lt;/sg;
		$addline =~ s/>/\&gt;/sg;
		$post1 .= length($_) > 5 ? $_ . "<font color=$postbackcolor>$addline</font><br>" : $_ . "<font color=$postbackcolor>\&copy;$boardname -- $boarddescription　　$addline</font><br>";
	    }
	    $$post =~ s/\[watermark\](.+?)\[\/watermark\]/$post1/is;
	}
        $$post =~ s/\{br\}/<br>/sg;

        if ($count eq 1) {  $quoteback = $postcolortwo; } else { $quoteback = $postcolorone; }
	$$post =~ s/\[quote\]\s*(.*?)\s*\[\/quote\]/<BR><table cellpadding=0 cellspacing=0 WIDTH=94\% bgcolor=#000000 align=center style=\"TABLE-LAYOUT: fixed\"><tr><td><table width=100% cellpadding=5 cellspacing=1 style=\"TABLE-LAYOUT: fixed\"><TR><TD BGCOLOR=$quoteback style=\"LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word; $paraspace; $wordspace\\pt\">$1<\/td><\/tr><\/table><\/td><\/tr><\/table><BR>/isg;

	if (($arrawpostfontsize eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
    	    $$post =~ s/\[size=\s*([1-6])\s*\]\s*(.*?)\s*\[\/size\]/<font size=$1>$2<\/font>/isg;
	}

	if (($arrawpostsound eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	    $$post =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.wav)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3 border=0><img src=$imagesurl\/images\/wave.gif width=16 height=16 alt=WAVE音乐>/isg;
	    $$post =~ s/(\[sound\])\s*(http|https|ftp):\/\/(\S+?\.)(mid|midi)\s*(\[\/sound\])/<bgsound src=$2:\/\/$3$4 border=0><img src=$imagesurl\/images\/mid.gif width=16 height=16 alt=MIDI音乐>/isg;
	}

        if (($arrawpostreal eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	    $$post =~ s/(\[ra\])(\S+?\.)(ram|rmm|mp3|mp2|mpa|ra|mpga)(\[\/ra\])/<b>这个是 RealPlayer 音乐：<\/b><br><object classid="clsid:CFCDAA03-8BE4-11CF-B84B-0020AFBBCCFA" id="RAOCX" width="480" height="70"><param name="_ExtentX" value="6694"><param name="_ExtentY" value="1588"><param name="AUTOSTART" value=$arrawautoplay><param name="SHUFFLE" value="0"><param name="PREFETCH" value="0"><param name="NOLABELS" value="0"><param name="SRC" value="$2$3"><param name="CONTROLS" value="StatusBar,ControlPanel"><param name="LOOP" value="0"><param name="NUMLOOP" value="0"><param name="CENTER" value="0"><param name="MAINTAINASPECT" value="0"><param name="BACKGROUNDCOLOR" value="#000000"><embed src="$2$3" width="320" autostart=$arrawautoplay height="70"><\/object><BR>/isg;
	    $$post =~ s/(\[rm\])(\S+?\.)(ram|rmm|rm|rmvb|mpg|mpv|mpeg|dat|avi|mpga)(\[\/rm\])/<b>这个是 RealPlayer 影片：<\/b><br><object classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" HEIGHT=300 ID=Player WIDTH=480 VIEWASTEXT><param NAME="_ExtentX" VALUE="12726"><param NAME="_ExtentY" VALUE="8520"><param NAME="AUTOSTART" VALUE=$arrawautoplay><param NAME="SHUFFLE" VALUE="0"><param NAME="PREFETCH" VALUE="0"><param NAME="NOLABELS" VALUE="0"><param NAME="CONTROLS" VALUE="ImageWindow"><param NAME="CONSOLE" VALUE="_master"><param NAME="LOOP" VALUE="0"><param NAME="NUMLOOP" VALUE="0"><param NAME="CENTER" VALUE="0"><param NAME="MAINTAINASPECT" VALUE="$2$3"><param NAME="BACKGROUNDCOLOR" VALUE="#000000"><\/object><br><object CLASSID=clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA HEIGHT=32 ID=Player WIDTH=480 VIEWASTEXT><param NAME="_ExtentX" VALUE="18256"><param NAME="_ExtentY" VALUE="794"><param NAME="AUTOSTART" VALUE=$arrawautoplay><param NAME="SHUFFLE" VALUE="0"><param NAME="PREFETCH" VALUE="0"><param NAME="NOLABELS" VALUE="0"><param NAME="CONTROLS" VALUE="controlpanel"><param NAME="CONSOLE" VALUE="_master"><param NAME="LOOP" VALUE="0"><param NAME="NUMLOOP" VALUE="0"><param NAME="CENTER" VALUE="0"><param NAME="MAINTAINASPECT" VALUE="0"><param NAME="BACKGROUNDCOLOR" VALUE="#000000"><param NAME="SRC" VALUE="$2$3"><\/object><BR>/isg;
	    $$post =~ s/(\[real=)(\S+?)(\,)(\S+?)(\])(\S+?\.)(ram|rmm|rm|rmvb|mpg|mpv|mpeg|dat|avi|mpga)(\[\/real\])/<b>这个是 RealPlayer 影片：<\/b><br><object classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" HEIGHT=$4 ID=Player WIDTH=$2 VIEWASTEXT><param NAME="_ExtentX" VALUE="12726"><param NAME="_ExtentY" VALUE="8520"><param NAME="AUTOSTART" VALUE=$arrawautoplay><param NAME="SHUFFLE" VALUE="0"><param NAME="PREFETCH" VALUE="0"><param NAME="NOLABELS" VALUE="0"><param NAME="CONTROLS" VALUE="ImageWindow"><param NAME="CONSOLE" VALUE="_master"><param NAME="LOOP" VALUE="0"><param NAME="NUMLOOP" VALUE="0"><param NAME="CENTER" VALUE="0"><param NAME="MAINTAINASPECT" VALUE="$6"><param NAME="BACKGROUNDCOLOR" VALUE="#000000"><\/object><br><object CLASSID=clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA HEIGHT=32 ID=Player WIDTH=$2 VIEWASTEXT><param NAME="_ExtentX" VALUE="18256"><param NAME="_ExtentY" VALUE="794"><param NAME="AUTOSTART" VALUE=$arrawautoplay><param NAME="SHUFFLE" VALUE="0"><param NAME="PREFETCH" VALUE="0"><param NAME="NOLABELS" VALUE="0"><param NAME="CONTROLS" VALUE="controlpanel"><param NAME="CONSOLE" VALUE="_master"><param NAME="LOOP" VALUE="0"><param NAME="NUMLOOP" VALUE="0"><param NAME="CENTER" VALUE="0"><param NAME="MAINTAINASPECT" VALUE="0"><param NAME="BACKGROUNDCOLOR" VALUE="#000000"><param NAME="SRC" VALUE="$6$7"><\/object><BR>/isg;
	} else {
	    $$post =~ s/(\[ra\])(\S+?\.)(ram|rmm|mp3|mp2|mpa|ra|mpga)(\[\/ra\])/<b>这个是 RealPlayer 音乐，点击播放<\/b><BR><a href="$2$3">$2$3<\/a>/isg;
	    $$post =~ s/(\[rm\])(\S+?\.)(ram|rmm|rm|rmvb|mpg|mpv|mpeg|dat|avi|mpga)(\[\/rm\])/<b>这个是 RealPlayer 影片，点击播放<\/b><BR><a href="$2$3">$2$3<\/a>/isg;
	    $$post =~ s/(\[real=)(\S+?)(\,)(\S+?)(\])(\S+?\.)(ram|rmm|rm|rmvb|mpg|mpv|mpeg|dat|avi|mpga)(\[\/real\])/<b>这个是 RealPlayer 影片，点击播放<\/b><BR><a href="$6$7">$6$7<\/a>/isg;
	}
	if (($arrawpostmedia eq "on")||($membercode{$membername} eq 'mo' || $membercode{$membername} eq 'amo' || $membercode{$membername} eq 'cmo' || $membercode{$membername} eq 'ad' || $inmembmod eq 'yes' || $membercode{$membername} eq 'smo')) {
	    $$post =~ s/(\[wma\])(\S+?\.)(ram|wma|wm|mp3|mp2|ra|mpa|mpga)(\[\/wma\])/<b>这个是 Windows Media Player 音乐：<\/b><br><embed type="application\/x-mplayer2" pluginspage="http:\/\/www.microsoft.com\/Windows\/Downloads\/Contents\/Products\/MediaPlayer\/" src="$2$3" name="realradio" showcontrols=1 ShowDisplay=0 ShowStatusBar=1 width=480 height=70 autostart=$arrawautoplay><\/embed><BR>/isg;
	    $$post =~ s/(\[wmv\])(\S+?\.)(ram|asf|asx|avi|wmv|mpg|mpv|mpeg|dat)(\[\/wmv\])/<b>这个是 Windows Media Player 影片：<\/b><br><object id="videowindow1" width="480" height="330" classid="CLSID:22d6f312-b0f6-11d0-94ab-0080c74c7e95"><param NAME="Filename" value="$2$3"><param name="AUTOSTART" value=$arrawautoplay><\/object><BR>/isg;
	    $$post =~ s/(\[wm=)(\S+?)(\,)(\S+?)(\])(\S+?\.)(ram|asf|asx|avi|wmv|mpg|mpeg|dat)(\[\/wm\])/<b>这个是 Windows Media Player 影片：<\/b><br><object id="videowindow1" width=$2 height=$4 classid="CLSID:22d6f312-b0f6-11d0-94ab-0080c74c7e95"><param NAME="Filename" value="$6$7"><param name="AUTOSTART" value=$arrawautoplay><\/object><BR>/isg;
	} else {
	    $$post =~ s/(\[wma\])(\S+?\.)(ram|wma|wm|mp3|mp2|ra|mpa|mpga)(\[\/wma\])/<b>这个是 Windows Media Player 音乐，点击播放<\/b><BR><a href="$2$3">$2$3<\/a>/isg;
	    $$post =~ s/(\[wmv\])(\S+?\.)(ram|asf|asx|avi|wmv|mpg|mpv|mpeg|dat)(\[\/wmv\])/<b>这个是 Windows Media Player 影片，点击播放<\/b><BR><a href="$2$3">$2$3<\/a>/isg;
	    $$post =~ s/(\[wm=)(\S+?)(\,)(\S+?)(\])(\S+?\.)(ram|asf|asx|avi|wmv|mpg|mpeg|dat)(\[\/wm\])/<b>这个是 Windows Media Player 影片，点击播放<\/b><BR><a href="$6$7">$6$7<\/a>/isg;
	}

        $$post =~ s/\[mms\]\s*mms:\/\/(.*?)\s*\[\/mms\]/<img src=$imagesurl\/images\/music.gif width=16 height=16 alt="WM 类数据流音乐" align=absmiddle> <a href="mms:\/\/$1">mms:\/\/$1<\/a>/isg;
	$$post =~ s/\[mms=\s*mms:\/\/(.*?)\s*\](.*?)\[\/mms\]/<img src=$imagesurl\/images\/music.gif width=16 height=16 alt="WM 类数据流音乐" align=absmiddle> <a href="mms:\/\/$1">$2<\/a>/isg;
        $$post =~ s/\[rtsp\]\s*(rtsp|pnm):\/\/(.*?)\s*\[\/rtsp\]/<img src=$imagesurl\/images\/ra.gif width=16 height=16 alt="Real 类数据流" align=absmiddle> <a href="$1:\/\/$2">$1:\/\/$2<\/a>/isg;
	$$post =~ s/\[rtsp=\s*(rtsp|pnm):\/\/(.*?)\s*\](.*?)\[\/rtsp\]/<img src=$imagesurl\/images\/ra.gif width=16 height=16 alt="Real 类数据流" align=absmiddle> <a href="$1:\/\/$2">$3<\/a>/isg;

        $$post =~ s/\[equote\]\s*(.*?)\s*\[\/equote\]/<BR><TABLE cellSpacing=0 cellPadding=0><TR><TD><IMG src=$imagesurl\/images\/top_l.gif><\/TD><TD background=$imagesurl\/images\/top_c.gif><\/TD><TD><IMG src=$imagesurl\/images\/top_r.gif><\/TD><\/TR><TR><TD vAlign=top background=$imagesurl\/images\/center_l.gif><\/TD><TD bgcolor=#fffff1 style=WORD-WRAP:break-word;>$1<TD vAlign=top background=$imagesurl\/images\/center_r.gif><\/TD><\/TR><TR><TD vAlign=top><IMG src=$imagesurl\/images\/foot_l1.gif ><\/TD><TD background=$imagesurl\/images\/foot_c.gif><IMG src=$imagesurl\/images\/foot_l3.gif><\/TD><TD align=right><IMG src=$imagesurl\/images\/foot_r.gif><\/TD><\/TR><\/TABLE><BR>/isg;
	$$post =~ s/\[fquote\]\s*(.*?)\s*\[\/fquote\]/<BR><table cellSpacing=0 cellPadding=0><tr><td><table cellSpacing=0 cellPadding=0><tr><td><img src=$imagesurl\/images\/top1_l.gif width=83 height=39><\/td><td width=100% background=$imagesurl\/images\/top1_c.gif>　<\/td><td><img src=$imagesurl\/images\/top1_r.gif width=7 height=39><\/td><\/tr><tr><td colSpan=3><table cellSpacing=0 cellPadding=0 width=100%><tr><td vAlign=top background=$imagesurl\/images\/center1_l.gif><img src=$imagesurl\/images\/top1_l2.gif width=11 height=1><\/td><td vAlign=center width=100% bgColor=#fffff1 style=WORD-WRAP:break-word;>$1<\/td><td vAlign=top background=$imagesurl\/images\/center1_r.gif><img src=$imagesurl\/images\/top1_r2.gif width=7 height=2><\/td><\/tr><\/table><\/td><\/tr><tr><td colSpan=3><table cellSpacing=0 cellPadding=0 width=100%><tr><td vAlign=top><img src=$imagesurl\/images\/foot1_l1.gif width=12 height=18><\/td><td width=100% background=$imagesurl\/images\/foot1_c.gif><img src=$imagesurl\/images\/foot1_l3.gif width=1 height=18><\/td><td align=right><img src=$imagesurl\/images\/foot1_r.gif width=8 height=18><\/td><\/tr><\/table><\/td><\/tr><\/table><\/td><\/tr><\/table><BR>/isg;

	$$post =~ s/\[hr\]/<hr width=40% align=left>/isg;
	$$post =~ s/\[b\](.+?)\[\/b\]/<b>$1<\/b>/isg;
	$$post =~ s/\[i\](.+?)\[\/i\]/<i>$1<\/i>/isg;
	$$post =~ s/\[u\](.+?)\[\/u\]/<u>$1<\/u>/isg;
	$$post =~ s/\[font=\s*(.*?)\s*\]\s*(.*?)\s*\[\/font\]/<font face=$1>$2<\/font>/isg;
	$$post =~ s/\[color=(\S+?)\]\s*(.*?)\s*\[\/color\]/<font color=$1>$2<\/font>/isg;
	$$post =~ s/(\[list\])(.+?)(\[\/list\])/<ul>$2<\/ul>/isg;
	$$post =~ s/(\[list=s\])(.+?)(\[\/list\])/<ol type="square">$2<\/ol>/isg;
	$$post =~ s/(\[list=)(A|1|I)(\])(.+?)(\[\/list\])/<OL TYPE=$2>$4<\/OL>/isg;
	$$post =~ s/(\[list=)(\S+?)(])(.+?)(\[\/list\])/ <ol start="$2">$4<\/ol>/isg;
	$$post =~ s/\[\*\]/<li>/isg;
	$$post =~ s/(\[fly\])(.+?)(\[\/fly\])/<marquee width=90% behavior=alternate scrollamount=3>$2<\/marquee>/isg;
	$$post =~ s/(\[s\])(.+?)(\[\/s\])/<s>$2<\/s>/isg;
	$$post =~ s/(\[sup\])(.+?)(\[\/sup\])/<sup>$2<\/sup>/isg;
	$$post =~ s/(\[sub\])(.+?)(\[\/sub\])/<sub>$2<\/sub>/isg;
	$$post =~ s/(\[align=)(left|center|right)(\])(.+?)(\[\/align\])/<DIV Align=$2>$4<\/DIV>/isg;
	$$post =~ s/(\[SHADOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/SHADOW\])/<table width=$2 style="filter:shadow\(color=$4\, direction=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
	$$post =~ s/(\[GLOW=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/GLOW\])/<table width=$2 style="filter:glow\(color=$4\, strength=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
	$$post =~ s/(\[BLUR=)(\S+?)(\,)(.+?)(\,)(.+?)(\])(.+?)(\[\/BLUR\])/<table width=$2 style="filter:blur\(Add=0, direction=$4\, strength=$6)"><tr><td>$8<\/td><\/tr><\/table>/isg;
	$$post =~ s/(\[FLIPH\])(.+?)(\[\/FLIPH\])/<table style="filter:flipH"><tr><td>$2<\/td><\/tr><\/table>/isg;
	$$post =~ s/(\[FLIPV\])(.+?)(\[\/FLIPV\])/<table style="filter:flipV"><tr><td>$2<\/td><\/tr><\/table>/isg;
	$$post =~ s/(\[INVERT\])(.+?)(\[\/INVERT\])/<table style="filter:invert"><tr><td>$2<\/td><\/tr><\/table>/isg;
	$$post =~ s/(\[xray\])(.+?)(\[\/xray\])/<table style="filter:xray"><tr><td>$2<\/td><\/tr><\/table>/isg;
	$$post =~ s/(\[MOVE\])(.+?)(\[\/Move\])/<MARQUEE scrollamount=3>$2<\/MARQUEE>/isg;
#	$$post =~ s/<\/MARQUEE>(.{1,40})<\/td><\/tr><\/table>/<\/MARQUEE>$1/isg;
	$$post =~ s/\[code(=.*?)?\](.+?)\[\/code\]/<br><table cellpadding=0 cellspacing=0 width=94% bgcolor=#000000 align=center style=table-layout:fixed><tr><td><table width=100% cellpadding=5 cellspacing=1 style=table-layout:fixed><tr><td bgColor=$quoteback style=\"left: 0px; width: 100%; word-wrap: break-word\">代码：<hr size=1><code>$2<\/code><\/td><\/tr><\/table><\/td><\/tr><\/table><br>/isg;

    return;
}

sub smilecode {
    my $post = shift;
    study($$post);
    unless ($subsmilecode) {
	if (open(FILE, "${lbdir}data/emoticons.pl")) {
  	    sysread(FILE, $subsmilecode,(stat(FILE))[7]);
	    close(FILE);
	    $subsmilecode =~ s/\r//isg;
	}
    }
    eval($subsmilecode);
    return;
}

sub doemoticons {
    my $post = shift;
    study($$post);
    return unless ($$post =~ /\:.{1,20}\:/);

    unless ($emoticoncode) {
	if (open(FILE, "${lbdir}data/emot.pl")) {
	    $emoticoncode = <FILE>;
	    close(FILE);
	}
    }
    eval($emoticoncode);
    return;
}

1;
