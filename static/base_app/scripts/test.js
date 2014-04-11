$(function() {
	//login button
	$('#gettime_button').off('click.gettime').on('click.gettime', function(evt) {
		console.log('hey')
		$.ajax({

			url: '/account/example/',
			success: function(data) {

				$('#server_time').html(data);
			},
		});
	});

});