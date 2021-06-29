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
		} else {
		  input.attr("type", "password");
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
});