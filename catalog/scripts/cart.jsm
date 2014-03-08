$(function() {
	$('.delete_button').click( function() {
		$.ajax({
			url: '/catalog/cart__remove/' + $(this).attr('data-id'),
			success: function(data) {
				$('.modal-body').html(data);
			},
		})

	});// click
});//ready