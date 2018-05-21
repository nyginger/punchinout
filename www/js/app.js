





var app_url="http://192.168.111.202:8400" ;  
document.addEventListener("deviceready", onDeviceReady, false);
function onDeviceReady() {
    console.log(device.cordova);
}
window.onload= function () {
    document.getElementById("search").setAttribute("href", app_url + "/search?query=" + device.uuid);
    document.getElementById("phone_uuid").value=device.uuid;

};

function updatetime1(){
    
    document.getElementById("io").value="In";
    //document.getElementById("time_rec").value= moment().format('YYYY-MM-DD HH:mm:ss');
    updatetime();
}

function updatetime2(){
    
    document.getElementById("io").value="Out";
    //document.getElementById("time_rec").value= 
    updatetime();
    
}
function updatetime(){
    var dt_phoneserial=device.uuid;
    $.getJSON(app_url + '/api/person?q={"filters":[{"name":"phoneserial","op":"equals","val":"' + dt_phoneserial + '"}]}')
        .done(function(data){
            var items=data.objects[0];
            document.getElementById("personName").value=items.person_name;
            var curtime = moment().format('YYYY-MM-DD HH:mm:ss');
            document.getElementById("time_rec").value=curtime
            var dt_in_out =$("#io").val();
            var dt_person =items.person_name;
            $.ajax({
                type: "POST",
                url: app_url + "/api/time_checked",
                data: JSON.stringify({
                    phoneserial: dt_phoneserial,
                    person_name: dt_person,
                    time_recorded : curtime,
                    in_out: dt_in_out
                } ),
                dataType: "json",
                contentType : "application/json"
                })
                .done(function(){
                    if (dt_in_out=='In'){
                        alert('출근처리 되었습니다!\nSuccess!'); 
                    } else {
                        alert('퇴근처리 되었습니다!\nSuccess!'); 
                    }
                    
                })
                .fail(function(){alert('입력 실패되었습니다.재시도하세요.\nFailed.Please retry.');});
        })
        .fail(function(){
            alert('등록되어 있지 않습니다.\nPhone info is unavailable.');
        });
    

}


