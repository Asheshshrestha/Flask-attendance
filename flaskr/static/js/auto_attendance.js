
(function () {
    $.AutoAttendanceManageObj = function () {

        var AutoAttendanceManage = {

            init: function () {
                AutoAttendanceManage.InitUIEvents();
            },

            InitUIEvents: function () {
                $("#start_stream").click(function () {
                    let $this = $(this);
                    $.confirm({
                        title: 'Confirm!',
                        content: 'Are you sure want to take attendance?',
                        type: 'yellow',
                        typeAnimated: true,
                        buttons: {
                            yes: {
                                text: 'Yes',
                                btnClass: 'btn-success',
                                action: function () {
                                    $("#video_feed").attr("src", video_feed_url);
                                    $this.hide();
                                    $("#stop_stream").show();
                                }
                            },
                            close: {
                                text: 'Cancel',
                                btnClass: 'btn-danger',
                                action: function () {
            
                                }
                            }
                        }
                    });
            
                });
            
                $("#stop_stream").click(function () {
                    
                    let $this = $(this);
                    $.confirm({
                        title: 'Confirm!',
                        content: 'Are you sure want to stop take attendance?',
                        type: 'red',
                        typeAnimated: true,
                        buttons: {
                            yes: {
                                text: 'Yes',
                                btnClass: 'btn-success',
                                action: function () {
                                    $("#video_feed").attr("src", no_video_url);
                                    AutoAttendanceManage.GetStudent();
                                    AutoAttendanceManage.ToggleForms('list');
                                }
                            },
                            close: {
                                text: 'Cancel',
                                btnClass: 'btn-danger',
                                action: function () {
            
                                }
                            }
                        }
                    });
                });

            },

            GetStudent: function(){
                $.ajax({
                    url: '/automatic_attendance/stop_taking_attendance',
                    type: 'GET',
                    data: {},
                    success: AutoAttendanceManage.GetStudentResponse,
                    error: function(xhr, status, error) {
                        console.error('Error:', error);
                    }
                });
            },
            GetStudentResponse:function(data){
                if(data != null){
                    if(data.length > 0 ){
                        html  = '';
                        $.each(data,function(index,item){
                            let snapshot = '/static/img/images.png';
                            let checked = '';
                            if(item.status == 'present')
                            {
                                snapshot = `/ml/snapshots/${item.id}_${item.confidence}.jpg`;
                                checked = 'checked';
                            }
                            
                            html += ` <tr>
                                            <td>${item.id}</td>
                                            <td><img src="${snapshot}" height=80 width=80 alt="..." class="img-thumbnail" heigh></td>
                                            <td>${item.first_name} ${item.last_name}</td>
                                            <td>${item.status}</td>
                                            <td>${item.confidence}</td>
                                            <td>
                                            <div class="form-group">
                                                <div class="form-check">
                                                <input class="form-check-input student-cb" data-id="${item.id}" type="checkbox" value="" id="cbPresent-${item.id}" ${checked}>
                                                <label class="form-check-label" for="cbPresent-${item.id}">
                                                    Present?
                                                </label>
                                                </div>
                                            </div>
                                            </td>
                                        </tr>`
                        });
                        $('#div_student_list').html(html);
                    }
                }
            },

            ToggleForms: function (type = 'preview') {
                $('.camera-preview').hide();
                $('.attendance-list').hide();
                switch (type) {
                    case 'preview': $('.camera-preview').show(); break;
                    case 'list': $('.attendance-list').show(); break;
                    default: break;
                }
            },
        }
        AutoAttendanceManage.init();
    }

    $.fn.AutoAttendanceManageFn = function () {
        $.AutoAttendanceManageObj();
    }
}(jQuery))