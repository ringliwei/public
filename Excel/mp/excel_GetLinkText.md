有时候，我们得到的数据表格中需要分离出超链接和文本。效果如下：


### 1. Excel

```vba
Function GetLinkText(Target As Range) As String

    Application.Volatile True

    Dim fValue As String
    Dim fLink As String

    ' 处理 HYPERLINK 函数
    If Application.IsFormula(Target) Then

        fValue = Target.Formula

        With Application.WorksheetFunction

            ' =HYPERLINK("https://www.baidu.com", "baidu")
            If InStr(LCase(fValue), "http") > 0 Then
                fLink = Mid(fValue, .Find("""", fValue) + 1, .Find("""", fValue, .Find("""", fValue) + 1) - .Find("""", fValue) - 1)
            Else
            ' =HYPERLINK(A2, "baidu")
                fLink = Mid(fValue, .Find("(", fValue) + 1, .Find(",", fValue) - .Find("(", fValue) - 1)
                fLink = Range(fLink).Value
            End If

        End With

        GetLinkText = fLink
        Exit Function
    End If

    With Target.Hyperlinks(1)
        GetLinkText = IIf(.Address = "", .SubAddress, .Address)
    End With

End Function
```

### 2. WPS

```js
function GetLinkText(rng) {
  try {
    // 方法1：优先使用Hyperlinks对象（最可靠）
    if (rng.Hyperlinks.Count > 0) {
      const hyperlink = rng.Hyperlinks(1);
      const url = hyperlink.Address;
      const text = hyperlink.TextToDisplay || rng.Value2;
      const subAddress = hyperlink.SubAddress;

      return [
        url, // 0: URL地址
        text, // 1: 显示文本
        subAddress, // 2: 子地址
        subAddress ? url + "#" + subAddress : url, // 3: 完整地址
        "HyperlinksObject", // 4: 数据来源
      ];
    }

    // 方法2：解析公式（备用方案）
    const formula = rng.Formula;
    if (formula.startsWith("=HYPERLINK(")) {
      const regex = /"([^"]+)"/g;
      const matches = [];
      let match;

      while ((match = regex.exec(formula)) !== null) {
        matches.push(match[1]);
      }

      if (matches.length >= 2) {
        return [
          matches[0], // URL地址
          matches[1], // 显示文本
          "", // 子地址
          matches[0], // 完整地址
          "FormulaParser", // 数据来源
        ];
      } else if (matches.length === 1) {
        return [
          matches[0], // URL地址
          rng.Value2, // 显示文本
          "", // 子地址
          matches[0], // 完整地址
          "FormulaParser", // 数据来源
        ];
      }
    }

    // 方法3：检查单元格值是否为URL格式
    const cellValue = rng.Value2;
    if (cellValue && /^https?:\/\/|^www\./i.test(cellValue)) {
      return [
        cellValue, // URL地址
        cellValue, // 显示文本
        "", // 子地址
        cellValue, // 完整地址
        "CellValue", // 数据来源
      ];
    }

    // 没有找到超链接
    return [
      "", // URL地址
      cellValue, // 显示文本
      "", // 子地址
      "", // 完整地址
      "NoHyperlink", // 数据来源
    ];
  } catch (error) {
    // 错误处理
    return [
      "", // URL地址
      rng.Value2, // 显示文本
      "", // 子地址
      "", // 完整地址
      "Error: " + error.message, // 数据来源
    ];
  }
}

// 简化版本：只返回URL和文本的数组
function GetSimpleLinkArray(rng) {
  const result = GetLinkText(rng);
  return [result[0], result[1]]; // 只返回URL和文本
}
```


