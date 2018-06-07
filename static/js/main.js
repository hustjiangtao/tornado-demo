// main js

// login
function do_login() {
    let account = document.getElementById('account').value;
    let password = document.getElementById('password').value;
    let data = {
        "account": account,
        "password": password,
    };
    axios.post('/user', data)
        .then(function (response) {
            if (response.data.code === 200) {
                window.location.href = '/posts'
            }
            else {
                alert(response.data.message)
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}

// add post
function add_post() {
    let title = document.getElementById('title').value;
    let content = document.getElementById('content').value;
    let data = {
        "title": title,
        "content": content,
    };
    axios.post('/post', data)
        .then(function (response) {
            if (response.data.code === 200) {
                let id = response.data.data.result;
                window.location.href = '/post?id=' + id
            }
            else {
                alert(response.data.message)
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}