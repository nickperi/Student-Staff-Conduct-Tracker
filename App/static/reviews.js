    function upvote(reviewId) {
        const upvoteButton = document.getElementById(`upvote-arrow-${reviewId}`);
        const downvoteButton = document.getElementById(`downvote-arrow-${reviewId}`);
        const reviewUpvotes = document.getElementById(`${reviewId}-num-upvotes`);
        const reviewDownvotes = document.getElementById(`${reviewId}-num-downvotes`);

        fetch('/upvotes', {
            method: 'POST',

            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ reviewid: reviewId }),
            }).then(response => response.json())
                .then(data => {
                console.log("Received data:", data);  // check what’s coming from the backend
      
                if (data.success) {
                    console.log("Vote was successful!");
                    reviewUpvotes.innerHTML = `<i id="upvote-arrow-${reviewId}" class="fas fa-arrow-alt-circle-up" onclick="unvote('${reviewId}')" type="submit" name="action"></i> <a href="/reviews/${reviewId}/upvotes"> <span> ${data.num_upvotes}</span></a>`;

                     /*if downvote button is shaded, unshade it*/
                    if(downvoteButton.classList.contains('fas')) {
                      reviewDownvotes.innerHTML = `<i id="downvote-arrow-${reviewId}" class="far fa-arrow-alt-circle-down" onclick="downvote('${reviewId}')" type="submit" name="action"></i> <span> ${data.num_downvotes}</span>`;
                    }

                  } else {
                      alert("Vote failed.");
                  }
                });
          }

    function unvote(reviewId) {
        const upvoteButton = document.getElementById(`upvote-arrow-${reviewId}`);
        const reviewUpvotes = document.getElementById(`${reviewId}-num-upvotes`);

        fetch(`/upvotes/${reviewId}`, {
            method: 'DELETE', 
            headers: {'Content-Type': 'application/json',},
        }).then(response => response.json())
        .then(data => {
      
        if (data.success) {
            reviewUpvotes.innerHTML = `<i id="upvote-arrow-${reviewId}" class="far fa-arrow-alt-circle-up" onclick="upvote('${reviewId}')" type="submit" name="action"></i> <a href="/reviews/${reviewId}/upvotes"> <span> ${data.num_upvotes}</span></a>`;
                   
        } else {
            alert("Unvote failed.");
        }});
    }

    function downvote(reviewId) {
        const downvoteButton = document.getElementById(`downvote-arrow-${reviewId}`);
        const reviewDownvotes = document.getElementById(`${reviewId}-num-downvotes`);
        const upvoteButton = document.getElementById(`upvote-arrow-${reviewId}`);
        const reviewUpvotes = document.getElementById(`${reviewId}-num-upvotes`);

        fetch('/downvotes', {
            method: 'POST',

            headers: {'Content-Type': 'application/json',},
            body: JSON.stringify({ reviewid: reviewId }),
            }).then(response => response.json())
                .then(data => {
                console.log("Received data:", data);  // check what’s coming from the backend
      
            if (data.success) {
                console.log("Downvote was successful!");
                reviewDownvotes.innerHTML = `<i id="downvote-arrow-${reviewId}" class="fas fa-arrow-alt-circle-down" onclick="undownvote('${reviewId}')" type="submit" name="action"></i> <span> ${data.num_downvotes}</span>`;

                /*if upvote button is shaded, unshade it*/
                if(upvoteButton.classList.contains('fas')) {
                    reviewUpvotes.innerHTML = `<i id="upvote-arrow-${reviewId}" class="far fa-arrow-alt-circle-up" onclick="upvote('${reviewId}')" type="submit" name="action"></i> <a href="/reviews/${reviewId}/upvotes"> <span> ${data.num_upvotes}</span></a>`;
                }

                 
                } else {
                    alert("Downvote failed.");
                }
            });
          }


    function undownvote(reviewId) {
    const downvoteButton = document.getElementById(`downvote-arrow-${reviewId}`);
    const reviewDownvotes = document.getElementById(`${reviewId}-num-downvotes`);

    fetch(`/downvotes/${reviewId}`, {method: 'DELETE', headers: {'Content-Type': 'application/json',},}).then(response => response.json())
            .then(data => {

            if (data.success) {
            reviewDownvotes.innerHTML = `<i id="downvote-arrow-${reviewId}" class="far fa-arrow-alt-circle-down" onclick="downvote('${reviewId}')" type="submit" name="action"></i> <span> ${data.num_downvotes}</span>`;
            
            } else {
                alert("Unvote failed.");
            }
        });
    }