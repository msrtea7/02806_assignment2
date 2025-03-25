document.addEventListener('DOMContentLoaded', function() {
    // 获取Markdown文件
    const contentPath = './content.md';
    fetch(contentPath)
        .then(response => {
            if (!response.ok) {
                throw new Error('无法加载Markdown文件');
            }
            return response.text();
        })
        .then(markdown => {
            // 配置Marked选项（可以根据需要调整）
            marked.setOptions({
                breaks: true,        // 将换行符转换为<br>
                gfm: true,           // 使用GitHub风格Markdown
                headerIds: true      // 为标题添加ID（便于目录跳转）
            });
            
            // 将Markdown转换为HTML并插入到页面中
            document.getElementById('content').innerHTML = marked.parse(markdown);
        })
        .catch(error => {
            console.error('加载Markdown失败:', error);
            document.getElementById('content').innerHTML = `<div class="error">加载失败: ${error.message}</div>`;
        });
});