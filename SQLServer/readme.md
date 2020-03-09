# SqlServer

- [SqlServer](#sqlserver)
  - [Script Snippet](#script-snippet)
    - [Table To POCO](#table-to-poco)
    - [Ticks To Datetime](#ticks-to-datetime)
    - [Search Text In PROC](#search-text-in-proc)
    - [Show Table Information Schema](#show-table-information-schema)
    - [Show Table Row Count](#show-table-row-count)
    - [Show Table Space And Rows](#show-table-space-and-rows)

## Script Snippet

### Table To POCO

```SQL
SELECT
    DATA_TYPE,
    GET_SET=CONCAT('public ',
    CASE
        WHEN DATA_TYPE = 'int' THEN 'int'
        WHEN DATA_TYPE = 'tinyint' THEN 'byte'
        WHEN DATA_TYPE = 'smallint' THEN 'short'
        WHEN DATA_TYPE = 'bigint' THEN 'long'
        WHEN DATA_TYPE = 'float' THEN 'float'
        WHEN DATA_TYPE = 'double' THEN 'double'
        WHEN DATA_TYPE = 'decimal' THEN 'decimal'
        WHEN DATA_TYPE = 'char' THEN 'string'
        WHEN DATA_TYPE = 'varchar' THEN 'string'
        WHEN DATA_TYPE = 'nvarchar' THEN 'string'
        WHEN DATA_TYPE = 'text' THEN 'string'
        WHEN DATA_TYPE = 'datetime' THEN 'DateTime'
        WHEN DATA_TYPE = 'time' THEN 'DateTime'
        WHEN DATA_TYPE = 'date' THEN 'DateTime'
        WHEN DATA_TYPE = 'uniqueidentifier' THEN 'Guid'
        ELSE
            DATA_TYPE
    END,
    ' ',
    COLUMN_NAME,
    ' { get; set; }'
    )
FROM
    information_schema.COLUMNS
WHERE
    table_schema = 'dbo' and table_name = 'cities'
```

### Ticks To Datetime

```SQL
SELECT date2long=CAST (DATEDIFF(s, '2000-1-1', GETDATE()) AS BIGINT) * 10000000 + 630822816000000000,
       long2date=DATEADD(s, 634687411300000000 / 10000000 - 630822816000000000 / 10000000, '2000-1-1')
```

### Search Text In PROC

```SQL
SELECT A.name FROM sys.sysobjects A JOIN sys.syscomments B ON A.id=B.id
WHERE A.xtype='P' AND B.text LIKE '%update weizhan%'
```

### Show Table Information Schema

```SQL
SELECT
[表名]=(CASE WHEN a.colorder=1 THEN d.name ELSE NULL END),
[字段序号]=a.colorder,
[字段名]=a.name,
[标识]=(CASE WHEN COLUMNPROPERTY(a.id, a.name,'IsIdentity')=1 THEN '√' ELSE '' END), 
[主键]=(CASE WHEN (
        SELECT COUNT(*) FROM sysobjects
        WHERE (name in (SELECT name FROM sysindexes WHERE (id = a.id) 
            AND (indid in (SELECT indid FROM sysindexkeys WHERE (id = a.id)
            AND (colid in (SELECT colid FROM syscolumns WHERE (id = a.id) AND (name = a.name))))))
        )
    AND (xtype='PK'))>0 THEN '√' ELSE '' END),
[类型]=b.name,
[占用字节数]=a.length,
[长度]=COLUMNPROPERTY(a.id, a.name, 'PRECISION'),
[小数位数]=ISNULL(COLUMNPROPERTY(a.id, a.name, 'Scale'), 0),
[允许空]=(CASE WHEN a.isnullable=1 THEN '√' ELSE '' END),
[默认值]=ISNULL(e.text, ''),
[说明]=ISNULL(g.[value], '')
FROM syscolumns a LEFT JOIN
    systypes b ON a.xtype=b.xusertype INNER JOIN
    sysobjects d ON a.id=d.id AND d.xtype='U' AND d.name<>'dtproperties' LEFT JOIN
    syscomments e ON a.cdefault=e.id LEFT JOIN
    sys.extended_properties g ON a.id=g.major_id AND a.colid=g.minor_id LEFT JOIN
    sys.extended_properties f ON d.id=f.class AND f.minor_id=0
WHERE b.name IS NOT NULL
--WHERE d.name='要查询的表' --如果只查询指定表,加上此条件
ORDER BY a.id,a.colorder
```

### Show Table Row Count

```SQL
SELECT TabeName=a.name, [RowCount]=b.rows 
FROM sysobjects a INNER JOIN sysindexes b ON a.id = b.id
WHERE (a.type = 'u') AND (b.indid IN (0, 1))
ORDER BY a.name, b.rows DESC
```

### Show Table Space And Rows

```SQL
SELECT
    tablename=OBJECT_NAME(id),
    reserved=8*reserved/1024,
    [used(KB)]=8*dpages,
    unused=8*(reserved-dpages)/1024,
    free=8*dpages/1024-rows/1024*minlen/1024,
    rows
FROM sysindexes
WHERE indid=1
ORDER BY used DESC
```
