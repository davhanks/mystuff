$(function() {
	$('.delete_button').click( function() {
		$.ajax({
			url: '/catalog/cart__remove/' + $(this).attr('data-id'),
			success: function(data) {
				$('.modal-body').html(data);
			},
		})

	});// click


	$(".shade").hover(function() {
		$(this).css({"background-color":"rgba(0,0,0,0.1)"});
	},function(){
		$(this).css({"background-color":"rgba(255,255,255,1)"});
	}); //hover function


});//ready