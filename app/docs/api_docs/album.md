# API document for album

## Get album list

- url: /album
- type: GET
- args: None
- return:

```json
{
    "code": 200,  // 状态码
    "message": 'success',  // 状态信息
    "data": {
        "albums": [{2018: []}],  // album list
    },
}
```

## Get a single album

- url: /album/(\d+)
- type: GET
- args: None
- return:

```json
{
    "code": 200,  // 状态码
    "message": 'success',  // 状态信息
    "data": {
        "album": [],  // single album
    },
}
```
