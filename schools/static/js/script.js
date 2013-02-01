$(document).on('ready',init);
function init(){
	callDep();
	callRequiredCheck()
}

function callRequiredCheck (argument) {
	$(document).on('submit',checkRequired)
}

function checkRequired () {
	if( $('#reporte input:checked').length == 0 )
	{

		alert('Seleccione los campos que apareceran en el reporte')
		return false;
	}
}

function callAjax(valor){
	$.ajax({
		type: "POST",
		url: "/departamento",
		data: { departamento: valor }
	})
		.done(function( msg ) {
			$('#municipio').html('<option>--------------</option>')
			$('#municipio').append(msg)
		});
}
function callDep () {
	$("#departamento").click( function(){ 
		var result  = 	$(this).find(':selected');
		var valor 	=	$(result[0]).attr('data-id');
		console.log(valor)
		callAjax(valor);
	});
}