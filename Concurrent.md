# Concurrent

- [Concurrent](#concurrent)
  - [Promise, Future](#promise-future)
    - [DeferredResult, WebAsyncTask](#deferredresult-webasynctask)
    - [CompletableFuture, Future](#completablefuture-future)
    - [TaskCompletionSource, Task, CancellationTokenSource, CancellationToken](#taskcompletionsource-task-cancellationtokensource-cancellationtoken)
  - [Reactor](#reactor)
    - [Publisher](#publisher)
    - [Subscriber](#subscriber)
    - [Subscription](#subscription)
    - [Processor](#processor)
    - [Flux.subscribeOn](#fluxsubscribeon)
    - [Flux.publishOn](#fluxpublishon)

## Promise, Future

这些类实现的语义都类似，代表一个异步结果: Promise, Future

异步结果可能呈现以下状态：

> timeout, error, completion, cancel

### DeferredResult, WebAsyncTask

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

## Reactor

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

### Publisher

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

### Subscriber

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

### Subscription

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

### Processor

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

### Flux.subscribeOn

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

### Flux.publishOn

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
}
```
