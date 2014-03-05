console.log('asdfasdf')

$(function() {
	console.log($('#login_button').length);

	$('#login_button').off('click.login').on('click.login', function() {
		console.log('asdf');
		$('#login_button').loadmodal({
			id: 'login_modal',
			title: 'Login',
			url: '/account/login/',

		});//loadmodal
		

	});//click

});//ready