$(document).ready(function(){  
  $("a[@class=a_add_attachment]").click(
    function(){
        $(this).hide();
        $(this).parent("li").children("div").fadeIn('slow');
    }
  );
  $("input[@name=btn_add_attachment]").click(function(){add_attachment(this)});
  $("a[@name=a_del_attachment]").click(function(){del_attachment(this)});
});

function add_attachment(ev)
{
    var li =$(ev).parent("div");    
    var pid = li.children("input[@name=pid]");    
    var task_name = li.children("input[@name=task_name]");
    if(!task_name)
        alert('error');
    if (task_name && task_name.val() == "")
    {
        task_name.addClass('required');
        return;
    }    
    var priority = li.children("select[@name=priority]")
    //alert('pid:'+pid.val() + 'task_name:'+task_name.val() +'priority:' + priority.val());
    $.post('/todo/task/add/',
           {pid:pid.val(),task_name:task_name.val(), priority:priority.val()},
           function(ret){
                if(ret == 'success')
                {
                    window.location.reload();
                    task_name.val('');
                    priority.val('0');
                }
                else
                    alert(ret);
           }           
           );
};





function del_attachment(obj){
  obj = $(obj);
  if(confirm('你真的要删除该附件吗？'))
  {
    $.post('/attachments/ajaxdeleteattachment/',
           {attachment_id:obj.attr('rel')},
           function(ret){
                if(ret == 'success')
                {
                    window.location.reload();
                }
                else
                    alert(ret);
           }           
           );
  }
};
