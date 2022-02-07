$(function() {
	'use strict';
    $("#pw-info").click(function() {

        window.open("https://portal.ecs.fbi.h-da.de/courses/password/units/why-do-we-need-secure-passwords/parts#0","_blank");

    });
        $("#pw-info-de").click(function() {

        window.open("https://portal.ecs.fbi.h-da.de/kurse/passwort/einheiten/warum-brauchen-wir-sichere-passwoerter/teile#0","_blank");

    });

    $("#phrase-info").click(function() {

        window.open("https://portal.ecs.fbi.h-da.de/courses/password/units/how-to-generate-secure-passwords/parts#0","_blank");

    });

    $("#phrase-info-de").click(function() {

    window.open("https://portal.ecs.fbi.h-da.de/kurse/passwort/einheiten/wie-erstellt-man-ein-sicheres-passwort/teile#0","_blank");

    });

    $("#2FA-info").click(function() {

        window.open("https://portal.ecs.fbi.h-da.de/courses/password/units/multi-factor-authentication/parts#0","_blank");

    });

    $("#2FA-info-de").click(function() {

    window.open("https://portal.ecs.fbi.h-da.de/kurse/passwort/einheiten/multi-faktor-authentifizierung/teile#0","_blank");

    });

    $("#pw-unit").click(function() {

        window.open("http://portal.ecs.fbi.h-da.de/courses/password/units","_blank");

    });
    $("#pw-einheit").click(function() {

    window.open("https://portal.ecs.fbi.h-da.de/kurse/passwort/einheiten","_blank");

    });
    $("#2FA-for-iOS").click(function() {

        window.open("https://apps.apple.com/en-us/app/2fa-authenticator-2fas/id1217793794","_blank");

    });
    $("#2FA-for-iOS-de").click(function() {

        window.open("https://apps.apple.com/de/app/2fa-authenticator-2fas/id1217793794","_blank");

    });
    $("#2FA-for-Android").click(function() {

        window.open("https://play.google.com/store/apps/details?id=com.twofasapp&amp;hl=de&amp;gl=US","_blank");

    });
    $("#2FA-for-Android-de").click(function() {

        window.open("https://play.google.com/store/apps/details?id=com.twofasapp&amp;hl=de&amp;gl=DE","_blank");

    });

    if($("2FA-info").has("a")){
        $("2FA-info").attr("href","https://portal.ecs.fbi.h-da.de/courses/password/units/multi-factor-authentication/parts#0");
        $("2FA-info").attr("type","_blank");
    }
    if($("2FA-info-de").has("a")){
        $("2FA-info-de").attr("href","https://portal.ecs.fbi.h-da.de/kurse/passwort/einheiten/multi-faktor-authentifizierung/teile#0");
        $("2FA-info-de").attr("type","_blank");
    }
});