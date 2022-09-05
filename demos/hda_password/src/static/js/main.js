$(function() {
	'use strict';

  $('.form-control').on('input', function() {
	  var $field = $(this).closest('.form-group');
	  if (this.value) {
	    $field.addClass('field--not-empty');
	  } else {
	    $field.removeClass('field--not-empty');
	  }
	});

	$(".toggle-password").click(function() {

		$(this).toggleClass("icon-eye icon-eye-slash");
		var input = $($(this).attr("toggle"));
		if (input.attr("type") == "password") {
		  input.attr("type", "text");
		  $(this).attr("title","click the eye for hiding the password.");
		} else {
		  input.attr("type", "password");
		  $(this).attr("title","click the eye for showing the password.");
		}
	  });

	$(".toggle-passwort").click(function() {
	$(this).toggleClass("icon-eye icon-eye-slash");
	var input = $($(this).attr("toggle"));
	if (input.attr("type") == "password") {
	  input.attr("type", "text");
	  $(this).attr("title","klicken Sie auf das Auge, um das Passwort zu verbergen.");
	} else {
	  input.attr("type", "password");
	  $(this).attr("title","klicken Sie auf das Auge, um das Passwort anzuzeigen.");
	}
  });
	
	$('#pwd-requirements').on('click',function(){
		$('#pwd-card-icon').toggleClass("icon-chevron-down icon-chevron-up");
		var card_text = $('#pwd-req-body');
		card_text.toggleClass("collapse collapse.show");
	})
	$('#tipp').on('click',function(){
		$('#tipp-card-icon').toggleClass("icon-chevron-down icon-chevron-up");
		var card_text = $('#tipp-body');
		card_text.toggleClass("collapse collapse.show");
	})
	$(".close").click(function() {

		$('#toast').removeClass("display");
		$('#toast').removeClass("fade");
		$('#toast').removeClass("show");

	  });
	 

	if($('#name').val()){
		$('#name_field').addClass('field--not-empty');
	}
	else{
		$('#name_field').removeClass('field--not-empty');
	}
	if($('#password').val()){
		$('#password_field').addClass('field--not-empty');
	}
	else{
		$('#password_field').removeClass('field--not-empty');
	}
});