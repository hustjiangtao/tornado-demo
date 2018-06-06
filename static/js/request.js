// Do request for methods [post, delete, put, get]
function request(method, url, data) {
    // let params = new URLSearchParams();
    // for (let key in data){
    //     params.append(key, data[key])
    // }
    // let params = new FormData();
    // for (let key in data){
    //     params.append(key, data[key])
    // }
    axios({
        method: method,
        url: url,
        data: data,
    })
        .then(function (response) {
            console.log(response)
        })
        .catch(function (error) {
            console.log(error);
        });
}
