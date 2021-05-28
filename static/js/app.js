var likeBtns=document.querySelectorAll('.likeBtn')
var likes = document.querySelectorAll('.likes')

// for(var i=0; i<likeBtns.length; i++){
//     likeBtns[i].onclick = function(){
//         console.log(this.dataset.commentid)
//         likes[i].innerHTML = 'like'
        
//     }
// }

for(var i = 0; i < likeBtns.length; i++){
    likeBtns[i].addEventListener('click', function(){
        var commentId= this.dataset.commentid
        if(user === 'AnonymousUser'){
            console.log("Not logged In")
            window.location.href = '/login'
        }
        else{
           hitLike(commentId, like)
        }
    })
}

function hitLike(commentId, like){
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
        console.log(data)
        like.innerHTML = data
        console.log(like)
    })
}