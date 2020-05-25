$('#id_province').select2();

$('#id_city').prop('readonly', true);

$('#id_province').change(function(){
var province = $(this).val()
    if(province =="" || province=="---------"){
        $('#id_city').prop("readonly", true);
    }
    else{
        $.ajax({
        method: 'GET',
        url:'http://127.0.0.1:8000/register/city/api/'+province,
            success:function(data){
                var select = $('#id_city');
                select.prop("readonly", false);
                select.empty();
                select.append("<option value=''>---Select City---</option>");
                for (var j = 0; j < data.length; j++){
                        console.log(data[j].name + "--" + data[j].id);
                        $("#id_city").append("<option value='" +data[j].id+ "'>" +data[j].name+ "     </option>");
                }
                $('#id_city').select2();
            }  
        })
    }
});