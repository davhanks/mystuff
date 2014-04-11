$(function() {
    $(".status").each(function() {
    	var print = $(this).html()
    	console.log(print);
    	
    	var suc = $(this).find(".label-success").html()

    	if (typeof suc == undefined) {
    		$('btn-checkout').css("visibility","hidden");
    	}
    	console.log(suc);
    });
  });