let page = 1;
let loading = false;

function createPostCard(post) {
    const attachmentsHtml = post.attachments ? `<img src="${post.attachments}" class="card-img-top" alt="Post image">` : '';
    return `
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">${post.created_by_username}</h5>
            </div>
            <div class="card-body">
                <div class='card-top-image text-center'>
                    ${attachmentsHtml}
                </div>
                <h5 class="card-title"><a href="/posts/${post.id}/">${post.title}</a></h5>
                <p>${post.description.substring(0, 30)}...</p>
                <p>Category: ${post.category.id}</p>
            </div> 
        </div>
    `;
}

function appendPosts(posts) {
    const postList = $('#post-list');
    posts.forEach(post => {
        const card = $(createPostCard(post));
        postList.append(card);
    });
}

function toggleLoadMoreButton(hasNext) {
    if (hasNext) {
        $('#load-more').show();
    } else {
        $('#load-more').hide();
    }
}

function loadPosts() {
    if (loading) return;
    loading = true;
    $('#loading').show();

    $.ajax({
        url: `/api/posts/?page=${page}`,
        method: 'GET',
        success: function(data) {
            console.log("API Fetched....!!");
            appendPosts(data.results);
            toggleLoadMoreButton(data.next);
            if (data.next) {
                page++;
            }
            loading = false;
            $('#loading').hide();
        },
        error: function() {
            loading = false;
            $('#loading').hide();
        }
    });
}

const handleScroll = () => {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 200) {
        loadPosts();
    }
};

$(document).ready(function() {
    loadPosts();
    // $(document).on('scroll', handleScroll);
    $('#load-more').click(loadPosts);
});
