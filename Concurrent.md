# Concurrent

- [Concurrent](#concurrent)
  - [Promise, Future](#promise-future)
    - [DeferredResult, WebAsyncTask](#deferredresult-webasynctask)
    - [CompletableFuture, Future](#completablefuture-future)
    - [TaskCompletionSource, Task, CancellationTokenSource, CancellationToken](#taskcompletionsource-task-cancellationtokensource-cancellationtoken)
  - [Stream](#stream)
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

[Java8 Stream原理深度解析](https://www.cnblogs.com/Dorae/p/7779246.html)

[深入理解Java Stream流水线](https://www.cnblogs.com/CarpenterLee/p/6637118.html)

[Java 8 Stream探秘](https://colobu.com/2014/11/18/Java-8-Stream/)

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

[reactive-extensions](https://docs.microsoft.com/en-us/previous-versions/dotnet/reactive-extensions/hh242985(v=vs.103))

[github](https://github.com/dotnet/reactive)

[Reactive Framework (Rx) Wiki](http://rxwiki.wikidot.com/)

#### Pulling vs. Pushing Data

In interactive programming, the application actively polls a data source for more information by pulling data from a sequence that represents the source. Such behavior is represented by the iterator pattern of `IEnumerable<T>/IEnumerator<T>`. The `IEnumerable<T>` interface exposes a single method GetEnumerator() which returns an `IEnumerator<T>` to iterate through this collection.  The `IEnumerator<T>` allows us to get the current item (by returning the Current property), and determine whether there are more items to iterate (by calling the MoveNext method).

The application is active in the data retrieval process: besides getting an enumerator by calling GetEnumerator, it also controls the pace of the retrieval by calling MoveNext at its own convenience. This enumeration pattern is synchronous, which means that the application might be blocked while polling the data source. Such pulling pattern is similar to visiting your library and checking out a book. After you are done with the book, you pay another visit to check out another one.

On the other hand, in reactive programming, the application is offered more information by subscribing to a data stream (called observable sequence in Rx), and any update is handed to it from the source. The application is passive in the data retrieval process: apart from subscribing to the observable source, it does not actively poll the source, but merely react to the data being pushed to it. When the stream has no more data to offer, or when it errs, the source will send a notice to the subscriber. In this way, the application will not be blocked by waiting for the source to update.

This is the push pattern employed by Reactive Extensions. It is similar to joining a book club in which you register your interest in a particular genre, and books that match your interest are automatically sent to you as they are published. You do not need to stand in line to acquire something that you want. Employing a push pattern is helpful in many scenarios, especially in a UI-heavy environment in which the UI thread cannot be blocked while the application is waiting for some events. This is also essential in programming environments such as Silverlight which has its own set of asynchronous requirements. In summary, by using Rx, you can make your application more responsive.

The push model implemented by Rx is represented by the observable pattern of `IObservable<T>/IObserver<T>`. The `IObservable<T>` interface is a dual of the familiar `IEnumerable<T>` interface. It abstracts a sequence of data, and keeps a list of `IObserver<T>` implementations that are interested in the data sequence. The IObservable will notify all the observers automatically of any state changes. To register an interest through a subscription, you use the Subscribe method of IObservable, which takes on an IObserver and returns an IDisposable. This gives you the ability to track and dispose of the subscription. In addition, Rx’s LINQ implementation over observable sequences allows developers to compose complex event processing queries over push-based sequences such as .NET events, APM-based (“IAsyncResult”) computations, `Task<T>-based` computations,  Windows 7 Sensor and Location APIs, SQL StreamInsight temporal event streams, F# first-class events, and asynchronous workflows. For more information on the `IObservable<T>/IObserver<T>` interfaces, see Exploring The Major Interfaces in Rx. For tutorials on using the different features in Rx, see Using Rx.

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

`Promise` 与 `Observable` 可以解决js中的回调地狱。

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

const PENDING = 'pending';
const FULFILLED = 'fulfilled';
const REJECTED = 'rejected';
function Promise(executor) {
    let self = this;
    self.status = PENDING;
    self.onFulfilled = [];//成功的回调
    self.onRejected = []; //失败的回调
    //PromiseA+ 2.1
    function resolve(value) {
        if (self.status === PENDING) {
            self.status = FULFILLED;
            self.value = value;
            self.onFulfilled.forEach(fn => fn());//PromiseA+ 2.2.6.1
        }
    }

    function reject(reason) {
        if (self.status === PENDING) {
            self.status = REJECTED;
            self.reason = reason;
            self.onRejected.forEach(fn => fn());//PromiseA+ 2.2.6.2
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
    onFulfilled = typeof onFulfilled === 'function' ? onFulfilled : value => value;
    onRejected = typeof onRejected === 'function' ? onRejected : reason => { throw reason };
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
}

function resolvePromise(promise2, x, resolve, reject) {
    let self = this;
    //PromiseA+ 2.3.1
    if (promise2 === x) {
        reject(new TypeError('Chaining cycle'));
    }
    if (x && typeof x === 'object' || typeof x === 'function') {
        let used; //PromiseA+2.3.3.3.3 只能调用一次
        try {
            let then = x.then;
            if (typeof then === 'function') {
                //PromiseA+2.3.3
                then.call(x, (y) => {
                    //PromiseA+2.3.3.1
                    if (used) return;
                    used = true;
                    resolvePromise(promise2, y, resolve, reject);
                }, (r) => {
                    //PromiseA+2.3.3.2
                    if (used) return;
                    used = true;
                    reject(r);
                });

            }else{
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

A stream is an abstract interface for working with streaming data in Node.js.

[gulp](https://www.gulpjs.com.cn/docs/api/concepts/) 实现了流式处理。

[stream-handbook](https://github.com/substack/stream-handbook) covers the basics of how to write node.js programs with streams.

[through2](https://github.com/rvagg/through2) A tiny wrapper around Node.js streams.Transform (Streams2/3) to avoid explicit subclassing noise

## Schedule

模拟 js 的单线程执行机制。1. 可执行普通Task, 2. 可执行定时任务。

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
