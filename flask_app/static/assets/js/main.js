(function ($) {
	"use strict";
	
	/*----------------------------
    Responsive menu Active
    ------------------------------ */
	$(".mainmenu ul#primary-menu").slicknav({
		allowParentLinks: true,
		prependTo: '.responsive-menu',
	});
	
	/*----------------------------
    START - Scroll to Top
    ------------------------------ */
	$(window).on('scroll', function() {
		if ($(this).scrollTop() > 600) {
			$('.scrollToTop').fadeIn();
		} else {
			$('.scrollToTop').fadeOut();
		}
	});
	$('.scrollToTop').on('click', function () {
		$('html, body').animate({scrollTop : 0},2000);
		return false;
	});
	$('.menu-area ul > li > .theme-btn').on('click', function () {
		$('.buy-ticket').show();
		return false;
	});
	$('.slide-trailor > .loggedUser > .theme-btn').on('click', function () {
		$('.buy-ticket').show();
		return false;
	});
	$('.slide-trailor > .theme-btn').on('click', function () {
		$('.login-area').show();
		return false;
	});
	
	$('.buy-ticket .buy-ticket-area > a').on('click', function () {
		$('.buy-ticket').hide();
		return false;
	});
	$('.login-popup').on('click', function () {
		$('.login-area').show();
		return false;
	});
	$('.login-box > a').on('click', function () {
		$('.login-area').hide();
		return false;
	});
	// REGISTER
	$('.register-popup').on('click', function () {
		$('.register-area').show();
		$('.login-area').hide();
		return false;
	});
	$('.register-box > a').on('click', function () {
		$('.register-area').hide();
		return false;
	});
	// New Movie
	$('.movie-popup').on('click', function () {
		$('.movie-area').show();
		$('.movie-area').hide();
		return false;
	});
	/*----------------------------
    START - Slider activation
    ------------------------------ */
	var heroSlider = $('.hero-area-slider');
	heroSlider.owlCarousel({
		loop:true,
		dots: true,
		autoplay: false,
		autoplayTimeout:4000,
		nav: false,
		items: 1,
		responsive:{
			992:{
				dots: false,
			}
		}
	});
	heroSlider.on('changed.owl.carousel', function(property) {
		var current = property.item.index;
		var prevRating = $(property.target).find(".owl-item").eq(current).prev().find('.hero-area-slide').html();
		var nextRating = $(property.target).find(".owl-item").eq(current).next().find('.hero-area-slide').html();
		$('.thumb-prev .hero-area-slide').html(prevRating);
		$('.thumb-next .hero-area-slide').html(nextRating);
	});
	$('.thumb-next').on('click', function() {
		heroSlider.trigger('next.owl.carousel', [300]);
		return false;
	});
	$('.thumb-prev').on('click', function() {
		heroSlider.trigger('prev.owl.carousel', [300]);
		return false;
	});
	var newsSlider = $('.news-slider');
	newsSlider.owlCarousel({
		loop:true,
		dots: true,
		autoplay: false,
		autoplayTimeout:4000,
		nav: false,
		items: 1,
		responsive:{
			992:{
				dots: false,
			}
		}
	});
	newsSlider.on('changed.owl.carousel', function(property) {
		var current = property.item.index;
		var prevRating = $(property.target).find(".owl-item").eq(current).prev().find('.single-news').html();
		var nextRating = $(property.target).find(".owl-item").eq(current).next().find('.single-news').html();
		$('.news-prev .single-news').html(prevRating);
		$('.news-next .single-news').html(nextRating);
	});
	$('.news-next').on('click', function() {
		newsSlider.trigger('next.owl.carousel', [300]);
		return false;
	});
	$('.news-prev').on('click', function() {
		newsSlider.trigger('prev.owl.carousel', [300]);
		return false;
	});
	var videoSlider = $('.video-slider');
	videoSlider.owlCarousel({
		loop:true,
		dots: true,
		autoplay: false,
		autoplayTimeout:4000,
		nav: false,
		responsive:{
			0:{
				items: 1,
				margin: 0
			},
			576:{
				items: 2,
				margin: 30
			},
			768:{
				items: 3,
				margin: 30
			},
			992:{
				items: 4,
				margin: 30
			}
		}
	});
	
	/*----------------------------
	START - videos popup
	------------------------------ */
	$('.popup-youtube').magnificPopup({type:'iframe'});
	//iframe scripts
	$.extend(true, $.magnificPopup.defaults, {  
		iframe: {
			patterns: {
				//youtube videos
				youtube: {
					index: 'youtube.com/', 
					id: 'v=', 
					src: 'https://www.youtube.com/embed/%id%?autoplay=1' 
				}
			}
		}
	});
	
	/*----------------------------
    START - Isotope
    ------------------------------ */
    jQuery(".portfolio-item").isotope();
    $(".portfolio-menu li").on("click", function(){
      $(".portfolio-menu li").removeClass("active");
      $(this).addClass("active");
      var selector = $(this).attr('data-filter');
      $(".portfolio-item").isotope({
        filter: selector
      })
    });
	
	/*----------------------------
    START - Preloader
    ------------------------------ */
	jQuery(window).load(function(){
		jQuery("#preloader").fadeOut(500);
	});
	

}(jQuery));

let tickets = []

function changeCol(e) {
	// console.log(document.getElementsByClassName("tickets").length);
	if (document.getElementsByClassName("tickets").length < 5 && e.classList.contains('tickets') == false) {
		document.getElementById("error").innerHTML = "";
		tickets.push(e.innerHTML);
		e.classList.add("active");
		e.classList.add("tickets");
		// console.log(tickets);
	}
	else if (e.classList.contains('tickets') == true) {
		e.classList.remove("active");
		e.classList.remove("tickets");
		for(let i = 0; i < tickets.length; i++){
			if(tickets[i] == e.innerHTML){
				tickets.splice(i, 1)
			}
		}
		// tickets.splice(e.innerHTML)
	}
	if (document.getElementsByClassName("tickets").length > 5) {
	document.getElementById("error").innerHTML ="*You can not select more than 5 tickets";
		e.classList.remove("active");
    e.classList.remove("tickets");
	tickets.push(e.innerHTML)
	}
	
}

// console.log(tickets);
// var form = new Array(tickets);
// console.log(form);
async function book_tickets() {
		let movie_id = document.getElementById('movie').innerHTML;
		// var form = new Array(tickets.length);
		let form = tickets;
		console.log(form);
		// console.log(all);
		fetch("http://127.0.0.1:5000/book_tickets/"+movie_id, {
		method: "POST",
		body: form,
		})
		.then((response) => response.json())
		.then((data) => console.log(data));
		document.getElementById("error").innerHTML =
		"*Tickets are succesfully booked";
		setTimeout(location.reload.bind(location), 5000);
};

// function booking(){
// 	let form = tickets;
// 	let movie_id = document.getElementById('movie').innerHTML;
// 	console.log(form);
// 	console.log(movie_id);
// 	document.getElementById("error").innerHTML = "*Tickets are succesfully booked";
// }