var frm = $('#enrol_btn');
frm.submit(function () {
	courseid = $(this).attr("data-courseid");

	$.ajax({
		type: frm.attr('method'),
		url: frm.attr('action'),
		data: frm.serialize(),
		success: function (data) {
			$('#enrol_btn').hide();
			
		},
		error: function(data) {
			$("#added").html("Something went wrong!");
		}
	}
	);
	return false;
});


