# VBA

- [VBA](#vba)
  - [Function](#function)
    - [GetLink](#getlink)

## Function

### GetLink

- 提取单元格内的超链接地址

```vb
Function GetLink(Rng)

    Application.Volatile True

    With Rng.Hyperlinks(1)
    GetLink = IIf(.Address = "", .SubAddress, .Address)
    End With

End Function
```
