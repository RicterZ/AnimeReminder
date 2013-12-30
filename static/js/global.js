String.prototype.replaceAll = function(s1,s2){    
    return this.replace(new RegExp(s1,"gm"),s2);    
}

$(function(){
    indexControl.__init__();
    indexControl.getData('/index', indexControl.indexHander, ".main-update-ul-container");
    indexControl.getData('/get_update_schedule', indexControl.scheduleHandler, ".main-schedule-container");
    $(".button").click(function(){if (this.attributes[1].value != 'undo') {indexControl[this.attributes[1].value]()}});
});