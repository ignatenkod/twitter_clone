document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всплывающих подсказок
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Обработчик для кнопки лайка
    document.body.addEventListener('htmx:afterSwap', function(event) {
        if (event.detail.target.id.includes('post-')) {
            const response = event.detail.xhr.response;
            if (response.is_liked !== undefined) {
                const likeBtn = event.detail.elt;
                likeBtn.classList.toggle('btn-danger', response.is_liked);
                likeBtn.classList.toggle('btn-outline-danger', !response.is_liked);
                
                const likeCount = likeBtn.querySelector('.like-count');
                if (likeCount) {
                    likeCount.textContent = response.likes_count;
                }
            }
        }
    });
    
    // Обработчик для формы комментариев
    const commentForm = document.getElementById('comment-form');
    if (commentForm) {
        commentForm.addEventListener('htmx:afterRequest', function() {
            commentForm.reset();
        });
    }
});
