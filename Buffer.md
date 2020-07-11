# Buffer

- [Buffer](#buffer)
  - [Java NIO Buffer](#java-nio-buffer)
    - [Basic Buffer Usage](#basic-buffer-usage)
  - [Netty Buffer](#netty-buffer)
  - [okio Buffer](#okio-buffer)
  - [RingBuffer](#ringbuffer)
    - [区分缓冲区是否为满的策略](#区分缓冲区是否为满的策略)
      - [总是保持一个存储单元为空](#总是保持一个存储单元为空)
      - [使用数据计数](#使用数据计数)

最近处理网络程序时，了解到读取数据时需要 `Buffer` 处理。大致原理类似：内置数组，然后提供读写操作；池化数组，提高性能。

阅读以下源码：

- SpringBoot 2.1.7.RELEASE
- JAVA SE 14
- Netty 4.1.38
- OKHTTP 3.14.9
- OKIO 1.17.2
  
## Java NIO Buffer

[Package java.nio](https://docs.oracle.com/en/java/javase/14/docs/api/java.base/java/nio/package-summary.html)

[Buffer](https://docs.oracle.com/en/java/javase/14/docs/api/java.base/java/nio/Buffer.html)

[Java NIO 系列教程](http://ifeve.com/java-nio-all/)

[Java NIO Tutorial](http://tutorials.jenkov.com/java-nio/index.html)

### Basic Buffer Usage

[buffers](http://tutorials.jenkov.com/java-nio/buffers.html)

Using a Buffer to read and write data typically follows this little 4-step process:

1. Write data into the Buffer
2. Call buffer.flip()
3. Read data out of the Buffer
4. Call buffer.clear() or buffer.compact()

When you write data into a buffer, the buffer keeps track of how much data you have written. Once you need to read the data, you need to switch the buffer from writing mode into reading mode using the flip() method call. In reading mode the buffer lets you read all the data written into the buffer.

Once you have read all the data, you need to clear the buffer, to make it ready for writing again. You can do this in two ways: By calling clear() or by calling compact(). The clear() method clears the whole buffer. The compact() method only clears the data which you have already read. Any unread data is moved to the beginning of the buffer, and data will now be written into the buffer after the unread data.

Here is a simple Buffer usage example, with the write, flip, read and clear operations maked in bold:

```java
RandomAccessFile aFile = new RandomAccessFile("data/nio-data.txt", "rw");
FileChannel inChannel = aFile.getChannel();

//create buffer with capacity of 48 bytes
ByteBuffer buf = ByteBuffer.allocate(48);

int bytesRead = inChannel.read(buf); //read into buffer.
while (bytesRead != -1) {

  buf.flip();  //make buffer ready for read

  while(buf.hasRemaining()){
      System.out.print((char) buf.get()); // read 1 byte at a time
  }

  buf.clear(); //make buffer ready for writing
  bytesRead = inChannel.read(buf);
}
aFile.close();
```

> The `flip()` method switches a Buffer from writing mode to reading mode.

## Netty Buffer

写入数据到 ByteBuf 后，writerIndex（写入索引）增加。开始读字节后，readerIndex（读取索引）增加。你可以读取字节，直到写入索引和读取索引处在相同的位置，ByteBuf 变为不可读。当访问数据超过数组的最后位，则会抛出 IndexOutOfBoundsException。

[ByteBuf - 字节数据的容器](https://waylau.com/essential-netty-in-action/CORE%20FUNCTIONS/ByteBuf%20-%20The%20byte%20data%20container.html)

[ByteBuf](https://github.com/netty/netty/blob/4.1/buffer/src/main/java/io/netty/buffer/ByteBuf.java)

[AbstractByteBuf](https://github.com/netty/netty/blob/4.1/buffer/src/main/java/io/netty/buffer/AbstractByteBuf.java)

[CompositeByteBuf](https://github.com/netty/netty/blob/4.1/buffer/src/main/java/io/netty/buffer/CompositeByteBuf.java)

```java
/**
CompositeByteBuf.getBytes

组合ByteBuf, 与 okio Buffter 中以 Segment 实现类似。

*/
public CompositeByteBuf getBytes(int index, ByteBuf dst, int dstIndex, int length) {
    checkDstIndex(index, length, dstIndex, dst.capacity());
    if (length == 0) {
        return this;
    }

    int i = toComponentIndex0(index);
    while (length > 0) {
        Component c = components[i];
        int localLength = Math.min(length, c.endOffset - index);
        c.buf.getBytes(c.idx(index), dst, dstIndex, localLength);
        index += localLength;
        dstIndex += localLength;
        length -= localLength;
        i ++;
    }
    return this;
}

private int toComponentIndex0(int offset) {
    int size = componentCount;
    if (offset == 0) { // fast-path zero offset
        for (int i = 0; i < size; i++) {
            if (components[i].endOffset > 0) {
                return i;
            }
        }
    }
    if (size <= 2) { // fast-path for 1 and 2 component count
        return size == 1 || offset < components[0].endOffset ? 0 : 1;
    }
    for (int low = 0, high = size; low <= high;) {
        int mid = low + high >>> 1;
        Component c = components[mid];
        if (offset >= c.endOffset) {
            low = mid + 1;
        } else if (offset < c.offset) {
            high = mid - 1;
        } else {
            return mid;
        }
    }

    throw new Error("should not reach here");
}

@Override
public CompositeByteBuf setBytes(int index, ByteBuffer src) {
    int limit = src.limit();
    int length = src.remaining();

    checkIndex(index, length);
    if (length == 0) {
        return this;
    }

    int i = toComponentIndex0(index);
    try {
        while (length > 0) {
            Component c = components[i];
            int localLength = Math.min(length, c.endOffset - index);
            src.limit(src.position() + localLength);
            c.buf.setBytes(c.idx(index), src);
            index += localLength;
            length -= localLength;
            i ++;
        }
    } finally {
        src.limit(limit);
    }
    return this;
}

@Override
public CompositeByteBuf setBytes(int index, ByteBuf src, int srcIndex, int length) {
    checkSrcIndex(index, length, srcIndex, src.capacity());
    if (length == 0) {
        return this;
    }

    int i = toComponentIndex0(index);
    while (length > 0) {
        Component c = components[i];
        int localLength = Math.min(length, c.endOffset - index);
        c.buf.setBytes(c.idx(index), src, srcIndex, localLength);
        index += localLength;
        srcIndex += localLength;
        length -= localLength;
        i ++;
    }
    return this;
}
```

## okio Buffer

[Buffer](https://github.com/square/okio/blob/okio-parent-1.17.2/okio/src/main/java/okio/Buffer.java)

[Segment](https://github.com/square/okio/blob/okio-parent-1.17.2/okio/src/main/java/okio/Segment.java)

[SegmentPool](https://github.com/square/okio/blob/okio-parent-1.17.2/okio/src/main/java/okio/SegmentPool.java)

`Buffer` 通过维护 `Segment` 链表形成池。

```java
/**
 * A segment of a buffer.
 *
 * <p>Each segment in a buffer is a circularly-linked list node referencing the following and
 * preceding segments in the buffer.
 *
 * <p>Each segment in the pool is a singly-linked list node referencing the rest of segments in the
 * pool.
 *
 * <p>The underlying byte arrays of segments may be shared between buffers and byte strings. When a
 * segment's byte array is shared the segment may not be recycled, nor may its byte data be changed.
 * The lone exception is that the owner segment is allowed to append to the segment, writing data at
 * {@code limit} and beyond. There is a single owning segment for each byte array. Positions,
 * limits, prev, and next references are not shared.
 */
final class Segment {
  /** The size of all segments in bytes. */
  static final int SIZE = 8192;

  /** Segments will be shared when doing so avoids {@code arraycopy()} of this many bytes. */
  static final int SHARE_MINIMUM = 1024;

  final byte[] data;

  /** The next byte of application data byte to read in this segment. */
  int pos;

  /** The first byte of available data ready to be written to. */
  int limit;

  /** True if other segments or byte strings use the same byte array. */
  boolean shared;

  /** True if this segment owns the byte array and can append to it, extending {@code limit}. */
  boolean owner;

  /** Next segment in a linked or circularly-linked list. */
  Segment next;

  /** Previous segment in a circularly-linked list. */
  Segment prev;

  Segment() {
    this.data = new byte[SIZE];
    this.owner = true;
    this.shared = false;
  }

  Segment(byte[] data, int pos, int limit, boolean shared, boolean owner) {
    this.data = data;
    this.pos = pos;
    this.limit = limit;
    this.shared = shared;
    this.owner = owner;
  }

  /**
   * Returns a new segment that shares the underlying byte array with this. Adjusting pos and limit
   * are safe but writes are forbidden. This also marks the current segment as shared, which
   * prevents it from being pooled.
   */
  final Segment sharedCopy() {
    shared = true;
    return new Segment(data, pos, limit, true, false);
  }

  /** Returns a new segment that its own private copy of the underlying byte array. */
  final Segment unsharedCopy() {
    return new Segment(data.clone(), pos, limit, false, true);
  }

  /**
   * Removes this segment of a circularly-linked list and returns its successor.
   * Returns null if the list is now empty.
   */
  public final @Nullable Segment pop() {
    Segment result = next != this ? next : null;
    prev.next = next;
    next.prev = prev;
    next = null;
    prev = null;
    return result;
  }

  /**
   * Appends {@code segment} after this segment in the circularly-linked list.
   * Returns the pushed segment.
   */
  public final Segment push(Segment segment) {
    segment.prev = this;
    segment.next = next;
    next.prev = segment;
    next = segment;
    return segment;
  }

  /**
   * Splits this head of a circularly-linked list into two segments. The first
   * segment contains the data in {@code [pos..pos+byteCount)}. The second
   * segment contains the data in {@code [pos+byteCount..limit)}. This can be
   * useful when moving partial segments from one buffer to another.
   *
   * <p>Returns the new head of the circularly-linked list.
   */
  public final Segment split(int byteCount) {
    if (byteCount <= 0 || byteCount > limit - pos) throw new IllegalArgumentException();
    Segment prefix;

    // We have two competing performance goals:
    //  - Avoid copying data. We accomplish this by sharing segments.
    //  - Avoid short shared segments. These are bad for performance because they are readonly and
    //    may lead to long chains of short segments.
    // To balance these goals we only share segments when the copy will be large.
    if (byteCount >= SHARE_MINIMUM) {
      prefix = sharedCopy();
    } else {
      prefix = SegmentPool.take();
      System.arraycopy(data, pos, prefix.data, 0, byteCount);
    }

    prefix.limit = prefix.pos + byteCount;
    pos += byteCount;
    prev.push(prefix);
    return prefix;
  }

  /**
   * Call this when the tail and its predecessor may both be less than half
   * full. This will copy data so that segments can be recycled.
   */
  public final void compact() {
    if (prev == this) throw new IllegalStateException();
    if (!prev.owner) return; // Cannot compact: prev isn't writable.
    int byteCount = limit - pos;
    int availableByteCount = SIZE - prev.limit + (prev.shared ? 0 : prev.pos);
    if (byteCount > availableByteCount) return; // Cannot compact: not enough writable space.
    writeTo(prev, byteCount);
    pop();
    SegmentPool.recycle(this);
  }

  /** Moves {@code byteCount} bytes from this segment to {@code sink}. */
  public final void writeTo(Segment sink, int byteCount) {
    if (!sink.owner) throw new IllegalArgumentException();
    if (sink.limit + byteCount > SIZE) {
      // We can't fit byteCount bytes at the sink's current position. Shift sink first.
      if (sink.shared) throw new IllegalArgumentException();
      if (sink.limit + byteCount - sink.pos > SIZE) throw new IllegalArgumentException();
      System.arraycopy(sink.data, sink.pos, sink.data, 0, sink.limit - sink.pos);
      sink.limit -= sink.pos;
      sink.pos = 0;
    }

    System.arraycopy(data, pos, sink.data, sink.limit, byteCount);
    sink.limit += byteCount;
    pos += byteCount;
  }
}
```

## RingBuffer

环形缓冲区通常有一个读指针和一个写指针。读指针指向环形缓冲区中可读的数据，写指针指向环形缓冲区中可写的缓冲区。通过移动读指针和写指针就可以实现缓冲区的数据读取和写入。在通常情况下，环形缓冲区的读用户仅仅会影响读指针，而写用户仅仅会影响写指针。

### 区分缓冲区是否为满的策略

缓冲区是满、或是空，都有可能出现读指针与写指针指向同一位置。

#### 总是保持一个存储单元为空

缓冲区中总是有一个存储单元保持未使用状态。缓冲区最多存入（size - 1） 个数据。如果读写指针指向同一位置，则缓冲区为空。如果写指针位于读指针的相邻后一个位置，则缓冲区为满。这种策略的优点是简单，缺点是语义上实际可存数据量与缓冲区容量不一致，测试缓冲区是否满需要做取余数计算。

```java

import java.util.Arrays;

/**
 * RingBuffer
 * 缓冲区 空：readIndex ==  writeIndex
 * 缓冲区 满：(writeIndex + 1) % bufferSize == readIndex
 * 特点：保持一个存储单元为空
 * @param <T> 元素类型
 */
public class RingBuffer<T> {
    private final static int DEFAULT_SIZE  = 1024;
    private Object[] buffer;
    private int readIndex = 0;
    private int writeIndex = 0;
    private int bufferSize;

    public RingBuffer(){
        this.bufferSize = DEFAULT_SIZE;
        this.buffer = new Object[bufferSize];
}

    public RingBuffer(int initSize){
        this.bufferSize = initSize;
        this.buffer = new Object[bufferSize];
    }

    private Boolean empty() {
        return readIndex == writeIndex;
    }

    private Boolean full() {
        return (writeIndex + 1) % bufferSize == readIndex;
    }

    public void clear(){
        Arrays.fill(buffer,null);
        this.readIndex = 0;
        this.writeIndex = 0;
    }

    public Boolean put(String value) {
        if (full()) {
            return false;
        }
        buffer[writeIndex] = value;
        writeIndex = (writeIndex + 1) % bufferSize;
        return true;
    }

    public T get() {
        if (empty()) {
            return null;
        }
        Object result = buffer[readIndex];
        readIndex = (readIndex + 1) % bufferSize;
        return (T) result;
    }

    public T[] getAll() {
        if (empty()) {
            return (T[])new Object[0];
        }
        int copyTail = writeIndex;
        int cnt = readIndex < copyTail ? copyTail - readIndex : bufferSize - readIndex + copyTail;
        Object[] result = new String[cnt];
        if (readIndex < copyTail) {
            for (int i = readIndex; i < copyTail; i++) {
                result[i - readIndex] = buffer[i];
            }
        } else {
            for (int i = readIndex; i < bufferSize; i++) {
                result[i - readIndex] = buffer[i];
            }
            for (int i = 0; i < copyTail; i++) {
                result[bufferSize - readIndex + i] = buffer[i];
            }
        }
        readIndex = copyTail;
        return (T[])result;
    }
}
```

#### 使用数据计数

这种策略不使用显式的写指针，而是保持着缓冲区内存储的数据的计数。因此测试缓冲区是空是满非常简单；对性能影响可以忽略。缺点是读写操作都需要修改这个存储数据计数，对于多线程访问缓冲区需要并发控制。

```java
public class RingBuffer<T> {
    private int capacity;

    /**
     * 读写时改变大小，并以此判断buffer空或满。
     */
    private int size;

    private int writeIndex;

    private int readIndex;

    private Object[] buffer;

    public RingBuffer(int capacity) {
        this.capacity = capacity;
        buffer = new Object[capacity];
        size = 0;
        writeIndex = 0;
        readIndex = 0;
    }

    public boolean isFull() {
        if (size == capacity) {
            return true;
        }
        return false;
    }

    public boolean isEmpty() {
        if (size == 0) {
            return true;
        }
        return false;
    }

    public boolean put(T object) {
        if (isFull()) {
            return false;
        }
        if (writeIndex == capacity - 1) {
            buffer[writeIndex] = object;
            writeIndex = 0;
        } else {
            buffer[writeIndex++] = object;
        }

        size++;
        return true;
    }

    public T take() {
        if (isEmpty()) {
            return null;
        }
        Object result;
        if (readIndex == capacity - 1) {
            //如果这次取出的位置在队列的最后一个元素
            result = buffer[readIndex];
            //将对于位置的元素清空
            buffer[readIndex] = null;
            readIndex = 0;
        } else {
            result = buffer[readIndex];
            buffer[readIndex++] = null;
        }

        size--;
        return (T)result;
    }
}
```
