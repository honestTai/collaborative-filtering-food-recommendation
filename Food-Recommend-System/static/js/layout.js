document.addEventListener('DOMContentLoaded', function () {
    // 获取所有导航链接
    const links = document.querySelectorAll('.nav-link');

    // 为每个链接添加悬停和点击事件
    links.forEach(link => {
        // 悬停效果
        link.addEventListener('mouseenter', function() {
            this.classList.add('hovered');
        });

        link.addEventListener('mouseleave', function() {
            this.classList.remove('hovered');
        });

        // 点击效果
        link.addEventListener('click', function() {
            // 移除其他链接的 active 类
            links.forEach(item => item.classList.remove('active'));
            // 添加 active 类到当前点击的链接
            this.classList.add('active');
        });
    });
});
