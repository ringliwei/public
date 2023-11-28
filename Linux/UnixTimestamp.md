# Unix timestamp

- [Unix timestamp](#unix-timestamp)
  - [get `Unix timestamp`](#get-unix-timestamp)
  - [`Unix timestamp` to Other](#unix-timestamp-to-other)
  - [Other to `Unix timestamp`](#other-to-unix-timestamp)
  - [Referance](#referance)

Unix 时间戳(Unix timestamp)，或称 Unix 时间(Unix time)、POSIX 时间(POSIX time)，是一种时间表示方式，定义为从格林威治时间 1970 年 01 月 01 日 00 时 00 分 00 秒起至现在的总秒数。

## get `Unix timestamp`

| 语言                                    | 方式                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------ |
| Java                                    | time                                                                           |
| JavaScript                              | Math.round(new Date().getTime()/1000) getTime()返回数值的单位是毫秒            |
| Microsoft .NET / C#                     | epoch = (DateTime.Now.ToUniversalTime().Ticks - 621355968000000000) / 10000000 |
| MySQL                                   | SELECT unix_timestamp(now())                                                   |
| Perl                                    | time                                                                           |
| PHP                                     | time()                                                                         |
| PostgreSQL                              | SELECT extract(epoch FROM now())                                               |
| Python                                  | 先 import time 然后 time.time()                                                |
| Ruby                                    | 获取 Unix 时间戳：Time.now 或 Time.new 显示 Unix 时间戳：Time.now.to_i         |
| SQL Server                              | SELECT DATEDIFF(s, '1970-01-01 00:00:00', GETUTCDATE())                        |
| Unix / Linux                            | date +%s                                                                       |
| VBScript / ASP                          | DateDiff("s", "01/01/1970 00:00:00", Now())                                    |
| 其他操作系统 (如果 Perl 被安装在系统中) | 命令行状态：perl -e "print time"                                               |

## `Unix timestamp` to Other

| 语言                                    | 方式                                                                                                                   |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Java                                    | String date = new java.text.SimpleDateFormat("dd/MM/yyyy HH:mm:ss").format(new java.util.Date(Unix timestamp \* 1000)) |
| JavaScript                              | 先 var unixTimestamp = new Date(Unix timestamp \* 1000) 然后 commonTime = unixTimestamp.toLocaleString()               |
| Linux                                   | date -d @Unix timestamp                                                                                                |
| MySQL                                   | from_unixtime(Unix timestamp)                                                                                          |
| Perl                                    | 先 my $time = Unix timestamp 然后 my ($sec, $min, $hour, $day, $month, $year) = (localtime($time))[0,1,2,3,4,5,6]      |
| PHP                                     | date('r', Unix timestamp)                                                                                              |
| PostgreSQL                              | SELECT TIMESTAMP WITH TIME ZONE 'epoch' + Unix timestamp) \* INTERVAL '1 second';                                      |
| Python                                  | 先 import time 然后 time.gmtime(Unix timestamp)                                                                        |
| Ruby                                    | Time.at(Unix timestamp)                                                                                                |
| SQL Server                              | DATEADD(s, Unix timestamp, '1970-01-01 00:00:00')                                                                      |
| VBScript / ASP                          | DateAdd("s", Unix timestamp, "01/01/1970 00:00:00")                                                                    |
| 其他操作系统 (如果 Perl 被安装在系统中) | 命令行状态：perl -e "print scalar(localtime(Unix timestamp))"                                                          |

## Other to `Unix timestamp`

| 语言           | 方式                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------ |
| Java           | long epoch = new java.text.SimpleDateFormat("dd/MM/yyyy HH:mm:ss").parse("01/01/1970 01:00:00"); |
| JavaScript     | var commonTime = new Date(Date.UTC(year, month - 1, day, hour, minute, second))                  |
| MySQL          | SELECT unix_timestamp(time) 时间格式: YYYY-MM-DD HH:MM:SS 或 YYMMDD 或 YYYYMMDD                  |
| Perl           | 先 use Time::Local 然后 my $time = timelocal($sec, $min, $hour, $day, $month, $year);            |
| PHP            | mktime(hour, minute, second, day, month, year)                                                   |
| PostgreSQL     | SELECT extract(epoch FROM date('YYYY-MM-DD HH:MM:SS'));                                          |
| Python         | 先 import time 然后 int(time.mktime(time.strptime('YYYY-MM-DD HH:MM:SS', '%Y-%m-%d %H:%M:%S')))  |
| Ruby           | Time.local(year, month, day, hour, minute, second)                                               |
| SQL Server     | SELECT DATEDIFF(s, '1970-01-01 00:00:00', time)                                                  |
| Unix / Linux   | date +%s -d"Jan 1, 1970 00:00:01"                                                                |
| VBScript / ASP | DateDiff("s", "01/01/1970 00:00:00", time)                                                       |

## Referance

- [什么是 Unix 时间戳？](https://www.cnblogs.com/ckie/p/6552678.html)
