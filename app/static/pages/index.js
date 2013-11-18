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
			if (!(curMax == 21 && max == 11)) {
				alert("Max Score Madness?! cur="+curMax+"; max="+max);
			}
			$("#first_player_score_id option:gt("+max+")").remove();
			$("#second_player_score_id option:gt("+max+")").remove();
		} else if (max > curMax) {
			if (!(curMax == 11 && max == 21)) {
				alert("Max Score Madness?! cur="+curMax+"; max="+max);
			}
			for(var i=Number(curMax)+1;i<=max;i++){
				$("#first_player_score_id").append(
					"<option value='"+i+"'>"+i+"</option>");
				$("#second_player_score_id").append(
					"<option value='"+i+"'>"+i+"</option>");
			}
		}
	});

	//------------------------------
	//
	// Exposure
	//
	//------------------------------

}(window.jQuery));

