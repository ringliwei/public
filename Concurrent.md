# Concurrent

- [Concurrent](#concurrent)
  - [Promise, Future](#promise-future)
    - [DeferredResult, WebAsyncTask](#deferredresult-webasynctask)
    - [CompletableFuture, Future](#completablefuture-future)
    - [TaskCompletionSource, Task, CancellationTokenSource, CancellationToken](#taskcompletionsource-task-cancellationtokensource-cancellationtoken)
  - [Stream](#stream)
    - [Sink](#sink)
    - [ReferencePipeline](#referencepipeline)
    - [ReduceOps](#reduceops)
    - [Collector](#collector)
  - [Reactive-Streams](#reactive-streams)
    - [Reactor](#reactor)
      - [Publisher](#publisher)
      - [Subscriber](#subscriber)
      - [Subscription](#subscription)
      - [Processor](#processor)
      - [Flux.subscribeOn](#fluxsubscribeon)
      - [Flux.publishOn](#fluxpublishon)
  - [ReactiveX](#reactivex)
    - [RxJava](#rxjava)
    - [Rx.NET](#rxnet)
      - [Pulling vs. Pushing Data](#pulling-vs-pushing-data)
  - [Linq](#linq)
    - [Pipeline](#pipeline)
  - [Node.js](#nodejs)
    - [Promise](#promise)
    - [Observable](#observable)
    - [Streams](#streams)
  - [Schedule](#schedule)
    - [okio](#okio)
    - [Netty](#netty)
    - [DotNetty](#dotnetty)
    - [Android](#android)
      - [Looper](#looper)
      - [RxJava AndroidSchedulers](#rxjava-androidschedulers)
      - [RxJava Schedulers](#rxjava-schedulers)
  - [Resources](#resources)

## Promise, Future

这些类实现的语义都类似，代表一个异步结果: Promise, Future

异步结果可能呈现以下状态：

> timeout, error, completion, cancel

### DeferredResult, WebAsyncTask

[Spring MVC 3.2 Preview: Introducing Servlet 3, Async Support](https://spring.io/blog/2012/05/07/spring-mvc-3-2-preview-introducing-servlet-3-async-support)

[Spring MVC 3.2 Preview: Techniques for Real-time Updates](https://spring.io/blog/2012/05/08/spring-mvc-3-2-preview-techniques-for-real-time-updates/)

[Spring MVC 3.2 Preview: Making a Controller Method Asynchronous](https://spring.io/blog/2012/05/10/spring-mvc-3-2-preview-making-a-controller-method-asynchronous)

[Spring MVC 3.2 Preview: Adding Long Polling to an Existing Web Application](https://spring.io/blog/2012/05/14/spring-mvc-3-2-preview-adding-long-polling-to-an-existing-web-application)

[Spring MVC 3.2 Preview: Chat Sample](https://spring.io/blog/2012/05/16/spring-mvc-3-2-preview-chat-sample/)

[SpringMVC Asynchronous Requests](https://docs.spring.io/spring/docs/current/spring-framework-reference/web.html#mvc-ann-async)

[apollo NotificationControllerV2](https://github.com/ctripcorp/apollo/blob/master/apollo-configservice/src/main/java/com/ctrip/framework/apollo/configservice/controller/NotificationControllerV2.java)

[Config Service 通知配置变化
](https://mp.weixin.qq.com/s/WZMLtkS9ysS4SyQv4O7nPg)

> Long polling 实现方案

### CompletableFuture, Future

```java
/**
 * A {@code Future} represents the result of an asynchronous
 * computation.  Methods are provided to check if the computation is
 * complete, to wait for its completion, and to retrieve the result of
 * the computation.  The result can only be retrieved using method
 * {@code get} when the computation has completed, blocking if
 * necessary until it is ready.  Cancellation is performed by the
 * {@code cancel} method.  Additional methods are provided to
 * determine if the task completed normally or was cancelled. Once a
 * computation has completed, the computation cannot be cancelled.
 * If you would like to use a {@code Future} for the sake
 * of cancellability but not provide a usable result, you can
 * declare types of the form {@code Future<?>} and
 * return {@code null} as a result of the underlying task.
 *
 * <p><b>Sample Usage</b> (Note that the following classes are all
 * made-up.)
 *
 * <pre> {@code
 * interface ArchiveSearcher { String search(String target); }
 * class App {
 *   ExecutorService executor = ...
 *   ArchiveSearcher searcher = ...
 *   void showSearch(String target) throws InterruptedException {
 *     Callable<String> task = () -> searcher.search(target);
 *     Future<String> future = executor.submit(task);
 *     displayOtherThings(); // do other things while searching
 *     try {
 *       displayText(future.get()); // use future
 *     } catch (ExecutionException ex) { cleanup(); return; }
 *   }
 * }}</pre>
 *
 * The {@link FutureTask} class is an implementation of {@code Future} that
 * implements {@code Runnable}, and so may be executed by an {@code Executor}.
 * For example, the above construction with {@code submit} could be replaced by:
 * <pre> {@code
 * FutureTask<String> future = new FutureTask<>(task);
 * executor.execute(future);}</pre>
 *
 * <p>Memory consistency effects: Actions taken by the asynchronous computation
 * <a href="package-summary.html#MemoryVisibility"> <i>happen-before</i></a>
 * actions following the corresponding {@code Future.get()} in another thread.
 *
 * @see FutureTask
 * @see Executor
 * @since 1.5
 * @author Doug Lea
 * @param <V> The result type returned by this Future's {@code get} method
 */
public interface Future<V> {

    /**
     * Attempts to cancel execution of this task.  This attempt will
     * fail if the task has already completed, has already been cancelled,
     * or could not be cancelled for some other reason. If successful,
     * and this task has not started when {@code cancel} is called,
     * this task should never run.  If the task has already started,
     * then the {@code mayInterruptIfRunning} parameter determines
     * whether the thread executing this task should be interrupted in
     * an attempt to stop the task.
     *
     * <p>After this method returns, subsequent calls to {@link #isDone} will
     * always return {@code true}.  Subsequent calls to {@link #isCancelled}
     * will always return {@code true} if this method returned {@code true}.
     *
     * @param mayInterruptIfRunning {@code true} if the thread executing this
     * task should be interrupted; otherwise, in-progress tasks are allowed
     * to complete
     * @return {@code false} if the task could not be cancelled,
     * typically because it has already completed normally;
     * {@code true} otherwise
     */
    boolean cancel(boolean mayInterruptIfRunning);

    /**
     * Returns {@code true} if this task was cancelled before it completed
     * normally.
     *
     * @return {@code true} if this task was cancelled before it completed
     */
    boolean isCancelled();

    /**
     * Returns {@code true} if this task completed.
     *
     * Completion may be due to normal termination, an exception, or
     * cancellation -- in all of these cases, this method will return
     * {@code true}.
     *
     * @return {@code true} if this task completed
     */
    boolean isDone();

    /**
     * Waits if necessary for the computation to complete, and then
     * retrieves its result.
     *
     * @return the computed result
     * @throws CancellationException if the computation was cancelled
     * @throws ExecutionException if the computation threw an
     * exception
     * @throws InterruptedException if the current thread was interrupted
     * while waiting
     */
    V get() throws InterruptedException, ExecutionException;

    /**
     * Waits if necessary for at most the given time for the computation
     * to complete, and then retrieves its result, if available.
     *
     * @param timeout the maximum time to wait
     * @param unit the time unit of the timeout argument
     * @return the computed result
     * @throws CancellationException if the computation was cancelled
     * @throws ExecutionException if the computation threw an
     * exception
     * @throws InterruptedException if the current thread was interrupted
     * while waiting
     * @throws TimeoutException if the wait timed out
     */
    V get(long timeout, TimeUnit unit)
        throws InterruptedException, ExecutionException, TimeoutException;
}
```

### TaskCompletionSource, Task, CancellationTokenSource, CancellationToken

```C#
//
// Summary:
//     Represents the current stage in the lifecycle of a System.Threading.Tasks.Task.
public enum TaskStatus
{
    //
    // Summary:
    //     The task has been initialized but has not yet been scheduled.
    Created = 0,
    //
    // Summary:
    //     The task is waiting to be activated and scheduled internally by the .NET Framework
    //     infrastructure.
    WaitingForActivation = 1,
    //
    // Summary:
    //     The task has been scheduled for execution but has not yet begun executing.
    WaitingToRun = 2,
    //
    // Summary:
    //     The task is running but has not yet completed.
    Running = 3,
    //
    // Summary:
    //     The task has finished executing and is implicitly waiting for attached child
    //     tasks to complete.
    WaitingForChildrenToComplete = 4,
    //
    // Summary:
    //     The task completed execution successfully.
    RanToCompletion = 5,
    //
    // Summary:
    //     The task acknowledged cancellation by throwing an OperationCanceledException
    //     with its own CancellationToken while the token was in signaled state, or the
    //     task's CancellationToken was already signaled before the task started executing.
    //     For more information, see Task Cancellation.
    Canceled = 6,
    //
    // Summary:
    //     The task completed due to an unhandled exception.
    Faulted = 7
}
```

Task Timeout extension

```C#
/// <summary>Creates a new Task that mirrors the supplied task but that will be canceled after the specified timeout.</summary>
/// <typeparam name="TResult">Specifies the type of data contained in the task.</typeparam>
/// <param name="task">The task.</param>
/// <param name="timeout">The timeout.</param>
/// <returns>The new Task that may time out.</returns>
public static Task WithTimeout(this Task task, TimeSpan timeout)
{
    var result = new TaskCompletionSource<object>(task.AsyncState);
    var timer = new Timer(state => ((TaskCompletionSource<object>)state).TrySetCanceled(), result, timeout, TimeSpan.FromMilliseconds(-1));
    task.ContinueWith(t =>
    {
        timer.Dispose();
        result.TrySetFromTask(t);
    }, TaskContinuationOptions.ExecuteSynchronously);
    return result.Task;
}
```

## Stream

[Java8 Stream 原理深度解析](https://www.cnblogs.com/Dorae/p/7779246.html)

[深入理解 Java Stream 流水线](https://www.cnblogs.com/CarpenterLee/p/6637118.html)

[Java 8 Stream 探秘](https://colobu.com/2014/11/18/Java-8-Stream/)

| Stream（pull） | Reactive-Stream(push) | Desc |
| -------------- | --------------------- | ---- |
| Stream         | Flux                  | 0…N  |
| Optional       | Mono                  | 0…1  |

```java
// view source
Stream.of(1, 2, 3).map(x -> x + 1).filter(x -> x % 2 == 0).collect(Collectors.toList());
```

### Sink

```java
/**
 * An extension of {@link Consumer} used to conduct values through the stages of
 * a stream pipeline, with additional methods to manage size information,
 * control flow, etc.  Before calling the {@code accept()} method on a
 * {@code Sink} for the first time, you must first call the {@code begin()}
 * method to inform it that data is coming (optionally informing the sink how
 * much data is coming), and after all data has been sent, you must call the
 * {@code end()} method.  After calling {@code end()}, you should not call
 * {@code accept()} without again calling {@code begin()}.  {@code Sink} also
 * offers a mechanism by which the sink can cooperatively signal that it does
 * not wish to receive any more data (the {@code cancellationRequested()}
 * method), which a source can poll before sending more data to the
 * {@code Sink}.
 *
 * <p>A sink may be in one of two states: an initial state and an active state.
 * It starts out in the initial state; the {@code begin()} method transitions
 * it to the active state, and the {@code end()} method transitions it back into
 * the initial state, where it can be re-used.  Data-accepting methods (such as
 * {@code accept()} are only valid in the active state.
 *
 * @apiNote
 * A stream pipeline consists of a source, zero or more intermediate stages
 * (such as filtering or mapping), and a terminal stage, such as reduction or
 * for-each.  For concreteness, consider the pipeline:
 *
 * <pre>{@code
 *     int longestStringLengthStartingWithA
 *         = strings.stream()
 *                  .filter(s -> s.startsWith("A"))
 *                  .mapToInt(String::length)
 *                  .max();
 * }</pre>
 *
 * <p>Here, we have three stages, filtering, mapping, and reducing.  The
 * filtering stage consumes strings and emits a subset of those strings; the
 * mapping stage consumes strings and emits ints; the reduction stage consumes
 * those ints and computes the maximal value.
 *
 * <p>A {@code Sink} instance is used to represent each stage of this pipeline,
 * whether the stage accepts objects, ints, longs, or doubles.  Sink has entry
 * points for {@code accept(Object)}, {@code accept(int)}, etc, so that we do
 * not need a specialized interface for each primitive specialization.  (It
 * might be called a "kitchen sink" for this omnivorous tendency.)  The entry
 * point to the pipeline is the {@code Sink} for the filtering stage, which
 * sends some elements "downstream" -- into the {@code Sink} for the mapping
 * stage, which in turn sends integral values downstream into the {@code Sink}
 * for the reduction stage. The {@code Sink} implementations associated with a
 * given stage is expected to know the data type for the next stage, and call
 * the correct {@code accept} method on its downstream {@code Sink}.  Similarly,
 * each stage must implement the correct {@code accept} method corresponding to
 * the data type it accepts.
 *
 * <p>The specialized subtypes such as {@link Sink.OfInt} override
 * {@code accept(Object)} to call the appropriate primitive specialization of
 * {@code accept}, implement the appropriate primitive specialization of
 * {@code Consumer}, and re-abstract the appropriate primitive specialization of
 * {@code accept}.
 *
 * <p>The chaining subtypes such as {@link ChainedInt} not only implement
 * {@code Sink.OfInt}, but also maintain a {@code downstream} field which
 * represents the downstream {@code Sink}, and implement the methods
 * {@code begin()}, {@code end()}, and {@code cancellationRequested()} to
 * delegate to the downstream {@code Sink}.  Most implementations of
 * intermediate operations will use these chaining wrappers.  For example, the
 * mapping stage in the above example would look like:
 *
 * <pre>{@code
 *     IntSink is = new Sink.ChainedReference<U>(sink) {
 *         public void accept(U u) {
 *             downstream.accept(mapper.applyAsInt(u));
 *         }
 *     };
 * }</pre>
 *
 * <p>Here, we implement {@code Sink.ChainedReference<U>}, meaning that we expect
 * to receive elements of type {@code U} as input, and pass the downstream sink
 * to the constructor.  Because the next stage expects to receive integers, we
 * must call the {@code accept(int)} method when emitting values to the downstream.
 * The {@code accept()} method applies the mapping function from {@code U} to
 * {@code int} and passes the resulting value to the downstream {@code Sink}.
 *
 * @param <T> type of elements for value streams
 * @since 1.8
 */
interface Sink<T> extends Consumer<T> {
    /**
     * Resets the sink state to receive a fresh data set.  This must be called
     * before sending any data to the sink.  After calling {@link #end()},
     * you may call this method to reset the sink for another calculation.
     * @param size The exact size of the data to be pushed downstream, if
     * known or {@code -1} if unknown or infinite.
     *
     * <p>Prior to this call, the sink must be in the initial state, and after
     * this call it is in the active state.
     */
    default void begin(long size) {}

    /**
     * Indicates that all elements have been pushed.  If the {@code Sink} is
     * stateful, it should send any stored state downstream at this time, and
     * should clear any accumulated state (and associated resources).
     *
     * <p>Prior to this call, the sink must be in the active state, and after
     * this call it is returned to the initial state.
     */
    default void end() {}

    /**
     * Indicates that this {@code Sink} does not wish to receive any more data.
     *
     * @implSpec The default implementation always returns false.
     *
     * @return true if cancellation is requested
     */
    default boolean cancellationRequested() {
        return false;
    }

    /**
     * Accepts an int value.
     *
     * @implSpec The default implementation throws IllegalStateException.
     *
     * @throws IllegalStateException if this sink does not accept int values
     */
    default void accept(int value) {
        throw new IllegalStateException("called wrong accept method");
    }

    /**
     * Accepts a long value.
     *
     * @implSpec The default implementation throws IllegalStateException.
     *
     * @throws IllegalStateException if this sink does not accept long values
     */
    default void accept(long value) {
        throw new IllegalStateException("called wrong accept method");
    }

    /**
     * Accepts a double value.
     *
     * @implSpec The default implementation throws IllegalStateException.
     *
     * @throws IllegalStateException if this sink does not accept double values
     */
    default void accept(double value) {
        throw new IllegalStateException("called wrong accept method");
    }

    /**
     * {@code Sink} that implements {@code Sink<Integer>}, re-abstracts
     * {@code accept(int)}, and wires {@code accept(Integer)} to bridge to
     * {@code accept(int)}.
     */
    interface OfInt extends Sink<Integer>, IntConsumer {
        @Override
        void accept(int value);

        @Override
        default void accept(Integer i) {
            if (Tripwire.ENABLED)
                Tripwire.trip(getClass(), "{0} calling Sink.OfInt.accept(Integer)");
            accept(i.intValue());
        }
    }

    /**
     * {@code Sink} that implements {@code Sink<Long>}, re-abstracts
     * {@code accept(long)}, and wires {@code accept(Long)} to bridge to
     * {@code accept(long)}.
     */
    interface OfLong extends Sink<Long>, LongConsumer {
        @Override
        void accept(long value);

        @Override
        default void accept(Long i) {
            if (Tripwire.ENABLED)
                Tripwire.trip(getClass(), "{0} calling Sink.OfLong.accept(Long)");
            accept(i.longValue());
        }
    }

    /**
     * {@code Sink} that implements {@code Sink<Double>}, re-abstracts
     * {@code accept(double)}, and wires {@code accept(Double)} to bridge to
     * {@code accept(double)}.
     */
    interface OfDouble extends Sink<Double>, DoubleConsumer {
        @Override
        void accept(double value);

        @Override
        default void accept(Double i) {
            if (Tripwire.ENABLED)
                Tripwire.trip(getClass(), "{0} calling Sink.OfDouble.accept(Double)");
            accept(i.doubleValue());
        }
    }

    /**
     * Abstract {@code Sink} implementation for creating chains of
     * sinks.  The {@code begin}, {@code end}, and
     * {@code cancellationRequested} methods are wired to chain to the
     * downstream {@code Sink}.  This implementation takes a downstream
     * {@code Sink} of unknown input shape and produces a {@code Sink<T>}.  The
     * implementation of the {@code accept()} method must call the correct
     * {@code accept()} method on the downstream {@code Sink}.
     */
    abstract static class ChainedReference<T, E_OUT> implements Sink<T> {
        protected final Sink<? super E_OUT> downstream;

        public ChainedReference(Sink<? super E_OUT> downstream) {
            this.downstream = Objects.requireNonNull(downstream);
        }

        @Override
        public void begin(long size) {
            downstream.begin(size);
        }

        @Override
        public void end() {
            downstream.end();
        }

        @Override
        public boolean cancellationRequested() {
            return downstream.cancellationRequested();
        }
    }

    /**
     * Abstract {@code Sink} implementation designed for creating chains of
     * sinks.  The {@code begin}, {@code end}, and
     * {@code cancellationRequested} methods are wired to chain to the
     * downstream {@code Sink}.  This implementation takes a downstream
     * {@code Sink} of unknown input shape and produces a {@code Sink.OfInt}.
     * The implementation of the {@code accept()} method must call the correct
     * {@code accept()} method on the downstream {@code Sink}.
     */
    abstract static class ChainedInt<E_OUT> implements Sink.OfInt {
        protected final Sink<? super E_OUT> downstream;

        public ChainedInt(Sink<? super E_OUT> downstream) {
            this.downstream = Objects.requireNonNull(downstream);
        }

        @Override
        public void begin(long size) {
            downstream.begin(size);
        }

        @Override
        public void end() {
            downstream.end();
        }

        @Override
        public boolean cancellationRequested() {
            return downstream.cancellationRequested();
        }
    }

    /**
     * Abstract {@code Sink} implementation designed for creating chains of
     * sinks.  The {@code begin}, {@code end}, and
     * {@code cancellationRequested} methods are wired to chain to the
     * downstream {@code Sink}.  This implementation takes a downstream
     * {@code Sink} of unknown input shape and produces a {@code Sink.OfLong}.
     * The implementation of the {@code accept()} method must call the correct
     * {@code accept()} method on the downstream {@code Sink}.
     */
    abstract static class ChainedLong<E_OUT> implements Sink.OfLong {
        protected final Sink<? super E_OUT> downstream;

        public ChainedLong(Sink<? super E_OUT> downstream) {
            this.downstream = Objects.requireNonNull(downstream);
        }

        @Override
        public void begin(long size) {
            downstream.begin(size);
        }

        @Override
        public void end() {
            downstream.end();
        }

        @Override
        public boolean cancellationRequested() {
            return downstream.cancellationRequested();
        }
    }

    /**
     * Abstract {@code Sink} implementation designed for creating chains of
     * sinks.  The {@code begin}, {@code end}, and
     * {@code cancellationRequested} methods are wired to chain to the
     * downstream {@code Sink}.  This implementation takes a downstream
     * {@code Sink} of unknown input shape and produces a {@code Sink.OfDouble}.
     * The implementation of the {@code accept()} method must call the correct
     * {@code accept()} method on the downstream {@code Sink}.
     */
    abstract static class ChainedDouble<E_OUT> implements Sink.OfDouble {
        protected final Sink<? super E_OUT> downstream;

        public ChainedDouble(Sink<? super E_OUT> downstream) {
            this.downstream = Objects.requireNonNull(downstream);
        }

        @Override
        public void begin(long size) {
            downstream.begin(size);
        }

        @Override
        public void end() {
            downstream.end();
        }

        @Override
        public boolean cancellationRequested() {
            return downstream.cancellationRequested();
        }
    }
}
```

### ReferencePipeline

```java
/**
 * Abstract base class for an intermediate pipeline stage or pipeline source
 * stage implementing whose elements are of type {@code U}.
 *
 * @param <P_IN> type of elements in the upstream source
 * @param <P_OUT> type of elements in produced by this stage
 *
 * @since 1.8
 */
abstract class ReferencePipeline<P_IN, P_OUT>
        extends AbstractPipeline<P_IN, P_OUT, Stream<P_OUT>>
        implements Stream<P_OUT>  {
    @Override
    @SuppressWarnings("unchecked")
    public final <R> Stream<R> map(Function<? super P_OUT, ? extends R> mapper) {
        Objects.requireNonNull(mapper);
        return new StatelessOp<P_OUT, R>(this, StreamShape.REFERENCE,
                                     StreamOpFlag.NOT_SORTED | StreamOpFlag.NOT_DISTINCT) {
            @Override
            Sink<P_OUT> opWrapSink(int flags, Sink<R> sink) {
                return new Sink.ChainedReference<P_OUT, R>(sink) {
                    @Override
                    public void accept(P_OUT u) {
                        downstream.accept(mapper.apply(u));
                    }
                };
            }
        };
    }

    @Override
    public final <R> Stream<R> flatMap(Function<? super P_OUT, ? extends Stream<? extends R>> mapper) {
        Objects.requireNonNull(mapper);
        return new StatelessOp<P_OUT, R>(this, StreamShape.REFERENCE,
                                     StreamOpFlag.NOT_SORTED | StreamOpFlag.NOT_DISTINCT | StreamOpFlag.NOT_SIZED) {
            @Override
            Sink<P_OUT> opWrapSink(int flags, Sink<R> sink) {
                return new Sink.ChainedReference<P_OUT, R>(sink) {
                    // true if cancellationRequested() has been called
                    boolean cancellationRequestedCalled;

                    @Override
                    public void begin(long size) {
                        downstream.begin(-1);
                    }

                    @Override
                    public void accept(P_OUT u) {
                        try (Stream<? extends R> result = mapper.apply(u)) {
                            if (result != null) {
                                if (!cancellationRequestedCalled) {
                                    result.sequential().forEach(downstream);
                                }
                                else {
                                    var s = result.sequential().spliterator();
                                    do { } while (!downstream.cancellationRequested() && s.tryAdvance(downstream));
                                }
                            }
                        }
                    }

                    @Override
                    public boolean cancellationRequested() {
                        // If this method is called then an operation within the stream
                        // pipeline is short-circuiting (see AbstractPipeline.copyInto).
                        // Note that we cannot differentiate between an upstream or
                        // downstream operation
                        cancellationRequestedCalled = true;
                        return downstream.cancellationRequested();
                    }
                };
            }
        };
    }

    @Override
    public final Stream<P_OUT> filter(Predicate<? super P_OUT> predicate) {
        Objects.requireNonNull(predicate);
        return new StatelessOp<P_OUT, P_OUT>(this, StreamShape.REFERENCE,
                                     StreamOpFlag.NOT_SIZED) {
            @Override
            Sink<P_OUT> opWrapSink(int flags, Sink<P_OUT> sink) {
                return new Sink.ChainedReference<P_OUT, P_OUT>(sink) {
                    @Override
                    public void begin(long size) {
                        downstream.begin(-1);
                    }

                    @Override
                    public void accept(P_OUT u) {
                        if (predicate.test(u))
                            downstream.accept(u);
                    }
                };
            }
        };
    }

    @Override
    @SuppressWarnings("unchecked")
    public final <R, A> R collect(Collector<? super P_OUT, A, R> collector) {
        A container;
        if (isParallel()
                && (collector.characteristics().contains(Collector.Characteristics.CONCURRENT))
                && (!isOrdered() || collector.characteristics().contains(Collector.Characteristics.UNORDERED))) {
            container = collector.supplier().get();
            BiConsumer<A, ? super P_OUT> accumulator = collector.accumulator();
            forEach(u -> accumulator.accept(container, u));
        }
        else {
            // ReduceOps 生成 TerminalOp
            // 假定接下来再调用 ReduceOps.evaluateSequential 生成 ReducingSink 传递给 wrapAndCopyInto
            container = evaluate(ReduceOps.makeRef(collector));
        }
        return collector.characteristics().contains(Collector.Characteristics.IDENTITY_FINISH)
               ? (R) container
               : collector.finisher().apply(container);
    }

    /**
     * Evaluate the pipeline with a terminal operation to produce a result.
     *
     * @param <R> the type of result
     * @param terminalOp the terminal operation to be applied to the pipeline.
     * @return the result
     */
    final <R> R evaluate(TerminalOp<E_OUT, R> terminalOp) {
        assert getOutputShape() == terminalOp.inputShape();
        if (linkedOrConsumed)
            throw new IllegalStateException(MSG_STREAM_LINKED);
        linkedOrConsumed = true;

        return isParallel()
               ? terminalOp.evaluateParallel(this, sourceSpliterator(terminalOp.getOpFlags()))
               : terminalOp.evaluateSequential(this, sourceSpliterator(terminalOp.getOpFlags()));
    }

    /**
     * Get the source spliterator for this pipeline stage.  For a sequential or
     * stateless parallel pipeline, this is the source spliterator.  For a
     * stateful parallel pipeline, this is a spliterator describing the results
     * of all computations up to and including the most recent stateful
     * operation.
     */
    @SuppressWarnings("unchecked")
    private Spliterator<?> sourceSpliterator(int terminalFlags) {
        // Get the source spliterator of the pipeline
        Spliterator<?> spliterator = null;
        if (sourceStage.sourceSpliterator != null) {
            spliterator = sourceStage.sourceSpliterator;
            sourceStage.sourceSpliterator = null;
        }
        else if (sourceStage.sourceSupplier != null) {
            spliterator = (Spliterator<?>) sourceStage.sourceSupplier.get();
            sourceStage.sourceSupplier = null;
        }
        else {
            throw new IllegalStateException(MSG_CONSUMED);
        }

        if (isParallel() && sourceStage.sourceAnyStateful) {
            // Adapt the source spliterator, evaluating each stateful op
            // in the pipeline up to and including this pipeline stage.
            // The depth and flags of each pipeline stage are adjusted accordingly.
            int depth = 1;
            for (@SuppressWarnings("rawtypes") AbstractPipeline u = sourceStage, p = sourceStage.nextStage, e = this;
                 u != e;
                 u = p, p = p.nextStage) {

                int thisOpFlags = p.sourceOrOpFlags;
                if (p.opIsStateful()) {
                    depth = 0;

                    if (StreamOpFlag.SHORT_CIRCUIT.isKnown(thisOpFlags)) {
                        // Clear the short circuit flag for next pipeline stage
                        // This stage encapsulates short-circuiting, the next
                        // stage may not have any short-circuit operations, and
                        // if so spliterator.forEachRemaining should be used
                        // for traversal
                        thisOpFlags = thisOpFlags & ~StreamOpFlag.IS_SHORT_CIRCUIT;
                    }

                    spliterator = p.opEvaluateParallelLazy(u, spliterator);

                    // Inject or clear SIZED on the source pipeline stage
                    // based on the stage's spliterator
                    thisOpFlags = spliterator.hasCharacteristics(Spliterator.SIZED)
                            ? (thisOpFlags & ~StreamOpFlag.NOT_SIZED) | StreamOpFlag.IS_SIZED
                            : (thisOpFlags & ~StreamOpFlag.IS_SIZED) | StreamOpFlag.NOT_SIZED;
                }
                p.depth = depth++;
                p.combinedFlags = StreamOpFlag.combineOpFlags(thisOpFlags, u.combinedFlags);
            }
        }

        if (terminalFlags != 0)  {
            // Apply flags from the terminal operation to last pipeline stage
            combinedFlags = StreamOpFlag.combineOpFlags(terminalFlags, combinedFlags);
        }

        return spliterator;
    }

    @Override
    final <P_IN, S extends Sink<E_OUT>> S wrapAndCopyInto(S sink, Spliterator<P_IN> spliterator) {
        copyInto(wrapSink(Objects.requireNonNull(sink)), spliterator);
        return sink;
    }

    @Override
    @SuppressWarnings("unchecked")
    final <P_IN> Sink<P_IN> wrapSink(Sink<E_OUT> sink) {
        // 代表 TerminalOp 的 ReducingSink
        Objects.requireNonNull(sink);

        for ( @SuppressWarnings("rawtypes") AbstractPipeline p=AbstractPipeline.this; p.depth > 0; p=p.previousStage) {
            sink = p.opWrapSink(p.previousStage.combinedFlags, sink);
        }
        return (Sink<P_IN>) sink;
    }

    @Override
    final <P_IN> void copyInto(Sink<P_IN> wrappedSink, Spliterator<P_IN> spliterator) {
        Objects.requireNonNull(wrappedSink);

        if (!StreamOpFlag.SHORT_CIRCUIT.isKnown(getStreamAndOpFlags())) {
            wrappedSink.begin(spliterator.getExactSizeIfKnown());
            spliterator.forEachRemaining(wrappedSink);
            wrappedSink.end();
        }
        else {
            copyIntoWithCancel(wrappedSink, spliterator);
        }
    }
}
```

### ReduceOps

```java
/**
 * Factory for creating instances of {@code TerminalOp} that implement
 * reductions.
 *
 * @since 1.8
 */
final class ReduceOps {

    private ReduceOps() { }

    @Override
    public <P_IN> R evaluateSequential(PipelineHelper<T> helper,
                                        Spliterator<P_IN> spliterator) {
        return helper.wrapAndCopyInto(makeSink(), spliterator).get();
    }

    /**
     * Constructs a {@code TerminalOp} that implements a mutable reduce on
     * reference values.
     *
     * @param <T> the type of the input elements
     * @param <I> the type of the intermediate reduction result
     * @param collector a {@code Collector} defining the reduction
     * @return a {@code ReduceOp} implementing the reduction
     */
    public static <T, I> TerminalOp<T, I>
    makeRef(Collector<? super T, I, ?> collector) {
        Supplier<I> supplier = Objects.requireNonNull(collector).supplier();
        BiConsumer<I, ? super T> accumulator = collector.accumulator();
        BinaryOperator<I> combiner = collector.combiner();
        class ReducingSink extends Box<I>
                implements AccumulatingSink<T, I, ReducingSink> {
            @Override
            public void begin(long size) {
                state = supplier.get();
            }

            @Override
            public void accept(T t) {
                accumulator.accept(state, t);
            }

            @Override
            public void combine(ReducingSink other) {
                state = combiner.apply(state, other.state);
            }
        }
        return new ReduceOp<T, I, ReducingSink>(StreamShape.REFERENCE) {
            @Override
            public ReducingSink makeSink() {
                return new ReducingSink();
            }

            @Override
            public int getOpFlags() {
                return collector.characteristics().contains(Collector.Characteristics.UNORDERED)
                       ? StreamOpFlag.NOT_ORDERED
                       : 0;
            }
        };
    }
}
```

### Collector

```java
/**
 * A <a href="package-summary.html#Reduction">mutable reduction operation</a> that
 * accumulates input elements into a mutable result container, optionally transforming
 * the accumulated result into a final representation after all input elements
 * have been processed.  Reduction operations can be performed either sequentially
 * or in parallel.
 *
 * <p>Examples of mutable reduction operations include:
 * accumulating elements into a {@code Collection}; concatenating
 * strings using a {@code StringBuilder}; computing summary information about
 * elements such as sum, min, max, or average; computing "pivot table" summaries
 * such as "maximum valued transaction by seller", etc.  The class {@link Collectors}
 * provides implementations of many common mutable reductions.
 *
 * <p>A {@code Collector} is specified by four functions that work together to
 * accumulate entries into a mutable result container, and optionally perform
 * a final transform on the result.  They are: <ul>
 *     <li>creation of a new result container ({@link #supplier()})</li>
 *     <li>incorporating a new data element into a result container ({@link #accumulator()})</li>
 *     <li>combining two result containers into one ({@link #combiner()})</li>
 *     <li>performing an optional final transform on the container ({@link #finisher()})</li>
 * </ul>
 *
 * <p>Collectors also have a set of characteristics, such as
 * {@link Characteristics#CONCURRENT}, that provide hints that can be used by a
 * reduction implementation to provide better performance.
 *
 * <p>A sequential implementation of a reduction using a collector would
 * create a single result container using the supplier function, and invoke the
 * accumulator function once for each input element.  A parallel implementation
 * would partition the input, create a result container for each partition,
 * accumulate the contents of each partition into a subresult for that partition,
 * and then use the combiner function to merge the subresults into a combined
 * result.
 *
 * <p>To ensure that sequential and parallel executions produce equivalent
 * results, the collector functions must satisfy an <em>identity</em> and an
 * <a href="package-summary.html#Associativity">associativity</a> constraints.
 *
 * <p>The identity constraint says that for any partially accumulated result,
 * combining it with an empty result container must produce an equivalent
 * result.  That is, for a partially accumulated result {@code a} that is the
 * result of any series of accumulator and combiner invocations, {@code a} must
 * be equivalent to {@code combiner.apply(a, supplier.get())}.
 *
 * <p>The associativity constraint says that splitting the computation must
 * produce an equivalent result.  That is, for any input elements {@code t1}
 * and {@code t2}, the results {@code r1} and {@code r2} in the computation
 * below must be equivalent:
 * <pre>{@code
 *     A a1 = supplier.get();
 *     accumulator.accept(a1, t1);
 *     accumulator.accept(a1, t2);
 *     R r1 = finisher.apply(a1);  // result without splitting
 *
 *     A a2 = supplier.get();
 *     accumulator.accept(a2, t1);
 *     A a3 = supplier.get();
 *     accumulator.accept(a3, t2);
 *     R r2 = finisher.apply(combiner.apply(a2, a3));  // result with splitting
 * } </pre>
 *
 * <p>For collectors that do not have the {@code UNORDERED} characteristic,
 * two accumulated results {@code a1} and {@code a2} are equivalent if
 * {@code finisher.apply(a1).equals(finisher.apply(a2))}.  For unordered
 * collectors, equivalence is relaxed to allow for non-equality related to
 * differences in order.  (For example, an unordered collector that accumulated
 * elements to a {@code List} would consider two lists equivalent if they
 * contained the same elements, ignoring order.)
 *
 * <p>Libraries that implement reduction based on {@code Collector}, such as
 * {@link Stream#collect(Collector)}, must adhere to the following constraints:
 * <ul>
 *     <li>The first argument passed to the accumulator function, both
 *     arguments passed to the combiner function, and the argument passed to the
 *     finisher function must be the result of a previous invocation of the
 *     result supplier, accumulator, or combiner functions.</li>
 *     <li>The implementation should not do anything with the result of any of
 *     the result supplier, accumulator, or combiner functions other than to
 *     pass them again to the accumulator, combiner, or finisher functions,
 *     or return them to the caller of the reduction operation.</li>
 *     <li>If a result is passed to the combiner or finisher
 *     function, and the same object is not returned from that function, it is
 *     never used again.</li>
 *     <li>Once a result is passed to the combiner or finisher function, it
 *     is never passed to the accumulator function again.</li>
 *     <li>For non-concurrent collectors, any result returned from the result
 *     supplier, accumulator, or combiner functions must be serially
 *     thread-confined.  This enables collection to occur in parallel without
 *     the {@code Collector} needing to implement any additional synchronization.
 *     The reduction implementation must manage that the input is properly
 *     partitioned, that partitions are processed in isolation, and combining
 *     happens only after accumulation is complete.</li>
 *     <li>For concurrent collectors, an implementation is free to (but not
 *     required to) implement reduction concurrently.  A concurrent reduction
 *     is one where the accumulator function is called concurrently from
 *     multiple threads, using the same concurrently-modifiable result container,
 *     rather than keeping the result isolated during accumulation.
 *     A concurrent reduction should only be applied if the collector has the
 *     {@link Characteristics#UNORDERED} characteristics or if the
 *     originating data is unordered.</li>
 * </ul>
 *
 * <p>In addition to the predefined implementations in {@link Collectors}, the
 * static factory methods {@link #of(Supplier, BiConsumer, BinaryOperator, Characteristics...)}
 * can be used to construct collectors.  For example, you could create a collector
 * that accumulates widgets into a {@code TreeSet} with:
 *
 * <pre>{@code
 *     Collector<Widget, ?, TreeSet<Widget>> intoSet =
 *         Collector.of(TreeSet::new, TreeSet::add,
 *                      (left, right) -> { left.addAll(right); return left; });
 * }</pre>
 *
 * (This behavior is also implemented by the predefined collector
 * {@link Collectors#toCollection(Supplier)}).
 *
 * @apiNote
 * Performing a reduction operation with a {@code Collector} should produce a
 * result equivalent to:
 * <pre>{@code
 *     R container = collector.supplier().get();
 *     for (T t : data)
 *         collector.accumulator().accept(container, t);
 *     return collector.finisher().apply(container);
 * }</pre>
 *
 * <p>However, the library is free to partition the input, perform the reduction
 * on the partitions, and then use the combiner function to combine the partial
 * results to achieve a parallel reduction.  (Depending on the specific reduction
 * operation, this may perform better or worse, depending on the relative cost
 * of the accumulator and combiner functions.)
 *
 * <p>Collectors are designed to be <em>composed</em>; many of the methods
 * in {@link Collectors} are functions that take a collector and produce
 * a new collector.  For example, given the following collector that computes
 * the sum of the salaries of a stream of employees:
 *
 * <pre>{@code
 *     Collector<Employee, ?, Integer> summingSalaries
 *         = Collectors.summingInt(Employee::getSalary))
 * }</pre>
 *
 * If we wanted to create a collector to tabulate the sum of salaries by
 * department, we could reuse the "sum of salaries" logic using
 * {@link Collectors#groupingBy(Function, Collector)}:
 *
 * <pre>{@code
 *     Collector<Employee, ?, Map<Department, Integer>> summingSalariesByDept
 *         = Collectors.groupingBy(Employee::getDepartment, summingSalaries);
 * }</pre>
 *
 * @see Stream#collect(Collector)
 * @see Collectors
 *
 * @param <T> the type of input elements to the reduction operation
 * @param <A> the mutable accumulation type of the reduction operation (often
 *            hidden as an implementation detail)
 * @param <R> the result type of the reduction operation
 * @since 1.8
 */
public interface Collector<T, A, R> {
    /**
     * A function that creates and returns a new mutable result container.
     *
     * @return a function which returns a new, mutable result container
     */
    Supplier<A> supplier();

    /**
     * A function that folds a value into a mutable result container.
     *
     * @return a function which folds a value into a mutable result container
     */
    BiConsumer<A, T> accumulator();

    /**
     * A function that accepts two partial results and merges them.  The
     * combiner function may fold state from one argument into the other and
     * return that, or may return a new result container.
     *
     * @return a function which combines two partial results into a combined
     * result
     */
    BinaryOperator<A> combiner();

    /**
     * Perform the final transformation from the intermediate accumulation type
     * {@code A} to the final result type {@code R}.
     *
     * <p>If the characteristic {@code IDENTITY_FINISH} is
     * set, this function may be presumed to be an identity transform with an
     * unchecked cast from {@code A} to {@code R}.
     *
     * @return a function which transforms the intermediate result to the final
     * result
     */
    Function<A, R> finisher();

    /**
     * Returns a {@code Set} of {@code Collector.Characteristics} indicating
     * the characteristics of this Collector.  This set should be immutable.
     *
     * @return an immutable set of collector characteristics
     */
    Set<Characteristics> characteristics();

    /**
     * Returns a new {@code Collector} described by the given {@code supplier},
     * {@code accumulator}, and {@code combiner} functions.  The resulting
     * {@code Collector} has the {@code Collector.Characteristics.IDENTITY_FINISH}
     * characteristic.
     *
     * @param supplier The supplier function for the new collector
     * @param accumulator The accumulator function for the new collector
     * @param combiner The combiner function for the new collector
     * @param characteristics The collector characteristics for the new
     *                        collector
     * @param <T> The type of input elements for the new collector
     * @param <R> The type of intermediate accumulation result, and final result,
     *           for the new collector
     * @throws NullPointerException if any argument is null
     * @return the new {@code Collector}
     */
    public static<T, R> Collector<T, R, R> of(Supplier<R> supplier,
                                              BiConsumer<R, T> accumulator,
                                              BinaryOperator<R> combiner,
                                              Characteristics... characteristics) {
        Objects.requireNonNull(supplier);
        Objects.requireNonNull(accumulator);
        Objects.requireNonNull(combiner);
        Objects.requireNonNull(characteristics);
        Set<Characteristics> cs = (characteristics.length == 0)
                                  ? Collectors.CH_ID
                                  : Collections.unmodifiableSet(EnumSet.of(Collector.Characteristics.IDENTITY_FINISH,
                                                                           characteristics));
        return new Collectors.CollectorImpl<>(supplier, accumulator, combiner, cs);
    }

    /**
     * Returns a new {@code Collector} described by the given {@code supplier},
     * {@code accumulator}, {@code combiner}, and {@code finisher} functions.
     *
     * @param supplier The supplier function for the new collector
     * @param accumulator The accumulator function for the new collector
     * @param combiner The combiner function for the new collector
     * @param finisher The finisher function for the new collector
     * @param characteristics The collector characteristics for the new
     *                        collector
     * @param <T> The type of input elements for the new collector
     * @param <A> The intermediate accumulation type of the new collector
     * @param <R> The final result type of the new collector
     * @throws NullPointerException if any argument is null
     * @return the new {@code Collector}
     */
    public static<T, A, R> Collector<T, A, R> of(Supplier<A> supplier,
                                                 BiConsumer<A, T> accumulator,
                                                 BinaryOperator<A> combiner,
                                                 Function<A, R> finisher,
                                                 Characteristics... characteristics) {
        Objects.requireNonNull(supplier);
        Objects.requireNonNull(accumulator);
        Objects.requireNonNull(combiner);
        Objects.requireNonNull(finisher);
        Objects.requireNonNull(characteristics);
        Set<Characteristics> cs = Collectors.CH_NOID;
        if (characteristics.length > 0) {
            cs = EnumSet.noneOf(Characteristics.class);
            Collections.addAll(cs, characteristics);
            cs = Collections.unmodifiableSet(cs);
        }
        return new Collectors.CollectorImpl<>(supplier, accumulator, combiner, finisher, cs);
    }

    /**
     * Characteristics indicating properties of a {@code Collector}, which can
     * be used to optimize reduction implementations.
     */
    enum Characteristics {
        /**
         * Indicates that this collector is <em>concurrent</em>, meaning that
         * the result container can support the accumulator function being
         * called concurrently with the same result container from multiple
         * threads.
         *
         * <p>If a {@code CONCURRENT} collector is not also {@code UNORDERED},
         * then it should only be evaluated concurrently if applied to an
         * unordered data source.
         */
        CONCURRENT,

        /**
         * Indicates that the collection operation does not commit to preserving
         * the encounter order of input elements.  (This might be true if the
         * result container has no intrinsic order, such as a {@link Set}.)
         */
        UNORDERED,

        /**
         * Indicates that the finisher function is the identity function and
         * can be elided.  If set, it must be the case that an unchecked cast
         * from A to R will succeed.
         */
        IDENTITY_FINISH
    }
}
```

## Reactive-Streams

[reactive-streams.org](http://www.reactive-streams.org/)

[java.util.concurrent.Flow](https://docs.oracle.com/en/java/javase/14/docs/api/java.base/java/util/concurrent/Flow.html)

A Flow.Publisher usually defines its own Flow.Subscription implementation; constructing one in method subscribe and issuing it to the calling Flow.Subscriber. It publishes items to the subscriber asynchronously, normally using an Executor. For example, here is a very simple publisher that only issues (when requested) a single TRUE item to a single subscriber. Because the subscriber receives only a single item, this class does not use buffering and ordering control required in most implementations (for example SubmissionPublisher).

```java
class OneShotPublisher implements Publisher<Boolean> {
   private final ExecutorService executor = ForkJoinPool.commonPool(); // daemon-based
   private boolean subscribed; // true after first subscribe
   public synchronized void subscribe(Subscriber<? super Boolean> subscriber) {
     if (subscribed)
       subscriber.onError(new IllegalStateException()); // only one allowed
     else {
       subscribed = true;
       subscriber.onSubscribe(new OneShotSubscription(subscriber, executor));
     }
   }
   static class OneShotSubscription implements Subscription {
     private final Subscriber<? super Boolean> subscriber;
     private final ExecutorService executor;
     private Future<?> future; // to allow cancellation
     private boolean completed;
     OneShotSubscription(Subscriber<? super Boolean> subscriber,
                         ExecutorService executor) {
       this.subscriber = subscriber;
       this.executor = executor;
     }
     public synchronized void request(long n) {
       if (n != 0 && !completed) {
         completed = true;
         if (n < 0) {
           IllegalArgumentException ex = new IllegalArgumentException();
           executor.execute(() -> subscriber.onError(ex));
         } else {
           future = executor.submit(() -> {
             subscriber.onNext(Boolean.TRUE);
             subscriber.onComplete();
           });
         }
       }
     }
     public synchronized void cancel() {
       completed = true;
       if (future != null) future.cancel(false);
     }
   }
 }
```

A Flow.Subscriber arranges that items be requested and processed. Items (invocations of Flow.Subscriber.onNext(T)) are not issued unless requested, but multiple items may be requested. Many Subscriber implementations can arrange this in the style of the following example, where a buffer size of 1 single-steps, and larger sizes usually allow for more efficient overlapped processing with less communication; for example with a value of 64, this keeps total outstanding requests between 32 and 64. Because Subscriber method invocations for a given Flow.Subscription are strictly ordered, there is no need for these methods to use locks or volatiles unless a Subscriber maintains multiple Subscriptions (in which case it is better to instead define multiple Subscribers, each with its own Subscription).

```java
class SampleSubscriber<T> implements Subscriber<T> {
   final Consumer<? super T> consumer;
   Subscription subscription;
   final long bufferSize;
   long count;
   SampleSubscriber(long bufferSize, Consumer<? super T> consumer) {
     this.bufferSize = bufferSize;
     this.consumer = consumer;
   }
   public void onSubscribe(Subscription subscription) {
     long initialRequestSize = bufferSize;
     count = bufferSize - bufferSize / 2; // re-request when half consumed
     (this.subscription = subscription).request(initialRequestSize);
   }
   public void onNext(T item) {
     if (--count <= 0)
       subscription.request(count = bufferSize - bufferSize / 2);
     consumer.accept(item);
   }
   public void onError(Throwable ex) { ex.printStackTrace(); }
   public void onComplete() {}
 }
```

The default value of defaultBufferSize() may provide a useful starting point for choosing request sizes and capacities in Flow components based on expected rates, resources, and usages. Or, when flow control is never needed, a subscriber may initially request an effectively unbounded number of items, as in:

```java
class UnboundedSubscriber<T> implements Subscriber<T> {
   public void onSubscribe(Subscription subscription) {
     subscription.request(Long.MAX_VALUE); // effectively unbounded
   }
   public void onNext(T item) { use(item); }
   public void onError(Throwable ex) { ex.printStackTrace(); }
   public void onComplete() {}
   void use(T item) { ... }
 }
```

### Reactor

[Reactor 3 Reference Guide](https://projectreactor.io/docs/core/release/reference/)

Reactor is a fully non-blocking reactive programming foundation for the JVM, with efficient demand management (in the form of managing “backpressure”). It integrates directly with the Java 8 functional APIs, notably CompletableFuture, Stream, and Duration. It offers composable asynchronous sequence APIs — Flux (for [N] elements) and Mono (for [0|1] elements) — and extensively implements the Reactive Streams specification.

Reactor is an implementation of the Reactive Programming paradigm, which can be summed up as follows:

Reactive programming is an asynchronous programming paradigm concerned with data streams and the propagation of change. This means that it becomes possible to express static (e.g. arrays) or dynamic (e.g. event emitters) data streams with ease via the employed programming language(s).

Java offers two models of asynchronous programming:

- Callbacks: Asynchronous methods do not have a return value but take an extra callback parameter (a lambda or anonymous class) that gets called when the result is available. A well known example is Swing’s EventListener hierarchy.

- Futures: Asynchronous methods immediately return a `Future<T>`. The asynchronous process computes a T value, but the Future object wraps access to it. The value is not immediately available, and the object can be polled until the value is available. For instance, an ExecutorService running `Callable<T>` tasks use Future objects.

> — [https://en.wikipedia.org/wiki/Reactive_programming](https://en.wikipedia.org/wiki/Reactive_programming)

```java
// view source
Flux.just(1, 2, 3, 4, 5)
    .map(x -> x + 2)
    .subscribe(System.out::print);
```

Subscriber -> subscribe -> subscribe -> subscribe -> DataSouce(Publisher)

DataSouce(Publisher) -> onSubscribe(Subscription) -> onSubscribe(Subscription) -> Subscriber

Subscriber -> Request(n) -> Request(n) -> DataSouce(Publisher)

DataSouce(Publisher) -> onNext -> onNext -> Subscriber

#### Publisher

```java
/**
 * A {@link Publisher} is a provider of a potentially unbounded number of sequenced elements, publishing them according to
 * the demand received from its {@link Subscriber}(s).
 * <p>
 * A {@link Publisher} can serve multiple {@link Subscriber}s subscribed {@link #subscribe(Subscriber)} dynamically
 * at various points in time.
 *
 * @param <T> the type of element signaled.
 */
public interface Publisher<T> {

    /**
     * Request {@link Publisher} to start streaming data.
     * <p>
     * This is a "factory method" and can be called multiple times, each time starting a new {@link Subscription}.
     * <p>
     * Each {@link Subscription} will work for only a single {@link Subscriber}.
     * <p>
     * A {@link Subscriber} should only subscribe once to a single {@link Publisher}.
     * <p>
     * If the {@link Publisher} rejects the subscription attempt or otherwise fails it will
     * signal the error via {@link Subscriber#onError}.
     *
     * @param s the {@link Subscriber} that will consume signals from this {@link Publisher}
     */
    public void subscribe(Subscriber<? super T> s);
}
```

#### Subscriber

```java
/**
 * Will receive call to {@link #onSubscribe(Subscription)} once after passing an instance of {@link Subscriber} to {@link Publisher#subscribe(Subscriber)}.
 * <p>
 * No further notifications will be received until {@link Subscription#request(long)} is called.
 * <p>
 * After signaling demand:
 * <ul>
 * <li>One or more invocations of {@link #onNext(Object)} up to the maximum number defined by {@link Subscription#request(long)}</li>
 * <li>Single invocation of {@link #onError(Throwable)} or {@link Subscriber#onComplete()} which signals a terminal state after which no further events will be sent.
 * </ul>
 * <p>
 * Demand can be signaled via {@link Subscription#request(long)} whenever the {@link Subscriber} instance is capable of handling more.
 *
 * @param <T> the type of element signaled.
 */
public interface Subscriber<T> {
    /**
     * Invoked after calling {@link Publisher#subscribe(Subscriber)}.
     * <p>
     * No data will start flowing until {@link Subscription#request(long)} is invoked.
     * <p>
     * It is the responsibility of this {@link Subscriber} instance to call {@link Subscription#request(long)} whenever more data is wanted.
     * <p>
     * The {@link Publisher} will send notifications only in response to {@link Subscription#request(long)}.
     *
     * @param s
     *            {@link Subscription} that allows requesting data via {@link Subscription#request(long)}
     */
    public void onSubscribe(Subscription s);

    /**
     * Data notification sent by the {@link Publisher} in response to requests to {@link Subscription#request(long)}.
     *
     * @param t the element signaled
     */
    public void onNext(T t);

    /**
     * Failed terminal state.
     * <p>
     * No further events will be sent even if {@link Subscription#request(long)} is invoked again.
     *
     * @param t the throwable signaled
     */
    public void onError(Throwable t);

    /**
     * Successful terminal state.
     * <p>
     * No further events will be sent even if {@link Subscription#request(long)} is invoked again.
     */
    public void onComplete();
}
```

#### Subscription

```java
/**
 * A {@link Subscription} represents a one-to-one lifecycle of a {@link Subscriber} subscribing to a {@link Publisher}.
 * <p>
 * It can only be used once by a single {@link Subscriber}.
 * <p>
 * It is used to both signal desire for data and cancel demand (and allow resource cleanup).
 *
 */
public interface Subscription {
    /**
     * No events will be sent by a {@link Publisher} until demand is signaled via this method.
     * <p>
     * It can be called however often and whenever needed—but the outstanding cumulative demand must never exceed Long.MAX_VALUE.
     * An outstanding cumulative demand of Long.MAX_VALUE may be treated by the {@link Publisher} as "effectively unbounded".
     * <p>
     * Whatever has been requested can be sent by the {@link Publisher} so only signal demand for what can be safely handled.
     * <p>
     * A {@link Publisher} can send less than is requested if the stream ends but
     * then must emit either {@link Subscriber#onError(Throwable)} or {@link Subscriber#onComplete()}.
     *
     * @param n the strictly positive number of elements to requests to the upstream {@link Publisher}
     */
    public void request(long n);

    /**
     * Request the {@link Publisher} to stop sending data and clean up resources.
     * <p>
     * Data may still be sent to meet previously signalled demand after calling cancel.
     */
    public void cancel();
}
```

#### Processor

```java
/**
 * A Processor represents a processing stage—which is both a {@link Subscriber}
 * and a {@link Publisher} and obeys the contracts of both.
 *
 * @param <T> the type of element signaled to the {@link Subscriber}
 * @param <R> the type of element signaled by the {@link Publisher}
 */
public interface Processor<T, R> extends Subscriber<T>, Publisher<R> {
}
```

#### Flux.subscribeOn

```java
/**
  * Run subscribe, onSubscribe and request on a specified {@link Scheduler}'s {@link Worker}.
  * As such, placing this operator anywhere in the chain will also impact the execution
  * context of onNext/onError/onComplete signals from the beginning of the chain up to
  * the next occurrence of a {@link #publishOn(Scheduler) publishOn}.
  * <p>
  * Note that if you are using an eager or blocking
  * {@link #create(Consumer, FluxSink.OverflowStrategy)}
  * as the source, it can lead to deadlocks due to requests piling up behind the emitter.
  * In such case, you should call {@link #subscribeOn(Scheduler, boolean) subscribeOn(scheduler, false)}
  * instead.
  * <p>
  * <img class="marble" src="doc-files/marbles/subscribeOnForFlux.svg" alt="">
  * <p>
  * Typically used for slow publisher e.g., blocking IO, fast consumer(s) scenarios.
  *
  * <blockquote><pre>
  * {@code flux.subscribeOn(Schedulers.single()).subscribe() }
  * </pre></blockquote>
  *
  * <p>
  *     Note that {@link Worker#schedule(Runnable)} raising
  *     {@link java.util.concurrent.RejectedExecutionException} on late
  *     {@link Subscription#request(long)} will be propagated to the request caller.
  *
  * @param scheduler a {@link Scheduler} providing the {@link Worker} where to subscribe
  *
  * @return a {@link Flux} requesting asynchronously
  * @see #publishOn(Scheduler)
  * @see #subscribeOn(Scheduler, boolean)
  */
public final Flux<T> subscribeOn(Scheduler scheduler) {
  return subscribeOn(scheduler, true);
}
```

#### Flux.publishOn

```java
/**
  * Run onNext, onComplete and onError on a supplied {@link Scheduler}
  * {@link Worker Worker}.
  * <p>
  * This operator influences the threading context where the rest of the operators in
  * the chain below it will execute, up to a new occurrence of {@code publishOn}.
  * <p>
  * <img class="marble" src="doc-files/marbles/publishOnForFlux.svg" alt="">
  * <p>
  * Typically used for fast publisher, slow consumer(s) scenarios.
  * <blockquote><pre>
  * {@code flux.publishOn(Schedulers.single()).subscribe() }
  * </pre></blockquote>
  *
  * @reactor.discard This operator discards elements it internally queued for backpressure upon cancellation or error triggered by a data signal.
  *
  * @param scheduler a {@link Scheduler} providing the {@link Worker} where to publish
  *
  * @return a {@link Flux} producing asynchronously on a given {@link Scheduler}
  */
public final Flux<T> publishOn(Scheduler scheduler) {
  return publishOn(scheduler, Queues.SMALL_BUFFER_SIZE);
}$$
```

## ReactiveX

An API for asynchronous programming
with observable streams

[intro](http://reactivex.io/intro.html)

ReactiveX provides a collection of operators with which you can filter, select, transform, combine, and compose Observables. This allows for efficient execution and composition.

You can think of the Observable class as a “push” equivalent to Iterable, which is a “pull.” With an Iterable, the consumer pulls values from the producer and the thread blocks until those values arrive. By contrast, with an Observable the producer pushes values to the consumer whenever values are available. This approach is more flexible, because values can arrive synchronously or asynchronously.

### RxJava

[RxJava](https://github.com/ReactiveX/RxJava) – Reactive Extensions for the JVM – a library for composing asynchronous and event-based programs using observable sequences for the Java VM.

### Rx.NET

[reactive-extensions](<https://docs.microsoft.com/en-us/previous-versions/dotnet/reactive-extensions/hh242985(v=vs.103)>)

[github](https://github.com/dotnet/reactive)

[Reactive Framework (Rx) Wiki](http://rxwiki.wikidot.com/)

#### Pulling vs. Pushing Data

In interactive programming, the application actively polls a data source for more information by pulling data from a sequence that represents the source. Such behavior is represented by the iterator pattern of `IEnumerable<T>/IEnumerator<T>`. The `IEnumerable<T>` interface exposes a single method GetEnumerator() which returns an `IEnumerator<T>` to iterate through this collection. The `IEnumerator<T>` allows us to get the current item (by returning the Current property), and determine whether there are more items to iterate (by calling the MoveNext method).

The application is active in the data retrieval process: besides getting an enumerator by calling GetEnumerator, it also controls the pace of the retrieval by calling MoveNext at its own convenience. This enumeration pattern is synchronous, which means that the application might be blocked while polling the data source. Such pulling pattern is similar to visiting your library and checking out a book. After you are done with the book, you pay another visit to check out another one.

On the other hand, in reactive programming, the application is offered more information by subscribing to a data stream (called observable sequence in Rx), and any update is handed to it from the source. The application is passive in the data retrieval process: apart from subscribing to the observable source, it does not actively poll the source, but merely react to the data being pushed to it. When the stream has no more data to offer, or when it errs, the source will send a notice to the subscriber. In this way, the application will not be blocked by waiting for the source to update.

This is the push pattern employed by Reactive Extensions. It is similar to joining a book club in which you register your interest in a particular genre, and books that match your interest are automatically sent to you as they are published. You do not need to stand in line to acquire something that you want. Employing a push pattern is helpful in many scenarios, especially in a UI-heavy environment in which the UI thread cannot be blocked while the application is waiting for some events. This is also essential in programming environments such as Silverlight which has its own set of asynchronous requirements. In summary, by using Rx, you can make your application more responsive.

The push model implemented by Rx is represented by the observable pattern of `IObservable<T>/IObserver<T>`. The `IObservable<T>` interface is a dual of the familiar `IEnumerable<T>` interface. It abstracts a sequence of data, and keeps a list of `IObserver<T>` implementations that are interested in the data sequence. The IObservable will notify all the observers automatically of any state changes. To register an interest through a subscription, you use the Subscribe method of IObservable, which takes on an IObserver and returns an IDisposable. This gives you the ability to track and dispose of the subscription. In addition, Rx’s LINQ implementation over observable sequences allows developers to compose complex event processing queries over push-based sequences such as .NET events, APM-based (“IAsyncResult”) computations, `Task<T>-based` computations, Windows 7 Sensor and Location APIs, SQL StreamInsight temporal event streams, F# first-class events, and asynchronous workflows. For more information on the `IObservable<T>/IObserver<T>` interfaces, see Exploring The Major Interfaces in Rx. For tutorials on using the different features in Rx, see Using Rx.

## Linq

### Pipeline

[ParallelExtensionsExtras](https://github.com/dotnet/samples/blob/master/csharp/parallel/ParallelExtensionsExtras/CoordinationDataStructures/Pipeline.cs)

```CSharp
/// <summary>Provides support for pipelined data processing.</summary>
public static class Pipeline
{
    internal readonly static TaskScheduler Scheduler = new ThreadPerTaskScheduler();

    /// <summary>Creates a new pipeline, with the specified function as the sole stage.</summary>
    /// <typeparam name="TInput">Specifies the type of the input data to the pipeline.</typeparam>
    /// <typeparam name="TOutput">Specifies the type of the output data from this stage of the pipeline.</typeparam>
    /// <param name="func">The function used to process input data into output data.</param>
    /// <returns>A pipeline for converting from input data to output data.</returns>
    public static Pipeline<TInput, TOutput> Create<TInput, TOutput>(Func<TInput, TOutput> func)
    {
        return Create(func, 1);
    }

    /// <summary>Creates a new pipeline, with the specified function as the sole stage.</summary>
    /// <typeparam name="TInput">Specifies the type of the input data to the pipeline.</typeparam>
    /// <typeparam name="TOutput">Specifies the type of the output data from this stage of the pipeline.</typeparam>
    /// <param name="func">The function used to process input data into output data.</param>
    /// <param name="degreeOfParallelism">The concurrency level for this stage of the pipeline.</param>
    /// <returns>A pipeline for converting from input data to output data.</returns>
    public static Pipeline<TInput, TOutput> Create<TInput, TOutput>(Func<TInput, TOutput> func, int degreeOfParallelism)
    {
        if (func == null) throw new ArgumentNullException("func");
        if (degreeOfParallelism < 1) throw new ArgumentOutOfRangeException("degreeOfParallelism");
        return new Pipeline<TInput, TOutput>(func, degreeOfParallelism);
    }
}

/// <summary>Provides support for pipelined data processing.</summary>
/// <typeparam name="TInput">Specifies the type of the input data to the pipeline.</typeparam>
/// <typeparam name="TOutput">Specifies the type of the output data from this stage of the pipeline.</typeparam>
public class Pipeline<TInput, TOutput>
{
    private readonly Func<TInput, TOutput> _stageFunc;
    private readonly int _degreeOfParallelism;

    internal Pipeline(int degreeOfParallelism) : this(null, degreeOfParallelism) { }

    internal Pipeline(Func<TInput, TOutput> func, int degreeOfParallelism)
    {
        _stageFunc = func;
        _degreeOfParallelism = degreeOfParallelism;
    }

    /// <summary>Creates a new pipeline that combines the current pipeline with a new stage.</summary>
    /// <typeparam name="TNextOutput">Specifies the new output type of the pipeline.</typeparam>
    /// <param name="func">
    /// The function used to convert the output of the current pipeline into the new
    /// output of the new pipeline.
    /// </param>
    /// <returns>A new pipeline that combines the current pipeline with the new stage.</returns>
    /// <remarks>This overload creates a parallel pipeline stage.</remarks>
    public Pipeline<TInput, TNextOutput> Next<TNextOutput>(Func<TOutput, TNextOutput> func)
    {
        return Next(func, 1);
    }

    /// <summary>Creates a new pipeline that combines the current pipeline with a new stage.</summary>
    /// <typeparam name="TNextOutput">Specifies the new output type of the pipeline.</typeparam>
    /// <param name="func">
    /// The function used to convert the output of the current pipeline into the new
    /// output of the new pipeline.
    /// </param>
    /// <param name="degreeOfParallelism">The concurrency level for this stage of the pipeline.</param>
    /// <returns>A new pipeline that combines the current pipeline with the new stage.</returns>
    public Pipeline<TInput, TNextOutput> Next<TNextOutput>(Func<TOutput, TNextOutput> func, int degreeOfParallelism)
    {
        if (func == null) throw new ArgumentNullException("func");
        if (degreeOfParallelism < 1) throw new ArgumentOutOfRangeException("degreeOfParallelism");
        return new InternalPipeline<TNextOutput>(this, func, degreeOfParallelism);
    }

    /// <summary>Runs the pipeline and returns an enumerable over the results.</summary>
    /// <param name="source">The source data to be processed by the pipeline.</param>
    /// <returns>An enumerable of the results of the pipeline.</returns>
    public IEnumerable<TOutput> Process(IEnumerable<TInput> source)
    {
        return Process(source, new CancellationToken());
    }

    /// <summary>Runs the pipeline and returns an enumerable over the results.</summary>
    /// <param name="source">The source data to be processed by the pipeline.</param>
    /// <param name="cancellationToken">The cancellation token used to signal cancellation of the pipelining.</param>
    /// <returns>An enumerable of the results of the pipeline.</returns>
    public IEnumerable<TOutput> Process(IEnumerable<TInput> source, CancellationToken cancellationToken)
    {
        // Validate arguments
        if (source == null) throw new ArgumentNullException("source");
        return ProcessNoArgValidation(source, cancellationToken);
    }

    /// <summary>Runs the pipeline and returns an enumerable over the results.</summary>
    /// <param name="source">The source data to be processed by the pipeline.</param>
    /// <param name="cancellationToken">The cancellation token used to signal cancellation of the pipelining.</param>
    /// <returns>An enumerable of the results of the pipeline.</returns>
    private IEnumerable<TOutput> ProcessNoArgValidation(IEnumerable<TInput> source, CancellationToken cancellationToken)
    {
        // Create a blocking collection for communication with the query running in a background task
        using (var output = new BlockingCollection<TOutput>())
        {
            // Start a task to run the core of the stage
            var processingTask = Task.Factory.StartNew(() =>
            {
                try { ProcessCore(source, cancellationToken, output); }
                finally { output.CompleteAdding(); }
            }, CancellationToken.None, TaskCreationOptions.None, Pipeline.Scheduler);

            // Enumerate and yield the results.  This makes ProcessNoArgValidation
            // lazy, in that processing won't start until enumeration begins.
            foreach (var result in output.GetConsumingEnumerable(cancellationToken))
            {
                yield return result;
            }

            // Make sure the processing task has shut down, and propagate any exceptions that occurred
            processingTask.Wait();
        }
    }

    /// <summary>Implements the core processing for a pipeline stage.</summary>
    /// <param name="source">The source data to be processed by the pipeline.</param>
    /// <param name="cancellationToken">The cancellation token used to signal cancellation of the pipelining.</param>
    /// <param name="output">The collection into which to put the output.</param>
    protected virtual void ProcessCore(IEnumerable<TInput> source, CancellationToken cancellationToken, BlockingCollection<TOutput> output)
    {
        var options = new ParallelOptions
        {
            CancellationToken = cancellationToken,
            MaxDegreeOfParallelism = _degreeOfParallelism,
            TaskScheduler = Pipeline.Scheduler
        };
        Parallel.ForEach(source, options, item => output.Add(_stageFunc(item)));
    }

    /// <summary>Helper used to add a new stage to a pipeline.</summary>
    /// <typeparam name="TNextOutput">Specifies the type of the output for the new pipeline.</typeparam>
    private sealed class InternalPipeline<TNextOutput> : Pipeline<TInput, TNextOutput>
    {
        private readonly Pipeline<TInput, TOutput> _beginningPipeline;
        private readonly Func<TOutput, TNextOutput> _lastStageFunc;

        public InternalPipeline(Pipeline<TInput, TOutput> beginningPipeline, Func<TOutput, TNextOutput> func, int degreeOfParallelism)
            : base(degreeOfParallelism)
        {
            _beginningPipeline = beginningPipeline;
            _lastStageFunc = func;
        }

        /// <summary>Implements the core processing for a pipeline stage.</summary>
        /// <param name="source">The source data to be processed by the pipeline.</param>
        /// <param name="cancellationToken">The cancellation token used to signal cancellation of the pipelining.</param>
        /// <param name="output">The collection into which to put the output.</param>
        protected override void ProcessCore(
            IEnumerable<TInput> source, CancellationToken cancellationToken, BlockingCollection<TNextOutput> output)
        {
            var options = new ParallelOptions
            {
                CancellationToken = cancellationToken,
                MaxDegreeOfParallelism = _degreeOfParallelism,
                TaskScheduler = Pipeline.Scheduler
            };
            Parallel.ForEach(_beginningPipeline.Process(source, cancellationToken), options, item => output.Add(_lastStageFunc(item)));
        }
    }
}
```

## Node.js

Node 库以多种方式[处理异步功能](https://www.gulpjs.com.cn/docs/getting-started/async-completion/)。最常见的模式是 [error-first callbacks](https://nodejs.org/api/errors.html#errors_error_first_callbacks)，但是你还可能会遇到 [streams](https://nodejs.org/api/stream.html)、[promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)、[event emitters](https://nodejs.org/api/events.html)、[child processes](https://nodejs.org/api/child_process.html), 或 [observables](https://github.com/tc39/proposal-observable/blob/master/README.md)。

`Promise` 与 `Observable` 可以解决 js 中的回调地狱。

### Promise

[MDN](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise)

[Referance](https://github.com/YvetteLau/Blog/issues/2)

```javascript
/**
 * 1. new Promise时，需要传递一个 executor 执行器，执行器立刻执行
 * 2. executor 接受两个参数，分别是 resolve 和 reject
 * 3. promise 只能从 pending 到 rejected, 或者从 pending 到 fulfilled
 * 4. promise 的状态一旦确认，就不会再改变
 * 5. promise 都有 then 方法，then 接收两个参数，分别是 promise 成功的回调 onFulfilled,
 *      和 promise 失败的回调 onRejected
 * 6. 如果调用 then 时，promise已经成功，则执行 onFulfilled，并将promise的值作为参数传递进去。
 *      如果promise已经失败，那么执行 onRejected, 并将 promise 失败的原因作为参数传递进去。
 *      如果promise的状态是pending，需要将onFulfilled和onRejected函数存放起来，等待状态确定后，再依次将对应的函数执行(发布订阅)
 * 7. then 的参数 onFulfilled 和 onRejected 可以缺省
 * 8. promise 可以then多次，promise 的then 方法返回一个 promise
 * 9. 如果 then 返回的是一个结果，那么就会把这个结果作为参数，传递给下一个then的成功的回调(onFulfilled)
 * 10. 如果 then 中抛出了异常，那么就会把这个异常作为参数，传递给下一个then的失败的回调(onRejected)
 * 11.如果 then 返回的是一个promise,那么需要等这个promise，那么会等这个promise执行完，promise如果成功，
 *   就走下一个then的成功，如果失败，就走下一个then的失败
 */

const PENDING = "pending";
const FULFILLED = "fulfilled";
const REJECTED = "rejected";
function Promise(executor) {
  let self = this;
  self.status = PENDING;
  self.onFulfilled = []; //成功的回调
  self.onRejected = []; //失败的回调
  //PromiseA+ 2.1
  function resolve(value) {
    if (self.status === PENDING) {
      self.status = FULFILLED;
      self.value = value;
      self.onFulfilled.forEach((fn) => fn()); //PromiseA+ 2.2.6.1
    }
  }

  function reject(reason) {
    if (self.status === PENDING) {
      self.status = REJECTED;
      self.reason = reason;
      self.onRejected.forEach((fn) => fn()); //PromiseA+ 2.2.6.2
    }
  }

  try {
    executor(resolve, reject);
  } catch (e) {
    reject(e);
  }
}

Promise.prototype.then = function (onFulfilled, onRejected) {
  //PromiseA+ 2.2.1 / PromiseA+ 2.2.5 / PromiseA+ 2.2.7.3 / PromiseA+ 2.2.7.4
  onFulfilled =
    typeof onFulfilled === "function" ? onFulfilled : (value) => value;
  onRejected =
    typeof onRejected === "function"
      ? onRejected
      : (reason) => {
          throw reason;
        };
  let self = this;
  //PromiseA+ 2.2.7
  let promise2 = new Promise((resolve, reject) => {
    if (self.status === FULFILLED) {
      //PromiseA+ 2.2.2
      //PromiseA+ 2.2.4 --- setTimeout
      setTimeout(() => {
        try {
          //PromiseA+ 2.2.7.1
          let x = onFulfilled(self.value);
          resolvePromise(promise2, x, resolve, reject);
        } catch (e) {
          //PromiseA+ 2.2.7.2
          reject(e);
        }
      });
    } else if (self.status === REJECTED) {
      //PromiseA+ 2.2.3
      setTimeout(() => {
        try {
          let x = onRejected(self.reason);
          resolvePromise(promise2, x, resolve, reject);
        } catch (e) {
          reject(e);
        }
      });
    } else if (self.status === PENDING) {
      self.onFulfilled.push(() => {
        setTimeout(() => {
          try {
            let x = onFulfilled(self.value);
            resolvePromise(promise2, x, resolve, reject);
          } catch (e) {
            reject(e);
          }
        });
      });
      self.onRejected.push(() => {
        setTimeout(() => {
          try {
            let x = onRejected(self.reason);
            resolvePromise(promise2, x, resolve, reject);
          } catch (e) {
            reject(e);
          }
        });
      });
    }
  });
  return promise2;
};

function resolvePromise(promise2, x, resolve, reject) {
  let self = this;
  //PromiseA+ 2.3.1
  if (promise2 === x) {
    reject(new TypeError("Chaining cycle"));
  }
  if ((x && typeof x === "object") || typeof x === "function") {
    let used; //PromiseA+2.3.3.3.3 只能调用一次
    try {
      let then = x.then;
      if (typeof then === "function") {
        //PromiseA+2.3.3
        then.call(
          x,
          (y) => {
            //PromiseA+2.3.3.1
            if (used) return;
            used = true;
            resolvePromise(promise2, y, resolve, reject);
          },
          (r) => {
            //PromiseA+2.3.3.2
            if (used) return;
            used = true;
            reject(r);
          }
        );
      } else {
        //PromiseA+2.3.3.4
        if (used) return;
        used = true;
        resolve(x);
      }
    } catch (e) {
      //PromiseA+ 2.3.3.2
      if (used) return;
      used = true;
      reject(e);
    }
  } else {
    //PromiseA+ 2.3.3.4
    resolve(x);
  }
}

module.exports = Promise;
```

### Observable

[RxJS](https://github.com/ReactiveX/RxJS)

### Streams

A [stream](https://nodejs.org/api/stream.html) is an abstract interface for working with streaming data in Node.js.

[gulp](https://www.gulpjs.com.cn/docs/api/concepts/) 实现了流式处理。

[stream-handbook](https://github.com/substack/stream-handbook) covers the basics of how to write node.js programs with streams.

[through2](https://github.com/rvagg/through2) A tiny wrapper around Node.js streams.Transform (Streams2/3) to avoid explicit subclassing noise

## Schedule

模拟 js 的单线程执行机制。1. 可执行普通 Task, 2. 可执行定时任务。

### okio

```java
/**
 * A policy on how much time to spend on a task before giving up. When a task
 * times out, it is left in an unspecified state and should be abandoned. For
 * example, if reading from a source times out, that source should be closed and
 * the read should be retried later. If writing to a sink times out, the same
 * rules apply: close the sink and retry later.
 *
 * <h3>Timeouts and Deadlines</h3>
 * This class offers two complementary controls to define a timeout policy.
 *
 * <p><strong>Timeouts</strong> specify the maximum time to wait for a single
 * operation to complete. Timeouts are typically used to detect problems like
 * network partitions. For example, if a remote peer doesn't return <i>any</i>
 * data for ten seconds, we may assume that the peer is unavailable.
 *
 * <p><strong>Deadlines</strong> specify the maximum time to spend on a job,
 * composed of one or more operations. Use deadlines to set an upper bound on
 * the time invested on a job. For example, a battery-conscious app may limit
 * how much time it spends pre-loading content.
 */
public class Timeout {
  /**
   * An empty timeout that neither tracks nor detects timeouts. Use this when
   * timeouts aren't necessary, such as in implementations whose operations
   * do not block.
   */
  public static final Timeout NONE = new Timeout() {
    @Override public Timeout timeout(long timeout, TimeUnit unit) {
      return this;
    }

    @Override public Timeout deadlineNanoTime(long deadlineNanoTime) {
      return this;
    }

    @Override public void throwIfReached() throws IOException {
    }
  };

  /**
   * True if {@code deadlineNanoTime} is defined. There is no equivalent to null
   * or 0 for {@link System#nanoTime}.
   */
  private boolean hasDeadline;
  private long deadlineNanoTime;
  private long timeoutNanos;

  public Timeout() {
  }

  /**
   * Wait at most {@code timeout} time before aborting an operation. Using a
   * per-operation timeout means that as long as forward progress is being made,
   * no sequence of operations will fail.
   *
   * <p>If {@code timeout == 0}, operations will run indefinitely. (Operating
   * system timeouts may still apply.)
   */
  public Timeout timeout(long timeout, TimeUnit unit) {
    if (timeout < 0) throw new IllegalArgumentException("timeout < 0: " + timeout);
    if (unit == null) throw new IllegalArgumentException("unit == null");
    this.timeoutNanos = unit.toNanos(timeout);
    return this;
  }

  /** Returns the timeout in nanoseconds, or {@code 0} for no timeout. */
  public long timeoutNanos() {
    return timeoutNanos;
  }

  /** Returns true if a deadline is enabled. */
  public boolean hasDeadline() {
    return hasDeadline;
  }

  /**
   * Returns the {@linkplain System#nanoTime() nano time} when the deadline will
   * be reached.
   *
   * @throws IllegalStateException if no deadline is set.
   */
  public long deadlineNanoTime() {
    if (!hasDeadline) throw new IllegalStateException("No deadline");
    return deadlineNanoTime;
  }

  /**
   * Sets the {@linkplain System#nanoTime() nano time} when the deadline will be
   * reached. All operations must complete before this time. Use a deadline to
   * set a maximum bound on the time spent on a sequence of operations.
   */
  public Timeout deadlineNanoTime(long deadlineNanoTime) {
    this.hasDeadline = true;
    this.deadlineNanoTime = deadlineNanoTime;
    return this;
  }

  /** Set a deadline of now plus {@code duration} time. */
  public final Timeout deadline(long duration, TimeUnit unit) {
    if (duration <= 0) throw new IllegalArgumentException("duration <= 0: " + duration);
    if (unit == null) throw new IllegalArgumentException("unit == null");
    return deadlineNanoTime(System.nanoTime() + unit.toNanos(duration));
  }

  /** Clears the timeout. Operating system timeouts may still apply. */
  public Timeout clearTimeout() {
    this.timeoutNanos = 0;
    return this;
  }

  /** Clears the deadline. */
  public Timeout clearDeadline() {
    this.hasDeadline = false;
    return this;
  }

  /**
   * Throws an {@link InterruptedIOException} if the deadline has been reached or if the current
   * thread has been interrupted. This method doesn't detect timeouts; that should be implemented to
   * asynchronously abort an in-progress operation.
   */
  public void throwIfReached() throws IOException {
    if (Thread.interrupted()) {
      Thread.currentThread().interrupt(); // Retain interrupted status.
      throw new InterruptedIOException("interrupted");
    }

    if (hasDeadline && deadlineNanoTime - System.nanoTime() <= 0) {
      throw new InterruptedIOException("deadline reached");
    }
  }

  /**
   * Waits on {@code monitor} until it is notified. Throws {@link InterruptedIOException} if either
   * the thread is interrupted or if this timeout elapses before {@code monitor} is notified. The
   * caller must be synchronized on {@code monitor}.
   *
   * <p>Here's a sample class that uses {@code waitUntilNotified()} to await a specific state. Note
   * that the call is made within a loop to avoid unnecessary waiting and to mitigate spurious
   * notifications. <pre>{@code
   *
   *   class Dice {
   *     Random random = new Random();
   *     int latestTotal;
   *
   *     public synchronized void roll() {
   *       latestTotal = 2 + random.nextInt(6) + random.nextInt(6);
   *       System.out.println("Rolled " + latestTotal);
   *       notifyAll();
   *     }
   *
   *     public void rollAtFixedRate(int period, TimeUnit timeUnit) {
   *       Executors.newScheduledThreadPool(0).scheduleAtFixedRate(new Runnable() {
   *         public void run() {
   *           roll();
   *          }
   *       }, 0, period, timeUnit);
   *     }
   *
   *     public synchronized void awaitTotal(Timeout timeout, int total)
   *         throws InterruptedIOException {
   *       while (latestTotal != total) {
   *         timeout.waitUntilNotified(this);
   *       }
   *     }
   *   }
   * }</pre>
   */
  public final void waitUntilNotified(Object monitor) throws InterruptedIOException {
    try {
      boolean hasDeadline = hasDeadline();
      long timeoutNanos = timeoutNanos();

      if (!hasDeadline && timeoutNanos == 0L) {
        monitor.wait(); // There is no timeout: wait forever.
        return;
      }

      // Compute how long we'll wait.
      long waitNanos;
      long start = System.nanoTime();
      if (hasDeadline && timeoutNanos != 0) {
        long deadlineNanos = deadlineNanoTime() - start;
        waitNanos = Math.min(timeoutNanos, deadlineNanos);
      } else if (hasDeadline) {
        waitNanos = deadlineNanoTime() - start;
      } else {
        waitNanos = timeoutNanos;
      }

      // Attempt to wait that long. This will break out early if the monitor is notified.
      long elapsedNanos = 0L;
      if (waitNanos > 0L) {
        long waitMillis = waitNanos / 1000000L;
        monitor.wait(waitMillis, (int) (waitNanos - waitMillis * 1000000L));
        elapsedNanos = System.nanoTime() - start;
      }

      // Throw if the timeout elapsed before the monitor was notified.
      if (elapsedNanos >= waitNanos) {
        throw new InterruptedIOException("timeout");
      }
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt(); // Retain interrupted status.
      throw new InterruptedIOException("interrupted");
    }
  }

  static long minTimeout(long aNanos, long bNanos) {
    if (aNanos == 0L) return bNanos;
    if (bNanos == 0L) return aNanos;
    if (aNanos < bNanos) return aNanos;
    return bNanos;
  }
}
```

```java
/**
 * This timeout uses a background thread to take action exactly when the timeout occurs. Use this to
 * implement timeouts where they aren't supported natively, such as to sockets that are blocked on
 * writing.
 *
 * <p>Subclasses should override {@link #timedOut} to take action when a timeout occurs. This method
 * will be invoked by the shared watchdog thread so it should not do any long-running operations.
 * Otherwise we risk starving other timeouts from being triggered.
 *
 * <p>Use {@link #sink} and {@link #source} to apply this timeout to a stream. The returned value
 * will apply the timeout to each operation on the wrapped stream.
 *
 * <p>Callers should call {@link #enter} before doing work that is subject to timeouts, and {@link
 * #exit} afterwards. The return value of {@link #exit} indicates whether a timeout was triggered.
 * Note that the call to {@link #timedOut} is asynchronous, and may be called after {@link #exit}.
 */
public class AsyncTimeout extends Timeout {
  /**
   * Don't write more than 64 KiB of data at a time, give or take a segment. Otherwise slow
   * connections may suffer timeouts even when they're making (slow) progress. Without this, writing
   * a single 1 MiB buffer may never succeed on a sufficiently slow connection.
   */
  private static final int TIMEOUT_WRITE_SIZE = 64 * 1024;

  /** Duration for the watchdog thread to be idle before it shuts itself down. */
  private static final long IDLE_TIMEOUT_MILLIS = TimeUnit.SECONDS.toMillis(60);
  private static final long IDLE_TIMEOUT_NANOS = TimeUnit.MILLISECONDS.toNanos(IDLE_TIMEOUT_MILLIS);

  /**
   * The watchdog thread processes a linked list of pending timeouts, sorted in the order to be
   * triggered. This class synchronizes on AsyncTimeout.class. This lock guards the queue.
   *
   * <p>Head's 'next' points to the first element of the linked list. The first element is the next
   * node to time out, or null if the queue is empty. The head is null until the watchdog thread is
   * started and also after being idle for {@link #IDLE_TIMEOUT_MILLIS}.
   */
  static @Nullable AsyncTimeout head;

  /** True if this node is currently in the queue. */
  private boolean inQueue;

  /** The next node in the linked list. */
  private @Nullable AsyncTimeout next;

  /** If scheduled, this is the time that the watchdog should time this out. */
  private long timeoutAt;

  public final void enter() {
    if (inQueue) throw new IllegalStateException("Unbalanced enter/exit");
    long timeoutNanos = timeoutNanos();
    boolean hasDeadline = hasDeadline();
    if (timeoutNanos == 0 && !hasDeadline) {
      return; // No timeout and no deadline? Don't bother with the queue.
    }
    inQueue = true;
    scheduleTimeout(this, timeoutNanos, hasDeadline);
  }

  private static synchronized void scheduleTimeout(
      AsyncTimeout node, long timeoutNanos, boolean hasDeadline) {
    // Start the watchdog thread and create the head node when the first timeout is scheduled.
    if (head == null) {
      head = new AsyncTimeout();
      new Watchdog().start();
    }

    long now = System.nanoTime();
    if (timeoutNanos != 0 && hasDeadline) {
      // Compute the earliest event; either timeout or deadline. Because nanoTime can wrap around,
      // Math.min() is undefined for absolute values, but meaningful for relative ones.
      node.timeoutAt = now + Math.min(timeoutNanos, node.deadlineNanoTime() - now);
    } else if (timeoutNanos != 0) {
      node.timeoutAt = now + timeoutNanos;
    } else if (hasDeadline) {
      node.timeoutAt = node.deadlineNanoTime();
    } else {
      throw new AssertionError();
    }

    // Insert the node in sorted order.
    long remainingNanos = node.remainingNanos(now);
    for (AsyncTimeout prev = head; true; prev = prev.next) {
      if (prev.next == null || remainingNanos < prev.next.remainingNanos(now)) {
        node.next = prev.next;
        prev.next = node;
        if (prev == head) {
          AsyncTimeout.class.notify(); // Wake up the watchdog when inserting at the front.
        }
        break;
      }
    }
  }

  /** Returns true if the timeout occurred. */
  public final boolean exit() {
    if (!inQueue) return false;
    inQueue = false;
    return cancelScheduledTimeout(this);
  }

  /** Returns true if the timeout occurred. */
  private static synchronized boolean cancelScheduledTimeout(AsyncTimeout node) {
    // Remove the node from the linked list.
    for (AsyncTimeout prev = head; prev != null; prev = prev.next) {
      if (prev.next == node) {
        prev.next = node.next;
        node.next = null;
        return false;
      }
    }

    // The node wasn't found in the linked list: it must have timed out!
    return true;
  }

  /**
   * Returns the amount of time left until the time out. This will be negative if the timeout has
   * elapsed and the timeout should occur immediately.
   */
  private long remainingNanos(long now) {
    return timeoutAt - now;
  }

  /**
   * Invoked by the watchdog thread when the time between calls to {@link #enter()} and {@link
   * #exit()} has exceeded the timeout.
   */
  protected void timedOut() {
  }

  /**
   * Returns a new sink that delegates to {@code sink}, using this to implement timeouts. This works
   * best if {@link #timedOut} is overridden to interrupt {@code sink}'s current operation.
   */
  public final Sink sink(final Sink sink) {
    return new Sink() {
      @Override public void write(Buffer source, long byteCount) throws IOException {
        checkOffsetAndCount(source.size, 0, byteCount);

        while (byteCount > 0L) {
          // Count how many bytes to write. This loop guarantees we split on a segment boundary.
          long toWrite = 0L;
          for (Segment s = source.head; toWrite < TIMEOUT_WRITE_SIZE; s = s.next) {
            int segmentSize = s.limit - s.pos;
            toWrite += segmentSize;
            if (toWrite >= byteCount) {
              toWrite = byteCount;
              break;
            }
          }

          // Emit one write. Only this section is subject to the timeout.
          boolean throwOnTimeout = false;
          enter();
          try {
            sink.write(source, toWrite);
            byteCount -= toWrite;
            throwOnTimeout = true;
          } catch (IOException e) {
            throw exit(e);
          } finally {
            exit(throwOnTimeout);
          }
        }
      }

      @Override public void flush() throws IOException {
        boolean throwOnTimeout = false;
        enter();
        try {
          sink.flush();
          throwOnTimeout = true;
        } catch (IOException e) {
          throw exit(e);
        } finally {
          exit(throwOnTimeout);
        }
      }

      @Override public void close() throws IOException {
        boolean throwOnTimeout = false;
        enter();
        try {
          sink.close();
          throwOnTimeout = true;
        } catch (IOException e) {
          throw exit(e);
        } finally {
          exit(throwOnTimeout);
        }
      }

      @Override public Timeout timeout() {
        return AsyncTimeout.this;
      }

      @Override public String toString() {
        return "AsyncTimeout.sink(" + sink + ")";
      }
    };
  }

  /**
   * Returns a new source that delegates to {@code source}, using this to implement timeouts. This
   * works best if {@link #timedOut} is overridden to interrupt {@code sink}'s current operation.
   */
  public final Source source(final Source source) {
    return new Source() {
      @Override public long read(Buffer sink, long byteCount) throws IOException {
        boolean throwOnTimeout = false;
        enter();
        try {
          long result = source.read(sink, byteCount);
          throwOnTimeout = true;
          return result;
        } catch (IOException e) {
          throw exit(e);
        } finally {
          exit(throwOnTimeout);
        }
      }

      @Override public void close() throws IOException {
        boolean throwOnTimeout = false;
        enter();
        try {
          source.close();
          throwOnTimeout = true;
        } catch (IOException e) {
          throw exit(e);
        } finally {
          exit(throwOnTimeout);
        }
      }

      @Override public Timeout timeout() {
        return AsyncTimeout.this;
      }

      @Override public String toString() {
        return "AsyncTimeout.source(" + source + ")";
      }
    };
  }

  /**
   * Throws an IOException if {@code throwOnTimeout} is {@code true} and a timeout occurred. See
   * {@link #newTimeoutException(java.io.IOException)} for the type of exception thrown.
   */
  final void exit(boolean throwOnTimeout) throws IOException {
    boolean timedOut = exit();
    if (timedOut && throwOnTimeout) throw newTimeoutException(null);
  }

  /**
   * Returns either {@code cause} or an IOException that's caused by {@code cause} if a timeout
   * occurred. See {@link #newTimeoutException(java.io.IOException)} for the type of exception
   * returned.
   */
  final IOException exit(IOException cause) throws IOException {
    if (!exit()) return cause;
    return newTimeoutException(cause);
  }

  /**
   * Returns an {@link IOException} to represent a timeout. By default this method returns {@link
   * java.io.InterruptedIOException}. If {@code cause} is non-null it is set as the cause of the
   * returned exception.
   */
  protected IOException newTimeoutException(@Nullable IOException cause) {
    InterruptedIOException e = new InterruptedIOException("timeout");
    if (cause != null) {
      e.initCause(cause);
    }
    return e;
  }

  private static final class Watchdog extends Thread {
    Watchdog() {
      super("Okio Watchdog");
      setDaemon(true);
    }

    public void run() {
      while (true) {
        try {
          AsyncTimeout timedOut;
          synchronized (AsyncTimeout.class) {
            timedOut = awaitTimeout();

            // Didn't find a node to interrupt. Try again.
            if (timedOut == null) continue;

            // The queue is completely empty. Let this thread exit and let another watchdog thread
            // get created on the next call to scheduleTimeout().
            if (timedOut == head) {
              head = null;
              return;
            }
          }

          // Close the timed out node.
          timedOut.timedOut();
        } catch (InterruptedException ignored) {
        }
      }
    }
  }

  /**
   * Removes and returns the node at the head of the list, waiting for it to time out if necessary.
   * This returns {@link #head} if there was no node at the head of the list when starting, and
   * there continues to be no node after waiting {@code IDLE_TIMEOUT_NANOS}. It returns null if a
   * new node was inserted while waiting. Otherwise this returns the node being waited on that has
   * been removed.
   */
  static @Nullable AsyncTimeout awaitTimeout() throws InterruptedException {
    // Get the next eligible node.
    AsyncTimeout node = head.next;

    // The queue is empty. Wait until either something is enqueued or the idle timeout elapses.
    if (node == null) {
      long startNanos = System.nanoTime();
      AsyncTimeout.class.wait(IDLE_TIMEOUT_MILLIS);
      return head.next == null && (System.nanoTime() - startNanos) >= IDLE_TIMEOUT_NANOS
          ? head  // The idle timeout elapsed.
          : null; // The situation has changed.
    }

    long waitNanos = node.remainingNanos(System.nanoTime());

    // The head of the queue hasn't timed out yet. Await that.
    if (waitNanos > 0) {
      // Waiting is made complicated by the fact that we work in nanoseconds,
      // but the API wants (millis, nanos) in two arguments.
      long waitMillis = waitNanos / 1000000L;
      waitNanos -= (waitMillis * 1000000L);
      AsyncTimeout.class.wait(waitMillis, (int) waitNanos);
      return null;
    }

    // The head of the queue has timed out. Remove it.
    head.next = node.next;
    node.next = null;
    return node;
  }
}
```

### Netty

[SingleThreadEventExecutor](https://github.com/netty/netty/blob/master/common/src/main/java/io/netty/util/concurrent/SingleThreadEventExecutor.java)

[HashedWheelTimer](https://github.com/netty/netty/blob/master/common/src/main/java/io/netty/util/HashedWheelTimer.java)

### DotNetty

[SingleThreadEventExecutor](https://github.com/Azure/DotNetty/blob/master/src/DotNetty.Common/Concurrency/SingleThreadEventExecutor.cs)

[HashedWheelTimer](https://github.com/Azure/DotNetty/blob/master/src/DotNetty.Common/Utilities/HashedWheelTimer.cs)

### Android

#### Looper

[Looper](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/master/core/java/android/os/Looper.java)

[MessageQueue](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/master/core/java/android/os/MessageQueue.java)

[Handler](https://mp.weixin.qq.com/s/H8mHoYHyTe6oOaUwfYh6_g)

[ActivityThread.main](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/master/core/java/android/app/ActivityThread.java)

- Looper.prepareMainLooper()
- Looper.loop()

```java
/*
 * Copyright (C) 2006 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package android.os;

import android.annotation.NonNull;
import android.annotation.Nullable;
import android.annotation.UnsupportedAppUsage;
import android.util.Log;
import android.util.Printer;
import android.util.Slog;
import android.util.proto.ProtoOutputStream;

/**
  * Class used to run a message loop for a thread.  Threads by default do
  * not have a message loop associated with them; to create one, call
  * {@link #prepare} in the thread that is to run the loop, and then
  * {@link #loop} to have it process messages until the loop is stopped.
  *
  * <p>Most interaction with a message loop is through the
  * {@link Handler} class.
  *
  * <p>This is a typical example of the implementation of a Looper thread,
  * using the separation of {@link #prepare} and {@link #loop} to create an
  * initial Handler to communicate with the Looper.
  *
  * <pre>
  *  class LooperThread extends Thread {
  *      public Handler mHandler;
  *
  *      public void run() {
  *          Looper.prepare();
  *
  *          mHandler = new Handler() {
  *              public void handleMessage(Message msg) {
  *                  // process incoming messages here
  *              }
  *          };
  *
  *          Looper.loop();
  *      }
  *  }</pre>
  */
public final class Looper {
    /*
     * API Implementation Note:
     *
     * This class contains the code required to set up and manage an event loop
     * based on MessageQueue.  APIs that affect the state of the queue should be
     * defined on MessageQueue or Handler rather than on Looper itself.  For example,
     * idle handlers and sync barriers are defined on the queue whereas preparing the
     * thread, looping, and quitting are defined on the looper.
     */

    private static final String TAG = "Looper";

    // sThreadLocal.get() will return null unless you've called prepare().
    @UnsupportedAppUsage
    static final ThreadLocal<Looper> sThreadLocal = new ThreadLocal<Looper>();
    @UnsupportedAppUsage
    private static Looper sMainLooper;  // guarded by Looper.class
    private static Observer sObserver;

    @UnsupportedAppUsage
    final MessageQueue mQueue;
    final Thread mThread;

    @UnsupportedAppUsage
    private Printer mLogging;
    private long mTraceTag;

    /**
     * If set, the looper will show a warning log if a message dispatch takes longer than this.
     */
    private long mSlowDispatchThresholdMs;

    /**
     * If set, the looper will show a warning log if a message delivery (actual delivery time -
     * post time) takes longer than this.
     */
    private long mSlowDeliveryThresholdMs;

    /** Initialize the current thread as a looper.
      * This gives you a chance to create handlers that then reference
      * this looper, before actually starting the loop. Be sure to call
      * {@link #loop()} after calling this method, and end it by calling
      * {@link #quit()}.
      */
    public static void prepare() {
        prepare(true);
    }

    private static void prepare(boolean quitAllowed) {
        if (sThreadLocal.get() != null) {
            throw new RuntimeException("Only one Looper may be created per thread");
        }
        sThreadLocal.set(new Looper(quitAllowed));
    }

    /**
     * Initialize the current thread as a looper, marking it as an
     * application's main looper. The main looper for your application
     * is created by the Android environment, so you should never need
     * to call this function yourself.  See also: {@link #prepare()}
     */
    public static void prepareMainLooper() {
        prepare(false);
        synchronized (Looper.class) {
            if (sMainLooper != null) {
                throw new IllegalStateException("The main Looper has already been prepared.");
            }
            sMainLooper = myLooper();
        }
    }

    /**
     * Returns the application's main looper, which lives in the main thread of the application.
     */
    public static Looper getMainLooper() {
        synchronized (Looper.class) {
            return sMainLooper;
        }
    }

    /**
     * Set the transaction observer for all Loopers in this process.
     *
     * @hide
     */
    public static void setObserver(@Nullable Observer observer) {
        sObserver = observer;
    }

    /**
     * Run the message queue in this thread. Be sure to call
     * {@link #quit()} to end the loop.
     */
    public static void loop() {
        final Looper me = myLooper();
        if (me == null) {
            throw new RuntimeException("No Looper; Looper.prepare() wasn't called on this thread.");
        }
        final MessageQueue queue = me.mQueue;

        // Make sure the identity of this thread is that of the local process,
        // and keep track of what that identity token actually is.
        Binder.clearCallingIdentity();
        final long ident = Binder.clearCallingIdentity();

        // Allow overriding a threshold with a system prop. e.g.
        // adb shell 'setprop log.looper.1000.main.slow 1 && stop && start'
        final int thresholdOverride =
                SystemProperties.getInt("log.looper."
                        + Process.myUid() + "."
                        + Thread.currentThread().getName()
                        + ".slow", 0);

        boolean slowDeliveryDetected = false;

        for (;;) {
            Message msg = queue.next(); // might block
            if (msg == null) {
                // No message indicates that the message queue is quitting.
                return;
            }

            // This must be in a local variable, in case a UI event sets the logger
            final Printer logging = me.mLogging;
            if (logging != null) {
                logging.println(">>>>> Dispatching to " + msg.target + " " +
                        msg.callback + ": " + msg.what);
            }
            // Make sure the observer won't change while processing a transaction.
            final Observer observer = sObserver;

            final long traceTag = me.mTraceTag;
            long slowDispatchThresholdMs = me.mSlowDispatchThresholdMs;
            long slowDeliveryThresholdMs = me.mSlowDeliveryThresholdMs;
            if (thresholdOverride > 0) {
                slowDispatchThresholdMs = thresholdOverride;
                slowDeliveryThresholdMs = thresholdOverride;
            }
            final boolean logSlowDelivery = (slowDeliveryThresholdMs > 0) && (msg.when > 0);
            final boolean logSlowDispatch = (slowDispatchThresholdMs > 0);

            final boolean needStartTime = logSlowDelivery || logSlowDispatch;
            final boolean needEndTime = logSlowDispatch;

            if (traceTag != 0 && Trace.isTagEnabled(traceTag)) {
                Trace.traceBegin(traceTag, msg.target.getTraceName(msg));
            }

            final long dispatchStart = needStartTime ? SystemClock.uptimeMillis() : 0;
            final long dispatchEnd;
            Object token = null;
            if (observer != null) {
                token = observer.messageDispatchStarting();
            }
            long origWorkSource = ThreadLocalWorkSource.setUid(msg.workSourceUid);
            try {
                msg.target.dispatchMessage(msg);
                if (observer != null) {
                    observer.messageDispatched(token, msg);
                }
                dispatchEnd = needEndTime ? SystemClock.uptimeMillis() : 0;
            } catch (Exception exception) {
                if (observer != null) {
                    observer.dispatchingThrewException(token, msg, exception);
                }
                throw exception;
            } finally {
                ThreadLocalWorkSource.restore(origWorkSource);
                if (traceTag != 0) {
                    Trace.traceEnd(traceTag);
                }
            }
            if (logSlowDelivery) {
                if (slowDeliveryDetected) {
                    if ((dispatchStart - msg.when) <= 10) {
                        Slog.w(TAG, "Drained");
                        slowDeliveryDetected = false;
                    }
                } else {
                    if (showSlowLog(slowDeliveryThresholdMs, msg.when, dispatchStart, "delivery",
                            msg)) {
                        // Once we write a slow delivery log, suppress until the queue drains.
                        slowDeliveryDetected = true;
                    }
                }
            }
            if (logSlowDispatch) {
                showSlowLog(slowDispatchThresholdMs, dispatchStart, dispatchEnd, "dispatch", msg);
            }

            if (logging != null) {
                logging.println("<<<<< Finished to " + msg.target + " " + msg.callback);
            }

            // Make sure that during the course of dispatching the
            // identity of the thread wasn't corrupted.
            final long newIdent = Binder.clearCallingIdentity();
            if (ident != newIdent) {
                Log.wtf(TAG, "Thread identity changed from 0x"
                        + Long.toHexString(ident) + " to 0x"
                        + Long.toHexString(newIdent) + " while dispatching to "
                        + msg.target.getClass().getName() + " "
                        + msg.callback + " what=" + msg.what);
            }

            msg.recycleUnchecked();
        }
    }

    private static boolean showSlowLog(long threshold, long measureStart, long measureEnd,
            String what, Message msg) {
        final long actualTime = measureEnd - measureStart;
        if (actualTime < threshold) {
            return false;
        }
        // For slow delivery, the current message isn't really important, but log it anyway.
        Slog.w(TAG, "Slow " + what + " took " + actualTime + "ms "
                + Thread.currentThread().getName() + " h="
                + msg.target.getClass().getName() + " c=" + msg.callback + " m=" + msg.what);
        return true;
    }

    /**
     * Return the Looper object associated with the current thread.  Returns
     * null if the calling thread is not associated with a Looper.
     */
    public static @Nullable Looper myLooper() {
        return sThreadLocal.get();
    }

    /**
     * Return the {@link MessageQueue} object associated with the current
     * thread.  This must be called from a thread running a Looper, or a
     * NullPointerException will be thrown.
     */
    public static @NonNull MessageQueue myQueue() {
        return myLooper().mQueue;
    }

    private Looper(boolean quitAllowed) {
        mQueue = new MessageQueue(quitAllowed);
        mThread = Thread.currentThread();
    }

    /**
     * Returns true if the current thread is this looper's thread.
     */
    public boolean isCurrentThread() {
        return Thread.currentThread() == mThread;
    }

    /**
     * Control logging of messages as they are processed by this Looper.  If
     * enabled, a log message will be written to <var>printer</var>
     * at the beginning and ending of each message dispatch, identifying the
     * target Handler and message contents.
     *
     * @param printer A Printer object that will receive log messages, or
     * null to disable message logging.
     */
    public void setMessageLogging(@Nullable Printer printer) {
        mLogging = printer;
    }

    /** {@hide} */
    @UnsupportedAppUsage
    public void setTraceTag(long traceTag) {
        mTraceTag = traceTag;
    }

    /**
     * Set a thresholds for slow dispatch/delivery log.
     * {@hide}
     */
    public void setSlowLogThresholdMs(long slowDispatchThresholdMs, long slowDeliveryThresholdMs) {
        mSlowDispatchThresholdMs = slowDispatchThresholdMs;
        mSlowDeliveryThresholdMs = slowDeliveryThresholdMs;
    }

    /**
     * Quits the looper.
     * <p>
     * Causes the {@link #loop} method to terminate without processing any
     * more messages in the message queue.
     * </p><p>
     * Any attempt to post messages to the queue after the looper is asked to quit will fail.
     * For example, the {@link Handler#sendMessage(Message)} method will return false.
     * </p><p class="note">
     * Using this method may be unsafe because some messages may not be delivered
     * before the looper terminates.  Consider using {@link #quitSafely} instead to ensure
     * that all pending work is completed in an orderly manner.
     * </p>
     *
     * @see #quitSafely
     */
    public void quit() {
        mQueue.quit(false);
    }

    /**
     * Quits the looper safely.
     * <p>
     * Causes the {@link #loop} method to terminate as soon as all remaining messages
     * in the message queue that are already due to be delivered have been handled.
     * However pending delayed messages with due times in the future will not be
     * delivered before the loop terminates.
     * </p><p>
     * Any attempt to post messages to the queue after the looper is asked to quit will fail.
     * For example, the {@link Handler#sendMessage(Message)} method will return false.
     * </p>
     */
    public void quitSafely() {
        mQueue.quit(true);
    }

    /**
     * Gets the Thread associated with this Looper.
     *
     * @return The looper's thread.
     */
    public @NonNull Thread getThread() {
        return mThread;
    }

    /**
     * Gets this looper's message queue.
     *
     * @return The looper's message queue.
     */
    public @NonNull MessageQueue getQueue() {
        return mQueue;
    }

    /**
     * Dumps the state of the looper for debugging purposes.
     *
     * @param pw A printer to receive the contents of the dump.
     * @param prefix A prefix to prepend to each line which is printed.
     */
    public void dump(@NonNull Printer pw, @NonNull String prefix) {
        pw.println(prefix + toString());
        mQueue.dump(pw, prefix + "  ", null);
    }

    /**
     * Dumps the state of the looper for debugging purposes.
     *
     * @param pw A printer to receive the contents of the dump.
     * @param prefix A prefix to prepend to each line which is printed.
     * @param handler Only dump messages for this Handler.
     * @hide
     */
    public void dump(@NonNull Printer pw, @NonNull String prefix, Handler handler) {
        pw.println(prefix + toString());
        mQueue.dump(pw, prefix + "  ", handler);
    }

    /** @hide */
    public void writeToProto(ProtoOutputStream proto, long fieldId) {
        final long looperToken = proto.start(fieldId);
        proto.write(LooperProto.THREAD_NAME, mThread.getName());
        proto.write(LooperProto.THREAD_ID, mThread.getId());
        if (mQueue != null) {
            mQueue.writeToProto(proto, LooperProto.QUEUE);
        }
        proto.end(looperToken);
    }

    @Override
    public String toString() {
        return "Looper (" + mThread.getName() + ", tid " + mThread.getId()
                + ") {" + Integer.toHexString(System.identityHashCode(this)) + "}";
    }

    /** {@hide} */
    public interface Observer {
        /**
         * Called right before a message is dispatched.
         *
         * <p> The token type is not specified to allow the implementation to specify its own type.
         *
         * @return a token used for collecting telemetry when dispatching a single message.
         *         The token token must be passed back exactly once to either
         *         {@link Observer#messageDispatched} or {@link Observer#dispatchingThrewException}
         *         and must not be reused again.
         *
         */
        Object messageDispatchStarting();

        /**
         * Called when a message was processed by a Handler.
         *
         * @param token Token obtained by previously calling
         *              {@link Observer#messageDispatchStarting} on the same Observer instance.
         * @param msg The message that was dispatched.
         */
        void messageDispatched(Object token, Message msg);

        /**
         * Called when an exception was thrown while processing a message.
         *
         * @param token Token obtained by previously calling
         *              {@link Observer#messageDispatchStarting} on the same Observer instance.
         * @param msg The message that was dispatched and caused an exception.
         * @param exception The exception that was thrown.
         */
        void dispatchingThrewException(Object token, Message msg, Exception exception);
    }
}
```

#### RxJava AndroidSchedulers

通过`Looper.getMainLooper()`得到 Android 主循环后完成线程上下文切换。

```java
/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.reactivex.android.schedulers;

import android.annotation.SuppressLint;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import io.reactivex.Scheduler;
import io.reactivex.android.plugins.RxAndroidPlugins;
import java.util.concurrent.Callable;

/** Android-specific Schedulers. */
public final class AndroidSchedulers {

    private static final class MainHolder {
        static final Scheduler DEFAULT
            = new HandlerScheduler(new Handler(Looper.getMainLooper()), false);
    }

    private static final Scheduler MAIN_THREAD = RxAndroidPlugins.initMainThreadScheduler(
            new Callable<Scheduler>() {
                @Override public Scheduler call() throws Exception {
                    return MainHolder.DEFAULT;
                }
            });

    /** A {@link Scheduler} which executes actions on the Android main thread. */
    public static Scheduler mainThread() {
        return RxAndroidPlugins.onMainThreadScheduler(MAIN_THREAD);
    }

    /** A {@link Scheduler} which executes actions on {@code looper}. */
    public static Scheduler from(Looper looper) {
        return from(looper, false);
    }

    /**
     * A {@link Scheduler} which executes actions on {@code looper}.
     *
     * @param async if true, the scheduler will use async messaging on API >= 16 to avoid VSYNC
     *              locking. On API < 16 this value is ignored.
     * @see Message#setAsynchronous(boolean)
     */
    @SuppressLint("NewApi") // Checking for an @hide API.
    public static Scheduler from(Looper looper, boolean async) {
        if (looper == null) throw new NullPointerException("looper == null");
        if (Build.VERSION.SDK_INT < 16) {
            async = false;
        } else if (async && Build.VERSION.SDK_INT < 22) {
            // Confirm that the method is available on this API level despite being @hide.
            Message message = Message.obtain();
            try {
                message.setAsynchronous(true);
            } catch (NoSuchMethodError e) {
                async = false;
            }
            message.recycle();
        }
        return new HandlerScheduler(new Handler(looper), async);
    }

    private AndroidSchedulers() {
        throw new AssertionError("No instances.");
    }
}
```

#### RxJava Schedulers

```java
/**
 * Copyright (c) 2016-present, RxJava Contributors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
 * the License for the specific language governing permissions and limitations under the License.
 */

package io.reactivex.schedulers;

import java.util.concurrent.*;

import io.reactivex.Scheduler;
import io.reactivex.annotations.*;
import io.reactivex.internal.schedulers.*;
import io.reactivex.plugins.RxJavaPlugins;

/**
 * Static factory methods for returning standard Scheduler instances.
 * <p>
 * The initial and runtime values of the various scheduler types can be overridden via the
 * {@code RxJavaPlugins.setInit(scheduler name)SchedulerHandler()} and
 * {@code RxJavaPlugins.set(scheduler name)SchedulerHandler()} respectively.
 * <p>
 * <strong>Supported system properties ({@code System.getProperty()}):</strong>
 * <ul>
 * <li>{@code rx2.io-keep-alive-time} (long): sets the keep-alive time of the {@link #io()} Scheduler workers, default is {@link IoScheduler#KEEP_ALIVE_TIME_DEFAULT}</li>
 * <li>{@code rx2.io-priority} (int): sets the thread priority of the {@link #io()} Scheduler, default is {@link Thread#NORM_PRIORITY}</li>
 * <li>{@code rx2.computation-threads} (int): sets the number of threads in the {@link #computation()} Scheduler, default is the number of available CPUs</li>
 * <li>{@code rx2.computation-priority} (int): sets the thread priority of the {@link #computation()} Scheduler, default is {@link Thread#NORM_PRIORITY}</li>
 * <li>{@code rx2.newthread-priority} (int): sets the thread priority of the {@link #newThread()} Scheduler, default is {@link Thread#NORM_PRIORITY}</li>
 * <li>{@code rx2.single-priority} (int): sets the thread priority of the {@link #single()} Scheduler, default is {@link Thread#NORM_PRIORITY}</li>
 * <li>{@code rx2.purge-enabled} (boolean): enables periodic purging of all Scheduler's backing thread pools, default is false</li>
 * <li>{@code rx2.purge-period-seconds} (int): specifies the periodic purge interval of all Scheduler's backing thread pools, default is 1 second</li>
 * </ul>
 */
public final class Schedulers {
    @NonNull
    static final Scheduler SINGLE;

    @NonNull
    static final Scheduler COMPUTATION;

    @NonNull
    static final Scheduler IO;

    @NonNull
    static final Scheduler TRAMPOLINE;

    @NonNull
    static final Scheduler NEW_THREAD;

    static final class SingleHolder {
        static final Scheduler DEFAULT = new SingleScheduler();
    }

    static final class ComputationHolder {
        static final Scheduler DEFAULT = new ComputationScheduler();
    }

    static final class IoHolder {
        static final Scheduler DEFAULT = new IoScheduler();
    }

    static final class NewThreadHolder {
        static final Scheduler DEFAULT = new NewThreadScheduler();
    }

    static {
        SINGLE = RxJavaPlugins.initSingleScheduler(new SingleTask());

        COMPUTATION = RxJavaPlugins.initComputationScheduler(new ComputationTask());

        IO = RxJavaPlugins.initIoScheduler(new IOTask());

        TRAMPOLINE = TrampolineScheduler.instance();

        NEW_THREAD = RxJavaPlugins.initNewThreadScheduler(new NewThreadTask());
    }

    /** Utility class. */
    private Schedulers() {
        throw new IllegalStateException("No instances!");
    }

    /**
     * Returns a default, shared {@link Scheduler} instance intended for computational work.
     * <p>
     * This can be used for event-loops, processing callbacks and other computational work.
     * <p>
     * It is not recommended to perform blocking, IO-bound work on this scheduler. Use {@link #io()} instead.
     * <p>
     * The default instance has a backing pool of single-threaded {@link ScheduledExecutorService} instances equal to
     * the number of available processors ({@link java.lang.Runtime#availableProcessors()}) to the Java VM.
     * <p>
     * Unhandled errors will be delivered to the scheduler Thread's {@link java.lang.Thread.UncaughtExceptionHandler}.
     * <p>
     * This type of scheduler is less sensitive to leaking {@link io.reactivex.Scheduler.Worker} instances, although
     * not disposing a worker that has timed/delayed tasks not cancelled by other means may leak resources and/or
     * execute those tasks "unexpectedly".
     * <p>
     * If the {@link RxJavaPlugins#setFailOnNonBlockingScheduler(boolean)} is set to true, attempting to execute
     * operators that block while running on this scheduler will throw an {@link IllegalStateException}.
     * <p>
     * You can control certain properties of this standard scheduler via system properties that have to be set
     * before the {@link Schedulers} class is referenced in your code.
     * <p><strong>Supported system properties ({@code System.getProperty()}):</strong>
     * <ul>
     * <li>{@code rx2.computation-threads} (int): sets the number of threads in the {@link #computation()} Scheduler, default is the number of available CPUs</li>
     * <li>{@code rx2.computation-priority} (int): sets the thread priority of the {@link #computation()} Scheduler, default is {@link Thread#NORM_PRIORITY}</li>
     * </ul>
     * <p>
     * The default value of this scheduler can be overridden at initialization time via the
     * {@link RxJavaPlugins#setInitComputationSchedulerHandler(io.reactivex.functions.Function)} plugin method.
     * Note that due to possible initialization cycles, using any of the other scheduler-returning methods will
     * result in a {@code NullPointerException}.
     * Once the {@link Schedulers} class has been initialized, you can override the returned {@link Scheduler} instance
     * via the {@link RxJavaPlugins#setComputationSchedulerHandler(io.reactivex.functions.Function)} method.
     * <p>
     * It is possible to create a fresh instance of this scheduler with a custom ThreadFactory, via the
     * {@link RxJavaPlugins#createComputationScheduler(ThreadFactory)} method. Note that such custom
     * instances require a manual call to {@link Scheduler#shutdown()} to allow the JVM to exit or the
     * (J2EE) container to unload properly.
     * <p>Operators on the base reactive classes that use this scheduler are marked with the
     * &#64;{@link io.reactivex.annotations.SchedulerSupport SchedulerSupport}({@link io.reactivex.annotations.SchedulerSupport#COMPUTATION COMPUTATION})
     * annotation.
     * @return a {@link Scheduler} meant for computation-bound work
     */
    @NonNull
    public static Scheduler computation() {
        return RxJavaPlugins.onComputationScheduler(COMPUTATION);
    }

    /**
     * Returns a default, shared {@link Scheduler} instance intended for IO-bound work.
     * <p>
     * This can be used for asynchronously performing blocking IO.
     * <p>
     * The implementation is backed by a pool of single-threaded {@link ScheduledExecutorService} instances
     * that will try to reuse previously started instances used by the worker
     * returned by {@link io.reactivex.Scheduler#createWorker()} but otherwise will start a new backing
     * {@link ScheduledExecutorService} instance. Note that this scheduler may create an unbounded number
     * of worker threads that can result in system slowdowns or {@code OutOfMemoryError}. Therefore, for casual uses
     * or when implementing an operator, the Worker instances must be disposed via {@link io.reactivex.Scheduler.Worker#dispose()}.
     * <p>
     * It is not recommended to perform computational work on this scheduler. Use {@link #computation()} instead.
     * <p>
     * Unhandled errors will be delivered to the scheduler Thread's {@link java.lang.Thread.UncaughtExceptionHandler}.
     * <p>
     * You can control certain properties of this standard scheduler via system properties that have to be set
     * before the {@link Schedulers} class is referenced in your code.
     * <p><strong>Supported system properties ({@code System.getProperty()}):</strong>
     * <ul>
     * <li>{@code rx2.io-keep-alive-time} (long): sets the keep-alive time of the {@link #io()} Scheduler workers, default is {@link IoScheduler#KEEP_ALIVE_TIME_DEFAULT}</li>
     * <li>{@code rx2.io-priority} (int): sets the thread priority of the {@link #io()} Scheduler, default is {@link Thread#NORM_PRIORITY}</li>
     * </ul>
     * <p>
     * The default value of this scheduler can be overridden at initialization time via the
     * {@link RxJavaPlugins#setInitIoSchedulerHandler(io.reactivex.functions.Function)} plugin method.
     * Note that due to possible initialization cycles, using any of the other scheduler-returning methods will
     * result in a {@code NullPointerException}.
     * Once the {@link Schedulers} class has been initialized, you can override the returned {@link Scheduler} instance
     * via the {@link RxJavaPlugins#setIoSchedulerHandler(io.reactivex.functions.Function)} method.
     * <p>
     * It is possible to create a fresh instance of this scheduler with a custom ThreadFactory, via the
     * {@link RxJavaPlugins#createIoScheduler(ThreadFactory)} method. Note that such custom
     * instances require a manual call to {@link Scheduler#shutdown()} to allow the JVM to exit or the
     * (J2EE) container to unload properly.
     * <p>Operators on the base reactive classes that use this scheduler are marked with the
     * &#64;{@link io.reactivex.annotations.SchedulerSupport SchedulerSupport}({@link io.reactivex.annotations.SchedulerSupport#IO IO})
     * annotation.
     * @return a {@link Scheduler} meant for IO-bound work
     */
    @NonNull
    public static Scheduler io() {
        return RxJavaPlugins.onIoScheduler(IO);
    }

    /**
     * Returns a default, shared {@link Scheduler} instance whose {@link io.reactivex.Scheduler.Worker}
     * instances queue work and execute them in a FIFO manner on one of the participating threads.
     * <p>
     * The default implementation's {@link Scheduler#scheduleDirect(Runnable)} methods execute the tasks on the current thread
     * without any queueing and the timed overloads use blocking sleep as well.
     * <p>
     * Note that this scheduler can't be reliably used to return the execution of
     * tasks to the "main" thread. Such behavior requires a blocking-queueing scheduler currently not provided
     * by RxJava itself but may be found in external libraries.
     * <p>
     * This scheduler can't be overridden via an {@link RxJavaPlugins} method.
     * @return a {@link Scheduler} that queues work on the current thread
     */
    @NonNull
    public static Scheduler trampoline() {
        return TRAMPOLINE;
    }

    /**
     * Returns a default, shared {@link Scheduler} instance that creates a new {@link Thread} for each unit of work.
     * <p>
     * The default implementation of this scheduler creates a new, single-threaded {@link ScheduledExecutorService} for
     * each invocation of the {@link Scheduler#scheduleDirect(Runnable)} (plus its overloads) and {@link Scheduler#createWorker()}
     * methods, thus an unbounded number of worker threads may be created that can
     * result in system slowdowns or {@code OutOfMemoryError}. Therefore, for casual uses or when implementing an operator,
     * the Worker instances must be disposed via {@link io.reactivex.Scheduler.Worker#dispose()}.
     * <p>
     * Unhandled errors will be delivered to the scheduler Thread's {@link java.lang.Thread.UncaughtExceptionHandler}.
     * <p>
     * You can control certain properties of this standard scheduler via system properties that have to be set
     * before the {@link Schedulers} class is referenced in your code.
     * <p><strong>Supported system properties ({@code System.getProperty()}):</strong>
     * <ul>
     * <li>{@code rx2.newthread-priority} (int): sets the thread priority of the {@link #newThread()} Scheduler, default is {@link Thread#NORM_PRIORITY}</li>
     * </ul>
     * <p>
     * The default value of this scheduler can be overridden at initialization time via the
     * {@link RxJavaPlugins#setInitNewThreadSchedulerHandler(io.reactivex.functions.Function)} plugin method.
     * Note that due to possible initialization cycles, using any of the other scheduler-returning methods will
     * result in a {@code NullPointerException}.
     * Once the {@link Schedulers} class has been initialized, you can override the returned {@link Scheduler} instance
     * via the {@link RxJavaPlugins#setNewThreadSchedulerHandler(io.reactivex.functions.Function)} method.
     * <p>
     * It is possible to create a fresh instance of this scheduler with a custom ThreadFactory, via the
     * {@link RxJavaPlugins#createNewThreadScheduler(ThreadFactory)} method. Note that such custom
     * instances require a manual call to {@link Scheduler#shutdown()} to allow the JVM to exit or the
     * (J2EE) container to unload properly.
     * <p>Operators on the base reactive classes that use this scheduler are marked with the
     * &#64;{@link io.reactivex.annotations.SchedulerSupport SchedulerSupport}({@link io.reactivex.annotations.SchedulerSupport#NEW_THREAD NEW_TRHEAD})
     * annotation.
     * @return a {@link Scheduler} that creates new threads
     */
    @NonNull
    public static Scheduler newThread() {
        return RxJavaPlugins.onNewThreadScheduler(NEW_THREAD);
    }

    /**
     * Returns a default, shared, single-thread-backed {@link Scheduler} instance for work
     * requiring strongly-sequential execution on the same background thread.
     * <p>
     * Uses:
     * <ul>
     * <li>event loop</li>
     * <li>support Schedulers.from(Executor) and from(ExecutorService) with delayed scheduling</li>
     * <li>support benchmarks that pipeline data from some thread to another thread and
     * avoid core-bashing of computation's round-robin nature</li>
     * </ul>
     * <p>
     * Unhandled errors will be delivered to the scheduler Thread's {@link java.lang.Thread.UncaughtExceptionHandler}.
     * <p>
     * This type of scheduler is less sensitive to leaking {@link io.reactivex.Scheduler.Worker} instances, although
     * not disposing a worker that has timed/delayed tasks not cancelled by other means may leak resources and/or
     * execute those tasks "unexpectedly".
     * <p>
     * If the {@link RxJavaPlugins#setFailOnNonBlockingScheduler(boolean)} is set to true, attempting to execute
     * operators that block while running on this scheduler will throw an {@link IllegalStateException}.
     * <p>
     * You can control certain properties of this standard scheduler via system properties that have to be set
     * before the {@link Schedulers} class is referenced in your code.
     * <p><strong>Supported system properties ({@code System.getProperty()}):</strong>
     * <ul>
     * <li>{@code rx2.single-priority} (int): sets the thread priority of the {@link #single()} Scheduler, default is {@link Thread#NORM_PRIORITY}</li>
     * </ul>
     * <p>
     * The default value of this scheduler can be overridden at initialization time via the
     * {@link RxJavaPlugins#setInitSingleSchedulerHandler(io.reactivex.functions.Function)} plugin method.
     * Note that due to possible initialization cycles, using any of the other scheduler-returning methods will
     * result in a {@code NullPointerException}.
     * Once the {@link Schedulers} class has been initialized, you can override the returned {@link Scheduler} instance
     * via the {@link RxJavaPlugins#setSingleSchedulerHandler(io.reactivex.functions.Function)} method.
     * <p>
     * It is possible to create a fresh instance of this scheduler with a custom ThreadFactory, via the
     * {@link RxJavaPlugins#createSingleScheduler(ThreadFactory)} method. Note that such custom
     * instances require a manual call to {@link Scheduler#shutdown()} to allow the JVM to exit or the
     * (J2EE) container to unload properly.
     * <p>Operators on the base reactive classes that use this scheduler are marked with the
     * &#64;{@link io.reactivex.annotations.SchedulerSupport SchedulerSupport}({@link io.reactivex.annotations.SchedulerSupport#SINGLE SINGLE})
     * annotation.
     * @return a {@link Scheduler} that shares a single backing thread.
     * @since 2.0
     */
    @NonNull
    public static Scheduler single() {
        return RxJavaPlugins.onSingleScheduler(SINGLE);
    }

    /**
     * Wraps an {@link Executor} into a new Scheduler instance and delegates {@code schedule()}
     * calls to it.
     * <p>
     * If the provided executor doesn't support any of the more specific standard Java executor
     * APIs, cancelling tasks scheduled by this scheduler can't be interrupted when they are
     * executing but only prevented from running prior to that. In addition, tasks scheduled with
     * a time delay or periodically will use the {@link #single()} scheduler for the timed waiting
     * before posting the actual task to the given executor.
     * <p>
     * Tasks submitted to the {@link Scheduler.Worker} of this {@code Scheduler} are also not interruptible. Use the
     * {@link #from(Executor, boolean)} overload to enable task interruption via this wrapper.
     * <p>
     * If the provided executor supports the standard Java {@link ExecutorService} API,
     * cancelling tasks scheduled by this scheduler can be cancelled/interrupted by calling
     * {@link io.reactivex.disposables.Disposable#dispose()}. In addition, tasks scheduled with
     * a time delay or periodically will use the {@link #single()} scheduler for the timed waiting
     * before posting the actual task to the given executor.
     * <p>
     * If the provided executor supports the standard Java {@link ScheduledExecutorService} API,
     * cancelling tasks scheduled by this scheduler can be cancelled/interrupted by calling
     * {@link io.reactivex.disposables.Disposable#dispose()}. In addition, tasks scheduled with
     * a time delay or periodically will use the provided executor. Note, however, if the provided
     * {@code ScheduledExecutorService} instance is not single threaded, tasks scheduled
     * with a time delay close to each other may end up executing in different order than
     * the original schedule() call was issued. This limitation may be lifted in a future patch.
     * <p>
     * Starting, stopping and restarting this scheduler is not supported (no-op) and the provided
     * executor's lifecycle must be managed externally:
     * <pre><code>
     * ExecutorService exec = Executors.newSingleThreadedExecutor();
     * try {
     *     Scheduler scheduler = Schedulers.from(exec);
     *     Flowable.just(1)
     *        .subscribeOn(scheduler)
     *        .map(v -&gt; v + 1)
     *        .observeOn(scheduler)
     *        .blockingSubscribe(System.out::println);
     * } finally {
     *     exec.shutdown();
     * }
     * </code></pre>
     * <p>
     * This type of scheduler is less sensitive to leaking {@link Scheduler.Worker} instances, although
     * not disposing a worker that has timed/delayed tasks not cancelled by other means may leak resources and/or
     * execute those tasks "unexpectedly".
     * <p>
     * Note that this method returns a new {@link Scheduler} instance, even for the same {@link Executor} instance.
     * @param executor
     *          the executor to wrap
     * @return the new Scheduler wrapping the Executor
     */
    @NonNull
    public static Scheduler from(@NonNull Executor executor) {
        return new ExecutorScheduler(executor, false);
    }

    /**
     * Wraps an {@link Executor} into a new Scheduler instance and delegates {@code schedule()}
     * calls to it.
     * <p>
     * The tasks scheduled by the returned {@link Scheduler} and its {@link Scheduler.Worker}
     * can be optionally interrupted.
     * <p>
     * If the provided executor doesn't support any of the more specific standard Java executor
     * APIs, tasks scheduled with a time delay or periodically will use the
     * {@link #single()} scheduler for the timed waiting
     * before posting the actual task to the given executor.
     * <p>
     * If the provided executor supports the standard Java {@link ExecutorService} API,
     * canceling tasks scheduled by this scheduler can be cancelled/interrupted by calling
     * {@link io.reactivex.disposables.Disposable#dispose()}. In addition, tasks scheduled with
     * a time delay or periodically will use the {@link #single()} scheduler for the timed waiting
     * before posting the actual task to the given executor.
     * <p>
     * If the provided executor supports the standard Java {@link ScheduledExecutorService} API,
     * canceling tasks scheduled by this scheduler can be cancelled/interrupted by calling
     * {@link io.reactivex.disposables.Disposable#dispose()}. In addition, tasks scheduled with
     * a time delay or periodically will use the provided executor. Note, however, if the provided
     * {@code ScheduledExecutorService} instance is not single threaded, tasks scheduled
     * with a time delay close to each other may end up executing in different order than
     * the original schedule() call was issued. This limitation may be lifted in a future patch.
     * <p>
     * Starting, stopping and restarting this scheduler is not supported (no-op) and the provided
     * executor's lifecycle must be managed externally:
     * <pre><code>
     * ExecutorService exec = Executors.newSingleThreadedExecutor();
     * try {
     *     Scheduler scheduler = Schedulers.from(exec, true);
     *     Flowable.just(1)
     *        .subscribeOn(scheduler)
     *        .map(v -&gt; v + 1)
     *        .observeOn(scheduler)
     *        .blockingSubscribe(System.out::println);
     * } finally {
     *     exec.shutdown();
     * }
     * </code></pre>
     * <p>
     * This type of scheduler is less sensitive to leaking {@link Scheduler.Worker} instances, although
     * not disposing a worker that has timed/delayed tasks not cancelled by other means may leak resources and/or
     * execute those tasks "unexpectedly".
     * <p>
     * Note that this method returns a new {@link Scheduler} instance, even for the same {@link Executor} instance.
     * @param executor
     *          the executor to wrap
     * @param interruptibleWorker if {@code true} the tasks submitted to the {@link Scheduler.Worker} will
     * be interrupted when the task is disposed.
     * @return the new Scheduler wrapping the Executor
     * @since 2.2.6 - experimental
     */
    @NonNull
    @Experimental
    public static Scheduler from(@NonNull Executor executor, boolean interruptibleWorker) {
        return new ExecutorScheduler(executor, interruptibleWorker);
    }

    /**
     * Shuts down the standard Schedulers.
     * <p>The operation is idempotent and thread-safe.
     */
    public static void shutdown() {
        computation().shutdown();
        io().shutdown();
        newThread().shutdown();
        single().shutdown();
        trampoline().shutdown();
        SchedulerPoolFactory.shutdown();
    }

    /**
     * Starts the standard Schedulers.
     * <p>The operation is idempotent and thread-safe.
     */
    public static void start() {
        computation().start();
        io().start();
        newThread().start();
        single().start();
        trampoline().start();
        SchedulerPoolFactory.start();
    }

    static final class IOTask implements Callable<Scheduler> {
        @Override
        public Scheduler call() throws Exception {
            return IoHolder.DEFAULT;
        }
    }

    static final class NewThreadTask implements Callable<Scheduler> {
        @Override
        public Scheduler call() throws Exception {
            return NewThreadHolder.DEFAULT;
        }
    }

    static final class SingleTask implements Callable<Scheduler> {
        @Override
        public Scheduler call() throws Exception {
            return SingleHolder.DEFAULT;
        }
    }

    static final class ComputationTask implements Callable<Scheduler> {
        @Override
        public Scheduler call() throws Exception {
            return ComputationHolder.DEFAULT;
        }
    }
}
```

## Resources

- [异步编程的几种方式](https://ericfu.me/several-ways-to-aync/)
- [CompletableFuture](https://ericfu.me/completable-future-not-so-bad/)
- [Java CompletableFuture 详解](https://colobu.com/2016/02/29/Java-CompletableFuture/)
