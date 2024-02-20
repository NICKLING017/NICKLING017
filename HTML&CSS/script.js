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
