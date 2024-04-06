$(document).ready(function() {
    let $validator = $('#form1').validate({
        errorElement: 'div', // Change the error element to a div
        errorClass: 'invalid-feedback', // Bootstrap 4 class for styling error messages
        rules: {
            slcBatch: { selectcheck: true },
            slcCourse: { selectcheck: true },
            slcSubject: { selectcheck: true },
            slcAttendanceDate: { required: true},


        },
        messages: {
            slcBatch: { selectcheck: "* required" },
            slcCourse: { selectcheck: "* required" },
            slcSubject: { selectcheck: "* required" },
            slcAttendanceDate: { required: "* required" },


        }
    });
    jQuery.validator.addMethod('selectcheck', function (value) {
        return (value != '0' && value.length > 0);
    }, "*");

    $('#btnSearch').off('click').on('click',function(){
        if($validator.form()){
            check_attendande()
        }
    });
    $('#btnTakeAttendance').off('click').on('click',function(){
        if($validator.form()){
            get_students()
        }


    });
    function get_students(){
        var batch_id = $('#slcBatch option:selected').val();
        var course_id = $('#slcCourse option:selected').val();
        var subject_id = $('#slcSubject option:selected').val();
        var attendance_date = $('#slcAttendanceDate').val();
        $.ajax({
            url: '/attendance/getstudents',
            type: 'GET',
            data: {
                batch_id: batch_id,
                course_id: course_id,
                subject_id: subject_id,
                attendance_date: attendance_date,
            },
            success: get_students_response,
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }
    function get_students_response(data){
        console.log(data);
        if(data != null){
            let html = '';
           $.each(data,function(index,item){
            html += `<tr>
                    <td>${item.id}</td>
                    <td>${item.first_name} ${item.last_name}</td>
                    <td>
                    <div class="form-group">
                        <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="cbPresent-${item.id}">
                        <label class="form-check-label" for="cbPresent-${item.id}">
                            Present?
                        </label>
                        </div>
                    </div>
                    </td>

                    </tr>`;

           });
           $('#div_student_list').html(html);
           $('#staticBackdrop').modal('hide');
        }
       
    }

    function check_attendande(){
        var batch_id = $('#slcBatch option:selected').val();
        var course_id = $('#slcCourse option:selected').val();
        var subject_id = $('#slcSubject option:selected').val();
        var attendance_date = $('#slcAttendanceDate').val();
        $.ajax({
            url: '/attendance/checkattendance',
            type: 'GET',
            data: {
                batch_id: batch_id,
                course_id: course_id,
                subject_id: subject_id,
                attendance_date: attendance_date,
            },
            success: check_attendande_response,
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }
    function check_attendande_response(data){
        console.log(data);
        if(data != null){
            $('#divCheckMessage').text(data.message);
            $('#staticBackdrop').modal('show');
        }
       
    }

  });