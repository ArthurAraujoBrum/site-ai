function like(postId) {

    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
    const dislikeButton = document.getElementById(`dislike-button-${postId}`);

    if (likeButton.className == "bi bi-hand-thumbs-up") {
    fetch(`/like-idea/${postId}`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            likeButton.className = "bi bi-hand-thumbs-up-fill";
            dislikeButton.className = "bi bi-hand-thumbs-down";
        });    
    }
}

function dislike(postId) {
    
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
    const dislikeButton = document.getElementById(`dislike-button-${postId}`);
  
    if (dislikeButton.className === "bi bi-hand-thumbs-down") {
    fetch(`/dislike-idea/${postId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
          likeCount.innerHTML = data["likes"];
          likeButton.className = "bi bi-hand-thumbs-up";
          dislikeButton.className = "bi bi-hand-thumbs-down-fill";
      });
    }
}