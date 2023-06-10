# VBA

- [VBA](#vba)
  - [Function](#function)
    - [GoInternet](#gointernet)
    - [GetLinkText](#getlinktext)
    - [Resources](#resources)

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

### Resources

- [xlwings](https://docs.xlwings.org/en/latest/index.html) Python for Exceland Google Sheets.
- [Strings in VBA](https://www.codevba.com/learn/strings.htm)
- [Excel-vba 开发使用手册](https://github.com/bluetata/concise-excel-vba)
- COM
  - [Introduction to COM - What It Is and How to Use It.](https://www.codeproject.com/articles/633/introduction-to-com-what-it-is-and-how-to-use-it)
- [在 Excel VBA 中写 SQL，是一种什么体验](https://www.cnblogs.com/new-june/p/15837906.html)
- [Excel VBA 中写 SQL，这些问题你一定为此头痛过](https://www.cnblogs.com/new-june/p/15847114.html)
- [Automate Chrome / Edge using VBA](https://www.codeproject.com/Tips/5307593/Automate-Chrome-Edge-using-VBA)
- VBA Library
  - [awesome-vba](https://github.com/sancarn/awesome-vba)
  - [stdVBA](https://github.com/sancarn/stdVBA)
  - [stdVBA-examples](https://github.com/sancarn/stdVBA-examples)
  - [VBA_personal](https://github.com/ringliwei/VBA_personal)
  - [VBA-Web](https://github.com/VBA-tools/VBA-Web)
  - [VBA-JSON](https://github.com/VBA-tools/VBA-JSON)
  - [VBA-Dictionary](https://github.com/VBA-tools/VBA-Dictionary) Drop-in replacement for Scripting.Dictionary on Mac
  - [VBA-CSV-interface](https://github.com/ws-garcia/VBA-CSV-interface)
  - [VBA-Expressions](https://github.com/ws-garcia/VBA-Expressions)
  - [VBA-SQL-Library](https://github.com/Beakerboy/VBA-SQL-Library)
  - [QRCodeLibVBA](https://github.com/yas78/QRCodeLibVBA)
  - [xlib](https://github.com/x-vba/xlib)
  - [SQLiteForExcel](https://github.com/govert/SQLiteForExcel)
