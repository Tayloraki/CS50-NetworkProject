document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#newpost').style.display = 'none';
    document.querySelector('#hide-button').style.display = 'none';
    document.querySelector('#show-button').addEventListener('click', show_post_form);
    document.querySelector('#hide-button').addEventListener('click', hide_post_form);

    var fuck = true

    fetch('/all')
    .then(response => response.json())
    .then(posts => {
        console.log(posts);

        posts.forEach(post => {
            const poster = post.poster
            const body = post.body
            const timestamp = post.timestamp
            const post_id = post.id

            console.log(poster)
            console.log(body)
            console.log(timestamp)
            console.log(post_id)

            const postcell = document.createElement('div');
            postcell.setAttribute("class", "postcell");
            document.querySelector('#posts').append(postcell);

            const postuser = document.createElement('div');
            // postuser.innerHTML = poster;
            postuser.setAttribute("class", "postuser");

                var a = document.createElement('a');
                var linkText = document.createTextNode(poster);
                a.appendChild(linkText);
                a.title = "userpage link";
                a.href = "http://127.0.0.1:8000/profile/"+poster;
                postuser.appendChild(a);

            postcell.append(postuser);

            const postbody = document.createElement('div');
            postbody.innerHTML = body;
            postbody.setAttribute("class", "postbody");
            postcell.append(postbody);

            const posttime = document.createElement('div');
            posttime.innerHTML = timestamp;
            posttime.setAttribute("class", "posttime");
            postcell.append(posttime);

            // const postlikes = document.createElement('div');
            // postlikes.innerHTML = 
            // postlikes.setAttribute("class", "postlikes");
            // postlikes.append(postcell);

            document.querySelector('#posts').append(postcell);

            document.querySelector('postuser').addEventListener('click', userposts(poster))
        })
    });
});

// FOR PROFILE PAGE
// document.addEventListener('DOMContentLoaded', function() {
function userposts(user) {
    // document.querySelector('#user_posts').innerHTML = 'user profile';
    // MAYBE A WAY TO PASS PROFILE PAGE VARIABLE TO AJAX REQUESt
    // var url = "{% url 'profile' %}";
    // var id = poster

    // document.location.href = url + "/" + id;

    // BASIC FETCH FOR PROFILE'S POSTS
    fetch('profile/'+user+'/posts')
    .then(response => response.json())
    .then(posts => {
        console.log(posts);

        posts.forEach(post => {
            const poster = post.poster
            const body = post.body
            const timestamp = post.timestamp
            const post_id = post.id

            console.log(poster)
            console.log(body)
            console.log(timestamp)
            console.log(post_id)

            const postcell = document.createElement('div');
            postcell.setAttribute("class", "postcell");
            document.querySelector('#user_posts').append(postcell);

            const postuser = document.createElement('div');
            // postuser.innerHTML = poster;
            postuser.setAttribute("class", "postuser");

                var a = document.createElement('a');
                var linkText = document.createTextNode(poster);
                a.appendChild(linkText);
                a.title = "userpage link";
                a.href = "http://127.0.0.1:8000/profile/"+poster;
                postuser.appendChild(a);

            postcell.append(postuser);

            const postbody = document.createElement('div');
            postbody.innerHTML = body;
            postbody.setAttribute("class", "postbody");
            postcell.append(postbody);

            const posttime = document.createElement('div');
            posttime.innerHTML = timestamp;
            posttime.setAttribute("class", "posttime");
            postcell.append(posttime);

            // const postlikes = document.createElement('div');
            // postlikes.innerHTML = 
            // postlikes.setAttribute("class", "postlikes");
            // postlikes.append(postcell);

            document.querySelector('#user_posts').append(postcell);
        })
    })
}
// });

//  FOR USER FOLLOWED POSTS
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#followed_posts').innerHTML = 'user following';
    // BASIC FETCH FOR PROFILE'S POSTS
    // fetch('/profile/'+following)
    // .then(response => response.json())
    // .then(posts => {
    //     console.log(posts);

    //     posts.forEach(post => {
    //         const poster = post.poster
    //         const body = post.body
    //         const timestamp = post.timestamp
    //         const post_id = post.id

    //         console.log(poster)
    //         console.log(body)
    //         console.log(timestamp)
    //         console.log(post_id)

    //         const postcell = document.createElement('div');
    //         postcell.setAttribute("class", "postcell");
    //         document.querySelector('#posts').append(postcell);

    //         const postuser = document.createElement('div');
    //         postuser.innerHTML = poster;
    //         postuser.setAttribute("class", "postuser");
    //         postcell.append(postuser);

    //         const postbody = document.createElement('div');
    //         postbody.innerHTML = body;
    //         postbody.setAttribute("class", "postbody");
    //         postcell.append(postbody);

    //         const posttime = document.createElement('div');
    //         posttime.innerHTML = timestamp;
    //         posttime.setAttribute("class", "posttime");
    //         postcell.append(posttime);

    //         // const postlikes = document.createElement('div');
    //         // postlikes.innerHTML = 
    //         // postlikes.setAttribute("class", "postlikes");
    //         // postlikes.append(postcell);

    //         document.querySelector('#posts').append(postcell);

});

function show_post_form() {
    document.querySelector('#newpost').style.display = 'block';
    document.querySelector('#hide-button').style.display = 'block';
    document.querySelector('#show-button').style.display = 'none';
    document.querySelector('#post-form').addEventListener('submit', add_post());
}

function hide_post_form() {
    document.querySelector('#newpost').style.display = 'none';
    document.querySelector('#hide-button').style.display = 'none';
    document.querySelector('#show-button').style.display = 'block';
}

function add_post() {
    document.querySelector('#post-body').value = '';

    document.querySelector('#post-form').onsubmit = function() {

        const body = document.querySelector('#post-body').value;

        console.log(body);

        fetch('/posts', {
            method: 'POST',
            body: JSON.stringify({
                body: body
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);

        // document.querySelector('#newpost').style.display = 'none';
        })
    }
}