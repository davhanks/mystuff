$(function() {
	$(".thumbnail").hover(function() {
		$(this).css({"background-color":"rgba(0,0,0,0.4)"});
	},function(){
		$(this).css({"background-color":"rgba(255,255,255,1)"});
	}); //hover function

	$(".thumbnail").hover(function() {
		$('h3').css({"color":"#fff"});
	},function(){
		$('h3').css({"color":"black"});
	});//hover

	$(".thumbnail").hover(function() {
		$('h4').css({"color":"#fff"});
	},function(){
		$('h4').css({"color":"black"});
	});//hover

}); //Ready