var frm = $('#enrol_btn');
frm.submit(function () {
	courseid = $(this).attr("data-courseid");
	$('#enrol_btn').hide();
	$.ajax({
		type: frm.attr('method'),
		url: frm.attr('action'),
		data: frm.serialize(),
		success: function (data) {
			$(this).hide();
			
		},
		error: function(data) {
			$("#added").html("Something went wrong!");
		}
	}
	);
	return false;
});


