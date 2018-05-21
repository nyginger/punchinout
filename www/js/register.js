





var app_url="http://192.168.111.202:8400" ;  
document.addEventListener("deviceready", onDeviceReady, false);
function onDeviceReady() {
    console.log(device.cordova);
}
window.onload= function () {
    document.getElementById("search").setAttribute("href", app_url + "/search?query=" + device.uuid);
    document.getElementById("phone_uuid").value=device.uuid;
};

function perRegister(){
    var dt_phoneserial=device.uuid;
    $.getJSON(app_url + '/api/person?q={"filters":[{"name":"phoneserial","op":"equals","val":"' + dt_phoneserial + '"}]}')
        .done(function(data){
            var chkcnt=data.num_results;
            if (chkcnt!=0){
                var items=data.objects[0];
                document.getElementById("perName").value=items.person_name;
                alert('이미 등록되어 있습니다.\nPhone info pre-existed.');
            } else {
                postRegister();
            }

        });
}

function postRegister(){
    var dt_phoneserial=device.uuid;
    var dt_person =document.getElementById("perName").value;
    $.ajax({
        type: "POST",
        url: app_url + "/api/person",
        data: JSON.stringify({
            phoneserial: dt_phoneserial,
            person_name: dt_person
        }),
        dataType: "json",
        contentType : "application/json"
        })
        .done(function(){
            timeRegister();
        })
        .fail(function(){
            alert('등록에 실패하였습니다.재시도하세요.\nRegistration failed.Please retry.');
        });

}

function timeRegister(){
    var dt_phoneserial=device.uuid;
    var dt_person =document.getElementById("perName").value;
    var curtime = moment().format('YYYY-MM-DD HH:mm:ss');
    var dt_in_out = 'Register';
    $.ajax({
        type: "POST",
        url: app_url + "/api/time_checked",
        data: JSON.stringify({
            phoneserial: dt_phoneserial,
            person_name: dt_person,
            time_recorded : curtime,
            in_out : dt_in_out
        }),
        dataType: "json",
        contentType : "application/json"
        })
        .done(function(){
            alert('등록하였습니다.\nRegistration succeeded!');
        });

}
    

