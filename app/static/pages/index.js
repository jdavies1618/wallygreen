/**
 * Index page
 *
 * Copyright (c) 2012 Knewton
 * Dual licensed under:
 *  MIT: http://www.opensource.org/licenses/mit-license.php
 *  GPLv3: http://www.opensource.org/licenses/gpl-3.0.html
 */
/*jslint browser: true, maxerr: 50, indent: 4, maxlen: 79 */
(function ($) {
	"use strict";

	//------------------------------
	//
	// Constants
	//
	//------------------------------

	//------------------------------
	//
	// Properties
	//
	//------------------------------

	//------------------------------
	//
	// Methods
	//
	//------------------------------

	//------------------------------
	//
	// Event bindings
	//
	//------------------------------
	$("#maxScore").change(function() {
		var max = $(this).val();
		var curMax = $("#first_player_score_id option:last").val();
		if (curMax > max) {
			$("#first_player_score_id option:gt("+max+")").remove();
			$("#second_player_score_id option:gt("+max+")").remove();
		} else if (max > curMax) {
			for(var i=Number(curMax)+1;i<=max;i++){
				$("#first_player_score_id").append(
					"<option value='"+i+"'>"+i+"</option>");
				$("#second_player_score_id").append(
					"<option value='"+i+"'>"+i+"</option>");
			}
		}
	});

	$(document).ready(function() {
		jQuery.validator.addMethod("player_id", function( value, element ) {
			var result = $("#second_player_id").val() !== $("#first_player_id").val();
			return result;
		}, "Players must have different ids.");
		jQuery.validator.addMethod("scores", function (value, element ) {
			var fp_score = $("#first_player_score_id").val()
			var sp_score = $("#second_player_score_id").val()
			var max_score = $("#maxScore").val()
			var result = (fp_score !== sp_score && (fp_score === max_score || sp_score === max_score));
			return result;
		}, "One player must have the max score, and both players must have different scores.");
		$("#score-form").validate({});
	});


	//------------------------------
	//
	// Exposure
	//
	//------------------------------

}(window.jQuery));

