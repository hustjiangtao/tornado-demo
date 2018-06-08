// main js

// register
function do_register() {
    let name = document.getElementById('register_name').value;
    let email = document.getElementById('register_email').value;
    let mobile = document.getElementById('register_mobile').value;
    let password = document.getElementById('register_password').value;
    let password_confirm = document.getElementById('register_password_confirm').value;
    let data = {
        "name": name,
        "email": email,
        "mobile": mobile,
        "password": password,
        "password_confirm": password_confirm,
    };
    if (name && email && password && password_confirm && password == password_confirm) {
        axios.post('/register', data)
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
}

// login
function do_login(next) {
    let account = document.getElementById('account').value;
    let password = document.getElementById('password').value;
    let data = {
        "account": account,
        "password": password,
    };
    axios.post('/auth', data)
        .then(function (response) {
            if (response.data.code === 200) {
                window.location.href = next || '/posts'
            }
            else {
                alert(response.data.message)
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}

// logout
function do_logout() {
    axios.delete('/auth')
        .then(function (response) {
            if (response.data.code === 200) {
                window.location.href = '/auth'
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
    let title = document.getElementById('post_add_title').value;
    let content = document.getElementById('post_add_content').value;
    let data = {
        "title": title,
        "content": content,
    };
    axios.post('/post', data)
        .then(function (response) {
            if (response.data.code === 200) {
                let id = response.data.data.id;
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

// update post
function update_post(id) {
    let title = document.getElementById('post_update_title').value;
    let content = document.getElementById('post_update_content').value;
    let data = {
        "id": id,
        "title": title,
        "content": content,
    };
    axios.put('/post', data)
        .then(function (response) {
            if (response.data.code === 200) {
                let id = response.data.data.id;
                window.location.reload()
            }
            else {
                alert(response.data.message)
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}

// user update
function user_update() {
    let name = document.getElementById('name').value;
    let email = document.getElementById('email').value;
    let mobile = document.getElementById('mobile').value;
    let data = {
        "name": name,
        "email": email,
        "mobile": mobile,
    };
    axios.put('/user', data)
        .then(function (response) {
            if (response.data.code === 200) {
                alert('修改成功')
            }
            else {
                alert(response.data.message)
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}

// to_register
function to_register() {
    document.getElementById('login_box').style.display='none';
    document.getElementById('register_box').style.display='';
}
// to_login
function to_login() {
    document.getElementById('register_box').style.display='none';
    document.getElementById('login_box').style.display='';
}
// to_add_post
function to_add_post() {
    window.location.href = '/post'
}
// to_update_post
function to_update_post() {
    document.getElementById('post_info').style.display='none';
    document.getElementById('post_update').style.display='';
}
// to_user_info
function to_user_info() {
    window.location.href = '/user'
}