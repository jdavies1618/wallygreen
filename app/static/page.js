/**
 * Knewton Labs
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

	$(".trigger-shade").live("click", function () {
		var s = $(this).parents(".shade");
		s.toggleClass("active");
	});

	$("body").live("click", function (e) {
		if ($(e.target).parents(".shade.active").length) {
			return;
		}

		$(".shade.active").removeClass("active");
	});

	//------------------------------
	//
	// Exposure
	//
	//------------------------------

}(window.jQuery));

