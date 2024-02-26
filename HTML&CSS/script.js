function convertTextToJson() {
    var text = document.getElementById('excelText').value;
    // 假设每行数据由制表符分隔
    var lines = text.trim().split('\n');
    var result = lines.map(line => {
        var cells = line.split('\t').map(cell => cell.trim());
        return cells;
    });

    // 如果需要将其转换为对象数组（根据表头）
    var headers = result[0];
    var jsonResult = result.slice(1).map(row => {
        var obj = {};
        row.forEach((cell, index) => {
            obj[headers[index]] = cell;
        });
        return obj;
    });

    document.getElementById('jsonResult').textContent = JSON.stringify(jsonResult, null, 2);
}


// 获取倒计时容器
var countdownElement = document.getElementById("countdown");

// 设置倒计时结束时间
var countDownDate = new Date("Dec 24, 2024 23:59:59").getTime();

// 每秒更新倒计时
var countdownInterval = setInterval(function() {
    // 获取当前时间
    var now = new Date().getTime();

    // 计算剩余时间
    var distance = countDownDate - now;

    // 计算剩余时间中的天、时、分、秒
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // 在倒计时容器中显示剩余时间
    countdownElement.innerHTML = days + "天 " + hours + "时 "
    + minutes + "分 " + seconds + "秒 ";

    // 如果倒计时结束，则显示提示信息并停止更新倒计时
    if (distance < 0) {
        clearInterval(countdownInterval);
        countdownElement.innerHTML = "倒计时结束";
    }
}, 1000); // 每秒更新一次
