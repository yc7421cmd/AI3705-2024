// let myHeading = document.querySelector('h1');
// myHeading.textContent = "Hello world!";
let selectcolor = document.getElementById("color");
let add_button = document.getElementById("add_button");
var reset_button = document.getElementById('reset');
var start_button = document.getElementById('start');
var selectedcolor = selectcolor.value;
var is_running = false;
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function init(){
    let canvas = document.getElementById("background");
    let arms_canvas = document.getElementById("arms");
    if (canvas.getContext) {
        var ctx = canvas.getContext("2d");
        // drawing code here
        ctx.fillStyle = "rgb(56,224,173)";
        ctx.fillRect(60, 120, 500, 60); //conveyor belt
        ctx.strokeRect(60, 120, 500, 60);
        ctx.fillStyle = "rgb(255, 255, 255)";
        ctx.fillRect(230, 15, 30, 105); // chute 1
        ctx.fillRect(380, 15, 30, 105); // chute 2
        ctx.fillRect(530, 15, 30, 105); // chute 3
        ctx.strokeRect(230, 15, 30, 105);
        ctx.strokeRect(380, 15, 30, 105);
        ctx.strokeRect(530, 15, 30, 105);
        // draw a semi-circle
        ctx.beginPath();
        ctx.arc(500, 120, 60, 0, Math.PI/2, false);
        ctx.stroke();
        arms_ctx = arms_canvas.getContext("2d");
        arms_ctx.fillStyle = "rgb(0, 0, 0)";
        arms_ctx.fillRect(180,120,5,110)// barrier
        arms_ctx.fillRect(242,180,5,110)// sorting arm 1
        arms_ctx.fillRect(392,180,5,110)// sorting arm 2

    } 
}
function clear_workpiece(){
    var wp_canvas = document.getElementById("workpiece");
    var wp_ctx = wp_canvas.getContext("2d");
    wp_ctx.clearRect(0, 0, wp_canvas.width, wp_canvas.height);
}
function clear_sort_arm(arm_id){
    var arm_canvas = document.getElementById("arms");
    var arm_ctx = arm_canvas.getContext("2d");
    // arm_id 0 为阻挡臂，1 为挑选臂1，2 为挑选臂2
    if (arm_id == 0){
        arm_ctx.clearRect(180,120,5,170);
    } else if (arm_id == 1){
        arm_ctx.clearRect(242,0,5,300);
    } else if (arm_id == 2){
        arm_ctx.clearRect(392,0,5,300);
    }
}
function draw(state){
    var wp_canvas = document.getElementById("workpiece");
    var wp_ctx = wp_canvas.getContext("2d");
    var arm_canvas = document.getElementById("arms");
    var arm_ctx = arm_canvas.getContext("2d");
    var wp_state = state.workpiece;
    var barrier_state = state.barrier;
    var sorting_1_state = state.sorting_1;
    var sorting_2_state = state.sorting_2;
    if (wp_state !== -1){
        clear_workpiece();
        switch(selectedcolor){
            case "red":
                wp_ctx.fillStyle = "rgb(255, 0, 0)";
                break;
            case "metallic":
                wp_ctx.fillStyle = "rgb(192, 192, 192)";
                break;
            case "black":
                wp_ctx.fillStyle = "rgb(0, 0, 0)";
                break;
            default:
                wp_ctx.fillStyle = "rgb(0, 0, 0)";
        }
        switch(wp_state){
            case 0:
                wp_ctx.fillRect(60, 135, 30, 30);
                break;
            case 1:
                wp_ctx.fillRect(150, 135, 30, 30);
                break;
            case 2:
                wp_ctx.fillRect(230, 135, 30, 30);
                break;
            case 3:
                wp_ctx.fillRect(380, 135, 30, 30);
                break;
            case 4:
                wp_ctx.save();
                // rotate 45 degree
                wp_ctx.translate(500+30*Math.sin(75*Math.PI/180), 120+30*Math.sin(75*Math.PI/180));
                wp_ctx.rotate(Math.PI/4);
                wp_ctx.translate(-500-30*Math.sin(75*Math.PI/180), -120-30*Math.sin(75*Math.PI/180));
                wp_ctx.fillRect(485+30*Math.sin(75*Math.PI/180), 105+30*Math.sin(75*Math.PI/180), 30, 30);
                wp_ctx.restore();
                break;
            case 5:
                wp_ctx.fillRect(230, 15, 30, 30);
                break;
            case 6:
                wp_ctx.fillRect(380, 15, 30, 30);
                break;
            case 7:
                wp_ctx.fillRect(530, 15, 30, 30);
                break;
            default:
                clear_workpiece();
        }
    }
    if (barrier_state !== -1){
        clear_sort_arm(0);
        arm_ctx.fillStyle = "rgb(0, 0, 0)";
        switch(barrier_state){
            case 0:
                arm_ctx.fillRect(180,120,5,110);
                break;
            case 1:
                arm_ctx.fillRect(180,180,5,110);
                break;
            default:
                clear_sort_arm(0);
        }
    }
    if (sorting_1_state !== -1){
        clear_sort_arm(1);
        arm_ctx.fillStyle = "rgb(0, 0, 0)";
        switch(sorting_1_state){
            case 0:
                arm_ctx.fillRect(242,45,5,245);
                break;
            case 1:
                arm_ctx.fillRect(242,165,5,125);
                break;
            case 2:
                arm_ctx.fillRect(242,180,5,110);
                break;
            default:
                clear_sort_arm(1);
        }
    }
    if (sorting_2_state !== -1){
        clear_sort_arm(2);
        arm_ctx.fillStyle = "rgb(0, 0, 0)";
        switch(sorting_2_state){
            case 0:
                arm_ctx.fillRect(392,45,5,245);
                break;
            case 1:
                arm_ctx.fillRect(392,165,5,125);
                break;
            case 2:
                arm_ctx.fillRect(392,180,5,110);
                break;
            default:
                clear_sort_arm(2);
        }
    }
}
async function animation(){
    if (is_running){
        alert("正在运行中，请稍等");
        return;
    }
    is_running = true;
    var data = document.getElementById("data_container");
    if (data !== null) {
        // console.log(data);
        var states = data.getAttribute('state');
        var lines = data.getAttribute('d');
        if (states !== null && lines !== null) {
            // console.log(lines);
            // console.log(states);
            lines = JSON.parse(lines);
            states = JSON.parse(states);
            var wp_canvas = document.getElementById("workpiece");
            var wp_ctx = wp_canvas.getContext("2d");
            wp_ctx.clearRect(60, 135, 30, 30);
            for (var i = 0; i < lines.length; i++) {
                // sleep(1000);
                await sleep(1500);
                var line = lines[i];
                var command_line = document.getElementById("command-line");
                command_line.textContent = line;
                var state = states[i];
                // workpiece,barrier,sorting_1,sorting_2
                draw(state);
                console.log(state);
                console.log(line);
            }
        }
    }
    $('#data_container').attr('d', '');
    $('#data_container').attr('state', '');
    is_running = false;
    var result = document.getElementById("result");
    switch(selectedcolor){
        case "red":
            result.textContent = "滑槽1";
            break;
        case "metallic":
            result.textContent = "滑槽2";
            break;
        case "black":
            result.textContent = "滑槽3";
            break;
        default:
            result.textContent = "";
    }
}
function update_data(color,event){
    // event.preventDefault();
    console.log(color);
    // console.log('asd');
    $.ajax({
        type: 'GET',
        url: '/update',
        data: color, 
        success: function(response){
            // console.log(response);
            $('#data_container').attr('d', response.lines);
            $('#data_container').attr('state', response.state);
        },
        error: function(error){
            console.log(error);
        }
    });
}
init();
add_button.addEventListener("click", function(event){
    event.preventDefault();
    selectedcolor = selectcolor.value;
    update_data(selectedcolor,event);
    var result = document.getElementById("result");
    result.textContent = "";
});


start_button.addEventListener('click',function(){
    var data = document.getElementById("data_container");
    var states = data.getAttribute('state');
    var lines = data.getAttribute('d');
    if (states.length===0|| lines.length===0){
        alert("请按下‘添加工件’按钮")
    }
    else{
        animation();
    }
    
})
reset_button.addEventListener('click',function(){
    if (is_running){
        alert("正在运行中，请稍等");
        return;
    }
    // alert("重置成功");
    clear_sort_arm(0);
    clear_sort_arm(1);
    clear_sort_arm(2);
    clear_workpiece();
})