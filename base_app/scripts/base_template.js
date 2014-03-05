$(function() {
	

	$('#login_button').off('click.login').on('click.login', function() {

		console.log('hey')

		$('#login_button').loadmodal({
			id: 'login_modal',
			title: 'Login',
			url: '/account/login/',
			width: '400px',
			

		});//loadmodals
		

	});//click

});//ready