$(function() {
    $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true
    });

    $('.ui-datepicker-calendar:second').addClass("cardDate");



    $('.datepicker2').datepicker( {
	    changeMonth: true,
	    changeYear: true,
	    showButtonPanel: true,
	    dateFormat: 'MM yy',
	    onClose: function(dateText, inst) { 
	        var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
	        var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
	        $(this).datepicker('setDate', new Date(year, month, 1));
	    }
	});

});