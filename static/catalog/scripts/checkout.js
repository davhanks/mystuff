$(function() {
    $( "#datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2018",
      // You can put more options here.

    });

    $('.use_same').click(function() {
    	var first_name = $('#id_ship_first').val()
    	var last_name = $('#id_ship_last').val()
    	var street = $('#id_ship_street').val()
    	var street2 = $('#id_ship_street2').val()
    	var city = $('#id_ship_city').val()
    	var state = $('#id_ship_state').val()
    	var zipcode = $('#id_ship_zipCode').val()

    	
    	$('#id_bill_first').val(first_name);
    	$('#id_bill_last').val(last_name);
    	$('#id_bill_street').val(street);
    	$('#id_bill_street2').val(street2);
    	$('#id_bill_city').val(city);
    	$('#id_bill_state').val(state);
    	$('#id_bill_zipCode').val(zipcode);

    	$('#id_first_name').val(first_name);
    	$('#id_last_name').val(last_name);
    });


    $('.clear').click(function() {
    	$('#id_ship_first').val('');
    	$('#id_ship_last').val('');
    	$('#id_ship_street').val('');
    	$('#id_ship_street2').val('');
    	$('#id_ship_city').val('');
    	$('#id_ship_state').val('');
    	$('#id_ship_zipCode').val('');

    	$('#id_bill_first').val('');
    	$('#id_bill_last').val('');
    	$('#id_bill_street').val('');
    	$('#id_bill_street2').val('');
    	$('#id_bill_city').val('');
    	$('#id_bill_state').val('');
    	$('#id_bill_zipCode').val('');

    	$('#id_first_name').val('');
    	$('#id_last_name').val('');
    });
  });