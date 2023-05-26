# VBA

- [VBA](#vba)
  - [Function](#function)
    - [GoInternet](#gointernet)
    - [GetLinkText](#getlinktext)

## Function

### GoInternet

```vb
Sub GoInternet()
    Dim item As Range
    
    If TypeName(Selection) <> "Range" Then
        Exit Sub
    End If
    
    Dim Url As String
    For Each item In Selection
        
        If InStr(item.Text, "http") < 1 Then
            Url = "http://" & item.Text
        End If
        
        ActiveSheet.Hyperlinks.Add item, Url
        
        item.Hyperlinks(1).Follow NewWindow:=False, AddHistory:=True
    Next item
    
End Sub
```

### GetLinkText

- 提取单元格内的超链接地址

```vb
Function GetLinkText(Target As Range) As String
    
    Application.Volatile True
    
    Dim fValue As String
    Dim fLink As String

    ' 处理 HYPERLINK 函数
    ' =HYPERLINK("https://www.baidu.com", "ddde")
    If Application.IsFormula(Target) Then
    
        fValue = Target.Formula
        
        With Application.WorksheetFunction
            fLink = Mid(fValue, .Find("""", fValue) + 1, .Find("""", fValue, .Find("""", fValue) + 1) - .Find("""", fValue) - 1)
        End With
        
        GetLinkText = fLink
        Exit Function
    End If
    
    With Target.Hyperlinks(1)
        GetLinkText = IIf(.Address = "", .SubAddress, .Address)
    End With

End Function
```
