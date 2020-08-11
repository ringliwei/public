# SqlServer

- [SqlServer](#sqlserver)
  - [Script Snippet](#script-snippet)
    - [Table To POCO](#table-to-poco)
    - [Ticks To Datetime](#ticks-to-datetime)
    - [Search Text In PROC](#search-text-in-proc)
    - [Show Table Information Schema](#show-table-information-schema)
    - [Show Table Row Count](#show-table-row-count)
    - [Show Table Space And Rows](#show-table-space-and-rows)
  - [Performance optimization](#performance-optimization)
    - [查看是否有死锁](#查看是否有死锁)
    - [查看当前正在执行的sql语句](#查看当前正在执行的sql语句)
    - [查询前 10 个可能是性能最差的 SQL 语句](#查询前-10-个可能是性能最差的-sql-语句)
    - [查询逻辑读取最高的存储过程](#查询逻辑读取最高的存储过程)
    - [查询从未使用过的索引](#查询从未使用过的索引)
    - [查询表下索引使用情况](#查询表下索引使用情况)
    - [查询缺失的索引](#查询缺失的索引)
  - [Monitor](#monitor)

## Script Snippet

### Table To POCO

```sql
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

```sql
SELECT date2long=CAST (DATEDIFF(s, '2000-1-1', GETDATE()) AS BIGINT) * 10000000 + 630822816000000000,
       long2date=DATEADD(s, 634687411300000000 / 10000000 - 630822816000000000 / 10000000, '2000-1-1')
```

### Search Text In PROC

```sql
SELECT A.name FROM sys.sysobjects A JOIN sys.syscomments B ON A.id=B.id
WHERE A.xtype='P' AND B.text LIKE '%update weizhan%'
```

### Show Table Information Schema

```sql
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

```sql
SELECT TabeName=a.name, [RowCount]=b.rows
FROM sysobjects a INNER JOIN sysindexes b ON a.id = b.id
WHERE (a.type = 'u') AND (b.indid IN (0, 1))
ORDER BY a.name, b.rows DESC
```

### Show Table Space And Rows

```sql
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

## Performance optimization

### 查看是否有死锁

```sql
DECLARE @tab TABLE (NAME VARCHAR(100), value VARCHAR(200));

INSERT INTO @tab
EXEC ('DBCC OPENTRAN WITH TABLERESULTS');

SELECT NAME,
       CAST(value AS DATETIME)                         startDate,
       GETDATE()                                       currentDate,
       DATEDIFF(s, CAST(value AS DATETIME), GETDATE()) diffsecond
FROM @tab
WHERE NAME IN ('OLDACT_STARTTIME');

SELECT spid,
       blocked,
       DB_NAME(sp.dbid) AS DBName,
       program_name,
       waitresource,
       lastwaittype,
       sp.loginame,
       sp.hostname,
       A.[text]         AS [TextData],
       SUBSTRING(
                    A.text,
                    sp.stmt_start / 2,
                    (CASE WHEN sp.stmt_end = -1 THEN DATALENGTH(A.text)ELSE sp.stmt_end END - sp.stmt_start) / 2
                )       AS [current_cmd]
FROM sys.sysprocesses                                AS sp
     OUTER APPLY sys.dm_exec_sql_text(sp.sql_handle) AS A
WHERE spid = (
                 SELECT CASE WHEN ISNUMERIC(value) = 0 THEN -1 ELSE value END
                 FROM @tab
                 WHERE NAME IN ('OLDACT_SPID')
             );
```

### 查看当前正在执行的sql语句

```sql
SELECT [Spid]                = er.session_id,
       [Blocking_session_id] = er.blocking_session_id,
       [Database]            = DB_NAME(sp.dbid),
       [User]                = nt_username,
       [Command]             = er.command,
       [Status]              = er.status,
       [Wait_type]           = er.wait_type,
       [Wait_time]           = er.wait_time,
       [Wait_resource]       = er.wait_resource,
       [Read]                = er.reads,
       [Writes]              = er.writes,
       [Logical_reads]       = er.logical_reads,
       [Individual Query]    = SUBSTRING(
                                            qt.text,
                                            er.statement_start_offset / 2,
                                            (CASE
                                                 WHEN er.statement_end_offset = -1 THEN
                                                     LEN(CONVERT(NVARCHAR(MAX), qt.text)) * 2
                                                 ELSE
                                                     er.statement_end_offset
                                             END - er.statement_start_offset
                                            ) / 2
                                        ),
       [Parent Query]        = qt.text,
       Program               = sp.program_name,
       sp.hostname,
       sp.nt_domain,
       er.start_time
FROM sys.dm_exec_requests                            er
     INNER JOIN sys.sysprocesses                     sp
         ON er.session_id = sp.spid
     CROSS APPLY sys.dm_exec_sql_text(er.sql_handle) AS qt
WHERE session_id > 50 -- Ignore system spids.
      AND session_id NOT IN (@@SPID) -- Ignore this current statement.
ORDER BY Spid, sp.ecid;
```

[sys.dm_exec_requests](https://docs.microsoft.com/zh-cn/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-requests-transact-sql?view=sql-server-ver15)

[sys.sysprocesses](https://docs.microsoft.com/zh-cn/sql/relational-databases/system-compatibility-views/sys-sysprocesses-transact-sql?view=sql-server-ver15)

[sys.dm_exec_sql_text](https://docs.microsoft.com/zh-cn/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-sql-text-transact-sql?view=sql-server-ver15)

### 查询前 10 个可能是性能最差的 SQL 语句

```sql
SELECT TOP (10)
       text                                                                                  AS 'SQL Statement',
       last_execution_time                                                                   AS 'Last Execution Time',
       (total_logical_reads + total_physical_reads + total_logical_writes) / execution_count AS [Average IO],
       (total_worker_time / execution_count) / 1000000.0                                     AS [Average CPU Time (sec)],
       (total_elapsed_time / execution_count) / 1000000.0                                    AS [Average Elapsed Time (sec)],
       execution_count                                                                       AS "Execution Count",
       qp.query_plan                                                                         AS "Query Plan"
FROM sys.dm_exec_query_stats                          qs
     CROSS APPLY sys.dm_exec_sql_text(qs.plan_handle) st
     CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) qp
ORDER BY total_elapsed_time / execution_count DESC;
```

### 查询逻辑读取最高的存储过程

```sql
SELECT TOP (25)
       p.name                                                                          AS [SP Name],
       deps.total_logical_reads                                                        AS [TotalLogicalReads],
       deps.total_logical_reads / deps.execution_count                                 AS [AvgLogicalReads],
       deps.execution_count,
       ISNULL(deps.execution_count / DATEDIFF(SECOND, deps.cached_time, GETDATE()), 0) AS [Calls/Second],
       deps.total_elapsed_time,
       deps.total_elapsed_time / deps.execution_count                                  AS [avg_elapsed_time],
       deps.cached_time
FROM sys.procedures                         AS p
     INNER JOIN sys.dm_exec_procedure_stats AS deps
         ON p.[object_id] = deps.[object_id]
WHERE deps.database_id = DB_ID()
ORDER BY deps.total_logical_reads DESC;
```

### 查询从未使用过的索引

```sql
SELECT DB_NAME(diu.database_id)                                                  AS DatabaseName,
       s.name + '.' + QUOTENAME(o.name)                                          AS TableName,
       i.index_id                                                                AS IndexID,
       i.name                                                                    AS IndexName,
       CASE WHEN i.is_unique = 1 THEN 'UNIQUE INDEX' ELSE 'NOT UNIQUE INDEX' END AS IS_UNIQUE,
       CASE WHEN i.is_disabled = 1 THEN 'DISABLE' ELSE 'ENABLE' END              AS IndexStatus,
       o.create_date                                                             AS IndexCreated,
       STATS_DATE(o.object_id, i.index_id)                                       AS StatisticsUpdateDate,
       diu.user_seeks                                                            AS UserSeek,
       diu.user_scans                                                            AS UserScans,
       diu.user_lookups                                                          AS UserLookups,
       diu.user_updates                                                          AS UserUpdates,
       p.TableRows,
       'DROP INDEX ' + QUOTENAME(i.name) + ' ON ' + QUOTENAME(s.name) + '.' + QUOTENAME(OBJECT_NAME(diu.object_id))
       + ';'                                                                     AS 'Drop Index Statement'
FROM sys.dm_db_index_usage_stats diu
     INNER JOIN sys.indexes      i
         ON i.index_id = diu.index_id AND diu.object_id = i.object_id
     INNER JOIN sys.objects      o
         ON diu.object_id = o.object_id
     INNER JOIN sys.schemas      s
         ON o.schema_id = s.schema_id
     INNER JOIN (
                    SELECT SUM(p.rows) TableRows, p.index_id, p.object_id
                    FROM sys.partitions p
                    GROUP BY p.index_id, p.object_id
                )                p
         ON p.index_id = diu.index_id AND diu.object_id = p.object_id
WHERE OBJECTPROPERTY(diu.object_id, 'IsUserTable') = 1 AND diu.database_id = DB_ID() AND i.is_primary_key = 0 --排除主键索引

      AND i.is_unique_constraint = 0 --排除唯一索引

      AND diu.user_updates <> 0 --排除没有数据变化的索引

      AND diu.user_lookups = 0 AND diu.user_seeks = 0 AND diu.user_scans = 0 AND i.name IS NOT NULL --排除那些没有任何索引的堆表

ORDER BY (diu.user_seeks + diu.user_scans + diu.user_lookups) ASC, diu.user_updates DESC;
```

### 查询表下索引使用情况

```sql
SELECT DB_NAME(database_id)     AS N'数据库名称',
       OBJECT_NAME(a.object_id) AS N'表名',
       b.name                   AS N'索引名称',
       user_seeks               AS N'用户索引查找次数',
       user_scans               AS N'用户索引扫描次数',
       MAX(last_user_seek)      AS N'最后查找时间',
       MAX(last_user_scan)      AS N'最后扫描时间',
       MAX(rows)                AS N'表中的行数'
FROM sys.dm_db_index_usage_stats a
     JOIN sys.indexes            b
         ON a.index_id = b.index_id AND a.object_id = b.object_id
     JOIN sysindexes             c
         ON c.id = b.object_id
WHERE database_id = DB_ID() --指定数据库

      AND OBJECT_NAME(a.object_id)NOT LIKE 'sys%' -- AND OBJECT_NAME(a.object_id) LIKE '表名' --指定索引表

      AND b.name IS NOT NULL

--and b.name like '索引名' --指定索引名称 可以先使用 sp_help '你的表名' 查看表的结构和所有的索引信息

GROUP BY DB_NAME(database_id), OBJECT_NAME(a.object_id), b.name, user_seeks, user_scans
ORDER BY user_seeks, user_scans, OBJECT_NAME(a.object_id);
```

### 查询缺失的索引

```sql
SELECT c.statement           AS [表名],
       c.equality_columns    AS [索引列],
       c.included_columns    AS [包含列],
       c.avg_user_impact     AS [百分比收益],
       c.last_user_seek      AS [使用后影响上次结果],
       c.avg_total_user_cost AS [减少的平均成本]
FROM (
         SELECT a.name, b.*
         FROM (
                  SELECT d.*, s.avg_total_user_cost, s.avg_user_impact, s.last_user_seek, s.unique_compiles
                  FROM sys.dm_db_missing_index_group_stats s WITH (NOLOCK),
                       sys.dm_db_missing_index_groups g WITH (NOLOCK),
                       sys.dm_db_missing_index_details d WITH (NOLOCK)
                  WHERE s.group_handle = g.index_group_handle AND d.index_handle = g.index_handle
              ) b ,
              sys.databases a WITH (NOLOCK)
         WHERE a.database_id = b.database_id
     ) c
WHERE avg_user_impact >= 99.5
ORDER BY last_user_seek DESC, avg_user_impact + avg_total_user_cost + unique_compiles DESC;
```

## Monitor

[sp_whoisactive](https://github.com/amachanic/sp_whoisactive)
