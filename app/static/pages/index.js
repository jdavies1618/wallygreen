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
			var result = this.optional(element) || $("#second_player_id").val() !== $("#first_player_id").val();
			return result;
		}, "Players must have different ids.");
		jQuery.validator.addMethod("scores", function (value, element ) {
			var result = this.optional(element) || (
							$("#first_player_score_id").val() === $("#maxScore").val() ||
						 	$("#second_player_score_id").val() === $("#maxScore").val());
			return result;
		}, "One player must have the max score.");
		$("#score-form").validate({});
	});


	//------------------------------
	//
	// Exposure
	//
	//------------------------------

}(window.jQuery));

