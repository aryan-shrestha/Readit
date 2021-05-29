var likeBtns=document.querySelectorAll('.likeBtn')
// var likes = document.querySelectorAll('.likes')

for(var i = 0; i < likeBtns.length; i++){
    likeBtns[i].addEventListener('click', function(){
        var commentId= this.dataset.commentid
        if(user === 'AnonymousUser'){
            console.log("Not logged In")
            window.location.href = '/login'
        }
        else{
            hitLike(commentId)
        }
    })
}

function hitLike(commentId){
    var url = '/hit_like/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'commentId': commentId})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        // likes = document.querySelector("[data-likeid=" + CSS.escape(likeId) + "]");
        parent = document.querySelector("[data-commentid=" + CSS.escape(commentId) + "]").parentElement
        likes = parent.children[1]
        likes.innerText = data
    })
}