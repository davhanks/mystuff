$(function() {
	

	$('#login_button').off('click.login').on('click.login', function() {

		console.log('hey')

		$('#login_button').loadmodal({
			id: 'login_modal',
			title: 'Login',
			url: '/account/login/',
			width: '400px',
			

		});//loadmodal
		

	});//click


	$('#cart_button').click( function() {

		console.log('hey')

		$('#cart_button').loadmodal({
			id: 'cart_modal',
			title: 'MyCart',
			url: '/catalog/cart/',
			width: '1000px',
			

		});//loadmodal
		

	});//click


	$('#rental_button').click( function() {

		console.log('hey')

		$('#rental_button').loadmodal({
			id: 'cart_modal',
			title: 'MyRentals',
			url: '/catalog/rentalcart/',
			width: '700px',
			

		});//loadmodal
		

	});//click

});//ready