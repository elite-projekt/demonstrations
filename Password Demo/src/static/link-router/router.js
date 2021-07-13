$(function() {
	'use strict';
    $("#pw-info").click(function() {

        window.open("http://portal.ecs.fbi.h-da.de/courses/password/units/save-passwords/parts#2","_blank");

    });

    $("#phrase-info").click(function() {

        window.open("http://portal.ecs.fbi.h-da.de/courses/password/units/algorithms-for-secure-password-construction/parts#1","_blank");

    });

    $("#2FA-info").click(function() {

        window.open("http://portal.ecs.fbi.h-da.de/courses/password/units/two-factor-authentication/parts","_blank");

    });

    $("#pw-unit").click(function() {

        window.open("http://portal.ecs.fbi.h-da.de/courses/password/units","_blank");

    });
    $("#2FA-for-iOS").click(function() {

        window.open("https://apps.apple.com/de/app/2fa-authenticator-2fas/id1217793794","_blank");

    });
    $("#2FA-for-Android").click(function() {

        window.open("https://play.google.com/store/apps/details?id=com.twofasapp&amp;hl=de&amp;gl=US","_blank");

    });

    if($("2FA-info").has("a")){
        $("2FA-info").attr("href","http://portal.ecs.fbi.h-da.de/courses/password/units/two-factor-authentication/parts");
        $("2FA-info").attr("type","_blank");
    }

});