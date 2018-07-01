// main js

function $(select) {
    if (select.startsWith('#')) {
        return document.getElementById(select.slice(1))
    } else if (select.startsWith('.')) {
        return document.getElementsByClassName(select.slice(1))
    }
}

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
function add_post(content) {
    let title = document.getElementById('post_add_title').value;
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
function update_post(id, content) {
    let title = document.getElementById('post_update_title').value;
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
// to_update_post
function to_update_post() {
    document.getElementById('post_detail').style.display='none';
    document.getElementById('post_update').style.display='';
}

// 滚动到底部刷新
function scroll_to_reload() {
    //获取滚动条当前的位置
    function getScrollTop() {
        let scrollTop = 0;
        if (document.documentElement && document.documentElement.scrollTop) {
            scrollTop = document.documentElement.scrollTop;
        }
        else if (document.body) {
            scrollTop = document.body.scrollTop;
        }
        return scrollTop;
    }

    //获取当前可视范围的高度
    function getClientHeight() {
        let clientHeight = 0;
        if (document.body.clientHeight && document.documentElement.clientHeight) {
            clientHeight = Math.min(document.body.clientHeight, document.documentElement.clientHeight);
        }
        else {
            clientHeight = Math.max(document.body.clientHeight, document.documentElement.clientHeight);
        }
        return clientHeight;
    }

    //获取文档完整的高度
    function getScrollHeight() {
        return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
    }
    window.onscroll = function () {
        if (getScrollTop() + getClientHeight() === getScrollHeight()) {
            //ajax从这里开始
            window.location.reload()
        }
    }
}

// 关键词检测
function keyWordCheck(keys) {
    // let keys_list = '{{ data.get("search") }}';
    let keys_list = keys;

    // title
    // $('.post_title').each(function () {
    for (let i=0;i<$('.post_title').length;i++) {
        // let thisThis = this;
        let thisThis = $('.post_title')[i];
        let keys = keys_list.split('|');
        for (let i = 0; i < keys.length; i++) {
            heightLight(thisThis, keys[i])
        }
    }
    // });

    // content
    // $('.post_content').each(function () {
    for (let i=0;i<$('.post_content').length;i++) {
        // let thisThis = this;
        let thisThis = $('.post_content')[i];
        let keys = keys_list.split('|');
        for (let i = 0; i < keys.length; i++) {
            heightLight(thisThis, keys[i])
        }
    }
    // });

    // 字符检测函数
    function strContainSubstr(str, subStr) {
        // 不区分大小写
        let lower_str = str.toLowerCase();
        let lower_subStr = subStr.toLowerCase();
        return lower_str.indexOf(lower_subStr) >= 0;
    }

    // 高亮
    function heightLight(thisThis, key) {
        let text = thisThis.innerHTML;
        if (strContainSubstr(text, key)) {
            let reg = new RegExp(key.toLowerCase(), 'ig');
            thisThis.innerHTML = text.replace(reg, '<span style="background-color: lightpink;">' + key + '</span>')
        }
    }
}
