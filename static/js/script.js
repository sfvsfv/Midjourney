$(document).ready(function() {
    // 连接到WebSocket服务器
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // 监听表单提交事件
    $('#promptForm').submit(function(e) {
        e.preventDefault();
        // 从输入框中获取prompt
        var prompt = $('input[name="prompt"]').val();
        // 发送prompt到后端
        socket.emit('submit_prompt', { prompt: prompt });
        // 清空输入框
        $('#promptForm').find('input').val('');
        // 显示进度条
        $('#progressBar').css('width', '0%').attr('aria-valuenow', 0);
        $('#progressText').text('Waiting for results...');
    });

    // 监听从服务器发送的task_status事件
    socket.on('task_status', function(data) {
        // 更新进度条和文字
        var progress = parseInt(data.progress.replace('%', ''), 10);
        $('#progressBar').css('width', progress + '%').attr('aria-valuenow', progress);
        $('#progressText').text('Progress: ' + data.progress);

        // 如果有图片URL，则显示图片
        if (data.imageUrl) {
            $('#result').html('<img src="' + data.imageUrl + '" class="img-fluid" />');
        }

        // 如果任务完成，移除进度条的条纹和动画效果
        if (progress === 100) {
            $('#progressBar').removeClass('progress-bar-striped progress-bar-animated');
        }
    });
});
