当你在 `Excel` 中有大量的超链接，并且希望可以批量在浏览器中打开时，可以使用下面的 `vba` 代码。

```vb
Sub GoInternet()
    Dim item As Range

    If TypeName(Selection) <> "Range" Then
        Exit Sub
    End If

    Dim Url As String
    For Each item In Selection

        If InStr(item.Text, "http") < 1 Then
            Url = "https://" & item.Text
        End If

        ActiveSheet.Hyperlinks.Add item, Url

        item.Hyperlinks(1).Follow NewWindow:=False, AddHistory:=True
    Next item

End Sub
```

将上面的代码添加到 `Excel` 中作为自定义`宏`，选中有超链接的`区域`后，执行 `GoInternet` 宏。

