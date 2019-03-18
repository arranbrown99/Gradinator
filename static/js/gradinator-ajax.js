$('#enrol-btn').click(function(){
	var courseid;
	courseid = $(this).attr("data-catid");
	$.get('/gradinator/enrol_to_course/', {course_id: courseid}, function(data){
		$('#added').html(data);
		$('#enrol-btn').hide();
	});
});
