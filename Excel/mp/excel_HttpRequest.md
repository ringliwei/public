今天要分享的代码是通过 `Excel` 发送 `HTTP` 请求，获取网络资源。

```vb
Function BytesToBString(Body, Cset)
    On Error Resume Next
    '"GB2312"
    '"GBK"
    '"UTF-8"
    ' excel 字节编码转换

    Dim Objstream
    Set Objstream = CreateObject("adodb.stream")
    Objstream.Type = 1
    Objstream.Mode = 3
    Objstream.Open
    Objstream.Write Body
    Objstream.Position = 0
    Objstream.Type = 2
    Objstream.Charset = Cset
    BytesToBString = Objstream.ReadText
    Objstream.Close
    Set Objstream = Nothing
End Function

Function HttpGet(Target As Range) As String
    ' http get
    Dim Client As New WebClient
    Dim Url As String
    Url = Target.Value


    Dim web_Request As New WebRequest

    web_Request.Resource = Url
    web_Request.Format = WebFormat.Json
    web_Request.Method = WebMethod.HttpGet

    Dim Response As New WebResponse
    Set Response = Client.Execute(web_Request)

    Dim ResponseText As String
    ResponseText = BytesToBString(Response.Body, "UTF-8")

    HttpGet = ResponseText
End Function
```

`HttpGet` 依赖项目 [VBA-Web](https://github.com/VBA-tools/VBA-Web)。需要先将`VBA-Web`复制到 excel 文件中，再把上面的代码复制到文件中。就可以使用了。

比如，我们要获取百度首页的内容：

```excel
=HttpGet("https://www.baidu.com")
```
