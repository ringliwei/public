# SqlServer

- [SqlServer](#sqlserver)
  - [Script Snippet](#script-snippet)
    - [How To Use `SAVE TRANSACTION`](#how-to-use-save-transaction)
    - [Table To POCO](#table-to-poco)
    - [Ticks To Datetime](#ticks-to-datetime)
    - [Search Text In PROC](#search-text-in-proc)
    - [Show Table Information Schema](#show-table-information-schema)
    - [Show Table Information Schema by MarkDown](#show-table-information-schema-by-markdown)
    - [Show Table Row Count](#show-table-row-count)
    - [Show Table Space And Rows](#show-table-space-and-rows)
    - [Generate Time Sequence](#generate-time-sequence)
    - [Generate Backup Script](#generate-backup-script)
    - [Convert Datetime](#convert-datetime)
  - [Performance optimization](#performance-optimization)
    - [查看是否有死锁](#查看是否有死锁)
    - [查看当前正在执行的 sql 语句](#查看当前正在执行的-sql-语句)
    - [查询 Buffer 使用情况](#查询-buffer-使用情况)
    - [查询前 10 个可能是性能最差的 SQL 语句](#查询前-10-个可能是性能最差的-sql-语句)
    - [查询逻辑读取最高的存储过程](#查询逻辑读取最高的存储过程)
    - [查询从未使用过的索引](#查询从未使用过的索引)
    - [查询表下索引使用情况](#查询表下索引使用情况)
    - [查询缺失的索引](#查询缺失的索引)
  - [Always on](#always-on)
    - [CREATE LOGIN](#create-login)
  - [Monitor](#monitor)

## Script Snippet

### How To Use `SAVE TRANSACTION`

```sql
USE AdventureWorks2012;
GO
IF EXISTS (SELECT name FROM sys.objects
           WHERE name = N'SaveTranExample')
    DROP PROCEDURE SaveTranExample;
GO
CREATE PROCEDURE SaveTranExample
    @InputCandidateID INT
AS
    -- Detect whether the procedure was called
    -- from an active transaction and save
    -- that for later use.
    -- In the procedure, @TranCounter = 0
    -- means there was no active transaction
    -- and the procedure started one.
    -- @TranCounter > 0 means an active
    -- transaction was started before the
    -- procedure was called.
    DECLARE @TranCounter INT;
    SET @TranCounter = @@TRANCOUNT;
    IF @TranCounter > 0
        -- Procedure called when there is
        -- an active transaction.
        -- Create a savepoint to be able
        -- to roll back only the work done
        -- in the procedure if there is an
        -- error.
        SAVE TRANSACTION ProcedureSave;
    ELSE
        -- Procedure must start its own
        -- transaction.
        BEGIN TRANSACTION;
    -- Modify database.
    BEGIN TRY
        DELETE HumanResources.JobCandidate
            WHERE JobCandidateID = @InputCandidateID;
        -- Get here if no errors; must commit
        -- any transaction started in the
        -- procedure, but not commit a transaction
        -- started before the transaction was called.
        IF @TranCounter = 0
            -- @TranCounter = 0 means no transaction was
            -- started before the procedure was called.
            -- The procedure must commit the transaction
            -- it started.
            COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        -- An error occurred; must determine
        -- which type of rollback will roll
        -- back only the work done in the
        -- procedure.
        IF @TranCounter = 0
            -- Transaction started in procedure.
            -- Roll back complete transaction.
            ROLLBACK TRANSACTION;
        ELSE
            -- Transaction started before procedure
            -- called, do not roll back modifications
            -- made before the procedure was called.
            IF XACT_STATE() <> -1
                -- If the transaction is still valid, just
                -- roll back to the savepoint set at the
                -- start of the stored procedure.
                ROLLBACK TRANSACTION ProcedureSave;
                -- If the transaction is uncommitable, a
                -- rollback to the savepoint is not allowed
                -- because the savepoint rollback writes to
                -- the log. Just return to the caller, which
                -- should roll back the outer transaction.

        -- After the appropriate rollback, echo error
        -- information to the caller.
        DECLARE @ErrorMessage NVARCHAR(4000);
        DECLARE @ErrorSeverity INT;
        DECLARE @ErrorState INT;

        SELECT @ErrorMessage = ERROR_MESSAGE();
        SELECT @ErrorSeverity = ERROR_SEVERITY();
        SELECT @ErrorState = ERROR_STATE();

        RAISERROR (@ErrorMessage, -- Message text.
                   @ErrorSeverity, -- Severity.
                   @ErrorState -- State.
                   );
    END CATCH
GO
```

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

```sql
-- 简略版
select
    B.name  as column_name,
    D.name  as column_type,
    C.value as column_desc
from sys.tables as A
    inner join sys.columns as B
    on B.object_id = A.object_id
    left join sys.extended_properties as C
    on C.major_id = B.object_id and C.minor_id = B.column_id
    left join sys.types as D
    on D.user_type_id = B.user_type_id
where A.name = '${table_name}'
order by B.column_id
```

### Show Table Information Schema by MarkDown

```sql
DECLARE @TableName NVARCHAR(256)='input your table name'
DECLARE @FieldTable TABLE
(
    FieldName NVARCHAR(256),
    PrimaryKey NVARCHAR(20),
    DataType NVARCHAR(50),
    FieldLength NVARCHAR(50),
    NeedNull NVARCHAR(50),
    DefaultValue NVARCHAR(1024),
    Description NVARCHAR(1024)
)
INSERT INTO @FieldTable VALUES('|字段名','|主键','| 类型','| 长度','| 允许空','| 默认值','| 字段说明|')
INSERT INTO @FieldTable VALUES('|:-------','|:-------','|:-------','|:-------','|:-------','|:-------','|:-------|')
INSERT INTO @FieldTable
SELECT
    字段名     = '|' + a.name ,
    主键       = '|' + case when exists(SELECT 1 FROM sysobjects where xtype='PK' and parent_obj=a.id and name in (
                     SELECT name FROM sysindexes WHERE indid in( SELECT indid FROM sysindexkeys WHERE id = a.id AND colid=a.colid))) then '√' else '' end,
    类型       = '|' + b.name,
    长度       = '|' + CONVERT(NVARCHAR(10),COLUMNPROPERTY(a.id,a.name,'PRECISION')),
    允许空     = '|' + case when a.isnullable=1 then '√' else '×' end,
    默认值     = '|' + ISNULL(e.text,''),
    字段说明   = '|' + CONVERT(NVARCHAR(1024),ISNULL(g.[value],'')) + '|'
FROM
    syscolumns a left join
    systypes b on a.xusertype=b.xusertype inner join
    sysobjects d on a.id=d.id  and d.xtype='U' and  d.name<>'dtproperties' left join
    syscomments e on a.cdefault=e.id left join
    sys.extended_properties g on a.id=G.major_id and a.colid=g.minor_id left join
    sys.extended_properties f on d.id=f.major_id and f.minor_id=0
WHERE d.name=@TableName
ORDER BY a.id, a.colorder

SELECT * FROM @FieldTable
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

### Generate Time Sequence

```sql
DECLARE @StartDate DATETIME='2021-07-12'
DECLARE @StartEnd DATETIME='2022-07-12'

DECLARE @TimeSequenceTable TABLE
(
TimeString NVARCHAR(20),
Status INT
)


WHILE @StartDate<=@StartEnd
BEGIN

    DECLARE @DayString NVARCHAR(50)
    SET @DayString = CONVERT(nvarchar(50), @StartDate, 112)

    DECLARE @DayStart INT=0
    DECLARE @DayEnd INT=24
    BEGIN TRANSACTION
    WHILE @DayStart<@DayEnd
    BEGIN
        DECLARE @HourString NVARCHAR(50)
        SET @HourString = stuff('00',1,len('' + @DayStart),'')+CONVERT(varchar(50),'' + @DayStart)
        SET @DayStart=@DayStart+1

        DECLARE @MinuteStart INT=0
        DECLARE @MinuteEnd INT=60

        WHILE @MinuteStart<@MinuteEnd
        BEGIN
            DECLARE @MinuteString NVARCHAR(50)
            SET @MinuteString=stuff('00',1,len('' + @MinuteStart),'')+CONVERT(varchar(50),'' + @MinuteStart)

            DECLARE @TimeSequence NVARCHAR(50)
            SET @TimeSequence = @DayString + @HourString + @MinuteString

            INSERT INTO @TimeSequenceTable(TimeString, Status) VALUES (@TimeSequence, 0)
            SET @MinuteStart=@MinuteStart+1
        END
    END
    COMMIT
    SET @StartDate=DATEADD(DAY, 1, @StartDate)
END

SELECT * FROM @TimeSequenceTable
```

### Generate Backup Script

```sql
DECLARE @BackDate nvarchar(50) =replace(replace(replace(convert(varchar,getdate(),20),'-',''),' ',''),':','')
SELECT 'backup database '+name+' to disk=''F:\DBbackup\'+name+'\'+name+'_'+@BackDate+'.bak'' with buffercount = 6, maxtransfersize = 2097152 ,compression,noformat,noinit,NAME=N''完整备份'',skip,norewind,nounload'
FROM sys.sysdatabases
WHERE NAME not in('master','msdb','tempdb','model','ReportServer','ReportServerTempDB') ORDER BY NAME
```

### Convert Datetime

```sql
SELECT CONVERT(nvarchar(50), GETDATE(), 0)    -- 12 28 2022 4:06PM
SELECT CONVERT(nvarchar(50), GETDATE(), 1)    -- 12/28/09
SELECT CONVERT(nvarchar(50), GETDATE(), 2)    -- 09.12.28
SELECT CONVERT(nvarchar(50), GETDATE(), 3)    -- 28/12/09
SELECT CONVERT(nvarchar(50), GETDATE(), 4)    -- 28.12.09
SELECT CONVERT(nvarchar(50), GETDATE(), 5)    -- 28-12-09
SELECT CONVERT(nvarchar(50), GETDATE(), 6)    -- 28 12 09
SELECT CONVERT(nvarchar(50), GETDATE(), 7)    -- 12 28, 09
SELECT CONVERT(nvarchar(50), GETDATE(), 8)    -- 16:06:26
SELECT CONVERT(nvarchar(50), GETDATE(), 9)    -- 12 28 2022 4:06:26:513PM
SELECT CONVERT(nvarchar(50), GETDATE(), 10)   -- 12-28-09
SELECT CONVERT(nvarchar(50), GETDATE(), 11)   -- 09/12/28
SELECT CONVERT(nvarchar(50), GETDATE(), 12)   -- 091228
SELECT CONVERT(nvarchar(50), GETDATE(), 13)   -- 28 12 2022 16:06:26:513
SELECT CONVERT(nvarchar(50), GETDATE(), 14)   -- 16:06:26:513
SELECT CONVERT(nvarchar(50), GETDATE(), 20)   -- 2022-12-28 16:06:26
SELECT CONVERT(nvarchar(50), GETDATE(), 21)   -- 2022-12-28 16:06:26.513
SELECT CONVERT(nvarchar(50), GETDATE(), 22)   -- 12/28/09 4:06:26 PM
SELECT CONVERT(nvarchar(50), GETDATE(), 23)   -- 2022-12-28
SELECT CONVERT(nvarchar(50), GETDATE(), 24)   -- 16:06:26
SELECT CONVERT(nvarchar(50), GETDATE(), 25)   -- 2022-12-28 16:06:26.513
SELECT CONVERT(nvarchar(50), GETDATE(), 100)  -- 12 28 2022 4:06PM
SELECT CONVERT(nvarchar(50), GETDATE(), 101)  -- 12/28/2022
SELECT CONVERT(nvarchar(50), GETDATE(), 102)  -- 2022.12.28
SELECT CONVERT(nvarchar(50), GETDATE(), 103)  -- 28/12/2022
SELECT CONVERT(nvarchar(50), GETDATE(), 104)  -- 28.12.2022
SELECT CONVERT(nvarchar(50), GETDATE(), 105)  -- 28-12-2022
SELECT CONVERT(nvarchar(50), GETDATE(), 106)  -- 28 12 2022
SELECT CONVERT(nvarchar(50), GETDATE(), 112)  -- 12 28, 2022
SELECT CONVERT(nvarchar(50), GETDATE(), 108)  -- 16:06:26
SELECT CONVERT(nvarchar(50), GETDATE(), 109)  -- 12 28 2022 4:06:26:513PM
SELECT CONVERT(nvarchar(50), GETDATE(), 110)  -- 12-28-2022
SELECT CONVERT(nvarchar(50), GETDATE(), 111)  -- 2022/12/28
SELECT CONVERT(nvarchar(50), GETDATE(), 112)  -- 20221228
SELECT CONVERT(nvarchar(50), GETDATE(), 113)  -- 28 12 2022 16:06:26:513
SELECT CONVERT(nvarchar(50), GETDATE(), 114)  -- 16:06:26:513
SELECT CONVERT(nvarchar(50), GETDATE(), 120)  -- 2022-12-28 16:06:26
SELECT CONVERT(nvarchar(50), GETDATE(), 121)  -- 2022-12-28 16:06:26.513
SELECT CONVERT(nvarchar(50), GETDATE(), 126)  -- 2022-12-28T16:06:26.513
SELECT CONVERT(nvarchar(50), GETDATE(), 130)  -- 23 ??? 1430 4:06:26:513PM
SELECT CONVERT(nvarchar(50), GETDATE(), 131)  -- 23/12/1430 4:06:26:513PM
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

### 查看当前正在执行的 sql 语句

```sql
SELECT [session_id]          = r.session_id,
       [blocking_session_id] = r.blocking_session_id,
       [loginame]            = sp.loginame,
       [db_name]             = DB_NAME(sp.dbid),
       [command]             = r.command,
       [status]              = r.status,
       [wait_type]           = r.wait_type,
       [wait_time]           = r.wait_time,
       [wait_resource]       = r.wait_resource,
       [read]                = r.reads,
       [writes]              = r.writes,
       [logical_reads]       = r.logical_reads,
       [row_count]           = r.row_count,
       [total_elapsed_time]  = r.total_elapsed_time,
       [cpu_time]            = r.cpu_time,
       [input_buffer]        = ib.event_info,
       [individual_query]    = SUBSTRING(
                                            st.text,
                                            r.statement_start_offset / 2,
                                            (CASE
                                                 WHEN r.statement_end_offset = -1 THEN
                                                     LEN(CONVERT(NVARCHAR(MAX), st.text)) * 2
                                                 ELSE
                                                     r.statement_end_offset
                                             END - r.statement_start_offset
                                            ) / 2
                                        ),
       [parent_query]        = st.text,
       [program]               = sp.program_name,
       sp.hostname,
       sp.nt_domain,
       r.start_time
FROM sys.dm_exec_requests                            r
     CROSS APPLY sys.dm_exec_input_buffer(r.session_id, r.request_id) ib
     CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) st
     INNER JOIN sys.sysprocesses                     sp
         ON r.session_id = sp.spid
WHERE session_id > 50 -- Ignore system spids.
      AND session_id NOT IN (@@SPID) -- Ignore this current statement.
ORDER BY sp.spid, sp.ecid;
```

[sys.dm_exec_requests](https://docs.microsoft.com/zh-cn/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-requests-transact-sql?view=sql-server-ver15)

[sys.sysprocesses](https://docs.microsoft.com/zh-cn/sql/relational-databases/system-compatibility-views/sys-sysprocesses-transact-sql?view=sql-server-ver15)

[sys.dm_exec_sql_text](https://docs.microsoft.com/zh-cn/sql/relational-databases/system-dynamic-management-views/sys-dm-exec-sql-text-transact-sql?view=sql-server-ver15)

### 查询 Buffer 使用情况

```sql
SELECT
	indexes.name AS index_name,
	objects.name AS object_name,
	objects.type_desc AS object_type_description,
	--COUNT(*) AS buffer_cache_total_pages,
 --   SUM(CASE WHEN dm_os_buffer_descriptors.is_modified = 1
	--			THEN 1
	--			ELSE 0
	--	END) AS buffer_cache_dirty_pages,
 --   SUM(CASE WHEN dm_os_buffer_descriptors.is_modified = 1
	--			THEN 0
	--			ELSE 1
	--	END) AS buffer_cache_clean_pages,
	COUNT(*) * 8 /1024 AS buffer_cache_MB,
    SUM(CASE WHEN dm_os_buffer_descriptors.is_modified = 1
				THEN 1
				ELSE 0
		END) * 8 / 1024 AS buffer_cache_dirty_page_MB,
    SUM(CASE WHEN dm_os_buffer_descriptors.is_modified = 1
				THEN 0
				ELSE 1
		END) * 8 / 1024 AS buffer_cache_clean_page_MB
FROM sys.dm_os_buffer_descriptors
    INNER JOIN sys.allocation_units ON allocation_units.allocation_unit_id = dm_os_buffer_descriptors.allocation_unit_id
    INNER JOIN sys.partitions ON (
        (
            allocation_units.container_id = partitions.hobt_id
            AND type IN (1, 3)
        )
        OR (
            allocation_units.container_id = partitions.partition_id
            AND type IN (2)
        )
    )
    INNER JOIN sys.objects ON partitions.object_id = objects.object_id
    INNER JOIN sys.indexes ON objects.object_id = indexes.object_id
    AND partitions.index_id = indexes.index_id
WHERE allocation_units.type IN (1, 2, 3)
    AND objects.is_ms_shipped = 0
    AND dm_os_buffer_descriptors.database_id = DB_ID()
GROUP BY indexes.name,
    objects.name,
    objects.type_desc
ORDER BY COUNT(*) DESC;
```

- [Insight into the SQL Server buffer cache](https://www.sqlshack.com/insight-into-the-sql-server-buffer-cache/)

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

```sql
SELECT o.name AS 表名,
    p.TableRows as 表行数,
    i.name AS 索引名,
    dm_ius.user_seeks AS 搜索次数,
    dm_ius.user_scans AS 扫描次数,
    dm_ius.user_lookups AS 查找次数,
    dm_ius.user_updates AS 更新次数
FROM sys.dm_db_index_usage_stats dm_ius
    JOIN sys.indexes i ON i.index_id = dm_ius.index_id
    AND dm_ius.object_id = i.object_id
    JOIN sys.objects o ON dm_ius.object_id = o.object_id
    JOIN sys.schemas s ON o.schema_id = s.schema_id
    JOIN (
        SELECT SUM(p.rows) TableRows,
            p.index_id,
            p.object_id
        FROM sys.partitions p
        GROUP BY p.index_id,
            p.object_id
    ) p ON p.index_id = dm_ius.index_id
    AND dm_ius.object_id = p.object_id
WHERE OBJECTPROPERTY(dm_ius.object_id, 'IsUserTable') = 1
    AND dm_ius.database_id = DB_ID()
order by o.name,
    i.name
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

## Always on

### CREATE LOGIN

```sql
-- always on 集群登陆账号需要通过脚本手动同步
select 'CREATE LOGIN [' + name + '] WITH PASSWORD=' + sys.fn_varbintohexstr(password_hash) + ' HASHED,SID=' + sys.fn_varbintohexstr(sid) + ';'
        from sys.sql_logins
        where name<>'sa'

union all

select 'CREATE LOGIN [' + name + '] FROM WINDOWS;'
    from sys.syslogins
    where isntname=1
        and name not like 'BUILTIN%'
        and name not like 'NT AUTHORITY%'
        and name not like @@servername + '%'
```

## Monitor

[sp_whoisactive](https://github.com/amachanic/sp_whoisactive)
